import os
from pathlib import Path
import pymupdf
import pymupdf4llm
from .pdf import get_page_important_object_coordinates, get_split_coordinates
import re
from typing import Optional


def process_split_to_markdown(split_path):
    """
    Process a single PDF split and convert it to markdown,
    removing any trailing newlines.
    """
    return pymupdf4llm.to_markdown(split_path, write_images=False, margins=(0,0,0,0), show_progress=False)
    
def split_and_convert_to_markdown(input_pdf_path, output_folder):
    """
    Split the PDF based on important objects, convert each split to markdown,
    and combine into a single markdown file with appropriate delimiters.
    """
    os.makedirs(output_folder, exist_ok=True)
    doc = pymupdf.open(input_pdf_path)
    
    all_markdown = ""
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        coordinates = get_page_important_object_coordinates(doc, page_num)
        splits = get_split_coordinates(page.rect, coordinates)

        page_markdown = ""
        
        for i, (start_y, end_y, split_type) in enumerate(splits):
            

            # Create a new PDF for this split
            output_doc = pymupdf.open()
            output_page = output_doc.new_page(width=page.rect.width, height=(end_y - start_y))
            # Copy the content from the original page to the new page
            output_page.show_pdf_page(
                output_page.rect,
                doc,
                page_num,
                clip=pymupdf.Rect(page.rect.x0, start_y, page.rect.x1, end_y),
                overlay = False
            )
            
            # Save the split PDF
            split_type_str = split_type if split_type else "text"
            output_filename = f"{os.path.splitext(os.path.basename(input_pdf_path))[0]}_page_{page_num + 1}_split_{i + 1}_{split_type_str}.pdf"
            output_path = os.path.join(output_folder, output_filename)
            output_doc.save(output_path)
            
            # Convert split to markdown
            split_markdown = process_split_to_markdown(output_path)
            
            # Remove the "-----" at the end of the split (if it exists)
            split_markdown = split_markdown.rstrip('-\n')
            
            # Add custom delimiters
            page_markdown += f"{split_markdown}\n"
            
            output_doc.close()
            os.remove(output_path)  # Remove the temporary split PDF file
        
        # Add page delimiter
        all_markdown += page_markdown
    
    doc.close()

    return all_markdown

def create_json_object(accumulated_result: Optional[dict], input_pdf_path: str, text: str) -> dict:
    """
    Process a PDF section and accumulate results across multiple calls.
    
    Args:
        accumulated_result (Optional[dict]): Previous result to accumulate with. None for first call.
        input_pdf_path (str): Path in format "split_sections/{name}_page{number}_{section}.pdf"
        text (str): The text content to be assigned to the appropriate section
        
    Returns:
        dict: Updated accumulated result with the new section
    """
    # Initialize result structure if this is the first call
    if accumulated_result is None:
        accumulated_result = {
            "pdf_with_lines": None,
            "pages": {}  # Using dict for accumulation, will convert to list at the end
        }
    
    # Convert to Path object and get just the filename
    path = Path(input_pdf_path)
    filename = path.name

    # Extract components from the input path using regex
    pattern = r"(.+)_page(\d+)_(header|main|footer)\.pdf"
    match = re.match(pattern, filename)
    
    if not match:
        raise ValueError("Invalid filename format")
    
    name, page_number, section = match.groups()
    page_number = int(page_number)
    # Set the pdf_with_lines path if not already set
    if accumulated_result["pdf_with_lines"] is None:
        accumulated_result["pdf_with_lines"] = f"{name}_final_boundaries.pdf"
    
    # Initialize the page dictionary if it doesn't exist
    if page_number not in accumulated_result["pages"]:
        accumulated_result["pages"][page_number] = {
            "number": page_number,
            "header": None,
            "body": None,
            "footer": None
        }
    
    # Update the appropriate section
    if section == "header":
        accumulated_result["pages"][page_number]["header"] = text
    elif section == "main":
        accumulated_result["pages"][page_number]["body"] = text
    elif section == "footer":
        accumulated_result["pages"][page_number]["footer"] = text
    return accumulated_result
