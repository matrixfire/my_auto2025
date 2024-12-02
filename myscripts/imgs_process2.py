
import os
import re
import requests
import pyperclip

# Define the working directory
WORKING_DIR = r'G:\main_work\imgs\t2'

# List of file extensions you want to support
file_ext = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]

def get_clipboard_text():
    """Retrieve text from the clipboard."""
    return pyperclip.paste()

def generate_url_pattern(extensions):
    """Generate a regex pattern for extracting URLs with specified extensions."""
    # Join the extensions with "|" to create the regex group
    ext_pattern = '|'.join(re.escape(ext) for ext in extensions)
    return re.compile(rf'https?://\S+\.?(?:{ext_pattern})')

def extract_image_urls(text, pattern):
    """Extract all image URLs from the provided text using the given pattern."""
    return pattern.findall(text)

def sanitize_filename(filename):
    """Sanitize the filename to ensure it is valid."""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def download_image(url, save_path):
    """Download an image from a URL and save it to the specified path."""
    try:
        print(f"Trying to download: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for request errors

        # Write the image to a file
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {url} to {save_path}")

    except requests.RequestException as e:
        print(f"Failed to download {url}. Reason: {e}")

def download_imgs():
    # Get text from clipboard
    clipboard_text = get_clipboard_text()
    
    # Generate regex pattern based on file extensions
    pattern = generate_url_pattern(file_ext)
    
    # Extract image URLs
    image_urls = extract_image_urls(clipboard_text, pattern)
    print(image_urls)
    
    if not image_urls:
        print("No image URLs found in clipboard text.")
        return
    
    # Create directory if it doesn't exist
    if not os.path.exists(WORKING_DIR):
        os.makedirs(WORKING_DIR)

    # Download each image
    for i, url in enumerate(image_urls, start=1):
        # Extract the file extension correctly
        file_extension = re.search(r'\.?(jpg|jpeg|png|gif|bmp|webp)', url)
        print(f"Fucking file ext: {file_extension}")
        if file_extension:
            file_extension = file_extension.group(1)
        else:
            file_extension = 'jpg'  # Default to jpg if no extension found
        
        # Create a valid filename
        filename = f"image_{i}.{file_extension}"
        filename = sanitize_filename(filename)
        file_path = os.path.join(WORKING_DIR, filename)
        
        download_image(url, file_path)



# Run the main function for testing
download_imgs()
