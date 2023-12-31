
# Update 30 Nov 2023
# Tommy bugs
# Miscellaneous utilities.
#

import os
from tqdm import tqdm
from PIL import Image
import numpy as np

def calculate_coverage(mask_path, threshold=0.01):
    with Image.open(mask_path) as img:
        mask_array = np.array(img)

    # Set all pixels higher than 0 to 255
    mask_array[mask_array > 0] = 255

    total_pixels = mask_array.size
    white_pixels = np.count_nonzero(mask_array)
    percentage_coverage = (white_pixels / total_pixels) * 100

    return percentage_coverage < threshold

def delete_low_coverage_masks(images_folder, masks_folder, threshold=0.01):
    image_files = os.listdir(images_folder)
    mask_files = os.listdir(masks_folder)

    deleted_count = 0

    for image_file in tqdm(image_files, desc="Deleting low-coverage masks"):
        image_path = os.path.join(images_folder, image_file)

        # Extract image name without extension
        image_name = os.path.splitext(image_file)[0]

        # Iterate through possible mask files for the image
        for mask_suffix in ["_1", "_2", "_3", "_4","_5"]:  # Add more if needed
            mask_file = f"{image_name}{mask_suffix}.png"
            mask_path = os.path.join(masks_folder, mask_file)

            if mask_file in mask_files and os.path.exists(mask_path) and calculate_coverage(mask_path, threshold):
                os.remove(mask_path)
                os.remove(image_path)  # Delete corresponding image
                deleted_count += 1

    return deleted_count

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Delete masks with low coverage and corresponding images.')
    parser.add_argument('--images_folder', help='Path to the images folder', required=True)
    parser.add_argument('--masks_folder', help='Path to the masks folder', required=True)
    parser.add_argument('--threshold', type=float, default=0.01, help='Coverage threshold (default: 0.01)')

    args = parser.parse_args()

    deleted_count = delete_low_coverage_masks(args.images_folder, args.masks_folder, args.threshold)

    if deleted_count == 0:
        print("No masks with low coverage found and deleted.")
    else:
        print(f"{deleted_count} masks with low coverage and corresponding images deleted.")

if __name__ == "__main__":
    main()
