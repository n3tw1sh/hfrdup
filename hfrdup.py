import os
import hashlib
import argparse
import re

def get_file_hash(file_path, hash_algo=hashlib.sha256):
    hasher = hash_algo()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

def get_creation_time(file_path):
    try:
        return os.path.getctime(file_path)
    except Exception as e:
        print(f"Error getting creation time for {file_path}: {e}")
        return float('inf')

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        print(f"Error getting size for {file_path}: {e}")
        return -1

def find_duplicate_files(folder, output_file, regex_filter=None, min_size=None, max_size=None):
    hashes = {}
    duplicates = {}
    total_duplicates = 0
    pattern = re.compile(regex_filter) if regex_filter else None
    
    for root, _, files in os.walk(folder):
        for file in files:
            if pattern and not pattern.search(file):
                continue
            file_path = os.path.join(root, file)
            file_size = get_file_size(file_path)
            if (min_size and file_size < min_size) or (max_size and file_size > max_size):
                continue
            file_hash = get_file_hash(file_path)
            
            if file_hash:
                if file_hash in hashes:
                    duplicates.setdefault(file_hash, []).append(file_path)
                    total_duplicates += 1
                else:
                    hashes[file_hash] = file_path
    
    with open(output_file, 'w') as f:
        for file_hash, paths in duplicates.items():
            all_files = [hashes[file_hash]] + paths
            original_file = min(all_files, key=get_creation_time)
            duplicates_only = [p for p in all_files if p != original_file]
            
            f.write(f"{file_hash}\n")
            f.write(f"ORIGINAL {original_file}\n")
            for dup in duplicates_only:
                f.write(f"DUPLICATE {dup}\n")
            f.write("\n")
    
    print(f"Duplicate file list saved to {output_file}")
    print(f"Total duplicate files found: {total_duplicates}")

def main():
    parser = argparse.ArgumentParser(description="File Deduplication Tool")
    parser.add_argument("mode", choices=["find", "del", "del_folder", "del_global", "del_ref"], help="Mode: find, del, del_folder, del_global, del_ref")
    parser.add_argument("path", help="Path to folder or log file")
    parser.add_argument("-o", "--output", help="Output file (for 'find')")
    parser.add_argument("-s", "--source", help="Source folder (for 'del_ref')")
    parser.add_argument("-t", "--target", help="Target folder (for 'del_ref')")
    parser.add_argument("-r", "--regex", help="Regex filter for file names")
    parser.add_argument("--min-size", type=int, help="Minimum file size in bytes")
    parser.add_argument("--max-size", type=int, help="Maximum file size in bytes")
    args = parser.parse_args()
    
    if args.mode == "find":
        if not args.output:
            print("Error: -o/--output is required for 'find'")
            return
        find_duplicate_files(args.path, args.output, regex_filter=args.regex, min_size=args.min_size, max_size=args.max_size)
    
if __name__ == "__main__":
    main()
