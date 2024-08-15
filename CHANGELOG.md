# Metadata Extractor

# Changelog

## [2.2.0] - 2024-08-15
### Added
- Added sorting function to place files into folders classified by date.

### Changed
- Adjusted input options to include an option to delete the previous log file.

---

## [2.1.0] - 2024-06-11
### Fixed
- Adjusted GPS coordinates to properly display Degrees Minutes and Seconds

---

## [2.0.0] - 2024-05-24
### Changed
- Changed libraries for GPS data

---

## [1.1.0] - 2024-05-24
### Added
- More robust error handling and user input on error.
- Increased MAX_IMAGE_PIXELS to 300000000

---

## [1.0.1] - 2024-05-16
### Added
- Functionality to remove processed files from the `IMAGES_IN` folder after successful processing.

---

## [1.0.0] - Initial Release - 2024-04-29
### Added
- Initial implementation of metadata extraction from images.
- Support for reading EXIF data and converting GPS coordinates.
- Capability to write metadata to both text and Excel files.
- Function to overlay metadata text onto images.
- Directory management for input, output, and error directories.