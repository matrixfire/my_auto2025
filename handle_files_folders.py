'''
About 
READING AND WRITING FILES
ORGANIZING FILES


'''


import os
import zipfile
import shutil
import pyperclip



def correct_names(directory):
    """
    Recursively corrects both file and folder names within the specified directory.

    Parameters:
        directory (str): The path to the directory to correct names in.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(root, file, sep='\nxxxxx\n')
            try:
                os.rename(*fix_characts(root, file))
            except Exception as e:
                print(f'{e}')
                
        for folder in dirs:
            print(root,folder, sep='\nxxxxx\n')
            try:
                os.rename(*fix_characts(root, folder))
            except Exception as e:
                print(f'{e}')


def fix_characts(root, file_name):
    old_name  = os.path.join(root, file_name)
    try:
        new_name = os.path.join(root, file_name.encode('cp437').decode('gbk'))
    except Exception as e:
        print(e)
        new_name = old_name
    return old_name, new_name





def process_zip_files(folder_path, include_string):
    # unfolder all zip files, and extract the folder including some string seperately!
    # Get the list of zip files in the specified folder
    zip_files = [f for f in os.listdir(folder_path) if f.endswith('.zip')]
    print(zip_files)
    # Process each zip file
    for zip_file in zip_files:
        # Create a folder name based on the zip file name
        unzip_folder = os.path.join(folder_path, os.path.splitext(zip_file)[0])

        # Unzip the contents
        with zipfile.ZipFile(os.path.join(folder_path, zip_file), 'r') as zip_ref:
            try:
                zip_ref.extractall(unzip_folder)
            except Exception as e:
                print(f'\n{zip_file} unzipping...error: \n{e}\n')
        # Correct file names if applicable
        for root, dirs, files in os.walk(folder_path, topdown=False):
            correct_names(root)
            


        # Find subfolders containing the include string
        matching_subfolders = [subfolder for subfolder in os.listdir(unzip_folder) if include_string in subfolder]


        # Create a new folder to move matching subfolders' content
        new_folder = os.path.join(folder_path, f"{os.path.splitext(zip_file)[0]}({include_string})")
        os.makedirs(new_folder, exist_ok=True)

        # Move content of matching subfolders to the new folder
        for matching_subfolder in matching_subfolders:
            source_path = os.path.join(unzip_folder, matching_subfolder)
            destination_path = new_folder
            for root, dirs, files in os.walk(source_path):
                for name in files + dirs:
                    shutil.move(os.path.join(root, name), os.path.join(destination_path, name))

        # Remove the original zip file
        os.remove(os.path.join(folder_path, zip_file))

        # Remove the unzipped folder
        shutil.rmtree(unzip_folder)
        print(f'{zip_file} finished.')




def rename_empty_folders(path):
    """
    Renames empty folders in the given path by appending '(empty)' to their names.
    
    Parameters:
        path (str): The path to check for empty folders.
    """
    for foldername, subfolders, filenames in os.walk(path):
        if not subfolders and not filenames:  # If the folder is empty
            new_name = os.path.join(os.path.dirname(foldername), "(empty) " + os.path.basename(foldername))
            shutil.move(foldername, new_name)
            print(f"Renamed '{foldername}' to '{new_name}'")




def pds(path, indent='', structure=''):
    """
    Prints the directory structure starting from the given path.
    """
    if os.path.isdir(path):
        structure += indent + os.path.basename(path) + '/\n'
        for item in sorted(os.listdir(path)):
            structure = pds(os.path.join(path, item), indent + '  ', structure)
    else:
        structure += indent + os.path.basename(path) + '\n'
    return structure

# - To read contents of a ZIP file in Python, create a `ZipFile` object using `zipfile.ZipFile()` function.
# - This object acts similarly to a `File` object returned by `open()`.
# - Use `ZipFile` object's `namelist()` method to get a list of all files and folders in the ZIP.
# - Obtain individual file information using `getinfo()` method, returning a `ZipInfo` object.
# - `ZipInfo` object provides attributes like `file_size` and `compress_size`, representing original and compressed sizes.
# - Calculate compression ratio with `original file size / compressed file size`.
# os.path.abspath('.'), os.listdir('.'), os.path.join(, ),  os.path.basename()




def organize_folders(folder_path, final_folder="organized_files"):
    organize_folders_path = os.path.join(folder_path, final_folder)
    os.makedirs(organize_folders_path)
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if not os.path.isdir(subfolder_path):
            continue
        for subfolder in os.listdir(subfolder_path):
            subfolder_path = os.path.join(subfolder_path, subfolder)
            shutil.move(subfolder_path, organize_folders_path)
            print(f'Moved {subfolder_path} -> {organize_folders_path}')
            


def organize_folders(folder_path, final_folder="organized_files"):
    organize_folders_path = os.path.join(folder_path, final_folder)
    os.makedirs(organize_folders_path, exist_ok=True)  # Create final folder if it doesn't exist

    # Move files directly within folder_path to final_folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            shutil.move(item_path, organize_folders_path)
            print(f'Moved {item_path} -> {organize_folders_path}')

    # Move files within subfolders to final_folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            shutil.move(file_path, organize_folders_path)
            print(f'Moved {file_path} -> {organize_folders_path}')

# Example usage:
organize_folders('/path/to/your/folder')



if __name__ == "__main__":
    # Specify the folder path and include string
    # folder_path = input("Enter the folder path: ")
    # include_string = input("Enter the include string: ")
    folder_path = r'C:\Users\34950\Desktop\full_time_work\temp\ttttt'
    include_string = '高清' # 高清
    # Call the function
    process_zip_files(folder_path, include_string)
    # backupToZip(r'C:\Users\34950\Desktop\full_time_work\myauto\33028详情页')





# Summary:
# - `os.unlink(path)`: Deletes a file.
# - `os.rmdir(path)`: Deletes an empty folder.
# - `shutil.rmtree(path)`: Deletes a folder and all its contents.
# - `send2trash`: Sends files and folders to the computer's trash/recycle bin, offering a safer deletion option.
# Absolute vs. Relative Paths:  The .\ at the start of a relative path is optional. For example, .\spam.txt and spam.txt refer to the same file; dot this directory, dot-dot the parent folder.
# os.makedirs()； Path(r'C:\Users\Al\spam').mkdir() Note that mkdir() can only make one directory at a time; it won’t make several subdirectories at once like os.makedirs().
# os.path.abspath(); os.path.isabs(); os.path.relpath(, )
# os.path.split() is the same as (os.path.dirname(), os.path.basename())
# os.path.getsize(); os.listdir()
# list(some_path_obj.glob('*.?x?'); both os.listdir(p) or p.glob('*') does the same.
# p.exists(); p.is_file(); p.is_dir()
    

def walk(path):
    import os
    for folderName, subfolders, filenames in os.walk(path):
        print('The current folder is ' + folderName)
        for subfolder in subfolders:
            print('SUBFOLDER OF ' + folderName + ': ' + subfolder)
        for filename in filenames:
            print('FILE INSIDE ' + folderName + ': '+ filename)
        print("\n"*3)



import os
import shutil
import random
def move_contents_to_result_folder(path, result_folder):
    # Walk through the directory tree rooted at 'path'
    for root, dirs, files in os.walk(path):
        # Get the relative path from the source folder, skipping the first level
        relative_path = os.path.relpath(root, path)
        relative_path = relative_path.split(os.path.sep, 1)[-1]

        # Construct the destination folder path
        dest_folder = os.path.join(result_folder, relative_path)

        # Create the destination folder if it doesn't exist
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        # Move files to the destination folder while preserving the directory structure
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_folder, file)
            try:
                shutil.move(src_file, dest_file)
            except Exception as e:
                dest_file = os.path.join(dest_folder, f'({str(random.random())})' + file)
                print(e, "renamed")
            print(f"Move {src_file} -> {dest_file}")



def copy_jpg_images(source_folder, result_folder):
    # Create the result folder if it doesn't exist
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # Walk through the directory tree rooted at 'source_folder'
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith('.jpg'):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(result_folder, file)

                # If a file with the same name exists in the result folder, rename it
                if os.path.exists(dest_file):
                    base_name, extension = os.path.splitext(file)
                    new_file_name = f"{base_name} (copied){extension}"
                    dest_file = os.path.join(result_folder, new_file_name)

                # Copy the file to the result folder
                shutil.copy(src_file, dest_file)



'''

import shelve

# Saving variables to a binary shelf file
def save_data():
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    with shelve.open('data.shelf') as shelf_file:
        shelf_file['data'] = data

# Restoring data from the binary shelf file
def load_data():
    with shelve.open('data.shelf') as shelf_file:
        data = shelf_file.get('data', {})
        print("Loaded data:", data)

        
def save_data():
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    with open('data.py', 'w') as file:
        file.write("variable = " + pprint.pformat(data))

def load_data():
    import data
    print("Loaded data:", data.variable)
        
# Save data to shelf file
save_data()

# Load data from shelf file
load_data()



'''


import random as r
def c(choices_list=["work", "learn"], weight_list=[30, 10]):
    what_2_do = r.choice(choices_list)
    index = choices_list.index(what_2_do)
    time_2_do = r.randint(weight_list[index]//2, weight_list[index])
    print(f'I decide to {what_2_do.title()} for {time_2_do} mins.')

# c()
    
import os
f = lambda input_path: [folder for folder in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, folder))] # dirs names
f2 = lambda input_path: [folder for folder in os.listdir(input_path)] # dirs and files names

g = lambda input_path: [os.path.join(input_path, folder) for folder in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, folder))] # dirs paths
g2 = lambda input_path: [os.path.join(input_path, folder) for folder in os.listdir(input_path)] # dirs and files path names

lt2 = list(map(lambda x: reg.search(x).group() if reg.search(x) else "none", lt))

b = list(filter(lambda x: "xxx" in x, g2(r'C:\Users\Administrator\Desktop\very_temp')))
















import re
import random

def change_file_name_(input_path):
    import random
    path_without_extension, extension = os.path.splitext(input_path)

    dirname = os.path.dirname(input_path)
    basename = os.path.basename(input_path)
    # new_base = f'({random.randint(1000, 9999)})'+ basename
    # new_path = os.path.join(dirname, new_base)
    new_path = path_without_extension+'(1)' + extension
    return new_path


def change_file_name(input_path):
    path_without_extension, extension = os.path.splitext(input_path)
    counter = 1  # Start with 1 as we'll be appending this to the filename if it exists.
    new_path = input_path  # Start with the original path
    # Keep incrementing the counter and updating the filename until we find one that doesn't exist.
    while os.path.exists(new_path):
        new_path = f"{path_without_extension}({counter}){extension}"
        counter += 1
    return new_path




def copy_first_images(input_path, output_folder):
    sku_regex = re.compile(r'\d+[a-zA-Z]?')
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    # Get all subfolders within the input path
    subfolders = [folder for folder in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, folder))]
    for folder in subfolders:
        # Join subfolder with relative path "主图\2000X2667"
        subfolder_path = os.path.join(input_path, folder, "主图", "750X1000")
        sku_mo = sku_regex.search(folder)
        if sku_mo:
            sku = sku_mo.group()
        else:
            sku = f"sku-unknown-{random.randint(100,999)}"
        # Print the joined path for verification
        print("Joined path:", subfolder_path)
        # Check if the joined path exists
        if os.path.exists(subfolder_path):
            # Get all files in the joined path
            files = os.listdir(subfolder_path)            
            # Filter out only image files (assuming images have extensions like .jpg, .png, etc.)
            image_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
            # If there are image files in the folder, copy the first image to the output folder
            if image_files:
                # Get the path of the first image file
                first_image_path = os.path.join(subfolder_path, image_files[0])
                _, extension = os.path.splitext(first_image_path)
                # Copy the first image file to the output folder
                shutil.copy(first_image_path, output_folder)
                print(f'copied file {first_image_path} to folder {output_folder}.')
                moved_file_name = os.path.basename(first_image_path)
                moved_file_path = os.path.join(output_folder, moved_file_name)
                # new_file_name = f'({sku}){moved_file_name}'
                new_file_name = f'{sku}'+ extension
                new_file_path = os.path.join(os.path.dirname(moved_file_path), new_file_name)
                try:
                    os.rename(moved_file_path, new_file_path)
                except FileExistsError:
                    new_file_path = change_file_name(new_file_path)
                    print(f'auto renaming to {new_file_path}.')
                    os.rename(moved_file_path, new_file_path)
                print("Copied", image_files[0], "to", new_file_path)
            else:
                print("No image files found in", subfolder_path)
        else:
            print("*******************Path does not exist:*******************\n", subfolder_path)



from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def sort_key(filename):
    # Split the filename by '_' and get the part after it, then remove the '.jpg' and convert to integer
    # return int(filename.split('-')[-1].split('.')[0])
    return int(filename.split('.')[0].split('(')[-1].rstrip(")"))

def jpg_to_pdf(folder_path, output_pdf):
    # Get list of all jpg files in the folder
    jpg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.jpeg')]
    # jpg_files.sort()  # Ensure the files are in the correct order
    # jpg_files = sorted(jpg_files, key=sort_key)
    
    # Create a canvas object for the PDF
    pdf = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter

    for jpg_file in jpg_files:
        img_path = os.path.join(folder_path, jpg_file)
        img = Image.open(img_path)
        img_width, img_height = img.size

        # Calculate the scaling factor to fit the image on the PDF page
        scale = min(width / img_width, height / img_height)
        img_width *= scale
        img_height *= scale

        # Center the image on the page
        x = (width - img_width) / 2
        y = (height - img_height) / 2

        # Draw the image on the PDF page
        pdf.drawImage(img_path, x, y, img_width, img_height)
        pdf.showPage()  # Add a new page for the next image

    pdf.save()
    print(f"PDF created successfully: {output_pdf}")



import pytesseract
from PIL import Image

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

def main(folder_path):
    import os
    import pyperclip as p
    all_text = ""
    g2 = lambda input_path: [os.path.join(input_path, folder) for folder in os.listdir(input_path)] # dirs and files path names
    def remove_empty_lines(text):
        lines = text.split('\n')
        non_empty_lines = filter(lambda line: line.strip(), lines)
        return '\n'.join(non_empty_lines)
    file_path_lt = g2(folder_path)
    for file_path in file_path_lt:
        all_text += (ocr(file_path) + '\n')
        print(f"{file_path} extracted.")
    result = remove_empty_lines(all_text)
    p.copy(result)
    print(result)

    
import os

def rename_path(old_path, new_name, keep_filename_suffix=False):
    try:
        # Check if new_name is a path or just a name
        if os.path.isabs(new_name):
            new_path = new_name
        else:
            # Split the path into directory and base name
            directory, base_name = os.path.split(old_path)
            
            if keep_filename_suffix:
                # Keep the old filename's suffix
                file_name, file_ext = os.path.splitext(base_name)
                new_base_name = f"{new_name}{file_ext}"
            else:
                new_base_name = new_name
            
            new_path = os.path.join(directory, new_base_name)
        
        # Check if the new path already exists
        if os.path.exists(new_path):
            # If it does, find a new name by adding a counter in parentheses
            counter = 1
            while True:
                new_base_name, new_ext = os.path.splitext(new_base_name)
                new_base_name = f"{new_base_name}({counter}){new_ext}"
                new_path = os.path.join(directory, new_base_name)
                if not os.path.exists(new_path):
                    break
                counter += 1
        
        # Rename the path
        os.rename(old_path, new_path)
        
        # Print the success message
        print(f"Success in renaming {os.path.basename(old_path)} to {os.path.basename(new_path)}")
        print(f"Old path: {old_path}")
        print(f"New path: {new_path}")
    except FileNotFoundError:
        print("Error: File or directory not found")
    except Exception as e:
        print(f"Error: {e}")

import re
sku_re = re.compile(r"\d+")



from PIL import Image
im = Image.open('captcha.jpg')
gray = im.convert('L')
gray.show()
gray.save("captcha_gray.jpg")

threshold = 150
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
out = gray.point(table, '1')
out.show()
out.save("captcha_thresholded.jpg")


import os
f = lambda input_path: [folder for folder in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, folder))] # dirs names
f2 = lambda input_path: [folder for folder in os.listdir(input_path)] # dirs and files names

g = lambda input_path: [os.path.join(input_path, folder) for folder in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, folder))] # dirs paths
g2 = lambda input_path: [os.path.join(input_path, folder) for folder in os.listdir(input_path)] # dirs and files path names

folders = g(r"C:\Users\Administrator\Desktop\work2024\产品视频\2024_05_13_66038 英文版")

for sub_folder_path in folders:
    new = sku_regex.search(os.path.basename(sub_folder_path))
    if not new:
        print(f"No sku for this folder: {os.path.basename(sub_folder_path)}")
        continue
    else:
        new_name = new.group()
        rn(sub_folder_path, new_name)
