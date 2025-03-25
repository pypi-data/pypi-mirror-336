import pymupdf
from typing import Tuple, Optional
from ..config import FooterBoundary
from .pdf import get_all_blocks
from tqdm.auto import tqdm

def is_fully_contained_in_header(block: Tuple[float, float, float, float], header_boundary: float) -> bool:
    _, y0, _, y1 = block
    return y0 >= 0 and y1 <= header_boundary

def is_fully_contained_in_bottom_footer(block: Tuple[float, float, float, float], 
                                      footer_boundary: float, page_height: float) -> bool:
    _, y0, _, y1 = block
    return y0 >= footer_boundary and y1 <= page_height

def is_fully_contained_in_right_footer(block: Tuple[float, float, float, float], 
                                     right_boundary: float, page_width: float) -> bool:
    x0, _, x1, _ = block
    return x0 >= right_boundary and x1 <= page_width

def detect_header_footer_boundaries(pdf_path: str, 
                                  n_pages: int = 3, 
                                  header_height_ratio: float = 0.25,
                                  footer_height_ratio: float = 0.25,
                                  right_width_ratio: float = 0.15,
                                  margin: float = 10) -> Tuple[Optional[float], FooterBoundary]:
    try:
        doc = pymupdf.open(pdf_path)
        
        # Check document has only one page
        if len(doc) == 1:
            return None, FooterBoundary()
        # Get first page to set initial boundaries
        first_page = doc[0]
        page_height = first_page.rect.height
        page_width = first_page.rect.width
        
        # Initial boundaries
        initial_header_boundary = page_height * header_height_ratio
        initial_footer_boundary = page_height * (1 - footer_height_ratio)
        initial_right_boundary = page_width * (1 - right_width_ratio)
        
        # Phase 1: Initial check in first n_pages
        pages_with_header = 0
        pages_with_bottom_footer = 0
        pages_with_right_footer = 0
        print("Checking if the pdf has headers or footers...")
        for page_num in tqdm(range(min(n_pages, len(doc)))):
            page = doc[page_num]
            text_blocks = get_all_blocks(page)
            
            # Check each region
            found_header = any(is_fully_contained_in_header(block["bbox"], initial_header_boundary) 
                             for block in text_blocks)
            found_right = any(is_fully_contained_in_right_footer(block["bbox"], initial_right_boundary, page_width) 
                            for block in text_blocks)
            found_bottom = any(is_fully_contained_in_bottom_footer(block["bbox"], initial_footer_boundary, page_height) 
                             for block in text_blocks)
            
            if found_header:
                pages_with_header += 1
            if found_right:
                pages_with_right_footer += 1
            if found_bottom:
                pages_with_bottom_footer += 1
            
        # Check if regions exist in first n_pages
        check_pages = min(n_pages, len(doc))
        header_exists = pages_with_header == check_pages
        right_footer_exists = pages_with_right_footer == check_pages
        bottom_footer_exists = pages_with_bottom_footer == check_pages
        
        if not (header_exists or right_footer_exists or bottom_footer_exists):
            return None, FooterBoundary()
            
        # Phase 2: Verify and get boundaries
        header_bottom = None
        footer_boundary = FooterBoundary()
        
        # First process right footer
        if right_footer_exists:
            print("Adding right footer line...")
            for page_num in tqdm(range(len(doc))):
                page = doc[page_num]
                text_blocks = get_all_blocks(page)
                
                # Get right footer blocks
                right_blocks = [block["bbox"] for block in text_blocks 
                              if is_fully_contained_in_right_footer(block["bbox"], 
                                                                  initial_right_boundary, 
                                                                  page_width)]
                
                if not right_blocks:  # If any page has no right footer blocks, invalidate
                    right_footer_exists = False
                    break
                    
                # Update right footer boundaries (keeping most restrictive)
                page_right_top = min(block[1] for block in right_blocks)
                page_right_left = min(block[0] for block in right_blocks)
                
                if footer_boundary.top_right is None or page_right_top > footer_boundary.top_right:
                    footer_boundary.top_right = page_right_top
                if footer_boundary.left_right is None or page_right_left > footer_boundary.left_right:
                    footer_boundary.left_right = page_right_left
        
        # Then process bottom footer, excluding right footer blocks
        if bottom_footer_exists:
            print("Adding bottom footer line...")
            for page_num in tqdm(range(len(doc))):
                page = doc[page_num]
                text_blocks = get_all_blocks(page)
                
                # Get bottom footer blocks, excluding those in right footer area
                bottom_blocks = []
                for block in text_blocks:
                    bbox = block["bbox"]
                    if is_fully_contained_in_bottom_footer(bbox, initial_footer_boundary, page_height):
                        if right_footer_exists:
                            # Only include if not in right footer area
                            if not is_fully_contained_in_right_footer(bbox, initial_right_boundary, page_width):
                                bottom_blocks.append(bbox)
                        else:
                            bottom_blocks.append(bbox)
                
                if not bottom_blocks:  # If any page has no bottom footer blocks, invalidate
                    bottom_footer_exists = False
                    break
                
                # Update bottom footer boundary (keeping most restrictive)
                page_footer_top = min(block[1] for block in bottom_blocks)
                if footer_boundary.top_bottom is None or page_footer_top > footer_boundary.top_bottom:
                    footer_boundary.top_bottom = page_footer_top
        
        # Finally process header
        if header_exists:
            print("Adding header line...")
            for page_num in tqdm(range(len(doc))):
                page = doc[page_num]
                text_blocks = get_all_blocks(page)
                
                header_blocks = [block["bbox"] for block in text_blocks 
                               if is_fully_contained_in_header(block["bbox"], initial_header_boundary)]
                
                if not header_blocks:  # If any page has no header blocks, invalidate
                    header_exists = False
                    break
                
                # Update header boundary (keeping most restrictive)
                page_header_bottom = max(block[3] for block in header_blocks)
                if header_bottom is None or page_header_bottom < header_bottom:
                    header_bottom = page_header_bottom
        
        # Clean up invalid boundaries
        if not right_footer_exists:
            footer_boundary.top_right = None
            footer_boundary.left_right = None
        if not bottom_footer_exists:
            footer_boundary.top_bottom = None
        if not header_exists:
            header_bottom = None
            
        # Apply margins
        if header_bottom is not None:
            header_bottom += margin
        if footer_boundary.top_bottom is not None:
            footer_boundary.top_bottom -= margin
        if footer_boundary.top_right is not None:
            footer_boundary.top_right -= margin
        if footer_boundary.left_right is not None:
            footer_boundary.left_right -= (margin/2)
        
        return header_bottom, footer_boundary
        
    finally:
        if 'doc' in locals():
            doc.close()
