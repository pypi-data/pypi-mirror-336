import pymupdf
from typing import List, Dict, Any

def poly_area(points):
    """Compute the area of the polygon represented by the given points.

    We are using the shoelace algorithm (Gauss) for this.
    """
    # remove duplicated connector points first
    for i in range(len(points) - 1, 0, -1):
        if points[i] == points[i - 1]:
            del points[i]

    area = 0
    for i in range(len(points) - 1):
        p0 = pymupdf.Point(points[i])
        p1 = pymupdf.Point(points[i + 1])
        area += p0.x * p1.y - p1.x * p0.y
    return abs(area) / 2

def refine_boxes(boxes):
    """Join any rectangles with a pairwise non-empty overlap."""
    new_rects = []
    # list of all vector graphic rectangles
    prects = boxes[:]

    while prects:  # the algorithm will empty this list
        r = +prects[0]  # copy of first rectangle
        repeat = True  # initialize condition
        while repeat:
            repeat = False  # set false as default
            for i in range(len(prects) - 1, 0, -1):  # from back to front
                if r.intersects(prects[i]):  # enlarge first rect with this
                    r |= prects[i]
                    del prects[i]  # delete this rect
                    repeat = True  # indicate we must try again

        new_rects.append(r)
        del prects[0]

    new_rects = sorted(set(new_rects), key=lambda r: (r.x0, r.y0))
    return new_rects

def is_significant(box, paths):
    """Check whether the rectangle "box" contains 'signifiant' drawings.

    For this to be true, at least one path must cover an area,
    which is less than 90% of box. Otherwise we assume
    that the graphic is decoration (highlighting, border-only etc.).
    """
    box_area = abs(box) * 0.9  # 90% of area of box

    for p in paths:
        if p["rect"] not in box:
            continue
        if p["type"] == "f" and set([i[0] for i in p["items"]]) == {"re"}:
            # only borderless rectangles are contained: ignore this path
            continue
        points = []  # list of points represented by the items.
        # We are going to append all the points as they occur.
        for itm in p["items"]:
            if itm[0] in ("l", "c"):  # line or curve
                points.extend(itm[1:])  # append all the points
            elif itm[0] == "qu":  # quad
                q = itm[1]
                # follow corners anti-clockwise
                points.extend([q.ul, q.ll, q.lr, q.ur, q.ul])
            else:  # rectangles come in two flavors.
                # starting point is always top-left
                r = itm[1]
                if itm[-1] == 1:  # anti-clockwise (the standard)
                    points.extend([r.tl, r.bl, r.br, r.tr, r.tl])
                else:  # clockwise: area counts as negative
                    points.extend([r.tl, r.tr, r.br, r.bl, r.tl])
        area = poly_area(points)  # compute area of polygon
        if area < box_area:  # less than threshold: graphic is significant
            return True
    return False

def intersects_rects(rect, rect_list):
    delta = (-1, -1, 1, 1)
    for i, r in enumerate(rect_list, start=1):
        if (rect.tl + rect.br) / 2 in r + delta:  # middle point is inside r
            return i
    return 0

def is_contained(rect1, rect2):
    """Check if rect1 is entirely contained within rect2."""
    return rect1.x0 >= rect2.x0 and rect1.x1 <= rect2.x1 and rect1.y0 >= rect2.y0 and rect1.y1 <= rect2.y1

def get_all_blocks(page: pymupdf.Page) -> List[Dict[str, Any]]:
    """Get all content blocks from a page including text, images, tables, graphics, 
    annotations, links and form fields."""
    blocks = []
    
    # Get text blocks from page dictionary
    page_dict = page.get_text("dict")
    blocks.extend({"type": "text", "bbox": block["bbox"]} for block in page_dict["blocks"] if block["type"] == 0)
    
    # Get images
    blocks.extend({"type": "image", "bbox": block["bbox"]} for block in page_dict["blocks"] if block["type"] == 1)
            
    # Get drawings (vector graphics)
    # Select paths not contained in any table
    page_clip = page.rect
    paths = [
        p for p in page.get_drawings()
        if p["rect"] in page_clip
        and p["rect"].width < page_clip.width
        and p["rect"].height < page_clip.height
    ]
    
    for path in paths:
        rect = path['rect']
        if is_significant(rect, paths):
            blocks.append({
                "type": "drawing",
                "bbox": (rect.x0, rect.y0, rect.x1, rect.y1),
            })
    
    # Get tables
    for table in page.find_tables():
        blocks.append({
            "type": "table",
            "bbox": table.bbox
        })
    # Get annotations
    for annot in page.annots():
        blocks.append({
            "type": "annotation",
            "bbox": annot.rect
        })
    
    # Get links
    for link in page.get_links():
        blocks.append({
            "type": "link",
            "bbox": link["from"]
        })
    
    # Get form fields
    widgets = page.widgets()
    for widget in widgets:
        blocks.append({
            "type": "form_field",
            "bbox": widget.rect
        })
    
    return blocks

def get_page_important_object_coordinates(doc, pno, margins=(0, 0, 0, 0), table_strategy="lines_strict", graphics_limit=None):
    """
    Get coordinates of important objects on a page, skipping the PyMuPDF clustering
    to prevent unwanted merging of vector graphics.
    
    Args:
        doc: PyMuPDF document
        pno: Page number
        margins: Tuple of (left, top, right, bottom) margins to exclude
        table_strategy: Strategy for table detection
        graphics_limit: Maximum number of vector graphics to process
        
    Returns:
        Dictionary of coordinates for different object types
    """
    page = doc[pno]
    page.remove_rotation()  # make sure we work on rotation=0
    
    coordinates = {
        "images": [],
        "tables": [],
        "vector_graphics": [],
        "vector_graphics_with_tables": []
    }
    
    # Check graphics limit
    if graphics_limit is not None:
        test_paths = page.get_cdrawings()
        if (excess := len(test_paths)) > graphics_limit:
            print(f"\n**Ignoring page {page.number} with {excess} vector graphics.**")
            return coordinates

    left, top, right, bottom = margins
    clip = page.rect + (left, top, -right, -bottom)

    # --- EXTRACT TABLES ---
    tabs = page.find_tables(clip=clip, strategy=table_strategy)
    tab_rects = {}
    for i, t in enumerate(tabs):
        # Handle tables with and without headers
        try:
            header_rect = pymupdf.Rect(t.header.bbox)
            combined_rect = pymupdf.Rect(t.bbox) | header_rect
        except (AttributeError, TypeError):
            # Table doesn't have a header or header bbox is invalid
            combined_rect = pymupdf.Rect(t.bbox)
            
        tab_rects[i] = combined_rect
        coordinates["tables"].append(combined_rect)
    
    tab_rects0 = list(tab_rects.values())

    # --- EXTRACT VECTOR GRAPHICS ---
    # Use a slightly smaller clip to avoid edge decorations
    page_clip = page.rect + (36, 36, -36, -36)
    
    # Get all paths with filtering
    all_paths = page.get_drawings()
    paths = []
    for p in all_paths:
        if not intersects_rects(p["rect"], tab_rects0) and p["rect"] in page_clip:
            # Keep the size filters, but make them very loose
            if p["rect"].width < page_clip.width * 1.5 and p["rect"].height < page_clip.height * 1.5:
                paths.append(p)
    
    # KEY CHANGE: Skip clustering and use raw drawings directly
    # Only keep ones that pass the significance test
    significant_drawings = []
    for p in paths:
        if is_significant(p["rect"], paths):
            significant_drawings.append(p["rect"])
    
    # --- HANDLE VECTOR GRAPHICS AND TABLES RELATIONSHIPS ---
    for vg in significant_drawings:
        tables_in_vg = [tab for tab in tab_rects0 if tab in vg]
        if tables_in_vg:
            coordinates["vector_graphics_with_tables"].append((vg, tables_in_vg))
        else:
            coordinates["vector_graphics"].append(vg)
    
    # --- EXTRACT IMAGES ---
    img_info = page.get_image_info()[:]
    img_info.sort(key=lambda i: pymupdf.Rect(i["bbox"]).width * pymupdf.Rect(i["bbox"]).height, reverse=True)
    
    filtered_img_info = []
    for i, img in enumerate(img_info):
        img_rect = pymupdf.Rect(img["bbox"]) & page.rect
        is_contained = False
        
        for j, bigger_img in enumerate(img_info):
            if i == j:
                continue
                
            bigger_rect = pymupdf.Rect(bigger_img["bbox"]) & page.rect
            if (img_rect.x0 >= bigger_rect.x0 and img_rect.y0 >= bigger_rect.y0 and
                img_rect.x1 <= bigger_rect.x1 and img_rect.y1 <= bigger_rect.y1):
                is_contained = True
                break
                
        if not is_contained:
            filtered_img_info.append(img)
    
    coordinates["images"] = [pymupdf.Rect(img["bbox"]) for img in filtered_img_info]

    return coordinates

def get_split_coordinates(page_rect, coordinates):
    """
    Generate split coordinates based on the important objects on the page,
    handling intersecting objects and vector graphics with tables.
    """
    all_objects = []
    vg_table_pairs = []  # To keep track of vector graphics and their tables

    # Helper function to validate coordinates
    def is_valid_split(start_y, end_y):
        return (start_y >= page_rect.y0 and 
                end_y <= page_rect.y1 and 
                start_y < end_y)
    
    for obj_type, obj_list in coordinates.items():
        if obj_type != "vector_graphics_with_tables":
            valid_objects = [(rect, obj_type) for rect in obj_list 
                           if is_valid_split(rect.y0, rect.y1)]
            all_objects.extend(valid_objects)
        else:
            for vg, tables in obj_list:
                if is_valid_split(vg.y0, vg.y1):
                    all_objects.append((vg, "vector_graphic"))
                    valid_tables = [table for table in tables 
                                  if is_valid_split(table.y0, table.y1)]
                    all_objects.extend([(table, "table") for table in valid_tables])
                    vg_table_pairs.append((vg, valid_tables))

    # Sort objects by their top y-coordinate
    all_objects.sort(key=lambda x: x[0].y0)

    # Remove objects that are entirely contained within others, considering vg-table relationships
    filtered_objects = []
    for i, (rect1, type1) in enumerate(all_objects):
        if type1 == "table":
            # Check if this table is within its associated vector graphic
            is_within_vg = any(rect1 in vg for vg, tables in vg_table_pairs if rect1 in tables)
            if is_within_vg:
                filtered_objects.append((rect1, type1))
                continue

        if not any(is_contained(rect1, rect2) for j, (rect2, _) in enumerate(all_objects) if i != j):
            filtered_objects.append((rect1, type1))

    # Re-sort filtered objects by their top y-coordinate
    filtered_objects.sort(key=lambda x: x[0].y0)

    splits = []
    current_y = page_rect.y0
    i = 0

    while i < len(filtered_objects):
        obj, obj_type = filtered_objects[i]

        if obj.y0 > current_y and is_valid_split(current_y, obj.y0):
            # Add a split from current_y to the top of this object
            splits.append((current_y, obj.y0, None))

        if obj_type == "vector_graphic":
            # Find tables within this vector graphic
            tables_in_vg = [t for t, t_type in filtered_objects if t_type == "table" and t in obj]

            if tables_in_vg:
                # Add split from top of vector graphic to top of first table
                if is_valid_split(obj.y0, tables_in_vg[0].y0):
                    splits.append((obj.y0, tables_in_vg[0].y0, "vector_graphic"))

                # Process tables and spaces between them
                for j in range(len(tables_in_vg)):
                    table = tables_in_vg[j]
                    splits.append((table.y0, table.y1, "table"))
                    if is_valid_split(table.y0, table.y1):
                        splits.append((table.y0, table.y1, "table"))
                    if j < len(tables_in_vg) - 1:
                        next_table = tables_in_vg[j+1]
                        if is_valid_split(table.y1, next_table.y0):
                            splits.append((table.y1, next_table.y0, "vector_graphic"))


                # Add split from bottom of last table to bottom of vector graphic
                if is_valid_split(tables_in_vg[-1].y1, obj.y1):
                    splits.append((tables_in_vg[-1].y1, obj.y1, "vector_graphic"))
            else:
                # If no tables, add the entire vector graphic as one split
                if is_valid_split(obj.y0, obj.y1):
                    splits.append((obj.y0, obj.y1, "vector_graphic"))

            # Move index past this vector graphic and its tables
            i = max([i] + [filtered_objects.index((t, "table")) for t in tables_in_vg]) + 1
            current_y = obj.y1
        else:
            # Find any intersecting objects
            intersecting = [o for j, (o, _) in enumerate(filtered_objects[i+1:], start=i+1) 
                            if o.y0 < obj.y1]

            if intersecting:
                # Take the object with the smallest top among intersecting objects
                top = min([obj.y0] + [o.y0 for o in intersecting])
                # Take the object with the largest bottom among intersecting objects
                bottom = max([obj.y1] + [o.y1 for o in intersecting])

                # Add a split for this group of intersecting objects
                if is_valid_split(top, bottom):
                    splits.append((top, bottom, obj_type))

                # Move the index to after the last intersecting object
                i += len(intersecting) + 1
                current_y = bottom
            else:
                # If no intersection, add a split for this object
                if is_valid_split(obj.y0, obj.y1):
                    splits.append((obj.y0, obj.y1, obj_type))
                current_y = obj.y1
                i += 1

    # Add a final split if there's space at the bottom of the page
    if current_y < page_rect.y1 and is_valid_split(current_y, page_rect.y1):
        splits.append((current_y, page_rect.y1, None))

    return splits
