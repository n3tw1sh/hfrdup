# File Deduplication Tool

## Overview
This Python script (`hfrdup.py`) helps identify and remove duplicate files using hash-based comparison. It offers multiple modes, including finding duplicates, deleting them globally or within specific folders, and filtering by name pattern or file size.

## Features
- Detect duplicate files using SHA-256 hashing.
- List duplicates in an output file with the original file based on creation time.
- Delete duplicates globally or within individual folders.
- Support regex-based filtering for filenames.
- Filter by minimum and maximum file size.

## Installation
Ensure you have Python installed, then download the script and run:
```sh
pip install argparse
```

## Usage

### Finding Duplicate Files
```sh
python hfrdup.py find <folder_path> -o <output_file>
```
Example:
```sh
python hfrdup.py find ./my_folder -o duplicates.txt
```

### Deleting Duplicates from Log File
```sh
python hfrdup.py del <log_file>
```
Example:
```sh
python hfrdup.py del duplicates.txt
```

### Removing Duplicates per Folder Separately
```sh
python hfrdup.py del_folder <folder_path>
```
Example:
```sh
python hfrdup.py del_folder ./my_folder
```

### Removing Duplicates Globally (Across All Folders)
```sh
python hfrdup.py del_global <folder_path>
```
Example:
```sh
python hfrdup.py del_global ./my_folder
```

### Removing Duplicates Based on a Reference Folder
```sh
python hfrdup.py del_ref -s <source_folder> -t <target_folder>
```
Example:
```sh
python hfrdup.py del_ref -s ./originals -t ./duplicates
```

## Additional Filtering Options

### Filter by File Extension (Regex)
```sh
python hfrdup.py find <folder_path> -o <output_file> -r "\.jpg$"
```
Example (only check `.jpg` files):
```sh
python hfrdup.py find ./photos -o duplicates.txt -r "\.jpg$"
```

### Filter by File Size
- Minimum Size: `--min-size <bytes>`
- Maximum Size: `--max-size <bytes>`

Example (only check files between 1MB and 10MB):
```sh
python hfrdup.py find ./documents -o duplicates.txt --min-size 1048576 --max-size 10485760
```

## Summary
After execution, the script prints the total duplicates found or removed and saves results to the specified file when applicable.

