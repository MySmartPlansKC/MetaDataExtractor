# MetadataExtractor/get_image_metadata.py

import os
from exifread import process_file
from datetime import datetime
import openpyxl
from PIL import Image, ImageDraw, ImageFont

script_dir = os.path.dirname(os.path.realpath(__file__))

# Global Configuration
METADATA_HEADER = "MySmartPlans MetaData Tracker\n\n"
# INPUT_DIRECTORY = os.path.join(script_dir, "../testFiles")  # TESTING
# OUTPUT_DIRECTORY = os.path.join(script_dir, "outputFolder-3")  # TESTING
INPUT_DIRECTORY = os.path.join(script_dir, r"L:\Fresno\Procore Files\Photos\Processed\2024-0422\Unclassified")
OUTPUT_DIRECTORY = os.path.join(script_dir, r"L:\Fresno\Procore Files\Photos\Processed\2024-0422\metadata")

# File tracking
LOG_FILE_PATH = os.path.join(OUTPUT_DIRECTORY, "metadata_log.txt")
CREATE_LOG_FILE = False
METADATA_FORMAT = "xlsx"  # Choose (txt or xlsx)
CREATE_METADATA_FILE = True

# Dynamic Padding Configuration
PADDING_LEFT_FACTOR = 0.03
PADDING_RIGHT_FACTOR = 0.50
PADDING_TOP_FACTOR = 0.02
PADDING_BOTTOM_FACTOR = 0.01

NO_METADATA_MESSAGE = "No Metadata Available\n"


def parse_image_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return date_str


def get_image_metadata(image_path):
    with open(image_path, 'rb') as file:
        tags = process_file(file)
    metadata = {
        "GPS GPSLatitude": [x for x in tags.get('GPS GPSLatitude').values] if tags.get('GPS GPSLatitude') else None,
        "GPS GPSLongitude": [x for x in tags.get('GPS GPSLongitude').values] if tags.get('GPS GPSLongitude') else None,
        "Origin Date": parse_image_date(str(tags.get('EXIF DateTimeOriginal'))) if tags.get(
            'EXIF DateTimeOriginal') else None
    }
    return metadata


def write_metadata(metadata, output_path, METADATA_FORMAT):
    print("DEBUG: Metadata format:", METADATA_FORMAT)
    print("DEBUG: Output path:", output_path)
    if METADATA_FORMAT == "txt":
        with open(output_path, "w") as f:
            f.write(METADATA_HEADER)  # Use the global header

            f.write(f"Filename: {os.path.basename(output_path)}\n")
            f.write("\n")
            for key, value in metadata.items():
                if key == "GPS GPSLatitude" and value:
                    lat_ref = metadata.get("GPS GPSLatitudeRef") or "N"
                    latitude = convert_gps_to_dms(value, lat_ref)
                    f.write(f"Latitude: {latitude}\n")
                elif key == "GPS GPSLongitude" and value:
                    lon_ref = metadata.get("GPS GPSLongitudeRef") or "E"
                    longitude = convert_gps_to_dms(value, lon_ref)
                    f.write(f"Longitude: {longitude}\n")
                else:
                    f.write(f"{key}: {value}\n")

    elif METADATA_FORMAT == "xlsx":
        wb = openpyxl.Workbook()
        sheet = wb.active
        row = 1
        for key, value in metadata.items():
            sheet.cell(row, 1).value = key
            sheet.cell(row, 2).value = value
            row += 1
        wb.save(output_path)
        for column_cells in sheet.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            sheet.column_dimensions[column_cells[0].column_letter].width = length
        wb.save(output_path)
    else:
        raise ValueError("Unsupported format")


def overlay_text(image_path, text, position, output_directory, color=(0, 0, 0), background_color=(255, 255, 255, 128)):
    img = Image.open(image_path).convert('RGBA')

    # Create a new image for semi-transparent overlay
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    width, height = img.size

    # Dynamic Font Scaling
    font_size = max(12, int(height * 0.02))  # Base size of 12, scales with 2% of image height
    font = ImageFont.truetype("arial.ttf", font_size)

    # Dynamic Padding
    padding_left = int(min(width, height) * PADDING_LEFT_FACTOR)
    padding_right = int(padding_left * PADDING_RIGHT_FACTOR)
    padding_top = int(height * PADDING_TOP_FACTOR)
    padding_bottom = int(height * PADDING_BOTTOM_FACTOR)

    if not text:
        text = NO_METADATA_MESSAGE

    text = METADATA_HEADER + text

    text_width, text_height = overlay_draw.textbbox((0, 0), text, font=font)[2:]
    overlay_draw.rectangle(((position[0] - padding_left, position[1] - padding_top),
                            (position[0] + text_width + padding_right, position[1] + text_height + padding_bottom)),
                           fill=background_color)
    overlay_draw.text((position[0], position[1]), text, fill=color, font=font)

    cropped_overlay = overlay.crop((position[0] - padding_left,
                                    position[1] - padding_top,
                                    position[0] + text_width + padding_right,
                                    position[1] + text_height + padding_bottom))

    # Paste only the cropped area onto the original image
    img.paste(cropped_overlay, (position[0] - padding_left, position[1] - padding_top), mask=cropped_overlay)

    # Save to output directory
    filename = os.path.basename(image_path)
    new_name = os.path.splitext(filename)[0] + "_MD.png"
    output_path = os.path.join(output_directory, new_name)
    img.save(output_path)


def convert_gps_to_dms(coordinates, reference):
    degrees = sum(float(x.numerator) / float(x.denominator) for x in coordinates[:1])
    minutes = sum(float(x.numerator) / float(x.denominator) / 60 for x in coordinates[1:2])
    seconds = sum(float(x.numerator) / float(x.denominator) / 3600 for x in coordinates[2:3])
    return f"{degrees:.0f}° {minutes:.0f}' {seconds:.2f}\" {reference}"


def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)


    for root, dirs, files in os.walk(INPUT_DIRECTORY):
        for filename in files:
            filepath = os.path.join(root, filename)

            print(f"Processing file: {filepath}")

            if filepath.lower().endswith((".jpg", ".jpeg")) and not filepath.endswith(("_MD.png", "_MD.txt")):
                metadata = get_image_metadata(filepath)
                output_path = os.path.join(OUTPUT_DIRECTORY,
                                           os.path.splitext(filename)[0] + "_MD." + METADATA_FORMAT)
                if CREATE_METADATA_FILE:
                    write_metadata(metadata, output_path, METADATA_FORMAT)

                if CREATE_LOG_FILE:
                    with open(LOG_FILE_PATH, "a") as log_file:
                        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        log_file.write(f"[{current_datetime}] File {filename} was a PNG and skipped.\n")

                overlay_text_content = ""
                for key, value in metadata.items():
                    if key == "GPS GPSLatitude" and value:
                        lat_ref = metadata.get("GPS GPSLatitudeRef") or "N"
                        latitude = convert_gps_to_dms(value, lat_ref)
                        overlay_text_content += f"Latitude: {latitude}\n"
                    elif key == "GPS GPSLongitude" and value:
                        lon_ref = metadata.get("GPS GPSLongitudeRef") or "E"
                        longitude = convert_gps_to_dms(value, lon_ref)
                        overlay_text_content += f"Longitude: {longitude}\n"
                    elif key == "Origin Date" and value:
                        overlay_text_content += f"Date/Time: {value}\n"

                overlay_text(filepath, overlay_text_content, (10, 10), OUTPUT_DIRECTORY)

            elif filepath.lower().endswith(".png"):
                overlay_text(filepath, "PNG File: Metadata Not Processed", (10, 10), OUTPUT_DIRECTORY)


if __name__ == "__main__":
    main()
