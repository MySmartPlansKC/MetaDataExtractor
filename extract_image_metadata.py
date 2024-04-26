from PIL import Image

def extract_image_metadata(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        return exif_data if exif_data is not None else {}

def write_metadata_to_file(metadata, output_file_path):
    with open(output_file_path, 'w') as file:
        if metadata:
            for tag, value in metadata.items():
                file.write(f"{tag}: {value}\n")
        else:
            file.write("No metadata found.\n")

# Example usage
image_metadata = extract_image_metadata(r'C:\Programming\Python\MetadataExtractor\testFiles\one.jpeg')
write_metadata_to_file(image_metadata, r'C:\Programming\Python\MetadataExtractor\outputFolder\image_metadata_output.txt')