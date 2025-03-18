# agents.py

"""
agents.py

This script implements an agent that:
1. Scans an input folder for files,
2. Identifies file types,
3. Moves files into categorized folders,
4. Compresses PDFs using ConvertAPI and images using TinyPNG.
"""

import os
import shutil
import yaml
import requests

# ---------------------
# Helper Functions
# ---------------------

def get_file_size(file_path):
    """
    Get the size of the specified file in bytes.
    
    Args:
        file_path (str): The full path to the file whose size is to be determined.
    
    Returns:
        int: The size of the file in bytes.
    
    Example:
        >>> size = get_file_size("data/input_folder/example.txt")
        >>> print(size)
    """
    return os.path.getsize(file_path)


def format_size(size_bytes):
    """
    Convert a file size from bytes into a human-readable string format.
    
    This function divides the byte size by 1024 iteratively and assigns
    an appropriate unit (B, KB, MB, GB, or TB) until the size is less than 1024.
    
    Args:
        size_bytes (int): The file size in bytes.
    
    Returns:
        str: A string representing the file size in a human-readable format.
    
    Example:
        >>> readable = format_size(1234567)
        >>> print(readable)  # e.g., "1.18MB"
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f}{unit}"
        size_bytes /= 1024


def load_config(config_path):
    """
    Load and parse a YAML configuration file.
    
    This function reads the YAML file from the given path and converts its contents
    into a Python dictionary. In case of an error during reading or parsing,
    it prints an error message and returns None.
    
    Args:
        config_path (str): The file path of the YAML configuration file.
    
    Returns:
        dict or None: A dictionary with the configuration data if successful; otherwise, None.
    
    Example:
        >>> config = load_config("agentic_config.yml")
        >>> if config:
        ...     print(config.get("input_folder_path"))
    """
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading configuration from {config_path}: {e}")
        return None

# ---------------------
# File Management Functions
# ---------------------

def scan_folder(folder_path):
    """
    Recursively scan the specified folder and return a list of all file paths.
    
    This function traverses the directory tree starting at the given folder path,
    collecting the full paths of every file found.
    
    Args:
        folder_path (str): The path to the folder to be scanned.
    
    Returns:
        list: A list of strings, each representing a full file path.
    
    Example:
        >>> files = scan_folder("data/input_folder")
        >>> print(files)
    """
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def get_file_category(file_path):
    """
    Determine the category of a file based on its extension.
    
    This function inspects the file's extension (case-insensitive) and classifies it into one of the following:
      - "PDFs" for files ending with '.pdf'
      - "Images" for files ending with '.png', '.jpg', or '.jpeg'
      - "Code" for files ending with '.py', '.js', '.java', '.c', or '.cpp'
      - "Others" for all other file types.
    
    Args:
        file_path (str): The full path to the file.
    
    Returns:
        str: A string indicating the file category ("PDFs", "Images", "Code", or "Others").
    
    Example:
        >>> category = get_file_category("data/input_folder/document.pdf")
        >>> print(category)  # Outputs: PDFs
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return 'PDFs'
    elif ext in ['.png', '.jpg', '.jpeg']:
        return 'Images'
    elif ext in ['.py', '.js', '.java', '.c', '.cpp']:
        return 'Code'
    else:
        return 'Others'


def move_file_to_category(file_path, base_output_folder):
    """
    Move a file to a categorized subfolder within the output folder.
    
    This function first determines the file's category using get_file_category,
    creates a subfolder within the output folder if it doesn't already exist,
    and then moves the file to that subfolder. It returns the new file path.
    
    Args:
        file_path (str): The full path to the file to be moved.
        base_output_folder (str): The root folder where files should be organized.
    
    Returns:
        str: The new path of the file after it has been moved.
    
    Example:
        >>> new_path = move_file_to_category("data/input_folder/example.pdf", "data/output_folder")
        >>> print(new_path)
    """
    category = get_file_category(file_path)
    destination_folder = os.path.join(base_output_folder, category)
    os.makedirs(destination_folder, exist_ok=True)  # Create destination folder if it doesn't exist
    new_file_path = os.path.join(destination_folder, os.path.basename(file_path))
    shutil.move(file_path, new_file_path)
    print(f"Moved {file_path} to {new_file_path}")
    return new_file_path

# ---------------------
# Compression Functions
# ---------------------

def compress_pdf(file_path, method):
    """
    Compress a PDF file using the specified method.
    
    This function supports compression via ConvertAPI. It sends an HTTP POST request
    to the ConvertAPI endpoint along with the PDF file and required parameters.
    If the response status is 200, it prints a success message and returns True;
    otherwise, it prints an error message and returns False.
    
    Args:
        file_path (str): The full path to the PDF file to be compressed.
        method (str): The compression method to be used (should be "convertapi").
    
    Returns:
        bool: True if the compression is successful, False otherwise.
    
    Example:
        >>> success = compress_pdf("data/output_folder/PDFs/sample.pdf", "convertapi")
        >>> print(success)
    """
    if method.lower() == "convertapi":
        convertapi_url = "paste url here"
        convertapi_secret = "xyz..."  # Provided ConvertAPI secret key
        params = {"Secret": convertapi_secret, "StoreFile": "true"}
        with open(file_path, 'rb') as f:
            files = {"File": f}
            response = requests.post(convertapi_url, params=params, files=files)
        if response.status_code == 200:
            print(f"PDF compression successful for {file_path}")
            return True
        else:
            print(f"PDF compression failed for {file_path}. Status: {response.status_code}")
            return False
    else:
        print("Unsupported PDF compression method.")
        return False


def compress_image(file_path, method):
    """
    Compress an image file (PNG or JPG) using the specified method.
    
    This function uses the TinyPNG API via the tinify package to compress image files.
    If tinify is not installed, it prints an error message. Upon successful compression,
    the function returns True; otherwise, it returns False.
    
    Args:
        file_path (str): The full path to the image file to be compressed.
        method (str): The compression method to use (should be "tinypng").
    
    Returns:
        bool: True if the compression is successful, False otherwise.
    
    Example:
        >>> success = compress_image("data/output_folder/Images/sample.png", "tinypng")
        >>> print(success)
    """
    if method.lower() == "tinypng":
        try:
            import tinify
        except ImportError:
            print("tinify package not installed. Please install it via pip.")
            return False
        tinify.key = "xyz..."  # Provided TinyPNG key
        try:
            source = tinify.from_file(file_path)
            source.to_file(file_path)
            print(f"Image compression successful for {file_path}")
            return True
        except Exception as e:
            print(f"Image compression failed for {file_path}: {e}")
            return False
    else:
        print("Unsupported image compression method.")
        return False


def select_compression_function(category):
    """
    Select and return the appropriate compression function based on file category.
    
    This function checks the file category and returns the corresponding compression
    function. For "PDFs", it returns compress_pdf; for "Images", it returns compress_image.
    If the category does not support compression, it returns None.
    
    Args:
        category (str): The category of the file (e.g., "PDFs", "Images", "Code", "Others").
    
    Returns:
        function or None: The selected compression function if available; otherwise, None.
    
    Example:
        >>> func = select_compression_function("Images")
        >>> print(func)  # Outputs the compress_image function
    """
    if category == "PDFs":
        print("Decision: Category is 'PDFs'. Selected function: compress_pdf")
        return compress_pdf
    elif category == "Images":
        print("Decision: Category is 'Images'. Selected function: compress_image")
        return compress_image
    else:
        print(f"Decision: Category '{category}' does not have a compression function.")
        return None

# ---------------------
# Main Agent Workflow
# ---------------------

def main():
    """
    Execute the main workflow of the file management agent.
    
    The workflow consists of:
      1. Loading configuration files for folder paths and compression methods.
      2. Scanning the input folder to collect all file paths.
      3. Moving each file to a categorized subfolder in the output directory.
      4. Compressing files (PDFs and Images) using the configured compression methods.
      5. Printing detailed status messages for each operation.
    
    Returns:
        None
    
    Example:
        >>> python3 agents.py
    """
    # Load configuration files for input/output paths and compression methods
    agent_config = load_config("agentic_config.yml")
    file_manager_config = load_config("file_manager_config.yml")
    if not agent_config or not file_manager_config:
        print("Configuration files are missing or invalid. Exiting.")
        return

    # Retrieve input and output folder paths from the configuration
    input_folder = agent_config.get("input_folder_path", "data/input_folder")
    output_folder = agent_config.get("output_folder_path", "data/output_folder")

    # Scan the input folder for all files
    files = scan_folder(input_folder)
    for file_path in files:
        # Determine and print the original file size in a readable format
        original_size = format_size(get_file_size(file_path))
        print(f"Original size of {file_path}: {original_size}")

        # Move the file to the corresponding category subfolder in the output folder
        new_file_path = move_file_to_category(file_path, output_folder)
        moved_size = format_size(get_file_size(new_file_path))
        print(f"Size after moving to output folder: {moved_size}")

        # Determine the file category and select the appropriate compression function
        category = get_file_category(new_file_path)
        compression_func = select_compression_function(category)
        if compression_func is not None:
            # Determine the compression method from configuration for PDFs and Images
            if category == "PDFs":
                compress_method = next(
                    (item.get("PDF") for item in file_manager_config.get("compression_method", []) if "PDF" in item),
                    None
                )
            elif category == "Images":
                ext = os.path.splitext(new_file_path)[1].lower()
                if ext in ['.jpg', '.jpeg']:
                    compress_method = next(
                        (item.get("JPG") for item in file_manager_config.get("compression_method", []) if "JPG" in item),
                        None
                    )
                elif ext == '.png':
                    compress_method = next(
                        (item.get("PNG") for item in file_manager_config.get("compression_method", []) if "PNG" in item),
                        None
                    )
                else:
                    compress_method = None
            else:
                compress_method = None

            # If a valid compression method is found, compress the file and print the new size
            if compress_method is not None and compression_func(new_file_path, compress_method):
                compressed_size = format_size(get_file_size(new_file_path))
                print(f"Size after {category[:-1]} compression: {compressed_size}")

        # Print a blank line for better readability between file processes
        print()

    print("All files processed. Agent work completed.")

if __name__ == "__main__":
    main()
