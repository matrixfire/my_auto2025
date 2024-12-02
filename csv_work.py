import csv
from pathlib import Path
import os
import re
import json



def bitch():
    '''author Bill Zou'''
    d = "divde and conquer" # 分而治之
    e = "begin with the end in mind" # 以始为终
    f = "framework" # 要有框架
    b = "backward thinking" # 逆向思维
    i = "intersections" # 寻找交集
    t = "tools" # 使用工具
    c = "core" # 找到问题核心
    h = "higer vision" # 更高的视角和维度看问题







def t(text):
    import re
    # Regex pattern for matching the year and month
    pattern = r'(\d{4})年(\d{1,2})月'
    match = re.search(pattern, text)
    if match:
        return f'{match.group(1)}/{match.group(2)}/1'  # Year and month



def extract_numbers_2_clipboard(alist):
    import re
    import pyperclip as p
    num_obj = re.compile(r'.*?(\d*).*?')
    alist_nums = [num_obj.search(i).group(0) for i in alist]
    print(len(alist_nums), alist_nums, sep="\n")
    p.copy('\n'.join(alist_nums).strip())


def extract_numbers(text):
    # Define regex pattern to match numbers with or without decimals
    pattern = r'\b\d+(?:\.\d+)?\b'
    # Use findall to extract all matching numbers from the text
    numbers = re.findall(pattern, text)
    return numbers

def get_largest_num(numbers):
    if not numbers:
        return 0
    else:
        nums = [float(i) for i in numbers]
        return max(nums)





def temp_price(num_str):
    e = 7.1
    num = float(num_str)
    if num <= 25.8:
        return 25.8*5/e
    elif num < 100:
        return num*5/e
    elif 100 <= num <= 300:
        return num*4.5/e
    elif 300 < num <= 600:
        return num*4/e
    else:
        return num*3.5/e


def tp(num_str):
    import pyperclip
    e = 7.1
    num = float(num_str)
    result = None
    if num <= 25.8:
        result = round(25.8*5/e, 2)
    elif num < 100:
        result = round(num*5/e, 2)
    elif 100 <= num <= 300:
        result = round(num*4.5/e, 2)
    elif 300 < num <= 600:
        result = round(num*4/e, 2)
    else:
        result = round(num*3.5/e, 2)
    pyperclip.copy(str(result))
    return result

# 1, getting data from my own cache csv products data, and generate the data list 
import csv

tmp = '''
<p data-mce-fragment="1"><span data-mce-fragment="1">Item : Reobrix {model_id}</span></p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Number of Pieces : {pcs_num} <br></span></p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Dimensions(L x W x H) : {dimension} CM</span></p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Package Type: Original packaging included (color box)</p>
'''

def read_from_csv_customize(input_file, fieldnames=['货号', '品名', '尺寸', '单价', '零件数量', '类型']):
    '''
    read from my customized csv file, namely my own cache file!
    '''
    result_data = []
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            filtered_row = {key: row[key] for key in fieldnames if key in row}
            model_id = filtered_row['货号']
            pcs_num = filtered_row['零件数量']
            dimension = filtered_row['尺寸']
            product_name = filtered_row['品名']
            price = filtered_row['单价']
            product_type = filtered_row['类型']
            
            new_data_dict = {}
            new_data_dict['Handle'] = 'reobrix-' + model_id + '-' + product_name
            new_data_dict['Title'] = 'Reobrix ' +  product_name.title()
            new_data_dict['Variant SKU'] = model_id
            new_data_dict['Variant Price'] = price
            new_data_dict['Body (HTML)'] = tmp.format(model_id=model_id, pcs_num=pcs_num, dimension=dimension)
            new_data_dict['Tags'] = product_type
            
            result_data.append(new_data_dict)
    return result_data


# 2, based on data and template to generate the preparing uploading file
def modify_csv(input_file, data_list, output_file=''):
    # Read the existing CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        header = reader.fieldnames # getting headers in a list

        # Prepare data for writing
        rows_to_write = []
        for data_dict in data_list: # data_list is a list of dictionaries
            # Ensure the keys in data_dict match the header
            row = {key: data_dict.get(key, '') for key in header}
            row["Status"] = "active"
            row["Variant Inventory Policy"] = "deny"
            row["Variant Fulfillment Service"] = "manual"
            rows_to_write.append(row)
        print(rows_to_write)
    if not output_file:
        dir, old_fn = os.path.split(input_file)
        output_file = os.path.join(dir,"data_populated_"+old_fn)
    # Write to a new CSV file
    with open(output_file, 'a', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=header)
        
        # Write the header
        writer.writeheader()

        # Write the rows from the provided data_list
        writer.writerows(rows_to_write)
        print(f'Filed saved at {output_file}.')




cus_csv = r'C:\Users\34950\Desktop\full_time_work\products_list3.csv' # this is my customized template

data_to_append = read_from_csv_customize(cus_csv)


existing_csv_file = r'C:\Users\34950\Desktop\full_time_work\product_template.csv' # this is offical template, but only to get the format


modify_csv(existing_csv_file, data_to_append)






path = Path(r'C:\Users\34950\Desktop\full_time_work\myauto') / 'data.json'
my_dict = json.loads(path.read_text())

def sanitize_file_name(file_name):
    invalid_chars = '\\/:*?"<>|'
    found = False
    new_file_name = file_name
    for char in invalid_chars:
        if char in file_name:
            new_file_name = new_file_name.replace(char, ' ')
            found = True
    if found:
        print(f"Sanitize name {file_name}->{new_file_name}")
    return new_file_name


def rename_images_in_folders(path, mapping_dict):
    import random
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        if os.path.isdir(folder_path):
            # Use regex to extract leading digits from the folder name
            match = re.match(r'^(\d+)', folder_name)
            if match:
                leading_digits = match.group(1)
                key = leading_digits
                # Check if the key exists in the dictionary
                if key in mapping_dict:
                    value = mapping_dict[key]
                    # Iterate through files in the folder and its subfolders
                    for root, dirs, files in os.walk(folder_path):
                        for filename in files:
                            file_path = os.path.join(root, filename)
                            # Check if the file is an image (jpg or png)
                            if filename.lower().endswith(('.jpg', '.png')):
                                # Create the new filename by appending the value and "-"
                                new_filename =sanitize_file_name(f"{value.strip().title()}-{filename}") # -{filename} {random.randint(1000, 9999)}
                                new_file_path = os.path.join(root, new_filename)
                                # Rename the file
                                try:
                                    os.rename(file_path, new_file_path)
                                except Exception as e:
                                    print(f'\nError for {file_path}: {e}')


rename_images_in_folders(r'C:\Users\34950\Desktop\full_time_work\temp\imgs13', my_dict)

'''

from pynput.keyboard import Key, Listener

def on_press(key):
    try:
        print(f'Alphanumeric key {key.char} pressed')
    except AttributeError:
        print(f'Special key {key} pressed')

def on_release(key):
    print(f'Key {key} released')
    # Stop listener
    if key == Key.esc:
        return False

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
'''