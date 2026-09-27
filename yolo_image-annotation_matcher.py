import os
import shutil
from pathlib import Path

def match_and_organize_files(images_folder, annotations_folder, output_base_folder):
    """
    Match images with their corresponding annotation files and copy them to new folders.
    
    Args:
        images_folder: Path to folder containing images
        annotations_folder: Path to folder containing .txt annotations
        output_base_folder: Path where new organized folders will be created
    """
    
    # Create output directories
    output_images = os.path.join(output_base_folder, "matched_images")
    output_annotations = os.path.join(output_base_folder, "matched_annotations")
    
    os.makedirs(output_images, exist_ok=True)
    os.makedirs(output_annotations, exist_ok=True)
    
    # Get all image files (common image extensions)
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    image_files = [f for f in os.listdir(images_folder) 
                   if os.path.splitext(f.lower())[1] in image_extensions]
    
    # Get all annotation files
    annotation_files = [f for f in os.listdir(annotations_folder) 
                        if f.endswith('.txt')]
    
    # Create a set of annotation basenames (without extension) for quick lookup
    annotation_basenames = {os.path.splitext(f)[0] for f in annotation_files}
    
    # Track results
    matched_count = 0
    unmatched_images = []
    unmatched_annotations = []
    counter = 1
    
    print(f"Found {len(image_files)} images and {len(annotation_files)} annotations")
    print("\nMatching files...")
    
    # Match images with annotations
    for image_file in image_files:
        image_basename = os.path.splitext(image_file)[0]
        
        if image_basename in annotation_basenames:
            # Found a match! Copy both files
            annotation_file = image_basename + '.txt'
            
            # Copy image
            if counter % 1 == 0:
                src_image = os.path.join(images_folder, image_file)
                dst_image = os.path.join(output_images, image_file)
                shutil.copy2(src_image, dst_image)
                
                # Copy annotation
                src_annotation = os.path.join(annotations_folder, annotation_file)
                dst_annotation = os.path.join(output_annotations, annotation_file)
                shutil.copy2(src_annotation, dst_annotation)
            
            matched_count += 1

            print(f"Matched: {image_file} <-> {annotation_file}")
        else:
            unmatched_images.append(image_file)
        counter += 1
    
    # Find annotations without matching images
    image_basenames = {os.path.splitext(f)[0] for f in image_files}
    for annotation_file in annotation_files:
        annotation_basename = os.path.splitext(annotation_file)[0]
        if annotation_basename not in image_basenames:
            unmatched_annotations.append(annotation_file)
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f" Successfully matched and copied: {counter} pairs")
    print(f" Unmatched images: {len(unmatched_images)}")
    print(f" Unmatched annotations: {len(unmatched_annotations)}")
    
    if unmatched_images:
        print("\nImages without annotations:")
        for img in unmatched_images[:10]:  # Show first 10
            print(f"  - {img}")
        if len(unmatched_images) > 10:
            print(f"  ... and {len(unmatched_images) - 10} more")
    
    if unmatched_annotations:
        print("\nAnnotations without images:")
        for ann in unmatched_annotations[:10]:  # Show first 10
            print(f"  - {ann}")
        if len(unmatched_annotations) > 10:
            print(f"  ... and {len(unmatched_annotations) - 10} more")
    
    print(f"\nMatched files saved to:")
    print(f"Images: {output_images}")
    print(f"Annotations: {output_annotations}")


if __name__ == "__main__":
    # CONFIGURE THESE PATHS
    images_folder = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\infra_record_extracted_uncompressed"
    annotations_folder = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\annot_infra_record_extracted_uncompressed"
    output_base_folder = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\infra_record_extract"
    # Run the matching
    match_and_organize_files(images_folder, annotations_folder, output_base_folder)