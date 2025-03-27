from pathlib import Path
from ..config import FooterBoundary
import os
from .pdf import get_all_blocks
import pymupdf
from tqdm.auto import tqdm
from typing import Optional


def clean_split_section(page, clip_rect, footer_boundary=None, section_type=None):
    """
    Create a clean split by redacting content outside the clip rectangle.
    section_type can be: 'bottom_footer', 'right_footer', 'both_footers', 'main', 'main_both_footers', or 'header'
    """
    page_width = page.rect.width
    page_height = page.rect.height
    
    if section_type == 'bottom_footer':
        redactions = [
            # Everything above bottom_top
            pymupdf.Rect(0, 0, page_width, footer_boundary.top_bottom)
        ]
    elif section_type == 'right_footer':
        redactions = [
            # From (0,0) to (page_height, left_right) and from (left_right,0) to (page_width, top_right)
            pymupdf.Rect(0, 0, footer_boundary.left_right, page_height),
            pymupdf.Rect(footer_boundary.left_right, 0, page_width, footer_boundary.top_right)
        ]
    elif section_type == 'both_footers':
        redactions = [
            # From (0,0) to (bottom_top, left_right) and from (left_right,0) to (page_width, top_right)
            pymupdf.Rect(0, 0, footer_boundary.left_right, footer_boundary.top_bottom),
            pymupdf.Rect(footer_boundary.left_right, 0, page_width, footer_boundary.top_right)
        ]
    elif section_type == 'main_both_footers':
        redactions = [
            # Top (if there's header)
            pymupdf.Rect(0, 0, page_width, clip_rect.y0),
            # Bottom footer area
            pymupdf.Rect(0, footer_boundary.top_bottom, footer_boundary.left_right, page_height),
            # Right footer area
            pymupdf.Rect(footer_boundary.left_right, footer_boundary.top_right, page_width, page_height)
        ]
    elif section_type == 'main':
        redactions = [
            # Top
            pymupdf.Rect(0, 0, page_width, clip_rect.y0),
            # Bottom
            pymupdf.Rect(0, clip_rect.y1, page_width, page_height),
            # Left
            pymupdf.Rect(0, clip_rect.y0, clip_rect.x0, clip_rect.y1),
            # Right
            pymupdf.Rect(clip_rect.x1, clip_rect.y0, page_width, clip_rect.y1)
        ]
    else:  # header
        redactions = [
            # Bottom
            pymupdf.Rect(0, clip_rect.y1, page_width, page_height),
            # Left
            pymupdf.Rect(0, clip_rect.y0, clip_rect.x0, clip_rect.y1),
            # Right
            pymupdf.Rect(clip_rect.x1, clip_rect.y0, page_width, clip_rect.y1)
        ]
    
    # Create a copy of the page
    temp_doc = pymupdf.open()
    temp_page = temp_doc.new_page(width=page_width, height=page_height)
    temp_page.show_pdf_page(temp_page.rect, page.parent, page.number)
    
    # Apply redactions
    for rect in redactions:
        temp_page.add_redact_annot(rect)
    temp_page.apply_redactions()
    
    # Create final page with exact dimensions
    doc = pymupdf.open()
    new_page = doc.new_page(width=clip_rect.width, height=clip_rect.height)
    new_page.show_pdf_page(new_page.rect, temp_doc, 0, clip=clip_rect)
    
    temp_doc.close()
    return doc, new_page

def split_pdf_in_sections(page: "pymupdf.Page", output_dir: str, base_name: str, page_num: int,
                         header_bottom: Optional[float], footer_boundary: FooterBoundary) -> None:
    """
    Split a PDF page into sections based on header and footer boundaries.
    Each section maintains its original position and dimensions.
    """
    page.remove_rotation()

    page_width = page.rect.width
    page_height = page.rect.height
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Header section
    if header_bottom is not None:
        header_clip = pymupdf.Rect(0, 0, page_width, header_bottom)
        header_doc, header_page = clean_split_section(page, header_clip, footer_boundary, section_type='header')
        header_path = os.path.join(output_dir, f"{base_name}_page{page_num+1}_header.pdf")
        header_doc.save(header_path)
        header_doc.close()
    
    
    # Main content section
    main_doc = pymupdf.open()
    
    # Case 1: Only header
    if header_bottom is not None and footer_boundary.top_bottom is None and footer_boundary.top_right is None:
        main_clip = pymupdf.Rect(0, header_bottom, page_width, page_height)
        main_doc, main_page = clean_split_section(page, main_clip, footer_boundary, section_type='main')
        
    # Case 2: Only bottom footer
    elif header_bottom is None and footer_boundary.top_bottom is not None and footer_boundary.top_right is None:
        main_clip = pymupdf.Rect(0, 0, page_width, footer_boundary.top_bottom)
        main_doc, main_page = clean_split_section(page, main_clip, footer_boundary, section_type='main')
        
    # Case 3: Only right footer
    elif header_bottom is None and footer_boundary.top_bottom is None and footer_boundary.top_right is not None:
        main_clip = pymupdf.Rect(0, 0, footer_boundary.left_right, page_height)
        main_doc, main_page = clean_split_section(page, main_clip, footer_boundary, section_type='main')
        
    # Case 4: Header + bottom footer
    elif header_bottom is not None and footer_boundary.top_bottom is not None and footer_boundary.top_right is None:
        main_clip = pymupdf.Rect(0, header_bottom, page_width, footer_boundary.top_bottom)
        main_doc, main_page = clean_split_section(page, main_clip, footer_boundary, section_type='main')
        
    # Case 5: Header + right footer
    elif header_bottom is not None and footer_boundary.top_bottom is None and footer_boundary.top_right is not None:
        main_clip = pymupdf.Rect(0, header_bottom, footer_boundary.left_right, page_height)
        main_doc, main_page = clean_split_section(page, main_clip, footer_boundary, section_type='main')
        
    # Case 6: Both footers (no header)
    elif header_bottom is None and footer_boundary.top_bottom is not None and footer_boundary.top_right is not None:
        main_clip = pymupdf.Rect(0, 0, page_width, max(footer_boundary.top_bottom, footer_boundary.top_right))
        main_doc, main_page = clean_split_section(page, main_clip, footer_boundary, section_type='main_both_footers')

    # Case 7: Header + both footers
    elif header_bottom is not None and footer_boundary.top_bottom is not None and footer_boundary.top_right is not None:
        main_clip = pymupdf.Rect(0, header_bottom, page_width, max(footer_boundary.top_bottom, footer_boundary.top_right))
        main_doc, main_page = clean_split_section(page, main_clip, footer_boundary, section_type='main_both_footers')

    else:
        main_clip = pymupdf.Rect(0, 0, page_width, page_height)
        main_doc, main_page = clean_split_section(page, main_clip, footer_boundary, section_type='main')
    
    # Save main section if we created any pages
    if main_doc.page_count > 0:
        main_path = os.path.join(output_dir, f"{base_name}_page{page_num+1}_main.pdf")
        main_doc.save(main_path)
    main_doc.close()
    
    # Footer section
    if footer_boundary.top_bottom is not None or footer_boundary.top_right is not None:
        footer_doc = pymupdf.open()
        
        # Only bottom footer
        if footer_boundary.top_bottom is not None and footer_boundary.top_right is None:
            footer_clip = pymupdf.Rect(0, footer_boundary.top_bottom, page_width, page_height)
            footer_doc, footer_page = clean_split_section(page, footer_clip, footer_boundary, section_type='bottom_footer')
        
        # Only right footer
        elif footer_boundary.top_bottom is None and footer_boundary.top_right is not None:
            footer_clip = pymupdf.Rect(footer_boundary.left_right, footer_boundary.top_right, page_width, page_height)
            footer_doc, footer_page = clean_split_section(page, footer_clip, footer_boundary, section_type='right_footer')
        
        # Both footers
        else:
            footer_clip = pymupdf.Rect(0, min(footer_boundary.top_bottom, footer_boundary.top_right), page_width, page_height)
            footer_doc, footer_page = clean_split_section(page, footer_clip, footer_boundary, section_type='both_footers')
        
        # Save footer section
        if footer_doc.page_count > 0:
            footer_path = os.path.join(output_dir, f"{base_name}_page{page_num+1}_footer.pdf")
            footer_doc.save(footer_path)
        footer_doc.close()
    
def delete_lines_if_needed(pdf_path: Path, output_dir: str, header_bottom: Optional[float], 
                          footer_boundary: FooterBoundary, save_boundaries_pdf: bool = True) -> None:
    """
    Check if header/footer boundaries intersect with text blocks and draw valid boundaries.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory where output files should be saved
        header_bottom: Y-coordinate of header boundary (or None)
        footer_boundary: FooterBoundary object containing footer coordinates
        save_boundaries_pdf: Whether to save the final PDF with boundary lines
    """
    doc = pymupdf.open(pdf_path)
    base_name = pdf_path.stem
    
    try:
        print(f"Splitting each page into header, main, footer...")
        for page_num in tqdm(range(len(doc))):
            page = doc[page_num]
            page.remove_rotation()
            
            blocks = get_all_blocks(page)
            
            # Calculate page area
            page_area = page.rect.width * page.rect.height

            # Initialize flags for each boundary
            header_valid = True if (header_bottom is not None and header_bottom >= 0) else False
            bottom_footer_valid = True if (footer_boundary.top_bottom is not None and footer_boundary.top_bottom >= 0) else False
            right_footer_valid = True if (footer_boundary.left_right is not None and footer_boundary.left_right >= 0 and footer_boundary.top_right >= 0) else False
            
            
            # Check each block for intersections, only if block is small enough
            for block in blocks:
                bbox = block["bbox"]
                x0, y0, x1, y1 = bbox
                
                # Calculate block area
                block_area = (x1 - x0) * (y1 - y0)
                
                # Only check intersections if block is smaller than 50% of page
                if block_area <= (page_area * 0.5) or block["type"]=="text":
                    # Check header intersection
                    if (header_bottom is not None and 
                        y0 < header_bottom < y1):
                        #page.draw_rect(pymupdf.Rect(bbox), color=(0, 0, 0.9) , width=0.5)
                        header_valid = False
                    
                    # Check bottom footer intersection
                    bottom_footer_intersection = False
                    if (footer_boundary.top_bottom is not None and
                        y0 < footer_boundary.top_bottom < y1):
                        # page.draw_rect(pymupdf.Rect(bbox), color=(0, 0.6, 0), width=0.5)
                        bottom_footer_valid = False
                        bottom_footer_intersection = True
                    
                    # Check right footer horizontal line intersection
                    if (footer_boundary.left_right is not None and
                        footer_boundary.top_right is not None and
                        (x0 < footer_boundary.left_right < x1 and
                        y0 < footer_boundary.top_right < y1)):
                        # page.draw_rect(pymupdf.Rect(bbox), color= (0.9, 0, 0), width=0.5)
                        right_footer_valid = False
                    if bottom_footer_intersection and footer_boundary.left_right is not None:
                        if x0 > footer_boundary.left_right:
                            bottom_footer_valid = True
            
                
            # Create adjusted boundaries based on valid lines
            valid_header = header_bottom if header_valid else None
            valid_footer = FooterBoundary(
                    top_bottom=footer_boundary.top_bottom if bottom_footer_valid else None,
                    top_right=footer_boundary.top_right if right_footer_valid else None,
                    left_right=footer_boundary.left_right if right_footer_valid else None
                )
            
            # Split the page into sections
            split_pdf_in_sections(
                page=page,
                output_dir=output_dir,
                base_name=base_name,
                page_num=page_num,
                header_bottom=valid_header,
                footer_boundary=valid_footer
                )
                
            
            # Draw valid boundaries
            # Header boundary (blue)
            if header_valid:
                page.draw_line(
                    (0, valid_header),
                    (page.rect.width, valid_header),
                    color=(0.25, 0.41, 0.88),
                    width=1.5
                )
            
            # Bottom footer line (green)
            if (bottom_footer_valid):
                end_x = (valid_footer.left_right 
                        if right_footer_valid 
                        else page.rect.width)
                
                page.draw_line(
                    (0, valid_footer.top_bottom),
                    (end_x, valid_footer.top_bottom),
                    color=(0, 0.6, 0),
                    width=1.5
                )
            
            # Right footer lines (red)
            if (right_footer_valid):
                start_y = (valid_footer.top_bottom 
                          if bottom_footer_valid
                          else page.rect.height)
                
                # Vertical line
                page.draw_line(
                    (valid_footer.left_right, start_y),
                    (valid_footer.left_right, valid_footer.top_right),
                    color=(0.9, 0, 0),
                    width=1.5
                )
                
                # Top horizontal line
                page.draw_line(
                    (valid_footer.left_right, valid_footer.top_right),
                    (page.rect.width, valid_footer.top_right),
                    color=(0.9, 0, 0),
                    width=1.5
                )
        
        if save_boundaries_pdf:
            output_path = Path(output_dir).parent / f"{base_name}_final_boundaries.pdf"        
            doc.save(str(output_path))
        
    finally:
        doc.close()
