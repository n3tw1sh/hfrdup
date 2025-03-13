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

def delete_duplicates_from_log(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if line.startswith("DUPLICATE"):
            file_path = line.split("DUPLICATE ")[1].strip()
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def delete_duplicates_per_folder(folder):
    hashes = {}
    
    for root, _, files in os.walk(folder):
        local_hashes = {}
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            
            if file_hash:
                if file_hash in local_hashes:
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                else:
                    local_hashes[file_hash] = file_path

def delete_duplicates_globally(folder):
    hashes = {}
    
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            
            if file_hash:
                if file_hash in hashes:
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                else:
                    hashes[file_hash] = file_path

def delete_duplicates_with_reference(source_folder, target_folder):
    source_hashes = {}
    
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            if file_hash:
                source_hashes[file_hash] = file_path
    
    for root, _, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            
            if file_hash in source_hashes:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="File Deduplication Tool")
    parser.add_argument("mode", choices=["find", "del", "del_folder", "del_global", "del_ref"], help="Mode: find, del, del_folder, del_global, del_ref")
    parser.add_argument("path", nargs="?", help="Path to folder or log file (not required for del_ref)")
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
    elif args.mode == "del":
        delete_duplicates_from_log(args.path)
    elif args.mode == "del_folder":
        delete_duplicates_per_folder(args.path)
    elif args.mode == "del_global":
        delete_duplicates_globally(args.path)
    elif args.mode == "del_ref":
        if not args.source or not args.target:
            print("Error: -s/--source and -t/--target are required for 'del_ref'")
            return
        delete_duplicates_with_reference(args.source, args.target)

if __name__ == "__main__":
    main()
