import os
import argparse
from pathlib import Path
from PIL import Image
import multiprocessing # Import the multiprocessing module
import functools # For passing multiple arguments with starmap
import logging
from tqdm import tqdm
import time  # Import the time module

# Predefined lists of image mime types
DEFAULT_MIME_TYPES = ["image/jpeg", "image/png", "image/gif"]
DEFAULT_SKIP_TYPES = ["image/webp"]

logging.basicConfig(level=logging.INFO, format="%(message)s")

# --- Worker Function ---
# This function processes a single image file.
# It needs to be defined at the top level so multiprocessing can pickle it.
def _process_single_image(file_path, input_path_base, output_path_base, quality, mime_types, skip_types, delete_original):
    """Worker function to convert a single image to WebP."""
    try:
        # Skip files that are already in WebP format (redundant check, but safer)
        if file_path.suffix.lower() == ".webp":
            return f"Skipped (already WebP): {file_path}"

        # Open the image and check its mime type
        with Image.open(file_path) as img:
            if img.format is None:
                return f"Skipped (unknown format): {file_path}"

            mime_type = Image.MIME.get(img.format)

            if mime_type in skip_types:
                return f"Skipped (mime type {mime_type}): {file_path}"

            if mime_type not in mime_types:
                return f"Skipped (unsupported mime type {mime_type}): {file_path}"

            # Determine output path
            relative_path = file_path.relative_to(input_path_base)
            output_file = output_path_base / relative_path.with_suffix(".webp")
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Convert and save the image as WebP
            img.save(output_file, "WEBP", quality=quality)
            result_msg = f"Converted {file_path} to {output_file}"

            # Delete original file if delete_original is True
            if delete_original:
                try:
                    file_path.unlink()
                    result_msg += f" | Deleted original {file_path}"
                except Exception as del_e:
                    result_msg += f" | FAILED to delete original {file_path}: {del_e}"

            return result_msg

    except Exception as e:
        return f"Error processing {file_path}: {e}"

# --- Main Conversion Logic ---
def convert_to_webp_parallel(input_path, output_path, quality, mime_types, skip_types, delete_original):
    """Converts images in the given path to WebP format using multiprocessing."""
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()

    if not input_path.exists():
        logging.error(f"The input path {input_path} does not exist.")
        return

    if not output_path.exists():
        logging.info(f"Creating output directory: {output_path}")
        output_path.mkdir(parents=True, exist_ok=True)

    tasks = []
    logging.info("Scanning for image files...")
    for root, _, files in os.walk(input_path):
        current_dir = Path(root)
        for file in files:
            file_path = current_dir / file
            if file_path.suffix.lower() == ".webp":
                continue
            tasks.append((
                file_path, input_path, output_path, quality, mime_types, skip_types, delete_original
            ))

    if not tasks:
        logging.info("No eligible image files found to convert.")
        return

    logging.info(f"Found {len(tasks)} potential images to process.")
    logging.info(f"Starting conversion with {os.cpu_count()} worker processes...")

    # Start timing the conversion process
    start_time = time.time()

    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        results = list(tqdm(pool.starmap(_process_single_image, tasks), total=len(tasks)))

    # End timing the conversion process
    end_time = time.time()
    elapsed_time = end_time - start_time

    processed_count = sum(1 for msg in results if "Converted" in msg)
    error_count = sum(1 for msg in results if "Error" in msg)
    skipped_count = sum(1 for msg in results if "Skipped" in msg)

    # Calculate average processing speed
    avg_speed = len(tasks) / elapsed_time if elapsed_time > 0 else 0

    logging.info("--- Conversion Summary ---")
    logging.info(f"Total tasks: {len(tasks)}")
    logging.info(f"Successfully converted: {processed_count}")
    logging.info(f"Skipped: {skipped_count}")
    logging.info(f"Errors: {error_count}")
    logging.info(f"Total time taken: {elapsed_time:.2f} seconds")
    logging.info(f"Average processing speed: {avg_speed:.2f} images/second")
    logging.info("Conversion process finished.")

# --- Main Execution Block ---
def main():
    parser = argparse.ArgumentParser(description="Convert images to WebP format using multiple processes.")
    # Keep arguments the same
    parser.add_argument("path", nargs="?", default=".", help="Path to the directory containing images (default: current directory).")
    parser.add_argument("-o", "--output", default=".", help="Output directory for converted images (default: current directory).")
    parser.add_argument("-q", "--quality", type=int, default=80, help="Quality of the WebP images (default: 80).")
    parser.add_argument("-m", "--mime-types", nargs="*", default=DEFAULT_MIME_TYPES, help="List of image mime types to convert.")
    parser.add_argument("-s", "--skip-types", nargs="*", default=DEFAULT_SKIP_TYPES, help="List of image mime types to skip.")
    parser.add_argument("--delete", action="store_true", help="Delete original files after conversion.")

    args = parser.parse_args()

    # Call the parallel conversion function
    convert_to_webp_parallel(
        input_path=args.path,
        output_path=args.output,
        quality=args.quality,
        mime_types=args.mime_types,
        skip_types=args.skip_types,
        delete_original=args.delete
    )

# --- IMPORTANT: Multiprocessing Guard ---
# This ensures the Pool is only created when the script is run directly,
# crucial on platforms like Windows!!
if __name__ == "__main__":
    # Ensure Pillow uses the correct MIME types (usually automatic, but good practice ig)
    Image.init()
    main()