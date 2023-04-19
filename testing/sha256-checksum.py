import hashlib
import os
import sys
import argparse

def hash_file(filepath, algorithm="sha256"):
    """
    Calculate the hash value of a file using the specified algorithm
    """
    with open(filepath, "rb") as f:
        hasher = hashlib.new(algorithm)
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def check_pyinstaller(main_file, compiled_file):
    """
    Check if the specified compiled file matches the source code in the main file
    """
    main_hash = hash_file(main_file)
    compiled_hash = hash_file(compiled_file)
    return main_hash == compiled_hash

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("main_file", help="path to the main Python file")
    parser.add_argument("compiled_file", help="path to the compiled file")
    args = parser.parse_args()

    if not os.path.isfile(args.main_file):
        print(f"Error: {args.main_file} is not a file", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(args.compiled_file):
        print(f"Error: {args.compiled_file} is not a file", file=sys.stderr)
        sys.exit(1)

    if check_pyinstaller(args.main_file, args.compiled_file):
        print(f"The compiled file {args.compiled_file} matches the source code in {args.main_file}")
    else:
        print(f"Warning: The compiled file {args.compiled_file} does not match the source code in {args.main_file}")
