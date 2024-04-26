import PyPDF2


def extract_pdf_metadata(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata
        # Ensure metadata is present and iterable
        if metadata and isinstance(metadata, dict):
            # Return cleaned up metadata, removing any leading '/' from keys
            return {key[1:] if key.startswith('/') else key: str(metadata[key]) for key in metadata}
        else:
            return {}  # Return an empty dictionary if no metadata is present


def write_metadata_to_file(metadata, output_file_path):
    with open(output_file_path, 'w') as file:
        if metadata:
            for key, value in metadata.items():
                file.write(f"{key}: {value}\n")
        else:
            file.write("No metadata found.\n")


# Example usage
pdf_metadata = extract_pdf_metadata(r'C:\Programming\Python\MetadataExtractor\testFiles\MySmartPMO_VIZNS.pdf')
write_metadata_to_file(pdf_metadata, r'C:\Programming\Python\MetadataExtractor\outputFolder\pdf_metadata_output.txt')
print(pdf_metadata)
