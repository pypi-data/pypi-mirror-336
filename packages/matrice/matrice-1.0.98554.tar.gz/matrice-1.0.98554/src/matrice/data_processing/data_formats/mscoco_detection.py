import os
import json
import traceback
import logging
from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
    generate_short_uuid
)

def calculate_bbox_properties(bbox):
    if len(bbox) != 4:
        raise ValueError("Bounding box must be in the format [x_min, y_min, width, height].")
    
    x_min, y_min, width, height = bbox
    
    center_x = x_min + width / 2
    center_y = y_min + height / 2
    
    area = width * height
    
    return {
        "height": float(height),
        "width": float(width), 
        "center": [float(center_x), float(center_y)],
        "area": float(area)
    }

def get_msococ_annotation_details(annotations, image_info, category_map, split_type):
    annotations_details = {}
    for annotation in annotations:
        if not isinstance(annotation, dict) or "image_id" not in annotation:
            continue

        image_id = annotation["image_id"]
        image_details = image_info.get(image_id)
        if not image_details:
            continue
            
        key = f"{split_type}/{image_details.get('file_name')}"

        bbox = [float(coord) for coord in annotation.get("bbox", [])]
        if not bbox or len(bbox) != 4:
            continue

        try:
            bbox_properties = calculate_bbox_properties(bbox)

            annotation_json = {
                "id": str(generate_short_uuid()),
                "segmentation": [
                    [float(coord) for coord in segment]
                    for segment in annotation.get("segmentation", []) if isinstance(segment, list)
                ],
                "isCrowd": [
                    float(item) if isinstance(item, (int, float)) else 0
                    for item in (
                        annotation.get("iscrowd", [0])
                        if isinstance(annotation.get("iscrowd"), list)
                        else [annotation.get("iscrowd", 0)]
                    )
                ],
                "confidence": float(annotation.get("confidence", 0.0)),
                "bbox": bbox,
                "height": bbox_properties["height"],
                "width": bbox_properties["width"],
                "center": bbox_properties["center"],
                "area": float(annotation.get("area", bbox_properties["area"])),
                "category": str(
                    category_map.get(annotation.get("category_id"), "Unknown")
                ),
                "masks": annotation.get("segmentation", []),
            }
            if key not in annotations_details:
                annotations_details[key] = []
            annotations_details[key].append(annotation_json)

        except Exception as e:
            logging.error(f"Error processing annotation: {e}")
            continue

    return annotations_details

def get_msococo_images_details(annotation_files):
    """Process MSCOCO annotation files and extract image details.

    Args:
        annotation_files: List of paths to MSCOCO annotation JSON files

    Returns:
        Dictionary of image details indexed by file location
    """
    images_annotations_details = {}

    logging.info(f"Processing {len(annotation_files)} annotation files")

    if not annotation_files:
        logging.error("No annotation files provided")
        return images_annotations_details

    for file_index, file_path in enumerate(annotation_files, 1):
        logging.debug(f"\nProcessing file {file_index}/{len(annotation_files)}: {file_path}")

        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            continue

        try:
            with open(file_path) as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    logging.error(f"Invalid JSON in {file_path}: {e}")
                    continue

            images = data.get("images", [])
            categories = data.get("categories", [])
            annotations = data.get("annotations", [])

            if not images:
                logging.error(f"Missing images in {file_path}")
                continue

            # Build lookup maps
            image_info = {
                img["id"]: img
                for img in images
                if isinstance(img, dict) and "id" in img
            }
            category_map = {
                cat["id"]: cat["name"]
                for cat in categories
                if isinstance(cat, dict) and "id" in cat
            }

            split_type = get_corresponding_split_type(file_path, include_year=False)

            annotations_details = get_msococ_annotation_details(annotations, image_info, category_map, split_type)
            
            for image in images:
                if not isinstance(image, dict):
                    continue
                    
                image_details = image.copy()
                image_details["split_type"] = split_type
                image_details["splitType"] = split_type
                
                key = f"{split_type}/{image_details.get('file_name')}"
                image_details['annotations'] = annotations_details.get(key, [])
                
                if "height" in image_details and "width" in image_details:
                    image_details.update({
                        "image_height": int(image_details["height"]),
                        "image_width": int(image_details["width"]),
                        "image_area": int(
                            image_details.get(
                                "area",
                                float(image_details["height"]) * float(image_details["width"])
                            )
                        ),
                    })
                    
                images_annotations_details[key] = image_details

        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
            traceback.print_exc()

    return images_annotations_details

def add_mscoco_dataset_items_details(batch_dataset_items, images_details):
    processed_batch = []
    for dataset_item in batch_dataset_items:
        if not dataset_item:
            continue
            
        image_key = f"{get_corresponding_split_type(dataset_item.get('fileLocation'))}/{dataset_item.get('filename')}"
        if image_key not in images_details:
            logging.warning(f"'{image_key}' not found in images_details")
            continue
            
        dataset_item.update(images_details[image_key])
        processed_batch.append({
            "sample_details": dataset_item,
            "is_complete": all(
                k in dataset_item
                for k in ["image_height", "image_width"]
            ),
        })
    return processed_batch