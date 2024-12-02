import os
import zipfile

def unzip_file_to_folder(zip_file_path):
    """
    Unzips a given zip file into a folder with the same name as the zip file.

    Parameters:
    zip_file_path (str): The path to the zip file.
    """
    # Get the directory and base name without the .zip extension
    extract_to = os.path.splitext(zip_file_path)[0]

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Create the folder if it doesn't exist
            os.makedirs(extract_to, exist_ok=True)
            zip_ref.extractall(extract_to)
            print(f"Successfully extracted: {zip_file_path} to {extract_to}")
    except zipfile.BadZipFile as e:
        print(f"Error extracting {zip_file_path}: {e}")

def unzip_multiple_files(zip_files, base_directory):
    """
    Unzips multiple zip files into folders with the same name as each zip file.

    Parameters:
    zip_files (list): A list of zip file paths to be unzipped.
    base_directory (str): The base directory where the zip files are located.
    """
    for zip_file in zip_files:
        zip_file_path = os.path.join(base_directory, zip_file)
        unzip_file_to_folder(zip_file_path)

# Main execution
if __name__ == "__main__":
    # Define the working directory and list of zip files
    working_directory = "F:\\BaiduNetdiskDownload"
    zip_files = [
        "815详情页.zip",
        "816详情页.zip",
        "817详情页.zip",
        "818详情页.zip",
        "819详情页.zip",
        "820详情页.zip",
        "821详情页.zip",
        "822详情页.zip"
    ]

    # Unzip all files to corresponding folders
    unzip_multiple_files(zip_files, working_directory)













import requests

def download_image(url, save_as):
    """
    Downloads an image from a URL and saves it locally.

    Parameters:
    url (str): The URL of the image.
    save_as (str): The filename to save the image as (with extension).
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        with open(save_as, 'wb') as file:
            for chunk in response.iter_content(1024):  # Download in chunks
                file.write(chunk)
        print(f"Image successfully downloaded: {save_as}")
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")

# Main execution
if __name__ == "__main__":
    image_url = "https://a4c2-119-123-33-164.ngrok-free.app/%E5%BD%A9%E7%9B%92%E8%83%8C%E9%9D%A2.jpg"
    output_file = "test.jpg"
    download_image(image_url, output_file)











import os
import re
import shutil
import pyperclip

def extract_image_paths_from_clipboard():
    """
    Extracts image paths from clipboard content.
    
    Returns:
    list: List of file paths extracted from clipboard.
    """
    clipboard_content = pyperclip.paste()
    image_paths = re.findall(r'"(.*?)"', clipboard_content)
    return image_paths

def copy_and_rename_images(image_paths, destination_folder, base_name="Reobrix"):
    """
    Copies and renames images to the destination folder with a custom base name.
    Each image will be renamed with an incrementing number in parentheses.

    Parameters:
    image_paths (list): List of original image paths.
    destination_folder (str): Destination folder to copy images to.
    base_name (str): Custom base name for the new files (default is "Reobrix").

    Returns:
    list: List of new image paths.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    new_image_paths = []
    
    for index, image_path in enumerate(image_paths, start=1):
        # Get the original extension (e.g., .jpg, .png)
        original_extension = os.path.splitext(image_path)[1]
        # Create the new filename with the base name and incrementing number
        new_filename = f"{base_name}-({index}){original_extension}"
        new_image_path = os.path.join(destination_folder, new_filename)
        
        # Copy the image to the new destination with the new name
        shutil.copy(image_path, new_image_path)
        new_image_paths.append(new_image_path)
    
    return new_image_paths

def convert_paths_to_urls(paths, base_url="https://a4c2-119-123-33-164.ngrok-free.app/"):
    """
    Converts file paths to URLs by prepending the base URL to the file names.

    Parameters:
    paths (list): List of file paths.
    base_url (str): The base URL to prepend (default is the provided ngrok URL).

    Returns:
    list: List of URL strings.
    """
    urls = []
    for path in paths:
        filename = os.path.basename(path)
        url = os.path.join(base_url, filename).replace('\\', '/')  # Ensure proper URL formatting
        urls.append(url)
    
    return urls

def m():
    # Extract image paths from the clipboard
    image_paths = extract_image_paths_from_clipboard()
    
    if not image_paths:
        print("No image paths found in the clipboard.")
    else:
        print("Image paths found:", image_paths)
        
        # Specify the destination folder
        destination_folder = input("Enter the destination folder (default is G:\\x\\t2\\新产品\\imgs): ") or "G:\\x\\t2\\新产品\\imgs"
        
        # Prompt for a base name for the new files
        base_name = input("Enter the base name for the new files (default is 'Reobrix'): ") or "Reobrix"
        
        # Copy and rename images
        new_image_paths = copy_and_rename_images(image_paths, destination_folder, base_name)
        print("Images have been copied and renamed to:")
        print(new_image_paths)
        

def m2():
    image_paths = extract_image_paths_from_clipboard()
    return convert_paths_to_urls(image_paths)
















import os
import shutil

# Define function to find the deepest subfolder containing "详情" in its name
def find_deepest_details_folder(root_folder):
    deepest_path = None
    deepest_level = -1
    
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for dirname in dirnames:
            if "详情" in dirname:
                current_path = os.path.join(dirpath, dirname)
                # Calculate the current depth of the folder in the tree
                current_level = current_path.count(os.sep)
                # If the current folder is deeper, update the deepest folder and level
                if current_level > deepest_level:
                    deepest_level = current_level
                    deepest_path = current_path
    
    return deepest_path

# Define function to find the first subfolder inside a given folder
def get_first_subfolder(folder):
    try:
        subfolders = [f.name for f in os.scandir(folder) if f.is_dir()]
        return subfolders[0] if subfolders else None
    except Exception as e:
        print(f"Error getting subfolder: {e}")
        return None

# Define function to copy images from the found subfolder to the destination folder
def copy_images(src_folder, dest_folder):
    try:
        # Check if destination folder exists, create it if it doesn't
        os.makedirs(dest_folder, exist_ok=True)
        
        # Copy images from the source folder to the destination
        for filename in os.listdir(src_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                src_file = os.path.join(src_folder, filename)
                dest_file = os.path.join(dest_folder, filename)
                shutil.copy2(src_file, dest_file)
                print(f"Copied {src_file} to {dest_file}")
    except Exception as e:
        print(f"Error copying images: {e}")

# Main function to perform the entire process
def process_folders(src_folder, dest_base_folder):
    for subfolder in os.listdir(src_folder):
        subfolder_path = os.path.join(src_folder, subfolder)
        
        if os.path.isdir(subfolder_path):
            # Find the deepest folder containing "详情"
            details_folder = find_deepest_details_folder(subfolder_path)
            
            if details_folder:
                print(f"Found deepest details folder: {details_folder}")
                
                # Find the first subfolder inside the deepest "详情" folder
                first_subfolder = get_first_subfolder(details_folder)
                first_subfolder_path = os.path.join(details_folder, first_subfolder) if first_subfolder else details_folder
                print(f"First subfolder inside deepest details folder: {first_subfolder_path}")
                
                # Define the destination folder path based on the subfolder name
                dest_folder = os.path.join(dest_base_folder, subfolder)
                
                # Copy all images from the first subfolder to the destination folder
                copy_images(first_subfolder_path, dest_folder)
            else:
                print(f"No details folder found in {subfolder_path}")

if __name__ == "__main__":
    # Define source and destination directories
    src_folder = r"G:\产品图"
    dest_base_folder = r"G:\x\t2\产品详情"

    # Call the main function to start processing the folders
    process_folders(src_folder, dest_base_folder)
 