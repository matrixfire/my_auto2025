'''
MANIPULATING IMAGES

Photos

need to edit a massive number of images


Pillow: crop, resize, and edit the content of an image
All the rotations, resizing, cropping, drawing, and other image manipulations will be done through method calls on this Image object.

The origin is the pixel at the top-left corner of the image and is specified with the notation (0, 0). 
Coordinates and Box Tuples: Many of Pillow’s functions and methods take a box tuple argument, like (3, 1, 9, 6), which is (Left, Top, Right, Bottom).
'''
from PIL import Image, ImageColor, ImageDraw
import os


aIm = Image.open('zophie.png')
aIm.save('zophie.jpg')

width, height = aIm.size
# catIm.format_description
print(f"{aIm.filename}, {aIm.format}")



def gis(image_path):
    with Image.open(image_path) as img:
        return img.size

cIm = aIm.crop((335, 345, 565, 560)) # exclusive
cIm.save('cropped.png')

dIm = aIm.copy()
dIm.paste(cIm, (0, 0))

x, y = dIm.size[0]-cIm.size[0], dIm.size[1]-cIm.size[1]
dIm.paste(cIm, (x, y))


eIm = aIm.resize((int(width / 2), int(height / 2)))
eIm.save('quartersized.png')


aIm.rotate(90).save('rotated90.png')

fIm = aIm.rotate(7, expand=True)
fIm.save('rotated7_expanded.png')

gIm.transpose(Image.FLIP_LEFT_RIGHT).save('horizontal_flip.png')
gIm.transpose(Image.FLIP_TOP_BOTTOM).save('vertical_flip.png')








def change_file_name(input_path):
    path_without_extension, extension = os.path.splitext(input_path)
    counter = 1  # Start with 1 as we'll be appending this to the filename if it exists.
    new_path = input_path  # Start with the original path
    # Keep incrementing the counter and updating the filename until we find one that doesn't exist.
    while os.path.exists(new_path):
        new_path = f"{path_without_extension}({counter}){extension}"
        counter += 1
    return new_path



def merge_and_save_images_corrected_lt(base_image_path, second_image_path_lt, factor=0.7):
    """
    Adjusts the function to resize the second image to 61.8% of the base image's height, ensuring the resized second
    image is pasted within the right side of the base image. The center of the second image will be equidistant from
    the upper, lower, and right side of the base image. This version also ensures the spacing on the right side of the
    base image is the same as the spacing to the sides of the second image. The final image is saved over the base image
    path, effectively updating the original base image.
    """
    from PIL import Image

    # Open the base image
    with Image.open(base_image_path) as base_img:
        base_width, base_height = base_img.size
        print(f"Base image size: {base_img.size}")
        base_width_ = base_width
        # Open the second image and resize it to 61.8% of the base image's height
        for second_image_path in second_image_path_lt:
            print(second_image_path)
            with Image.open(second_image_path) as second_img:
                resize_height = int(base_height * factor)
                resize_width = int(resize_height*second_img.size[0]//second_img.size[1])
                second_img_resized = second_img.resize((resize_width, resize_height))

                # Calculate the position to paste the resized second image
                # Ensure it's within the base image and equidistant from the top, bottom, and right edge
                spacing = (base_height - resize_height) // 2
                x_position = base_width_ - resize_width - spacing
                y_position = spacing

                # Paste the resized second image onto the base image at the calculated position
                base_img.paste(second_img_resized, (x_position, y_position))

                # Save the modified image back to the base image path
                # new_base_image_path = 'new_' + base_image_path
                # new_base_image_path = change_file_name(new_base_image_path)
            base_width_ -= resize_height*second_img.size[0]//second_img.size[1] *1
            base_width_ = int(base_width_)
        new_base_image_path = os.path.join(os.path.dirname(base_image_path), "new_" + os.path.basename(base_image_path))
        new_base_image_path = change_file_name(new_base_image_path)
        base_img.save(new_base_image_path)






def merge_and_save_images_corrected_lt_whole(base_image_path, second_image_path_lt, factor=0.7):
    """
    This function resizes each image in second_image_path_lt to a height that is 70% of the base image's height,
    ensuring all are the same size. Each image's width-to-height ratio is checked to be within 10% of 3/4.
    Images are pasted side by side, closely to each other, ensuring the distance from the leftmost and rightmost
    images to the base image's borders are equal. The final image is saved over the base image path, effectively
    updating the original base image.
    """
    from PIL import Image
    import os

    # Open the base image
    with Image.open(base_image_path) as base_img:
        base_width, base_height = base_img.size
        print(f"Base image size: {base_img.size}")

        # Resize height for all images
        resize_height = int(base_height * factor)
        
        # Initialize variables for pasting images
        total_width = 0
        images_resized = []
        valid_ratios = True

        # Process each image
        for second_image_path in second_image_path_lt:
            with Image.open(second_image_path) as second_img:
                ratio = second_img.width / second_img.height
                if not (0.675 <= ratio <= 0.825):
                    print(f"Image {second_image_path} ratio {ratio:.2f} is out of the acceptable range.")
                    valid_ratios = False
                    continue

                # Calculate resized width to maintain the same height
                resize_width = int(resize_height * second_img.width / second_img.height)
                second_img_resized = second_img.resize((resize_width, resize_height))
                images_resized.append(second_img_resized)
                total_width += resize_width

        if not valid_ratios:
            return
        
        # Calculate the starting x position
        spacing = (base_width - total_width) // 2
        
        # Paste images side by side
        current_x = spacing
        for img in images_resized:
            base_img.paste(img, (current_x, (base_height - resize_height) // 2))
            current_x += img.width

        # Save the modified image
        new_base_image_path = os.path.join(os.path.dirname(base_image_path), "updated_" + os.path.basename(base_image_path))
        base_img.save(new_base_image_path)
        print(f"Modified image saved as {new_base_image_path}")






def copy_files_by_list(source_folder, str_list, output_folder):
    # Ensure output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all files in the source folder
    source_files = os.listdir(source_folder)

    # Track found files to handle items with no corresponding file
    found_files = set()

    # Iterate over each item in the list
    for item in str_list:
        # Flag to check if the file was found for this item
        file_found = False

        # Check each file in the source folder
        for file in source_files:
            # If the item matches the file basename (without extension)
            if item in os.path.splitext(file)[0] and len(item)==len(os.path.splitext(file)[0]):# == item:
                # Mark as found
                file_found = True
                found_files.add(item)

                # Copy the file to the output folder
                src_file_path = os.path.join(source_folder, file)
                dst_file_path = os.path.join(output_folder, file)
                shutil.copy2(src_file_path, dst_file_path)
                print(f"Copied '{file}' to '{output_folder}'.")

        if not file_found:
            print(f"No file found for '{item}'.")

    # Check for items with no corresponding file
    for item in set(str_list) - found_files:
        print(f"No corresponding file found for '{item}'.")










def _merge_and_save_images_corrected(base_image_path, second_image_path, factor=0.7):
    """
    Adjusts the function to resize the second image to 61.8% of the base image's height, ensuring the resized second
    image is pasted within the right side of the base image. The center of the second image will be equidistant from
    the upper, lower, and right side of the base image. This version also ensures the spacing on the right side of the
    base image is the same as the spacing to the sides of the second image. The final image is saved over the base image
    path, effectively updating the original base image.
    """
    from PIL import Image

    # Open the base image
    with Image.open(base_image_path) as base_img:
        base_width, base_height = base_img.size
        print(f"Base image size: {base_img.size}")

        # Open the second image and resize it to 61.8% of the base image's height
        with Image.open(second_image_path) as second_img:
            resize_height = int(base_height * factor)
            second_img_resized = second_img.resize((resize_height, resize_height))

            # Calculate the position to paste the resized second image
            # Ensure it's within the base image and equidistant from the top, bottom, and right edge
            spacing = (base_height - resize_height) // 2
            x_position = base_width - resize_height - spacing-resize_height
            y_position = spacing

            # Paste the resized second image onto the base image at the calculated position
            base_img.paste(second_img_resized, (x_position, y_position))

            # Save the modified image back to the base image path
            new_base_image_path = 'new_' + base_image_path
            base_img.save(new_base_image_path)

# Note: To use this function, replace 'base_image_path' and 'second_image_path' with your actual image paths.
# This code will not run here due to the absence of actual file paths and images.
# Example usage:
# base_image_path = "/path/to/your/base/image.jpg"
# second_image_path = "/path/to/your/second/image.jpg"
# merge_and_save_images_corrected(base_image_path, second_image_path)
# The modified base image will be saved over the original file.

# Example usage
# base_image_path = "/path/to/base/image.jpg"
# second_image_path = "/path/to/second/image.jpg"
# modified_image = merge_images_within_base(base_image_path, second_image_path)
# modified_image.show() # This will display the base image with the second image merged within its right side.


# Example usage
# base_image_path = "/path/to/base/image.jpg"
# second_image_path = "/path/to/second/image.jpg"
# new_image = merge_images(base_image_path, second_image_path)
# new_image.show() # This will display the new image with the modifications.




















def change_individual_pixels():
    # Create a new RGBA image with dimensions 100x100
    im = Image.new('RGBA', (100, 100))
    # bIm = Image.new('RGBA', (100, 200), 'purple') # ('purple' can be omitted which means Invisible black, (0, 0, 0, 0), is the default color used if no color argument is specified
    # Set the pixels in the top half of the image to (210, 210, 210, 255)
    for x in range(100):
        for y in range(50):
            im.putpixel((x, y), (210, 210, 210, 255))
    # Set the pixels in the bottom half of the image to 'darkgray'
    for x in range(100):
        for y in range(50, 100):
            im.putpixel((x, y), ImageColor.getcolor('darkgray', 'RGBA'))
            # get RGBA values from color name
            # ImageColor.getcolor('red', 'RGBA') # case-insensitive
    # Print the pixel values at specific coordinates
    print(im.getpixel((0, 0)))    # (210, 210, 210, 255)
    print(im.getpixel((0, 50)))   # (169, 169, 169, 255)
    # Save the image
    im.save('putPixel.png')




# tile Zophie’s head across the entire image
def tile_object_across_background(background_path, object_path, output_path):
    # Open the images
    background = Image.open(background_path)
    obj = Image.open(object_path)
    # Get image dimensions
    background_width, background_height = background.size
    obj_width, obj_height = obj.size
    # Create a copy of the background image
    result_image = background.copy()
    # Iterate over positions and paste the object image
    for left in range(0, background_width, obj_width):
        for top in range(0, background_height, obj_height):
            result_image.paste(obj, (left, top))
    # Save the result
    result_image.save(output_path)

# the boring job of resizing thousands of images and adding a small logo watermark to the corner of each.
    




def resize_and_add_logo(input_dir='.', output_dir='withLogo', square_fit_size=300, logo_filename='catlogo.png'):
    # Load the logo image
    logo_im = Image.open(logo_filename)
    logo_width, logo_height = logo_im.size
    print(f"Logo dimensions: {logo_width} x {logo_height}")
    # Create a directory to store images with logos
    os.makedirs(output_dir, exist_ok=True)
    # Loop over all files in the input directory
    for filename in os.listdir(input_dir):
        # Skip non-image files and the logo file itself
        if not (filename.endswith('.png') or filename.endswith('.jpg')) or filename == logo_filename:
            continue
        # Open the image
        im = Image.open(os.path.join(input_dir, filename))
        width, height = im.size
        print(f"Original image dimensions: {width} x {height}")
        ori_width, ori_height = width, height
        # Check if the image needs to be resized
        if width > square_fit_size or height > square_fit_size:
            # Calculate the new width and height to resize to
            if width > height:
                height = int((square_fit_size / width) * height)
                width = square_fit_size
            else:
                width = int((square_fit_size / height) * width)
                height = square_fit_size
            # Resize the image
            print(f'Resizing {filename}... from original ({ori_width}, {ori_height}) to ({width}, {height}).')
            im = im.resize((width, height))
        # Add the logo to the lower-right corner
        print(f'Adding logo to {filename}...')
        logo_im_resized = logo_im.resize((int(min(width, height) * 1/10), int(min(width, height) * 1/10 * logo_height/logo_width)))
        logo_resized_width, logo_resized_height = logo_im_resized.size
        im.paste(logo_im_resized, (width - logo_resized_width, height - logo_resized_height), logo_im_resized)
        # Save changes
        im.save(os.path.join(output_dir, filename))

# Example usage
# resize_and_add_logo(input_dir='.', output_dir='withLogo', square_fit_size=300, logo_filename='catlogo.png')




def get_size(size, required_dimension):
    a, b = size
    if max(a, b) > required_dimension:
        return size
    else:
        if a >b:
            return (required_dimension, required_dimension*b//a)
        else:
            return (required_dimension*a//b, required_dimension)
    

def resize_images(input_folder, output_folder, size=(200, 200)):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    # Iterate over all files in the input folder
    for file_name in os.listdir(input_folder):
        # Get the full path of the file
        file_path = os.path.join(input_folder, file_name)
        # Check if the file is an image (you can extend this check if needed)
        if os.path.isfile(file_path) and file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            # Open the image using PIL
            try:
                with Image.open(file_path) as img:

                    size = get_size(img.size, 3000)
                    # Resize the image
                    img_resized = img.resize(size)
                    
                    # Get the file name (without extension) and extension
                    file_name_no_ext, file_ext = os.path.splitext(file_name)
                    
                    # Construct the output file path
                    output_file_path = os.path.join(output_folder, f"{file_name_no_ext}_resized{file_ext}")

                    # Save the resized image to the output folder
                    img_resized.save(output_file_path)
                    print(f"Resized image saved: {output_file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        else:
            print(f"Skipping {file_path}. Not an image file.")


a_d = r'C:\Users\34950\Desktop\test3\1'
b_d = r'C:\Users\34950\Desktop\test3'
resize_images(a_d, b_d)
'''PATTERN MATCHING WITH REGULAR EXPRESSIONS


ttps://pythex.org/.

'''





'''
My work:
Ideas for Similar Programs
Being able to composite images or modify image sizes in a batch can be useful in many applications. You could write similar programs to do the following:

Add text or a website URL to images.
Add timestamps to images.
Copy or move images into different folders based on their sizes.
Add a mostly transparent watermark to an image to prevent others from copying it.'''



# Create a new RGBA image with a white background
im = Image.new('RGBA', (200, 200), 'white')
draw = ImageDraw.Draw(im)

# Draw a black square
draw.line([(0, 0), (199, 0), (199, 199), (0, 199), (0, 0)], fill='black')

# Draw a blue rectangle
draw.rectangle((20, 30, 60, 60), fill='blue')

# Draw a red ellipse (or circle in this case)
draw.ellipse((120, 30, 160, 60), fill='red')

# Draw a brown polygon
draw.polygon(((57, 87), (79, 62), (94, 85), (120, 90), (103, 113)), fill='brown')

# Draw green lines
for i in range(100, 200, 10):
    draw.line([(i, 0), (200, i - 100)], fill='green')

# Save the image
im.save('drawing.png')



from PIL import Image, ImageDraw, ImageFont
import os

# Create a new RGBA image with a white background
im = Image.new('RGBA', (200, 200), 'white')
draw = ImageDraw.Draw(im)

# Draw text using the default font
draw.text((20, 150), 'Hello', fill='purple')

# Specify a custom font (Arial in this case)
fonts_folder = 'FONT_FOLDER'  # Replace with the actual path to your font folder
arial_font_path = os.path.join(fonts_folder, 'arial.ttf')
arial_font = ImageFont.truetype(arial_font_path, 32)
draw.text((100, 150), 'Howdy', fill='gray', font=arial_font)

# Save the image
im.save('text.png')







def make_66_plans():
    import pyperclip as p
    import random as r
    text = p.paste().strip()
    lines = text.split('\n')
    print(f'Lines found: {len(lines)}')
    if len(lines) < 36:
        lines.extend(["contiue"]*(36-len(lines)))
    r.shuffle(lines)
    pre_plans = lines[:36]
    plans = []
    for i in range(1,7):
        for j in range(1, 7):
            plans.append(f"D{i}{j}-{pre_plans.pop()}")
    print(plans)
    txt = '\n'.join(plans).strip()
    p.copy(txt)

    
import re
phoneNumRegex = re.compile(r'((\d\d\d)|(\(\d\d\d\))-)?(\d\d\d-\d\d\d\d)') # The first set of parentheses in a regex string will be group 1
mo = phoneNumRegex.search('My number is 415-555-4242.')
mo = phoneNumRegex.search('My number is (415)-555-4242.')
mo = phoneNumRegex.search('My number is 555-4242.')
print(f'{mo.group(1)}, {mo.group(0)}, {mo.group()}, {mo.groups()}')
# Passing 0 or nothing to the group() method will return the entire matched text. 
# If you would like to retrieve all the groups at once, use the groups() method

def magic(temp):
    ts = temp.group(1)
    ts_all = temp.group()
    return rf"{ts}{'*'*(len(ts_all)-7)}"

sample_str =  'Agent Alice told Agent Carol that Agent Eve knew Agent Bob was a double agent.'
agentNamesRegex = re.compile(r'Agent (\w)\w*')
agentNamesRegex.sub(r'\1****',sample_str)
agentNamesRegex.sub(magic, sample_str)
agentNamesRegex.sub(lambda mo:mo.group(1).title(), sample_str)

def m():
    import pyperclip as p
    import re
    original_txt = p.paste()
    re_obj = re.compile(r'第(\d)章')
    re_obj = re.compile(r'\d,\s+\w*.+')
    re_obj = re.compile(r"\{% static '(.*?)' %\}") # {% static 'css/nucleo-icons.css' %}
    new_txt = re_obj.sub(r"{% static 'new_/\1' %}", original_txt)
    # txt_lt = re_obj.findall(original_txt)
    p.copy(new_txt)
    # p.copy('\n'.join(txt_lt).strip())

def reverse_lines_in_clipboard():
    import pyperclip
    # Get text from clipboard
    clipboard_text = pyperclip.paste()

    # Split the text into lines and reverse their order
    lines = clipboard_text.splitlines()
    reversed_lines = reversed(lines)

    # Join the reversed lines and set the result back to the clipboard
    reversed_text = '\n'.join(reversed_lines)
    pyperclip.copy(reversed_text)

def magic_lines():
    import pyperclip
    # Get text from clipboard
    clipboard_text = pyperclip.paste()
    # Split the text into lines and reverse their order
    lines = clipboard_text.splitlines()
    new_lines = list(filter(lambda x: "import" in x, lines))
    # Join the reversed lines and set the result back to the clipboard
    new_text = '\n'.join(new_lines)
    pyperclip.copy(new_text)



import os

def extract_and_combine_py_files(folder_path, output_file):
    """
    Extracts all .py files from the specified folder and its subdirectories,
    excluding .pyc files and the 'myenv' directory, and combines them into a single output file.
    """
    with open(output_file, 'w') as outfile:
        for root, dirs, files in os.walk(folder_path):
            # Exclude 'myenv' directory and its subdirectories
            if 'myenv' in dirs:
                dirs.remove('myenv')
            for filename in files:
                if filename.endswith('.py') and not filename.endswith('.pyc'):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n' + '_' * 30 + "\n\n")  # Add a newline separator between files
                    print(f'Finished {filename}!')

# Example usage:
folder_to_extract = '/path/to/your/folder'
output_filename = 'combined_python_files.py'
extract_and_combine_py_files(folder_to_extract, output_filename)
print(f"Combined .py files saved to {output_filename}")




import pandas as pd
import os

# Load the Excel file
df = pd.read_excel(r'C:\Users\Administrator\Desktop\very_temp\items.xlsx')

# Directory where images are stored
image_directory = r'C:\Users\Administrator\Desktop\very_temp\products_imgs'

# Function to find image for each SKU
def find_image(sku):
    # Convert sku to string to ensure compatibility with startswith
    sku = str(sku)
    for file in os.listdir(image_directory):
        if file.startswith(sku):  # Now comparing strings with strings
            return os.path.join(image_directory, file)
    return "No Image Found"

# Apply the function to each SKU in the dataframe
df['Image Link'] = df['SKU'].apply(find_image)

# Save the updated DataFrame back to Excel
df.to_excel('updated_file.xlsx', index=False)








import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    # Specify the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(img)
    return text

ocr = extract_text_from_image
















def modify_excel(excel_path):
    # Load the existing workbook
    wb_old = openpyxl.load_workbook(excel_path)
    ws_old = wb_old.active

    # Create a new workbook
    new_excel_name = os.path.splitext(os.path.basename(excel_path))[0]
    new_excel_path = os.path.join(os.path.dirname(excel_path), f"{new_excel_name} (modified).xlsx")
    wb_new = openpyxl.Workbook()
    ws_new = wb_new.active

    # Copy the first 5 columns from the old workbook to the new workbook
    for row in ws_old.iter_rows(min_row=1, max_col=5, max_row=ws_old.max_row, values_only=True):
        ws_new.append(row)

    # Add "OK" to the sixth column in each row of the new workbook
    for row_idx in range(1, ws_new.max_row + 1):
        old_value = ws_new.cell(row=row_idx, column=5).value
        # ws_new.cell(row=row_idx, column=6).value = str(old_value) + "OK"
        img_path = os.path.join(r"C:\Users\Administrator\Desktop\very_temp\products_imgs", f"{old_value}.jpg")
        print(img_path)
        if not os.path.exists(img_path):
            print(f"not found {img_path}")
        else:
            try:
                _insert_image_into_excel(wb_new, img_path, new_excel_path, cell_reference=f'F{row_idx}', img_width=100)
                print("Insert success")
                break
            except Exception as e:
                print(e)
                break

    # Save the new workbook
    wb_new.save(new_excel_path)


folder_path = r'C:\Users\Administrator\Desktop\very_temp\temp'

output_path = r'C:\Users\Administrator\Desktop\very_temp\out_new.xlsx'
'''
