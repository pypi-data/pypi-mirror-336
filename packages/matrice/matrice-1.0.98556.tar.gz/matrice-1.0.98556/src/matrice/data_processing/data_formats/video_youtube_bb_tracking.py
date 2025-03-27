import os
import logging
from matrice.data_processing.server_utils import (
get_corresponding_split_type,
generate_short_uuid
)
import os
import configparser
import pandas as pd

def calculate_mot_bbox_properties(bbox):
        """Calculate properties for MOT bounding box [x, y, width, height]"""
        x, y, width, height = bbox
        return {
            "bbox": bbox,
            "height": height,
            "width": width,
            "center": [x + width/2, y + height/2],
            "area": width * height
        }

import os
import pandas as pd
import logging
import configparser

import os
import logging
import pandas as pd

def get_youtube_bb_video_frame_details(dataset_path):
    """
    Process YouTube Bounding Box dataset and extract details for each video sequence.

    Args:
        dataset_path (list): List of paths to CSV annotation files.

    Returns:
        Tuple containing:
        - Dictionary of video details indexed by youtube_id
        - List of frames missing annotations
        - Dictionary of class-wise statistics
    """
    complete_videos = {}
    missing_annotations = []
    classwise_stats = {}

    if not isinstance(dataset_path, list) or not all(os.path.exists(path) for path in dataset_path):
        logging.error(f"Invalid dataset paths provided: {dataset_path}")
        return complete_videos, missing_annotations, classwise_stats
    
    for csv_file in dataset_path:
        try:
            annotations = pd.read_csv(csv_file)
        except Exception as e:
            logging.error(f"Error reading CSV file {csv_file}: {e}")
            continue

        # Infer split type from the file name (train, test, val)
        split_match = re.search(r'(train|test|val)', os.path.basename(csv_file).lower())
        split = split_match.group(0) if split_match else 'unknown'

        # Group by youtube_id and sort by timestamp_ms within each video
        grouped = annotations.groupby('youtube_id')
        for youtube_id, group in grouped:
            group = group.sort_values(by='timestamp_ms').reset_index(drop=True)

            frame_rate = 30  # Assuming fixed frame rate (YouTube BB standard)

            metadata = {
                'sequence_name': youtube_id,
                'splitType': split,
                'total_frames': len(group),
                'frame_rate': frame_rate,
                'duration_seconds': len(group) / frame_rate,
                'video_height': 640,  # TODO: Make dynamic
                'video_width': 640,   # TODO: Make dynamic
                'annotation': {},
            }

            expected_frames = {
                i: {
                    "frame_id": i,
                    "file_name": f"{youtube_id}_{i}.jpg",
                    "file_path": os.path.join(os.path.dirname(csv_file), youtube_id, f"{youtube_id}_{i}.jpg"),
                    "has_annotations": False
                }
                for i in range(len(group))
            }

            # Process annotations
            for i, row in group.iterrows():
                class_name = row['class_name']
                bbox = [
                    row['xmin'], row['ymin'],
                    row['xmax'] - row['xmin'],
                    row['ymax'] - row['ymin']
                ]

                annotation_json = {
                    "id": str(generate_short_uuid()),
                    "order": i,
                    "file_name": expected_frames[i]['file_name'],
                    "file_location": expected_frames[i]['file_path'],
                    "bbox": bbox,
                    "height": bbox[3],
                    "width": bbox[2],
                    "center": [(bbox[0] + bbox[2] / 2), (bbox[1] + bbox[3] / 2)],
                    "area": bbox[2] * bbox[3],
                    "confidence": row['object_presence'],
                    "category": class_name,
                    "visibility": row['object_presence'],
                    "segmentation": [],
                    "isCrowd": [],
                    "masks": [],
                }

                # Store annotations under the frame index
                frame_key = str(i)
                if frame_key not in metadata['annotation']:
                    metadata['annotation'][frame_key] = []
                metadata['annotation'][frame_key].append(annotation_json)

                # Mark frame as annotated
                expected_frames[i]['has_annotations'] = True

                # Update class statistics
                if class_name not in classwise_stats:
                    classwise_stats[class_name] = {"train": 0, "test": 0, "val": 0}
                classwise_stats[class_name][split] += 1

            # Add missing frames
            for frame_id, frame_info in expected_frames.items():
                if not frame_info['has_annotations']:
                    missing_annotations.append(frame_info['file_path'])

                # Ensure each frame has an entry in annotations
                frame_key = str(frame_id)
                if frame_key not in metadata['annotation']:
                    metadata['annotation'][frame_key] = []

            # Store complete metadata
            complete_videos[youtube_id] = metadata

    # Add total count for each class
    for category, counts in classwise_stats.items():
        counts['total'] = sum(counts.values())

    logging.info(f"Complete video sequences: {len(complete_videos)}")
    logging.info(f"Frames missing annotations: {len(missing_annotations)}")
    logging.info(f"Class-wise statistics: {classwise_stats}")

    return complete_videos, missing_annotations, classwise_stats




def add_youtube_bb_dataset_items_details(batch_dataset_items, frames_details):
    logging.debug(f'batch_dataset_items: {batch_dataset_items}')
    logging.debug(f'frames_details: {frames_details}')
    
    """Update MOT dataset items with frame details from the processed annotations.

    Args:
        batch_dataset_items: List of dataset items, each containing at least a 'file_path' key
        frames_details: Dictionary of frame details indexed by frame file path

    Returns:
        List of processed dataset items with updated information
    """
    import logging
    
    processed_batch = []

    for dataset_item in batch_dataset_items:
        split_type = get_corresponding_split_type(dataset_item.get('fileLocation'))
        file_name = dataset_item.get('filename')

        matched = False

        for video_key, video_data in frames_details.items():
            if video_data.get('splitType') == split_type:
                for frame_id, annotations in video_data.get('annotation', {}).items():
                    for annotation in annotations:
                        if annotation.get('file_name') == file_name:
                            dataset_item.update(video_data)  # Add video-level details
                            dataset_item.update(annotation)  # Add frame-level details
                            processed_batch.append(
                                {
                                    "sample_details": dataset_item,
                                    "is_complete": all(
                                        dataset_item.get(k) is not None
                                        for k in ["video_height", "video_width"]
                                    ),
                                }
                            )
                            matched = True
                            break
                    if matched:
                        break
            if matched:
                break

        if not matched:
            logging.warning(f"'{file_name}' not found in frames_details")

    return processed_batch
