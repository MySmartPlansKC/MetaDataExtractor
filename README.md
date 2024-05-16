# Metadata Extractor User Manual

## Introduction
Metadata Extractor is a tool designed to extract and log metadata from JPEG images stored in a specified directory. This document provides detailed instructions on how to set up and use Metadata Extractor effectively.

## Prerequisites
- The executable should be placed in a directory with access to subdirectories named `IMAGES_IN`, `IMAGES_OUT`, and `IMAGES_ERROR`.
- The `IMAGES_IN` directory should contain the JPEG images from which metadata will be extracted.

## Installation
No installation is necessary. Download and run the executable from your chosen directory.

## Usage Instructions
1. **Prepare Image Directory**:
   Ensure that `IMAGES_IN` contains JPEG images. If this directory does not exist or is incorrectly named, the program will terminate with an error message.

2. **Run the Program**:
   Double-click the MetadataExtractor executable to start the process.

3. **Directory Checking**:
   Upon launch, the program checks the `IMAGES_OUT` and `IMAGES_ERROR` directories:
   - If these directories contain files, the program will prompt you to either clear them or abort the operation.
   - Confirm to proceed by typing `y` (yes) to clear the directories or `n` (no) to abort.

4. **Processing Images**:
   The program processes all JPEG images in the `IMAGES_IN` directory, extracts metadata, and logs the results:
   - Extracted metadata and images with overlays (if processed) are saved in `IMAGES_OUT`.
   - Any errors encountered during processing are logged and the problematic images are moved to `IMAGES_ERROR`.

5. **Reviewing Output**:
   - Check the `IMAGES_OUT` directory for processed images and metadata outputs.
   - Errors can be reviewed in the `IMAGES_ERROR` directory and the `metadata_extraction.log` file.

6. **Log File**:
   The `metadata_extraction.log` provides a detailed log of operations including any errors or informational messages generated during processing.

## Configuration Options
- **Metadata Format**: Choose between text (.txt) and Excel (.xlsx) formats for output metadata files through the configuration in the script.

## Troubleshooting
- **Permission Errors**: Ensure the executable has the necessary permissions to read from and write to the specified directories.
- **Missing Images or Directories**: Verify that all required directories exist and contain the correct files before running the executable.

## Version History
- **1.0.0**: Initial release.

For more information or support, please contact the repository maintainer or open an issue on the GitHub repository page.
