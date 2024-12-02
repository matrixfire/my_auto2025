import csv

def modify_csv(input_file, data_list, output_file):
    # Read the existing CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        header = reader.fieldnames

        # Prepare data for writing
        rows_to_write = []
        for data_dict in data_list:
            # Ensure the keys in data_dict match the header
            row = {key: data_dict.get(key, '') for key in header}
            rows_to_write.append(row)
        print(rows_to_write)
    # Write to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=header)
        
        # Write the header
        writer.writeheader()

        # Write the rows from the provided data_list
        writer.writerows(rows_to_write)


def read_from_csv(input_file, fieldnames):
    result_data = []
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        for row in reader:
            filtered_row = {key: row[key] for key in fieldnames if key in row}
            result_data.append(filtered_row)
    return result_data

model_id=''
pcs_num=''
dimension=''
tmp = f'''
<p data-mce-fragment="1"><span data-mce-fragment="1">Item : Reobrix {model_id}</span></p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Number of Pieces : {pcs_num} <br></span></p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Dimensions(L x W x H) : {dimension} CM</span></p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Package Type: Carton (w</span>ithout original box)</p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Include instruction book, Miniatur Guns and Weapons included,<br data-mce-fragment="1"></span></p>
<p data-mce-fragment="1"><strong data-mce-fragment="1">Note: <span style="color: #ff2a00;">The Mini Figures are <span style="text-decoration: underline;">NOT INCLUDED</span> in this Set !</span></strong></p>
'''


def read_from_csv_customize(input_file, fieldnames=['货号', '品名', '尺寸', '单价', '零件数量']):
    result_data = []
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            filtered_row = {key: row[key] for key in fieldnames if key in row}
            model_id = filtered_row['货号']
            pcs_num = filtered_row['零件数量']
            dimension = filtered_row['尺寸']
            tmp = f'''
<p data-mce-fragment="1"><span data-mce-fragment="1">Item : Reobrix {model_id}</span></p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Number of Pieces : {pcs_num} <br></span></p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Dimensions(L x W x H) : {dimension} CM</span></p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Package Type: Carton (w</span>ithout original box)</p>
<p data-mce-fragment="1"><span data-mce-fragment="1">Include instruction book, Miniatur Guns and Weapons included,<br data-mce-fragment="1"></span></p>
<p data-mce-fragment="1"><strong data-mce-fragment="1">Note: <span style="color: #ff2a00;">The Mini Figures are <span style="text-decoration: underline;">NOT INCLUDED</span> in this Set !</span></strong></p>
'''
            new_data_dict = {}
            new_data_dict['Handle'] = 'reobrix-' + str(filtered_row['货号']) + '-' + filtered_row['品名']
            new_data_dict['Title'] = 'Reobrix ' +  filtered_row['品名'].title()
            new_data_dict['Variant SKU'] = str(filtered_row['货号'])
            new_data_dict['Variant Price'] = str(filtered_row['单价'])
            new_data_dict['Body (HTML)'] = tmp
            result_data.append(new_data_dict)
    return result_data

# Example usage:
existing_csv_file = 'products_data - 副本.csv'
# desired_fieldnames = ['货号', '品名', '尺寸', '单价']

data_read = read_from_csv_customize(existing_csv_file)
print(data_read)



# # Example usage:
# existing_csv_file = 'exampleWithHeader.csv'
# data_to_append = [
#     {'Fruit': 'Value1', 'Quantity': 'Value2'},
#     {'Fruit': 'ValueA', 'Quantity': 'ValueB'},

#     # Add more dictionaries as needed
# ]
# new_csv_file = 'exampleWithHeader_n.csv'

existing_csv_file = 'product_template.csv'
data_to_append = data_read


# how to prepare data_to_append
# Handle
# Title
# Body (HTML)
# Variant SKU
# Variant Price

def read_from_csv(input_file, fieldnames):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        # header = reader.fieldnames



new_csv_file = 'new_' + existing_csv_file

modify_csv(existing_csv_file, data_to_append, new_csv_file)
