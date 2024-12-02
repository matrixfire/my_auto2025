import shelve
import pyperclip
import sys
import csv
import os
import lorem
import datetime
import json

# Determine the directory of the script
script_dir = os.path.dirname(__file__)
# Set the directory for the database and CSV files
data_dir = os.path.join(script_dir, 'mcb')
# Create the directory if it does not exist
os.makedirs(data_dir, exist_ok=True)

# Adjust the filename for shelve to include the directory path
shelve_filename = os.path.join(data_dir, 'mcb')

# Open a shelve file to store the data
my_shelf = shelve.open(shelve_filename)

# Markdown template for key-value pairs
MARKDOWN_TEMPLATE = """
**<span style="color:red">Key:</span>**
{key}<br>
**<span style="color:green">Value:</span>**
{value}


---
"""

# Function to export data to a CSV file
def export_to_csv(filename):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['key', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in my_shelf.keys():
            writer.writerow({'key': key, 'value': my_shelf[key]})

# Function to import data from a CSV file
def import_from_csv(filename):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, newline='') as csvfile, shelve.open(shelve_filename) as my_shelf:
        reader = csv.DictReader(csvfile)
        for row in reader:
            my_shelf[row['key']] = row['value']

# Function to display help information
def display_help():
    help_text = """
    Multi-Clipboard Script Usage:
    -----------------------------
    -save <keyword> [-m "message"] : Save the current clipboard content under the specified keyword.
                                    Optionally, add a brief usage message.
    -save+ <keyword>               : Append the current clipboard content to the specified keyword's content
                                    with three empty lines in between.
    -delete <keyword>              : Delete the content associated with the specified keyword.
    -delete                        : Prompt for keyword if not specified.
    -list                          : List all saved key-value pairs and copy them to the clipboard.
    -list -k                       : List all saved keys one per line and copy them to the clipboard.
    -export <filename.csv>         : Export all saved data to the specified CSV file (default: mydata.csv).
    -import <filename.csv>         : Import data from the specified CSV file (default: mydata.csv).
    -flush                         : Clear all data from the shelve database.
    -json                          : Convert all key-value pairs to a formatted JSON string and copy to clipboard.
    <keyword>                      : Retrieve the content associated with the specified keyword and copy it to the clipboard.
    -lorem1                        : Copy a lorem ipsum sentence to the clipboard.
    -lorem2                        : Copy a lorem ipsum paragraph to the clipboard.
    -git ["message"]               : Generate and copy Git commands to the clipboard.
                                     If no message is provided, use the current date as the commit message.
    -help                          : Display this help information and copy it to the clipboard.
    """
    print(help_text)
    pyperclip.copy(help_text)

# Get the length of the command line arguments
arg_len = len(sys.argv)

# Process command-line arguments
if arg_len >= 2:
    action = sys.argv[1].lower()
    if action == '-save':
        if arg_len >= 3:
            keyword = sys.argv[2]
            value = pyperclip.paste()
            if arg_len >= 5 and sys.argv[3] == '-m':
                # Append the message to the value
                message = sys.argv[4]
                value += f"\n***Bill Super Clipboard-{message}***"
            my_shelf[keyword] = value
        else:
            print("Keyword not specified.")
    elif action == '-save+':
        if arg_len >= 3:
            keyword = sys.argv[2]
            new_value = pyperclip.paste()
            if keyword in my_shelf:
                old_value = my_shelf[keyword]
                combined_value = f"{old_value}\n\n\n{new_value}"
            else:
                combined_value = new_value
            my_shelf[keyword] = combined_value
        else:
            print("Keyword not specified.")
    elif action == '-delete':
        # Delete a specific keyword from the shelve database
        keyword = sys.argv[2] if arg_len == 3 else None
        if keyword and keyword in my_shelf:
            del my_shelf[keyword]
        elif not keyword:
            print("Keyword for deletion not specified.")
    elif action == '-list':
        if arg_len == 3 and sys.argv[2] == '-k':
            # List all keys one per line and copy to clipboard
            print("List all keys one per line and copy to clipboard")
            formatted_keys = "\n".join(
                f"{key}: {my_shelf[key].split('***Bill Super Clipboard-')[-1].rstrip('***')}" if '***Bill Super Clipboard-' in my_shelf[key] else key
                for key in my_shelf.keys()
            )
            pyperclip.copy(formatted_keys)
            print(formatted_keys)
        else:
            # List all key-value pairs using the Markdown template and copy to clipboard
            print("List all key-value pairs and copy to clipboard")
            formatted_list = "\n".join(MARKDOWN_TEMPLATE.format(key=key, value=my_shelf[key]) for key in my_shelf.keys())
            pyperclip.copy(formatted_list)
            print(formatted_list)
    elif action == '-export':
        # Export the shelve database to a CSV file
        print("Export the shelve database to a CSV file")
        filename = sys.argv[2] if arg_len == 3 else 'mydata.csv'
        export_to_csv(filename)
    elif action == '-import':
        # Import data from a CSV file into the shelve database
        print("Import data from a CSV file into the shelve database")
        filename = sys.argv[2] if arg_len == 3 else 'mydata.csv'
        import_from_csv(filename)
    elif action == '-flush':
        # Clear all data from the shelve database
        print("Clear all data from the shelve database")
        my_shelf.clear()
        print("All data cleared from the shelve.")
    elif action == '-help':
        # Display help information and copy it to the clipboard
        display_help()
    elif action == '-lorem1':
        pyperclip.copy(lorem.sentence().title())
    elif action == '-lorem2':
        pyperclip.copy(lorem.paragraph())
    elif action == '-git':
        if arg_len == 3:
            message = sys.argv[2].strip('"')
        else:
            message = datetime.datetime.now().strftime("%B %d, %Y, %I:%M %p")
        git_commands = f'git add .\ngit commit -m "{message}"\ngit push'
        pyperclip.copy(git_commands)
        print(git_commands)
    elif action == '-json':
        # Convert all key-value pairs to a formatted JSON string and copy to clipboard
        data_dict = {key: my_shelf[key] for key in my_shelf.keys()}
        json_string = json.dumps(data_dict, indent=4)
        pyperclip.copy(json_string)
        print("JSON string copied to clipboard")
    else:
        # Retrieve and paste a value from the shelve database by keyword
        if action in my_shelf:
            content = my_shelf[action]
            # Replace any content within curly braces {{}} with the current clipboard content
            if '{{' in content and '}}' in content and "dj_note" not in action:
                content_to_paste = pyperclip.paste()
                content = content.replace(content[content.find('{{'):content.find('}}')+len('}}')], content_to_paste)
            # Remove the brief usage message before copying to clipboard
            if "***Bill Super Clipboard-" in content:
                content = content.split("\n***Bill Super Clipboard-")[0]
            pyperclip.copy(content.strip().strip("\""))

# Always close the shelve file
my_shelf.close()
