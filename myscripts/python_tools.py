n = lambda input_path: [folder for folder in os.listdir(input_path)] # dirs and files names
n = lambda input_path: [file for file in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, file))] # files names
n = lambda input_path: [folder for folder in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, folder))] # dirs names

p = lambda input_path: [os.path.join(input_path, folder) for folder in os.listdir(input_path)] # dirs and files paths
p = lambda input_path: [os.path.join(input_path, folder) for folder in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, folder))] # files paths
p = lambda input_path: [os.path.join(input_path, folder) for folder in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, folder))] # dirs paths


import pyperclip as p; cl=lambda lt: p.copy("\n".join(lt))
pl = lambda lt: print("\n".join(lt))


###################################################################################
from PIL import Image
import os

def concatenate_images_vertically(folder_path):
    # Get all image file paths from the folder
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
    
    # Open all images and store them in a list
    images = [Image.open(img_file) for img_file in image_files]
    
    # Calculate the total height and the max width of the concatenated image
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)
    
    # Create a new image with the calculated max width and total height
    concatenated_image = Image.new('RGB', (max_width, total_height))
    
    # Paste each image into the concatenated image
    current_y = 0
    for img in images:
        concatenated_image.paste(img, (0, current_y))
        current_y += img.height
    
    # Define the output path
    output_path = os.path.join(folder_path, 'concatenated_image_vertically.jpg')
    
    # Save the concatenated image
    concatenated_image.save(output_path)
    
    return output_path

cv = concatenate_images_vertically


###################################################################################
import webbrowser

def open_links():
    links = [
        "https://chat.openai.com",
        "https://www.bing.com/chat",
        "https://yiyan.baidu.com/"
    ]
    for link in links:
        webbrowser.open(link)

# Call the function to open the links
open_links()


###################################################################################
from PIL import Image, ImageDraw

def generate_background_image(size, color_str, output_path):
    # Parse the color string into RGB components
    color = tuple(int(color_str[i:i+2], 16) for i in (1, 3, 5))
    
    # Create a new image with the specified size and background color
    img = Image.new('RGB', size, color)
    
    # Save the image to the specified output path
    img.save(output_path)
    
    print(f"Generated background image with size {size} and color {color_str}. Saved to {output_path}")

# Example usage:
if __name__ == "__main__":
    size = (940, 348)  # Example size (width, height)
    color_str = "#EBE6E4"  # Example color string
    output_path = r"C:\Users\34950\Desktop\test\background_image.png"  # Example output path
    
    generate_background_image(size, color_str, output_path)
	
	
###################################################################################


#! python3
# stopwatch.py - A simple stopwatch program.

import time

# Display the program's instructions.
print('Press ENTER to begin. Afterward, press ENTER to "click" the stopwatch.\nPress Ctrl-C to quit.')
input()  # press Enter to begin
print('Started.')
startTime = time.time()  # get the first lap's start time
lastTime = startTime
lapNum = 1

# Start tracking the lap times.
try:
    while True:
        input()
        lapTime = round(time.time() - lastTime, 2)
        totalTime = round(time.time() - startTime, 2)
        print(f'Lap #{lapNum}: {totalTime} ({lapTime})', end='')
        lapNum += 1
        lastTime = time.time()  # reset the last lap time
except KeyboardInterrupt:
    # Handle the Ctrl-C exception to keep its error message from displaying.
    print('\nDone.')

###################################################################################


def cells_2_list(txt=''):
    '''still have bugs...'''
    import pyperclip as p
    # Check if the text contains double quotes
    if not txt:
        txt = p.paste()
    txt = txt.strip()
    if '"' in txt:
        # Replace new lines within quotes with whitespace
        cleaned_txt = ''
        in_quote = False
        for char in txt:
            if char == '"':
                in_quote = not in_quote
            if in_quote and char == '\n':
                cleaned_txt += ' '
            else:
                cleaned_txt += char
        # Remove double quotes
        # cleaned_txt = cleaned_txt.replace('"', '')
    else:
        cleaned_txt = txt.strip()  # Remove leading/trailing whitespace
    # Split text into a list based on newline separator
    result_list = cleaned_txt.split('\n')
    result_list = [i.strip() for i in result_list]
    print(f'Found {len(result_list)} item(s).')
    return result_list

c2l = cells_2_list


# import pyperclip; pyperclip.copy("\n".join



###################################################################################

import phonenumbers
from phonenumbers import geocoder

def guess_country(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country = geocoder.country_name_for_number(parsed_number, "en")
        return country
    except phonenumbers.NumberParseException:
        return "Invalid phone number"

gc = guess_country

###################################################################################

import random
from PIL import Image, ImageDraw, ImageFont
import lorem

def generate_background_image(size, output_path, color_str=None, lorem_words=False):
    # Generate a random color if color_str isn't provided
    if color_str is None:
        color = tuple(random.randint(0, 255) for _ in range(3))
    else:
        # Parse the color string into RGB components
        color = tuple(int(color_str[i:i+2], 16) for i in (1, 3, 5))
    
    # Create a new image with the specified size and background color
    img = Image.new('RGB', size, color)
    
    # If lorem_words is True, add lorem text to the image
    if lorem_words:
        draw = ImageDraw.Draw(img)
        # Generate lorem text
        text = lorem.sentence()
        
        # Choose a font size that fits within the image size
        font_size = 30
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        
        # Determine the size of the text
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculate position to center the text
        text_x = (size[0] - text_width) // 2
        text_y = (size[1] - text_height) // 2
        
        # Draw the text on the image
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))
    
    # Save the image to the specified output path
    img.save(output_path)
    
    print(f"Generated background image with size {size} and color {color}. Saved to {output_path}")

# Example usage:
# generate_background_image((800, 600), 'output.png', lorem_words=True)


t = generate_background_image

# Example usage:

output_path = r"C:\Users\34950\Desktop\test\background_image.png"
t((800, 600), output_path, lorem_words=True)
t((1920, 1080), output_path, lorem_words=True)


# generate_background_image((800, 600), 'output.png', lorem_words=True)




################################################################################### 






import os
import re
import pyperclip

def get_folder_contents(folder_path, exclude_regex=[]):
    """
    Collects subfolders and files in a folder based on exclusion criteria.

    Parameters:
    - folder_path (str): Path to the folder to collect contents of.
    - exclude_regex (list): List of regex patterns. Folders or files matching any of these patterns will be excluded.

    Returns:
    - tuple: A tuple containing two lists: (subfolders, files)
      subfolders (list): List of subfolder paths.
      files (list): List of file names.
    """
    subfolders = []
    files = []

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return subfolders, files
    
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            subfolders.append(item_path)
        elif os.path.isfile(item_path):
            files.append(item)

    # Filter out subfolders and files based on exclude_regex
    subfolders = [folder for folder in subfolders if not any(re.search(pattern, folder) for pattern in exclude_regex)]
    files = [file for file in files if not any(re.search(pattern, file) for pattern in exclude_regex)]

    return subfolders, files

def print_folder_contents(folder_path, indent=0, print_files=True, exclude_regex=[]):
    """
    Prints subfolders and files in a folder with hierarchical indentation.

    Parameters:
    - folder_path (str): Path to the folder to print contents of.
    - indent (int): Indentation level for subfolders and files.
    - print_files (bool): If True, prints both folders and files. If False, prints only subfolders.
    - exclude_regex (list): List of regex patterns. Folders or files matching any of these patterns will be excluded.

    Returns:
    - str: The formatted string of folder contents.
    """
    subfolders, files = get_folder_contents(folder_path, exclude_regex)

    folder_name = os.path.basename(folder_path)
    output = f"{' ' * indent}{folder_name}\n"

    if print_files:
        for file in files:
            output += f"{' ' * (indent + 4)}- {file}\n"

    for subfolder in subfolders:
        output += print_folder_contents(subfolder, indent + 4, print_files, exclude_regex)

    return output

# Example usage:
folder_path = r"C:\Users\34950\Desktop\work\mysite2024"
folder_path = r"C:\Users\34950\Desktop\work\mysite2024\shop\templates"


output = print_folder_contents(folder_path, print_files=True)
print(output)
pyperclip.copy(output)


######################################################################




import os
import re
import pyperclip

def get_folder_contents(folder_path, exclude_regex=[]):
    """
    Collects subfolders and files in a folder based on exclusion criteria.

    Parameters:
    - folder_path (str): Path to the folder to collect contents of.
    - exclude_regex (list): List of regex patterns. Folders or files matching any of these patterns will be excluded.

    Returns:
    - tuple: A tuple containing two lists: (subfolders, files)
      subfolders (list): List of subfolder paths.
      files (list): List of file names.
    """
    subfolders = []
    files = []

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return subfolders, files
    
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            subfolders.append(item_path)
        elif os.path.isfile(item_path):
            files.append(item)

    # Filter out subfolders and files based on exclude_regex
    subfolders = [folder for folder in subfolders if not any(re.search(pattern, folder) for pattern in exclude_regex)]
    files = [file for file in files if not any(re.search(pattern, file) for pattern in exclude_regex)]

    return subfolders, files

def print_folder_contents(folder_path, indent=0, print_files=True, exclude_regex=[]):
    """
    Prints subfolders and files in a folder with hierarchical indentation.

    Parameters:
    - folder_path (str): Path to the folder to print contents of.
    - indent (int): Indentation level for subfolders and files.
    - print_files (bool): If True, prints both folders and files. If False, prints only subfolders.
    - exclude_regex (list): List of regex patterns. Folders or files matching any of these patterns will be excluded.

    Returns:
    - str: The formatted string of folder contents.
    """
    subfolders, files = get_folder_contents(folder_path, exclude_regex)

    folder_name = os.path.basename(folder_path)
    output = f"{' ' * indent}{folder_name}\n"

    if print_files:
        for file in files:
            output += f"{' ' * (indent + 4)}- {file}\n"

    for subfolder in subfolders:
        output += print_folder_contents(subfolder, indent + 4, print_files, exclude_regex)

    return output

# Example usage:
folder_path = r"C:\Users\34950\Desktop\work\mysite2024"
# folder_path = r"C:\Users\34950\Desktop\work\mysite2024\shop\templates"
exclude_regex = [
    r'(^|[\\/])\.git($|[\\/])',  # Exclude .git and its subfolders/files
    r'(^|[\\/])migrations($|[\\/])',  # Exclude migrations and its subfolders/files
    r'(^|[\\/])__pycache__($|[\\/])'  # Exclude __pycache__ and its subfolders/files
]

# output = print_folder_contents(folder_path, print_files=True)
output = print_folder_contents(folder_path, print_files=True, exclude_regex=exclude_regex)
print(output)
pyperclip.copy(output)


######################################################################

import os
import requests
from urllib.parse import urlparse

def download_image(image_url, save_path):
    """
    Downloads an image from a given URL and saves it to a specified path.
    
    :param image_url: str, URL of the image to be downloaded
    :param save_path: str, path where the image will be saved. If a directory is provided,
                      the image will be saved in the current working directory.
    :return: str, full path of the saved image
    """
    try:
        # Check if save_path is a directory
        if os.path.isdir(save_path):
            # Get the image name from the URL
            parsed_url = urlparse(image_url)
            image_name = os.path.basename(parsed_url.path)
            save_path = os.path.join(save_path, image_name)
        
        # Send a GET request to the image URL
        response = requests.get(image_url, stream=True)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Open the file in binary mode and write the content
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image successfully downloaded: {save_path}")
            return save_path
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    image_url = "https://pantasy.com/cdn/shop/files/03_58872eac-0e01-4fbd-969d-680e070d84fd.jpg"
    save_path = r"C:\Users\Administrator\Desktop\work2024\reobrix_site\reobrix2\core\static\core\images\youtube.jpg"
    download_image(image_url, save_path)




#############################################################################################

import chardet

def detect_file_encoding(file_path):
    """
    Detect the encoding of a given file.
    
    Parameters:
    file_path (str): The path to the file.
    
    Returns:
    str: The detected encoding of the file.
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']     
    print(f"The encoding of the file is {encoding}")    
    return encoding

# Usage example
file_path = r"C:\Users\Administrator\Desktop\work2024\reobrix_site\reobrix2\p.csv"
encoding = detect_file_encoding(file_path)
print(f"The encoding of the file is {encoding}")







#############################################################################################

###############################################################################################################
import os

def remove_link_tag(folder_path):
    # The specific link tag to remove
    link_tag_to_remove = '<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Dancing+Script:700%7CLato:300,300italic,400,700,900">'

    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)

                # Read the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_contents = f.read()

                # Remove the specific link tag
                updated_contents = file_contents.replace(link_tag_to_remove, '')

                # Write the updated contents back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_contents)


import os
import re

def remove_link_tags(folder_path):
    # Define a regex pattern to match <link> tags with href starting with "//fonts.googleapis.com/"
    link_tag_pattern = re.compile(r'<link\s+rel="stylesheet"\s+type="text/css"\s+href="//fonts\.googleapis\.com/[^"]*"\s*/?>', re.IGNORECASE)

    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)

                # Read the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_contents = f.read()

                # Find all matching link tags
                matches = link_tag_pattern.findall(file_contents)
                if matches:
                    print(f"Found {len(matches)} link tag(s) to remove in file: {file_path}")

                # Remove all matching link tags
                updated_contents = re.sub(link_tag_pattern, '', file_contents)

                # Write the updated contents back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_contents)

                if matches:
                    print(f"Removed {len(matches)} link tag(s) from file: {file_path}")

# Example usage
remove_link_tags('/path/to/your/folder')



######################################

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from PIL import Image
import io
import time

def initialize_driver():
    """
    Initialize the Firefox driver with options for headless mode if needed.
    Returns the initialized WebDriver instance.
    """
    options = FirefoxOptions()
    # options.add_argument("--headless")  # Uncomment if you want to run Firefox in headless mode
    service = FirefoxService()
    return webdriver.Firefox(service=service, options=options)

def switch_to_tab(driver, tab_index):
    """
    Switches to the tab specified by tab_index (0-based index).
    """
    driver.switch_to.window(driver.window_handles[tab_index])

def take_full_page_screenshot_(driver, file_path='full_page_screenshot.png'):
    """
    Takes a full-page screenshot of the current webpage displayed in the driver.
    Saves the screenshot as 'file_path'.
    """
    # Maximize the window to ensure full-page screenshot
    driver.maximize_window()

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Initialize a list to store the screenshot parts
    screenshot_parts = []

    # Scroll and take screenshots
    viewport_height = driver.execute_script("return window.innerHeight")
    for i in range(0, total_height, viewport_height):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(2)  # Give the page time to load
        screenshot_parts.append(driver.get_screenshot_as_png())

    # Stitch the screenshots together
    stitched_image = Image.new('RGB', (driver.execute_script("return document.body.scrollWidth"), total_height))
    offset = 0
    for part in screenshot_parts:
        image = Image.open(io.BytesIO(part))
        stitched_image.paste(image, (0, offset))
        offset += image.height

    # Save the final stitched image
    stitched_image.save(file_path)

    print(f"Full page screenshot saved as '{file_path}'")


def take_full_page_screenshot(driver, file_path='full_page_screenshot.png'):
    """
    Takes a smoother full-page screenshot of the current webpage displayed in the driver.
    Saves the screenshot as 'file_path'.
    """
    # Maximize the window to ensure full-page screenshot
    driver.maximize_window()

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Initialize a list to store the screenshot parts
    screenshot_parts = []

    # Define scroll increment (adjust as needed)
    scroll_increment = 500  # Scroll by 500 pixels each time

    # Scroll and take screenshots
    for i in range(0, total_height, scroll_increment):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.5)  # Adjust wait time as needed (e.g., 0.5 seconds)
        screenshot_parts.append(driver.get_screenshot_as_png())

    # Stitch the screenshots together
    stitched_image = Image.new('RGB', (driver.execute_script("return document.body.scrollWidth"), total_height))
    offset = 0
    for part in screenshot_parts:
        image = Image.open(io.BytesIO(part))
        stitched_image.paste(image, (0, offset))
        offset += image.height

    # Save the final stitched image
    stitched_image.save(file_path)

    print(f"Full page screenshot saved as '{file_path}'")



if __name__ == "__main__":
    # Initialize the driver
    driver = initialize_driver()

    # Open the desired website
    driver.get('https://www.dedao.cn/')

    # Switch to the third tab (index 2)
    switch_to_tab(driver, 2)

    # Take a full-page screenshot of the third tab
    take_full_page_screenshot(driver, 'third_tab_screenshot.png')

    # Close the browser
    driver.quit()

driver = initialize_driver()

# Open the desired website
driver.get('https://www.dedao.cn/')

TAB = 2
# Switch to the third tab (index 2)
switch_to_tab(driver, TAB-1)

# Take a full-page screenshot of the third tab
take_full_page_screenshot(driver, 'third_tab_screenshot.png')

# Close the browser
driver.quit()



#####################################################################################################


import os
import subprocess
import sys

def create_django_project(base_path, project_name):
    project_path = os.path.join(base_path, project_name)
    # 1, Create the project directory
    os.makedirs(project_path, exist_ok=True)
    print(f"Created project directory: {project_path}")
    # 2, Create virtual environment
    subprocess.check_call([sys.executable, '-m', 'venv', os.path.join(project_path, 'myenv')])
    print("Virtual environment created")
    # 3, Activate virtual environment
    activate_script = os.path.join(project_path, 'myenv', 'Scripts', 'activate')
    activate_command = f'{activate_script} && '
    # 4, Install Django
    subprocess.check_call(f"{activate_command}pip install Django -i https://pypi.tuna.tsinghua.edu.cn/simple", shell=True)
    print("Django installed")
    # 5, Create Django project
    subprocess.check_call(f"{activate_command}django-admin startproject {project_name} {project_path}", shell=True)
    print("Django project created")
    # 6, Create Django app
    os.chdir(project_path)
    subprocess.check_call(f"{activate_command}python manage.py startapp core", shell=True)
    print("Django app 'core' created")
    # 7, Add 'core' app to settings.py
    settings_path = os.path.join(project_path, project_name, 'settings.py')
    with open(settings_path, 'r') as file:
        settings = file.readlines()
    
    installed_apps_index = None
    for i, line in enumerate(settings):
        if 'INSTALLED_APPS' in line:
            installed_apps_index = i
            break
    
    if installed_apps_index is not None:
        for i in range(installed_apps_index, len(settings)):
            if ']' in settings[i]:
                settings[i] = settings[i].replace(']', "    'core',\n]")
                break

    with open(settings_path, 'w') as file:
        file.writelines(settings)
    
    print("Added 'core' app to INSTALLED_APPS in settings.py")

if __name__ == "__main__":
    base_path = r"C:\Users\Administrator\Desktop\work2024"
    project_name = "dj_test"
    create_django_project(base_path, project_name)








import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import font_manager
import textwrap

def wrap_text(text, width):
    """
    Wrap text for Chinese characters and English words without breaking English words in half.
    Each Chinese character is considered twice the width of an English letter.
    """
    wrapped_lines = []
    paragraphs = text.split('\n')
    
    for paragraph in paragraphs:
        if paragraph == '':
            # Preserve empty lines
            wrapped_lines.append('')
            continue

        line = ""
        current_width = 0
        word = ""

        for char in paragraph:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character
                char_width = 2
            else:
                char_width = 1

            if char.isspace():
                if current_width + len(word) > width:
                    wrapped_lines.append(line)
                    line = word + char
                    current_width = len(word) + char_width
                else:
                    line += word + char
                    current_width += len(word) + char_width
                word = ""
            elif char_width == 2:
                if current_width + char_width > width:
                    wrapped_lines.append(line)
                    line = char
                    current_width = char_width
                else:
                    line += word + char
                    current_width += len(word) + char_width
                word = ""
            else:
                if current_width + len(word) + char_width > width:
                    wrapped_lines.append(line)
                    line = word + char
                    current_width = len(word) + char_width
                    word = ""
                else:
                    word += char

        # Append any remaining text
        if current_width + len(word) > width:
            wrapped_lines.append(line)
            line = word
        else:
            line += word
        
        if line:
            wrapped_lines.append(line)

    return wrapped_lines


def add_text_to_image(background_color, output_path, rows, font_path, font_size=20, padding=20):
    """
    Adds formatted text to an image with a specified background color.

    Args:
        background_color (tuple): RGB values for the background color.
        output_path (str): Path to save the image with text.
        rows (list): List of text lines to add to the image.
        font_path (str): Path to the font file that supports Chinese characters.
        font_size (int): Font size of the text.
        padding (int): Padding from the edges.
    """
    # Load the font
    font_prop = font_manager.FontProperties(fname=font_path, size=font_size)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 12))  # Adjust size as needed
    fig.patch.set_facecolor(background_color)
    ax.axis('off')

    # Define text height
    text_height = font_size * 1.2  # A rough estimate, adjust if needed

    # Calculate the maximum number of lines that fit in the image height
    fig_height_inches = fig.get_size_inches()[1]*0.6
    max_lines_per_image = int((fig_height_inches * fig.dpi - 2 * padding) / text_height)
    
    # Split rows into chunks that fit the image height
    for i in range(0, len(rows), max_lines_per_image):
        chunk = rows[i:i + max_lines_per_image]
        text_chunk = '\n'.join(chunk)
        
        # Add text to the image
        ax.text(
            0.01, 0.99, text_chunk,
            fontsize=font_size,
            color='black',
            ha='left',
            va='top',
            bbox=dict(facecolor='none', edgecolor='none', pad=0),
            fontproperties=font_prop,
            transform=ax.transAxes
        )
        
        # Save the image
        fig.canvas.draw()
        img = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        img.save(output_path.format(i // max_lines_per_image))
        print(f"Image saved to {output_path.format(i // max_lines_per_image)}")
        
        # Clear the figure for the next chunk
        ax.clear()
        fig, ax = plt.subplots(figsize=(10, 12))
        fig.patch.set_facecolor(background_color)
        ax.axis('off')



text = '''标题： 理解不同类型的人工智能

1, English: Each kind of AI has its own special function and way of working, just like tools in a toolbox.
Chinese: 每种人工智能都有其独特的功能和工作方式，就像工具箱中的工具一样。

2, English: In the following sections, we look at these different types of AI to understand what they’re like and how they work.
Chinese: 在接下来的部分，我们将探讨这些不同类型的人工智能，以了解它们的特点和工作原理。

3, English: We start with two main types:
Chinese: 我们从两种主要类型开始：

4, English: AI that learns from data, which we call machine learning (ML)
Chinese: 从数据中学习的人工智能，我们称之为机器学习（ML）

5, English: AI that follows specific rules
Chinese: 遵循特定规则的人工智能

6, English: Both types of AI have their own strengths, making them suitable for different kinds of tasks.
Chinese: 这两种类型的人工智能各有优点，使它们适用于不同类型的任务。

7, English: Understanding this will help you get a clear picture of how AI is changing our world, from health care to manufacturing and beyond.
Chinese: 理解这些将帮助你清楚地了解人工智能如何改变我们的世界，从医疗保健到制造业以及其他领域。

8, English: Each type of AI brings something valuable to the table, showing just how diverse and useful these technologies can be.
Chinese: 每种类型的人工智能都带来了一些有价值的东西，展示了这些技术的多样性和实用性。'''


max_line_length = 60
rows_ = wrap_text(text, max_line_length)

# Example usage with multiple image files
add_text_to_image(
    background_color=(144/255, 238/255, 144/255),  # Light green background color
    output_path=r"G:\main_work\output_image_matplotlib_{:02d}.jpg",  # Use format string for multiple files
    rows=rows_,
    font_path=r'G:\main_work\msyh.ttc'  # Replace with the path to your .ttc or .ttf font file
)



import os
import re

def search_in_files(directory, file_extension, search_string, regex=False, ignore_case=True):
    """
    Searches for a string in files with a given extension within a directory and its subfolders.

    Args:
        directory (str): The directory to search in.
        file_extension (str): The file extension to search in (e.g., 'scss').
        search_string (str): The string to search for.
        regex (bool): Whether to interpret the search string as a regular expression (default is False).
        ignore_case (bool): Whether to ignore case in the search (default is True).
    """
    # Prepare search pattern based on whether regex is used or not
    if regex:
        flags = re.IGNORECASE if ignore_case else 0
        search_pattern = re.compile(search_string, flags)
    else:
        search_pattern = re.compile(re.escape(search_string), re.IGNORECASE if ignore_case else 0)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(f'.{file_extension}'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if search_pattern.search(content):
                            print(f"Found in: {file_path}")
                except (IOError, UnicodeDecodeError) as e:
                    print(f"Error reading {file_path}: {e}")

# Example usage
if __name__ == "__main__":
    search_in_files(
        directory=r"C:\Users\Administrator\Desktop\work2024\myauto",
        file_extension='html',
        search_string='Handmader',
        regex=False,
        ignore_case=True
    )

if __name__ == "__main__":
    search_in_files(
        directory=r"C:\Users\Administrator\Desktop\work2024\my_new_ecommerce3\static\assets",
        file_extension='js',
        search_string='theiaStickySidebar',
        regex=False,
        ignore_case=True
    )


import os
import re

def search_in_files(directory, file_extensions, search_string, ignored_files_folders=None, regex=False, ignore_case=True):
    """
    Searches for a string in files with specified extensions within a directory and its subfolders,
    while ignoring specific files or folders.

    Args:
        directory (str): The directory to search in.
        file_extensions (list): A list of file extensions to search in (e.g., ['scss', 'css']).
        search_string (str): The string to search for.
        ignored_files_folders (list): A list of filenames or folder names to ignore (e.g., ['.git', 'myenv']).
        regex (bool): Whether to interpret the search string as a regular expression (default is False).
        ignore_case (bool): Whether to ignore case in the search (default is True).
    """
    # Ensure file_extensions and ignored_files_folders are lists
    if isinstance(file_extensions, str):
        file_extensions = [file_extensions]
    if ignored_files_folders is None:
        ignored_files_folders = []
    
    # Prepare search pattern based on whether regex is used or not
    flags = re.IGNORECASE if ignore_case else 0
    search_pattern = re.compile(search_string, flags) if regex else re.compile(re.escape(search_string), flags)
    
    # Normalize directory path
    directory = os.path.normpath(directory)
    
    for root, dirs, files in os.walk(directory):
        # Skip ignored folders
        dirs[:] = [d for d in dirs if d not in ignored_files_folders]

        for file in files:
            # Skip ignored files
            if any(file.startswith(prefix) for prefix in ignored_files_folders):
                continue

            # Check if the file's extension matches any in the list
            if any(file.endswith(f'.{ext}') for ext in file_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = search_pattern.findall(content)
                        match_count = len(matches)
                        if match_count > 0:
                            print(f"Found in: {file_path} ({match_count} {'times' if match_count > 1 else 'time'})")
                except (IOError, UnicodeDecodeError) as e:
                    print(f"Error reading {file_path}: {e}")

search = search_in_files

# Example usage:
search_in_files(r'C:\Users\Administrator\Desktop\work2024\myauto', ['py','html'], 'api', ignored_files_folders=['.git', 'myenv', 'learning.html'])





import markdown
import pyperclip

def convert_clipboard_markdown_to_html():
    # Get the content from the clipboard
    markdown_text = pyperclip.paste()
    
    # Convert Markdown to HTML
    html = markdown.markdown(markdown_text)
    
    # Copy the HTML back to the clipboard
    pyperclip.copy(html)
    
    print("Converted Markdown to HTML and copied to clipboard.")

# Run the function
convert_clipboard_markdown_to_html()
mh = convert_clipboard_markdown_to_html







import pyperclip

def generate_todo_markdown(color: str, title: str, items: list, repeat_num: int = 1, ordered: bool = False) -> str:
    """
    Generates a markdown-formatted to-do list.

    :param color: Emoji color indicator (e.g., "🟢", "🟡", "🔴").
    :param title: Title of the to-do list section (e.g., "Today", "This Week").
    :param items: List of to-do items.
    :param repeat_num: Number of times to repeat the list (default is 1).
    :param ordered: Boolean to indicate if the list should be ordered (default is False).
    :return: Markdown-formatted to-do list as a string.
    """
    markdown_lines = []
    
    # Section title
    markdown_lines.append(f"## {color} {title}")
    
    # Initialize item counter for ordered list
    item_counter = 1
    
    # Generate list items with proper numbering
    for _ in range(repeat_num):
        for item in items:
            if ordered:
                markdown_lines.append(f"- [ ] {item_counter}. {item}")
            else:
                markdown_lines.append(f"- [ ] {item}")
            item_counter += 1
    
    # Join all lines into a single string separated by newlines
    return "\n".join(markdown_lines)

def copy_to_clipboard(text: str):
    """
    Copies the given text to the system clipboard using pyperclip.
    
    :param text: The text to be copied to the clipboard.
    """
    pyperclip.copy(text)
    print("Markdown has been copied to the clipboard!")

# Example usage
todo_list = [
    'Finish reading Chapter 5 of "Atomic Habits"',
    'Reply to pending emails',
    'Grocery shopping',
    '30-minute workout'
]

# Generate the Markdown-formatted to-do list
markdown_text = generate_todo_markdown("🟢", "Today", todo_list, repeat_num=3, ordered=True)
markdown_text = generate_todo_markdown("🟢", "Learn PS 100 mins", ["Learn PS 5 mins"], repeat_num=20, ordered=True)
markdown_text = generate_todo_markdown("🟢", "5, Chatgpt Book", ["2 pages"], repeat_num=40, ordered=False)

# Copy the generated text to the clipboard
copy_to_clipboard(markdown_text)










def manipulate_strings(input_text):
    # Step 1: Split the input text into words
    words = input_text.split()

    # Step 2: Replace digits with 'X'
    redacted = [''.join('X' if w.isdigit() else w for w in word) for word in words]

    # Step 3: Transform words into ASCII, replacing non-ASCII characters
    ascii_text = [word.encode('ascii', errors='replace').decode('ascii') for word in redacted]

    # Step 4: Insert newlines at the end of sentences and split into lines of 80 characters max
    newlines = [word + '\n' if word.endswith('.') else word for word in ascii_text]
    LINE_SIZE = 80
    lines = []
    line = ''
    
    for word in newlines:
        # If adding this word exceeds the limit or the current line ends with a newline, finalize the current line
        if len(line) + len(word) + 1 > LINE_SIZE or line.endswith('\n'):
            lines.append(line.strip())  # Strip any extra spaces
            line = ''
        
        # Add the word to the current line
        line = line + (' ' if line else '') + word
    
    # Append the last line if it's not empty
    if line:
        lines.append(line.strip())
    
    # Step 5: Convert lines to title case
    lines = [line.title() for line in lines]
    
    # Join the lines into the final result
    result = '\n'.join(lines)
    
    return result


import parse
from decimal import Decimal
import delorean

class PriceLog(object):
    def __init__(self, timestamp, product_id, price):
        # Initialize PriceLog object with timestamp, product_id, and price
        self.timestamp = timestamp
        self.product_id = product_id
        self.price = price

    def __repr__(self):
        # Define string representation of PriceLog object
        return '<PriceLog ({}, {}, {})>'.format(self.timestamp, self.product_id, self.price)

    @classmethod
    def parse(cls, text_log):
        '''
        Parse from a text log with the format
        [<Timestamp>] - SALE - PRODUCT: <product id> - PRICE: $<price>
        to a PriceLog object
        for eample:
        [2018-05-06T14:58:59.051545] - SALE - PRODUCT: 827 - PRICE: $22.25
        '''
        def price(string):
            # Convert string to Decimal
            return Decimal(string)

        def isodate(string):
            # Parse string to datetime using delorean
            return delorean.parse(string)

        # Define the format of the log string
        FORMAT = ('[{timestamp:isodate}] - SALE - PRODUCT: {product:d} - '
                  'PRICE: ${price:price}')

        # Define custom parsing functions for price and isodate
        formats = {'price': price, 'isodate': isodate}

        # Parse the text_log using the defined format and custom parsing functions
        result = parse.parse(FORMAT, text_log, formats)

        # Create and return a new PriceLog object with parsed data
        return cls(timestamp=result['timestamp'],
                   product_id=result['product'],
                   price=result['price'])


import pyperclip
import markdown

def markdown_to_html_clipboard():
    # Step 1: Get the Markdown text from the clipboard
    markdown_text = pyperclip.paste()

    # Step 2: Convert Markdown text to HTML
    html_text = markdown.markdown(markdown_text)

    # Step 3: Copy the resulting HTML text back to the clipboard
    pyperclip.copy(html_text)

    print("Markdown has been converted to HTML and copied back to clipboard.")

# Call the function to perform the operation
markdown_to_html_clipboard()







# ai 0
import requests
import json

def create_chat_completion(api_key, model, messages):
    url = "https://api.deepbricks.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": model,
        "messages": messages
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

# Example usage
api_key = "sk-NpvUEGWHfd45VYyaOXwhWA40xZsHCrOg98SbdKleI4BJv320"
model = "gpt-4-turbo"
messages = [
    {
        "role": "user",
        "content": "Hello!"
    }
]

response = create_chat_completion(api_key, model, messages)
print(response)













# ai 1

from openai import OpenAI
API_KEY = "Bearer sk-NpvUEGWHfd45VYyaOXwhWA40xZsHCrOg98SbdKleI4BJv320"
BASE_URL = "https://api.deepbricks.ai/v1/"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  stream=True
)
for chunk in completion:
  print(chunk.choices[0].delta)





from openai import OpenAI
API_KEY = "Bearer sk-NpvUKleI4BJv320"
BASE_URL = "https://api.deepbricks.ai/v1/"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  stream=True
)
for chunk in completion:
  print(chunk.choices[0].delta)




import os
import pyperclip

def generate_structure(path, ignore_folders=None, prefix=''):
    """Generates a folder and file structure from the given path, ignoring specified folders and their contents."""
    if ignore_folders is None:
        ignore_folders = []

    structure = []
    if os.path.isdir(path):
        # List all items in the directory
        items = os.listdir(path)
        items.sort()  # Sort items for a consistent output
        
        for item in items:
            item_path = os.path.join(path, item)
            # Check if the folder name matches any in ignore_folders
            if item in ignore_folders:
                continue  # Skip the ignored folder and its contents

            # If it's a directory, add it and go deeper
            if os.path.isdir(item_path):
                structure.append(f"{prefix}├── {item}/")
                # Recursively add the contents of the subdirectory
                structure.append(generate_structure(item_path, ignore_folders, prefix + '│   '))
            elif os.path.isfile(item_path):
                # Add the file with a proper prefix
                structure.append(f"{prefix}├── {item}")
                
        # Replace the last '├──' with '└──' for the last item
        if structure:
            structure[-1] = structure[-1].replace('├──', '└──', 1)
    
    return '\n'.join(structure)

def copy_structure_to_clipboard(path=None, ignore_folders=None):
    """Generates the structure of the folder and copies it to the clipboard, ignoring specified folders and their contents.
    If no path is provided, it uses the clipboard content as the folder path."""
    if path is None:
        # Get the path from the clipboard
        path = pyperclip.paste()

    if os.path.exists(path):
        # No need to convert to full paths, just use folder names
        structure = generate_structure(path, ignore_folders)
        # Copy the structure to the clipboard
        pyperclip.copy(structure)
        print("Folder structure copied to clipboard:")
        print(structure)
    else:
        print(f"The path '{path}' does not exist.")

# Example usage
# copy_structure_to_clipboard(ignore_folders=['.git', 'myenv', '__pycache__'])

copy_structure_to_clipboard(ignore_folders=['.git', 'myenv', '__pycache__', 'static', 'media', 'migrations'])



import os
import pyperclip as p
from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    gray_img = img.convert('L')
    # Specify the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(gray_img)
    return text

ocr = extract_text_from_image

def write_to_txt_file(func):
    def wrapper(folder_path=None):
        if folder_path is None:
            folder_path = p.paste().strip()  # Get folder path from clipboard if not provided
            print(f"Using clipboard content as folder path: {folder_path}")
        
        result = func(folder_path)
        
        # Determine the file path to save the text
        txt_file_path = os.path.join(folder_path, "extracted_text.txt")
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(result)
        print(f"Text written to {txt_file_path}")
        return result
    return wrapper

@write_to_txt_file
def extract_text_from_images_in_folder(folder_path=None):
    def remove_empty_lines(text):
        lines = text.split('\n')
        non_empty_lines = filter(lambda line: line.strip(), lines)
        return '\n'.join(non_empty_lines)

    all_text = ""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                try:
                    all_text += (ocr(file_path) + '\n')
                    print(f"{file_path} extracted.")
                except PermissionError as e:
                    print(f"Permission error for file {file_path}: {e}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    result = remove_empty_lines(all_text)
    p.copy(result)
    print(result)
    return result

# Call the function with no arguments to use the clipboard content
main = extract_text_from_images_in_folder




'''
prompts:


You are going to act as a Django expert who understands both web development and e-commerce.

Here’s what I want to do: I am going to build a full-featured website using Django. This website will introduce my company and provide a shop for customers to buy products. The most important app, in my opinion, should be the shop, which will handle online sales, followed by a blog for product promotion and SEO. Ultimately, my goal is to create a website that can rival a Shopify store, allowing me to run my business independently.

Below is a brief introduction to the two apps, listing the minimum features the site should have:

The shop app has the following features:

1. **Product Catalog and Shopping Cart:**- A catalog of products.- A shopping cart implemented using sessions.- A custom context processor to make the cart accessible across all templates.

2. **Order Placement:**- A form for placing orders.

3. **Asynchronous Task Management:**- Proficiency in employing asynchronous tasks with Celery and RabbitMQ for handling complex background operations.

4. **Payment Integration:**- Integration with the Stripe payment gateway.- A webhook endpoint for receiving payment notifications.

5. **Administrative Actions and Customization:**- Custom actions in the administration site to export orders to CSV.- Custom views and templates in Django's administration interface.

6. **PDF Generation and Email Integration:**- Generation of PDF files using WeasyPrint.- Integration of generated PDFs as email attachments.

7. **Coupon System:**- Implementation of a coupon system using Django sessions.- Integration of the coupon system with Stripe.

8. **Product Recommendation Engine:**- Development of a product recommendation engine powered by Redis to suggest products typically purchased together.

9. **Internationalization and Localization:**- Marking code and template strings for translation.- Generating and compiling translation files.- Managing translations with Rosetta via a web interface.- Translating URL patterns.- Implementing a language selector for users to switch site languages.- Using django-parler for model translations.- Validating localized form fields with django-localflavor.

The blog app has the following features:
1. **Basic Blog Functionality:**- A simple blog application with data models, views, templates, and URLs.

2. **SEO Optimization:**- Canonical URLs and SEO-friendly URLs for blog posts.

3. **Pagination:**- Posts are paginated to improve navigation and readability.

4. **User Interaction:**- Forms for users to recommend blog posts via email.- A comment system for readers to engage with posts.

5. **Tagging System:**- Tags to categorize posts and improve content organization.

6. **Advanced QuerySets:**- Functionality to recommend similar posts based on content similarity.

7. **Custom Template Tags and Filters:**- Specialized functionalities to enhance the templates.

8. **Sitemap and RSS Feed:**- A sitemap to help search engines index the site.- An RSS feed for users to subscribe to updates.

9. **Full-Text Search:**- A powerful search engine using PostgreSQL to find relevant content within the blog.


If you understand, simply say OK, I will later tell you what I want you to do.

'''




'''
1, Managing GitHub and Git
   - Sign up for a GitHub account and create a repository.
   - Initialize Git in the local project folder.
   - Add and commit project files to the repository.
   - Push the code to GitHub.
   
git init
git add .
git commit -m "first version"
git branch -M main
git remote add origin <your-origin-path>
git push -u origin main

2, Cloning our code onto PythonAnywhere
   - Create a free account on PythonAnywhere.
   - Open a Bash console on PythonAnywhere.
   - Clone the GitHub repository to PythonAnywhere.
---

**PythonAnywhere Bash Setup**

1. **Accessing Bash Console:**
   - Open PythonAnywhere.
   - Click **Dashboard** > **New console** > **$ Bash**.

2. **Cloning from GitHub:**
   - Go to your GitHub repository.
   - Click **Code** and copy the URL.
   - In PythonAnywhere Bash shell, run:
     ```
     git clone <repo-url>
     ```

---

git clone https://github.com/matrixfire/mysite2024.git



3, Configuring virtual environments
   - Create a virtual environment using `mkvirtualenv`.
   - Install required packages (Django, Pillow) in the virtual environment.
---

**Managing Virtual Environments on PythonAnywhere**

1. **Creating a Virtual Environment:**
   - To create using Python 3.8:
     ```
     mkvirtualenv -p python3.8 <environment name>
     ```
	 mkvirtualenv -p python3.10 reobrix_venv
	 

2. **Activating and Deactivating:**
   - To deactivate the virtual environment:
     ```
     deactivate
     ```
   - To activate a virtual environment:
     ```
     workon <virtualenv-name>
	 
	 workon reobrix_venv
	 
	 workon reobrix_venv && cd /home/reobrix/mysite2024 && celery -A reobrix worker
	 
	 workon your_virtualenv && cd /path/to/your_project && celery -A your_project worker

     ```

---



4, Setting up your web app
   - Gather information: project path, project name, virtual environment name.
   - Create a web app with manual configuration on PythonAnywhere.
   - Configure the WSGI file to point to the Django project.
   - Update `ALLOWED_HOSTS` in `settings.py` and reload the web app.

---

**Setting up Django Web App on PythonAnywhere**

1. **Prepare Information:**
   - "A": Get the path to your Django project's top folder using `pwd` in Bash, e.g., `/home/danielgara/moviereviews/`.(the folder that contains "manage.py")
   - "B": Note your project's name (folder containing `settings.py`), e.g., `moviereviews`.
   - "C": Remember your virtualenv name, e.g., `moviereviewsenv`.

A: /home/reobrix/mysite2024
B: reobrix
C: reobrix_venv



2. **PythonAnywhere Setup:**
   - Open PythonAnywhere dashboard.
   - Go to **Web** > **Add a new web app**.
   - Choose **Manual configuration** under Python Web framework.
   - Select Python version (e.g., Python 3.8) and click **Next**.
   - enter the name of your virtualenv（i.e. "C" info） in the Virtualenv section
   - Enter project folder path(i.e. "A" info) in **Source code** and **Working directory**.

3. **Configure WSGI File:**
   - Open `wsgi.py` and modify to:
     ```python
	# +++++++++++ DJANGO +++++++++++
	# To use your own django app use code like this:
     import os
     import sys

     path = '/home/danielgara/moviereviews' # "A" info
     if path not in sys.path:
         sys.path.append(path)

     os.environ['DJANGO_SETTINGS_MODULE'] = 'moviereviews.settings' # "B" info

     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```

4. **Update ALLOWED_HOSTS:**
   - Navigate to **Files** > find `settings.py` in `moviereviews/`.
   - Modify `ALLOWED_HOSTS`:
     ```python
     DEBUG = True
     ALLOWED_HOSTS = ['*']
     ```

5. **Reload and Test:**
   - Go to **Web** tab, click **Reload** for your domain.
   - Visit your project's URL to see the home page.

---

mysql -u reobrix -h reobrix.mysql.pythonanywhere-services.com -p 'reobrix$default'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
		'TEST': {'NAME': config('TEST_DB_NAME'),}
    }
}



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<your_username>$<your_database_name>',
        'USER': '<your_username>',
        'PASSWORD': '<your_mysql_password>',
        'HOST': '<your_mysql_hostname>',
		'TEST': {
            'NAME': '<your username>$test_<your database name>',
        }
    }
}







reobrix
reobrix.mysql.pythonanywhere-services.com


5, Configuring static files
   - Define `STATIC_URL` and `STATIC_ROOT` in `settings.py`.
   - Run `python manage.py collectstatic` to gather static files.
   - Set up static file mappings on PythonAnywhere.

---

**Configuring Static Files in Django on PythonAnywhere**

1. **Update `settings.py`:**
   - Add the following line:
     ```python
     STATIC_ROOT = os.path.join(BASE_DIR, 'static')
     ```
   - This sets a central location (`STATIC_ROOT`) for collecting all static files.

2. **Collect Static Files:**
   - In the Bash console (inside virtualenv), navigate to your project folder:
     ```
     cd moviereviews/
     ```
   - Run the command to collect static files:
     ```
     python manage.py collectstatic
     ```
   - This gathers static files from app folders and admin, copying them to `STATIC_ROOT`.

3. **Configure Static Files on PythonAnywhere:**
   - Go to PythonAnywhere dashboard **Web** tab.
   - Under **Static files**:
     - Enter `STATIC_URL` (typically `/static/`) in the **URL** section.
     - Enter full path from `STATIC_ROOT` in the **Path** section (e.g., `/home/username/moviereviews/static`).

4. **Reload Web App:**
   - Click **Reload** on the **Web** tab in PythonAnywhere.
   - Your static images should now appear correctly on your site.

---


---

**Production Configuration and .gitignore Setup**

1. **Setting DEBUG for Production:**
   - Go to PythonAnywhere dashboard.
   - Open `settings.py` for your project.
   - Set `DEBUG = False`.
   - Save the file and reload the web app.

2. **Creating .gitignore:**
   - Create a `.gitignore` file in your project root folder.
   - Add the following lines to ignore specific files:
     ```
     __pycache__/
     db.sqlite3
     .DS_Store
     ```
   - These files include cached Python files, database storage, and macOS folder settings.

---




6, Changing db.sqlite3 to MySQL or PostgresSQL

   - Use MySQL or PostgreSQL for larger projects.
   - Follow PythonAnywhere's documentation for database setup.
   - Recreate superuser and run migrations for the new database.

---

**Switching Database to MySQL or PostgreSQL**

1. **Setting Up MySQL:**
   - Refer to PythonAnywhere's documentation for setting up MySQL:
     - Free MySQL setup: [PythonAnywhere MySQL Documentation](https://help.pythonanywhere.com/pages/UsingMySQL/)
     - PostgreSQL setup requires a paid account.

2. **After Database Setup:**
   - Once MySQL or PostgreSQL is set up:
     - Create a new superuser for the new database:
       ```
       python manage.py createsuperuser
       ```
     - Make migrations for database changes:
       ```
       python manage.py makemigrations
       ```
     - Apply migrations to the database:
       ```
       python manage.py migrate
       ```

---

This note provides a detailed guide on deploying a Django project to PythonAnywhere, covering GitHub management, virtual environment setup, web app configuration, static file management, and database migration.


'''

################################################# FINAL VERSION 1


from openai import OpenAI
import pyperclip

API_KEY = "Bearer sk-NpvUEGWHfd45VYyaOXwhWA40xZsHCrOg98SbdKleI4BJv320"
BASE_URL = "https://api.deepbricks.ai/v1/"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def generate_chat_completion(messages, model="GPT-3.5-turbo", max_tokens=1024, n=1, stop=None, temperature=0.8, stream=True):
    """
    Generate a chat completion using OpenAI's API.

    Args:
        messages (list): A list of messages for the chat.
        model (str): The model to use for the completion. Default is "GPT-3.5-turbo".
        max_tokens (int): The maximum number of tokens to generate in the response.
        n (int): Number of completions to generate for each prompt.
        stop (str or list): The stopping sequence(s) where the API will stop generating further tokens.
        temperature (float): Controls randomness in the output. Lower values make the output more deterministic.
        stream (bool): Whether to stream the response. Default is True.

    Returns:
        None: Prints the complete response.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
        stream=stream
    )
    
    # Collecting the complete response
    full_response = ""
    for chunk in completion:
        full_response += chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
    
    pyperclip.copy(full_response)
    return full_response

def main():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("Start chatting with the assistant (type 'exit' to stop):")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        messages.append({"role": "user", "content": user_input})

        # Generate the assistant's response
        assistant_response = generate_chat_completion(messages)

        # Print formatted output
        print("\n" + "=" * 50)
        print("Assistant:", assistant_response.strip())
        print("=" * 50)

if __name__ == "__main__":
    main()



################################################# FINAL VERSION 1
API_KEY = "Bearer sk-NpvUEGWHfd45VYyaOXwhWA40xZsHCrOg98SbdKleI4BJv320"



import pyperclip
from openai import OpenAI
import time

API_KEY = "Bearer sk-NpvUEGWHfd45VYyaOXwhWA40xZsHCrOg98SbdKleI4BJv320"
BASE_URL = "https://api.deepbricks.ai/v1/"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def generate_chat_completion(messages, model="GPT-4o-mini", max_tokens=1024, n=1, stop=None, temperature=0.8, stream=True):
    """
    Generate a chat completion using OpenAI's API.
    
    Args:
        messages (list): A list of messages for the chat.
        model (str): The model to use for the completion. Default is "GPT-3.5-turbo".
        max_tokens (int): The maximum number of tokens to generate in the response.
        n (int): Number of completions to generate for each prompt.
        stop (str or list): The stopping sequence(s) where the API will stop generating further tokens.
        temperature (float): Controls randomness in the output. Lower values make the output more deterministic.
        stream (bool): Whether to stream the response. Default is True.
    
    Returns:
        str: The assistant's response.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
        stream=stream
    )
    
    # Collecting the complete response
    full_response = ""
    for chunk in completion:
        full_response += chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
    
    return full_response.strip()

def clipboard_chat_(initial_prompt):
    """
    Start a chat session using clipboard input.
    
    Args:
        initial_prompt (str): The initial prompt to set up the conversation.
    
    Returns:
        None
    """
    messages = [{"role": "system", "content": initial_prompt}]
    print("Chat session started. Press Enter to use clipboard text as input.")

    while True:
        input("Press Enter to get text from clipboard...")
        
        clipboard_text = pyperclip.paste()
        if clipboard_text:
            print(f"Using clipboard text: '{clipboard_text}'")
            messages.append({"role": "user", "content": clipboard_text})

            # Generate the assistant's response
            assistant_response = generate_chat_completion(messages)

            # Copy the response to clipboard
            pyperclip.copy(assistant_response)
            print("Assistant:", assistant_response)
            print("Response copied to clipboard!")
        else:
            print("Clipboard is empty. Please copy some text.")


def clipboard_chat(initial_prompt, max_history_length=5):
    """
    Start a chat session using clipboard input, keeping the initial prompt 
    and the most recent messages within a specified limit.
    
    Args:
        initial_prompt (str): The initial system message for context.
        max_history_length (int): The number of user/assistant messages to retain.
    """
    messages = [{"role": "system", "content": initial_prompt}]
    print("Chat session started with initial system message.")
    print(generate_chat_completion(messages))

    while True:
        input("Press Enter to get text from clipboard...")
        
        clipboard_text = pyperclip.paste()
        if clipboard_text:
            print(f"Using clipboard text: '{clipboard_text}'")
            messages.append({"role": "user", "content": clipboard_text})

            # Adjust the message history to keep the system message, latest user input, 
            # and up to the max_history_length of previous user/assistant exchanges.
            if len(messages) > max_history_length + 2:  # +2 to account for system message and latest user input
                messages = [messages[0]] + messages[-(max_history_length + 1):]

            # Generate the assistant's response
            assistant_response = generate_chat_completion(messages)

            # Copy the response to clipboard
            pyperclip.copy(assistant_response)
            print("Assistant:", assistant_response)
        else:
            print("Clipboard is empty. Please copy some text.")



def bot():
    input("Press Enter to set initalial prompt text from clipboard...")
    initial_prompt = pyperclip.paste() or "You are a helpful assistant."
    clipboard_chat(initial_prompt)





if __name__ == "__main__":
    bot()











import os
import re
import shutil
import pyperclip

def move_file_and_generate_path():
    # Step 1: Get the file path from the clipboard
    file_path = pyperclip.paste().strip('"')

    # Check if the file path is valid
    if not os.path.isfile(file_path):
        print("The path provided is not valid.")
        return

    # Step 2: Define the target folder
    target_folder = r"F:\BaiduNetdiskDownload\已经上传Youtube视频"
    
    # Step 3: Move the file to the target folder
    try:
        shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))
        print(f"Moved file to {target_folder}")
    except Exception as e:
        print(f"Error moving file: {e}")
        return

    # Step 4: Extract the product ID from the filename
    filename = os.path.basename(file_path)
    match = re.search(r'(\d+)', filename)

    if match:
        product_id = match.group(1)
        # Step 5: Generate the new path
        new_path = rf"G:\x\t2\产品详情\{product_id}"
        
        # Step 6: Copy the new path to the clipboard
        pyperclip.copy(new_path)
        print(f"Generated path: {new_path} and copied to clipboard.")
    else:
        print("No product ID found in the filename.")

# Run the function
move_file_and_generate_path()






import pyperclip
import os

def create_file_from_clipboard():
    # Get the text from the clipboard and strip whitespace from both ends
    clipboard_text = pyperclip.paste().strip()
    
    # Split the clipboard text into lines
    lines = clipboard_text.splitlines()
    
    # Check if there are at least three lines (file name, path, and code)
    if len(lines) < 3:
        print("Clipboard content is incomplete. Please include a file name, file path, and code.")
        return
    
    # Get the file name, path, and code
    file_name = lines[0].strip()
    file_path = lines[1].strip()
    code = "\n".join(lines[2:]).strip()
    
    # Create the full file path
    full_path = os.path.join(file_path, file_name)
    
    try:
        # Ensure the directory exists
        os.makedirs(file_path, exist_ok=True)
        
        # Write the code into the file
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(code)
        print(f"File created successfully at: {full_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
create_file_from_clipboard()
















import shutil

def read_css_file(file_path):
    """Read CSS content from a specified file path."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_css_file(file_path, css_content):
    """Save updated CSS content to the specified file path."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(css_content)

def find_all_occurrences(css_content, search_text):
    """Find all occurrences of a specified text in the CSS content."""
    occurrences = []
    start = 0
    while start < len(css_content):
        start = css_content.find(search_text, start)
        if start == -1:
            break
        end = start + len(search_text)
        occurrences.append({'start': start, 'end': end, 'text': search_text})
        start = end  # Move past the last found occurrence
    return occurrences

def replace_occurrences_in_range(css_content, occurrences, start_idx, end_idx, new_value):
    """Replace specified occurrences in the CSS content with a new value within a given range."""
    modified_content = css_content
    offset = 0

    for i in range(start_idx, min(end_idx + 1, len(occurrences))):
        occurrence = occurrences[i]
        original_text = occurrence['text']
        modified_content = (
            modified_content[:occurrence['start'] + offset] +
            new_value +
            modified_content[occurrence['end'] + offset:]
        )
        offset += len(new_value) - len(original_text)
    
    return modified_content

def main():
    file_path = r"C:\Users\Administrator\Desktop\work2024\reobrix_site\reobrix2\core\static\core\css\style2base_un.css"
    backup_path = file_path + ".backup"
    
    # Backup the original CSS file
    shutil.copyfile(file_path, backup_path)
    original_css_content = read_css_file(file_path)

    while True:
        search_text = input("Enter the text to search for in the CSS file (or 'q' to quit): ")
        if search_text.lower() == 'q':
            break

        occurrences = find_all_occurrences(original_css_content, search_text)
        
        if not occurrences:
            print(f"No occurrences of '{search_text}' found. Please try a different text.")
            continue

        print(f"Found {len(occurrences)} occurrences of '{search_text}'.")

        while True:
            range_input = input("Enter the range of occurrences to modify (e.g., '1-39') or 'q' to quit: ")
            
            if range_input.lower() == 'q':
                break

            # Handle single-item range (e.g., "35" as "35-35")
            if '-' not in range_input:
                range_input = f"{range_input}-{range_input}"

            try:
                start_idx, end_idx = map(int, range_input.split('-'))
                start_idx -= 1  # Convert to zero-based index
                end_idx -= 1    # Convert to zero-based index

                new_value = input("Enter the new value to replace with (leave blank to skip): ")
                if not new_value:
                    print("No new value provided, skipping replacement.")
                    continue
                
                modified_content = replace_occurrences_in_range(original_css_content, occurrences, start_idx, end_idx, new_value)
                save_css_file(file_path, modified_content)
                print(f"Modified CSS content from occurrence {start_idx + 1} to {end_idx + 1}. Press Enter to revert.")
                
                input()  # Wait for user to press Enter to revert
                save_css_file(file_path, original_css_content)
                print("CSS file reverted to original content.")
            
            except ValueError:
                print("Invalid input. Please enter a valid range.")

if __name__ == "__main__":
    main()
