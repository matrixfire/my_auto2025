

##########################################################################

# COMPRESS

import fitz  # PyMuPDF
from pathlib import Path

def compress_pdf(input_path, output_path, dpi_reduction=150):
    """
    Compress a PDF by reducing the resolution of images.

    Args:
        input_path (str or Path): Path to the input PDF.
        output_path (str or Path): Path to save the compressed PDF.
        dpi_reduction (int): DPI to scale images (default is 150).
    """
    try:
        input_pdf = fitz.open(input_path)
        output_pdf = fitz.open()  # New compressed PDF

        for page_num in range(input_pdf.page_count):
            page = input_pdf.load_page(page_num)
            
            # Create a new page in the output PDF with the same dimensions
            new_page = output_pdf.new_page(width=page.rect.width, height=page.rect.height)

            # Render the page as an image with reduced DPI
            pix = page.get_pixmap(dpi=dpi_reduction)
            
            # Create a rectangle matching the size of the original page
            rect = fitz.Rect(0, 0, page.rect.width, page.rect.height)
            
            # Insert the rendered image back into the new page
            new_page.insert_image(rect, pixmap=pix)

        # Save the compressed PDF
        output_pdf.save(output_path, deflate=True)  # Enable compression
        print(f"Compressed PDF saved at: {output_path}")

    except Exception as e:
        print(f"Error during compression: {e}")

    finally:
        input_pdf.close()
        output_pdf.close()


if __name__ == "__main__":
    # Input and output paths
    input_file = Path(r"G:\books\parts\interleaved_output_with_labels.pdf")
    output_file = Path(r"G:\books\parts\interleaved_output_with_labels_compressed.pdf")
    
    # Call the compression function
    compress_pdf(input_file, output_file)



##########################################################################

import fitz  # PyMuPDF
import pyinputplus as pyip
import os


def extract_pages_p_better(pdf_path, start_page, end_page, output_path=None):
    # Open the original PDF
    pdf_document = fitz.open(pdf_path)

    # Check if the page numbers are within the range
    num_pages = pdf_document.page_count
    if start_page < 1 or end_page > num_pages or start_page > end_page:
        print(f"Invalid page range. The PDF has {num_pages} pages.")
        return

    # Create a new PDF to save the extracted pages
    new_pdf_document = fitz.open()

    # Extract pages from start_page to end_page (inclusive)
    for page_num in range(start_page - 1, end_page):
        new_pdf_document.insert_pdf(pdf_document, from_page=page_num, to_page=page_num, links=False, annots=False)

    # Determine the output path
    if output_path is None:
        base_name, ext = os.path.splitext(pdf_path)
        output_path = f"{base_name}({start_page}-{end_page}){ext}"

    # Save the new PDF
    new_pdf_document.save(output_path)
    new_pdf_document.close()
    pdf_document.close()

    print(f"Extracted pages {start_page} to {end_page} and saved to '{output_path}'.")



def extract_pages_p(pdf_path, start_page, end_page, output_path=None):
    # Open the original PDF
    pdf_document = fitz.open(pdf_path)

    # Check if the page numbers are within the range
    num_pages = pdf_document.page_count
    if start_page < 1 or end_page > num_pages or start_page > end_page:
        print(f"Invalid page range. The PDF has {num_pages} pages.")
        return

    # Create a new PDF to save the extracted pages
    new_pdf_document = fitz.open()

    # Extract pages from start_page to end_page (inclusive)
    for page_num in range(start_page - 1, end_page):
        page = pdf_document.load_page(page_num)
        new_pdf_document.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

    # Determine the output path
    if output_path is None:
        base_name, ext = os.path.splitext(pdf_path)
        output_path = f"{base_name}({start_page}-{end_page}){ext}"

    # Save the new PDF
    new_pdf_document.save(output_path)
    new_pdf_document.close()
    pdf_document.close()

    print(f"Extracted pages {start_page} to {end_page} and saved to '{output_path}'.")

def extract():
    # Prompting for input using pyinputplus
    pdf_path = input("Enter the path for PDF: ").strip().strip('"')
    start_page = pyip.inputInt(prompt="Enter the start page number: ", min=1)

    # Open the PDF document to get the total number of pages
    pdf_document = fitz.open(pdf_path)
    num_pages = pdf_document.page_count
    pdf_document.close()

    # Ask for end page, allowing for empty input
    end_page_input = input("Enter the end page number (leave blank for last page): ").strip()
    end_page = num_pages if end_page_input == "" else int(end_page_input)

    # Call the function with the specified page range
    extract_pages_p(pdf_path, start_page, end_page)

extract()


##########################################################################



##########################################################################


import fitz  # PyMuPDF
from pathlib import Path

def interleaving_combine_pdfs_with_circles(dir_path, output_file_name):
    # Step 1: Ask how many PDFs the user wants to combine
    num_pdfs = int(input("Enter the number of PDFs to combine: "))
    
    if num_pdfs < 2:
        print("You need at least 2 PDFs to perform interleaving.")
        return
    
    # Step 2: Collect paths for all PDFs
    pdf_paths = []
    for i in range(num_pdfs):
        pdf_path = input(f"Enter the path for PDF {i+1}: ").strip().strip('"')  # Remove quotes and spaces
        if not Path(pdf_path).is_file():
            print(f"File not found: {pdf_path}")
            return
        pdf_paths.append(pdf_path)
    
    # Step 3: Open all PDFs
    pdfs = []
    try:
        pdfs = [fitz.open(path) for path in pdf_paths]
    except Exception as e:
        print(f"Error opening PDFs: {e}")
        return
    
    # Step 4: Create a new PDF for the combined result
    output_pdf = fitz.open()

    # Step 5: Get the maximum page count across all PDFs
    max_pages = max(pdf.page_count for pdf in pdfs)

    # Step 6: Define colors for the circles (more colors can be added here)
    colors = [
        (1, 0, 0),   # Red
        (0, 0, 1),   # Blue
        (0, 1, 0),   # Green
        (1, 1, 0),   # Yellow
        (1, 0, 1),   # Magenta
        (0, 1, 1)    # Cyan
    ]

    # Step 7: Interleave pages from all PDFs with circles
    for page_num in range(max_pages):
        for i, pdf in enumerate(pdfs):
            if page_num < pdf.page_count:
                # Insert the page from the current PDF
                output_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)
                # Add a colored circle, alternating based on the PDF number
                page = output_pdf[-1]  # Get the last added page
                draw_colored_circle(page, colors[i % len(colors)])  # Alternate through the colors

    # Step 8: Save the combined PDF output path
    # output_file_name = "interleaved_output_with_circles.pdf"
    output_file_path = Path(dir_path, output_file_name)
    try:
        output_pdf.save(output_file_path)
        print(f"PDFs have been successfully interleaved with colored circles. The combined file is saved at:\n{output_file_path}")
    except Exception as e:
        print(f"Error saving the output PDF: {e}")
    finally:
        output_pdf.close()

    # Close the individual PDFs
    for pdf in pdfs:
        pdf.close()

# Helper function to draw a small circle at the top-left corner of a PDF page
def draw_colored_circle(page, color):
    # Define circle position and size
    circle_center = (30, 30)  # Coordinates near the top-left corner
    circle_radius = 10        # Radius of the circle
    
    # Create a circle using the draw_circle method
    page.draw_circle(center=circle_center, radius=circle_radius, color=color, fill=color)

# Call the function to combine PDFs with colored circles
if __name__ == "__main__":
    interleaving_combine_pdfs_with_circles(Path(r"G:\books\parts"), "interleaved_output_with_circles.pdf")




##########################################################################

import fitz  # PyMuPDF
import os

def interleave_pdfs_with_grouped_pages():
    # Step 1: Ask how many PDFs the user wants to combine
    num_pdfs = int(input("Enter the number of PDFs to combine: "))
    
    if num_pdfs < 2:
        print("You need at least 2 PDFs to perform interleaving.")
        return
    
    # Step 2: Collect paths and page group sizes for all PDFs
    pdf_paths = []
    pages_per_pdf = []
    
    for i in range(num_pdfs):
        pdf_path = input(f"Enter the path for PDF {i+1}: ").strip().strip('"')  # Remove quotes and spaces
        pdf_paths.append(pdf_path)
        
        # Ask for the number of pages to treat as a group for the current PDF
        pages_group = input(f"Enter the number of pages to treat as a group for PDF {i+1} (default is 1): ")
        pages_per_pdf.append(int(pages_group) if pages_group.isdigit() else 1)

    # Step 3: Open all PDFs
    pdfs = [fitz.open(path) for path in pdf_paths]
    
    # Step 4: Create a new PDF for the combined result
    output_pdf = fitz.open()

    # Step 5: Interleave pages from all PDFs with circles
    max_pages = max(pdf.page_count for pdf in pdfs)

    # Step 6: Define colors for the circles
    colors = [
        (1, 0, 0),   # Red
        (0, 0, 1),   # Blue
        (0, 1, 0),   # Green
        (1, 1, 0),   # Yellow
        (1, 0, 1),   # Magenta
        (0, 1, 1)    # Cyan
    ]

    # Step 7: Interleave pages from all PDFs with circles
    for page_num in range(max_pages):
        for i, (pdf, group_size) in enumerate(zip(pdfs, pages_per_pdf)):
            for j in range(group_size):
                if page_num * group_size + j < pdf.page_count:
                    # Insert the page from the current PDF
                    output_pdf.insert_pdf(pdf, from_page=page_num * group_size + j, to_page=page_num * group_size + j)
                    # Add a colored circle
                    page = output_pdf[-1]  # Get the last added page
                    draw_colored_circle(page, colors[i % len(colors)])  # Alternate through the colors

    # Step 8: Save the combined PDF output path
    output_file_name = "interleaved_output_with_circles.pdf"
    output_file_path = os.path.abspath(output_file_name)
    output_pdf.save(output_file_path)
    output_pdf.close()
    
    # Close the individual PDFs
    for pdf in pdfs:
        pdf.close()

    # Step 9: Print the absolute path of the combined output PDF
    print(f"PDFs have been successfully interleaved with colored circles. The combined file is saved at:\n{output_file_path}")

# Helper function to draw a small circle at the top-left corner of a PDF page
def draw_colored_circle(page, color):
    # Define circle position and size
    circle_center = (30, 30)  # Coordinates near the top-left corner
    circle_radius = 10        # Radius of the circle
    
    # Create a circle using the draw_circle method
    page.draw_circle(center=circle_center, radius=circle_radius, color=color, fill=color)


interleave_pdfs_with_grouped_pages()

#################################################




############################ interleaving learning


output_folder = r"G:\temp"


# 1, Making the interleaving pdf
import fitz  # PyMuPDF
import os

def interleave_pdfs_with_grouped_pages(pdf_specs, output_folder, output_filename):
    if len(pdf_specs) < 2:
        print("You need at least 2 PDFs to perform interleaving.")
        return
    
    # Step 1: Collect paths, labels, and page group sizes for all PDFs from the provided list
    pdf_paths = []
    labels = []
    pages_per_pdf = []
    
    for pdf_path, label, group_size in pdf_specs:
        pdf_paths.append(pdf_path)
        if label == '_':
            labels.append(os.path.basename(pdf_path))
        elif label == '':
            labels.append('')
        else:
            labels.append(label)
            
        # labels.append(label if label else os.path.basename(pdf_path))
        pages_per_pdf.append(group_size if group_size else 1)

    # Step 2: Open all PDFs
    pdfs = [fitz.open(path) for path in pdf_paths]
    
    # Step 3: Determine the common page size (using the largest width and height)
    max_width = 0
    max_height = 0
    for pdf in pdfs:
        for page in pdf:
            rect = page.rect
            max_width = max(max_width, rect.width)
            max_height = max(max_height, rect.height)

    # Step 4: Create a new PDF for the combined result
    output_pdf = fitz.open()

    # Step 5: Define colors for the labels
    colors = [
        (1, 0, 0),   # Red
        (0, 0, 1),   # Blue
        (0, 1, 0),   # Green
        (1, 0, 1),   # Magenta
        (0, 1, 1)    # Cyan
    ]

    # Step 6: Interleave pages from all PDFs with labels
    max_pages = max(pdf.page_count for pdf in pdfs)
    common_rect = fitz.Rect(0, 0, max_width, max_height)
    
    for page_num in range(max_pages):
        for i, (pdf, group_size, label) in enumerate(zip(pdfs, pages_per_pdf, labels)):
            for j in range(group_size):
                original_page_num = page_num * group_size + j
                if original_page_num < pdf.page_count:
                    page = pdf[original_page_num]
                    # Use show_pdf_page to insert and scale the content directly
                    new_page = output_pdf.new_page(width=max_width, height=max_height)
                    transformation = fitz.Matrix(
                        max_width / page.rect.width,
                        max_height / page.rect.height
                    )
                    new_page.show_pdf_page(common_rect, pdf, original_page_num, transformation)
                    
                    # Add the label with the page indicator and color
                    label_with_page = f"{label} ({original_page_num + 1})" if label else ""
                    label_color = colors[i % len(colors)]
                    write_page_label(new_page, label_with_page, label_color)

    # Step 7: Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, output_filename)
    
    # Save the combined PDF
    output_pdf.save(output_file_path)
    output_pdf.close()
    
    # Close the individual PDFs
    for pdf in pdfs:
        pdf.close()

    # Step 8: Print the absolute path of the combined output PDF
    print(f"PDFs have been successfully interleaved with labels. The combined file is saved at:\n{output_file_path}")

# Helper function to write a label on a PDF page with a specified color
def write_page_label(page, label, color):
    # Define text position and appearance
    text_position = (30, 34)  # Coordinates near the top-left corner
    font_size = 10  # Font size for the label
    page.insert_text(text_position, label, fontsize=font_size, color=color)

# Example usage


# Define the list of PDFs with paths, labels, and group sizes
pdf_specs = [
    (r"G:\books\X_1113_redact(161-596).pdf", "", 3),
    (r"G:\books\X1_1218.pdf", "_", 1),
    
    # (r"C:\Users\Administrator\Downloads\python_ai.pdf", "", 3),
    # (r"G:\books\1210t\Z-Math for Deep Learning What You Need to Know to Understand Neural Networks.pdf", "", 2),



]


output_folder=r"G:\books"
output_filename = "X_1113_redact(161-596)_2.pdf"

interleave_pdfs_with_grouped_pages(pdf_specs, output_folder, output_filename)




# 2， Creating the plan based on the pages




from datetime import datetime, timedelta
import pyperclip

# Constants for total pages
ORIGINAL_PAGES = 1020  # Original book pages
DAYS_LEARN = 180  # Total days for learning
review_intervals = [0, 1, 2, 4, 8, 16, 32, 64, 128]

ADDITIONAL_PAGES = 0  # Additional content


# Calculate the total number of pages
total_pages = ORIGINAL_PAGES + ADDITIONAL_PAGES
pages_per_day = total_pages // DAYS_LEARN

# Start page should be the page after the additional content
start_page = ADDITIONAL_PAGES + 1

# Calculate the total parts to be read (each part = pages_per_day)
book_parts = total_pages // pages_per_day
if total_pages % pages_per_day != 0:  # Account for any leftover pages
    book_parts += 1

# Define the spaced repetition intervals (in days)


# Function to generate the reading and review schedule
def generate_reading_and_review_schedule():
    # Today's date (start date)
    start_date = datetime.now()

    # Create a list to store the review days for each part
    review_schedule = {}

    # Generate the reading and review schedule for each part of the book
    for part in range(1, book_parts + 1):
        part_name = f"part {part}"  # Part name without page numbers

        # Add today's part to the review schedule
        review_schedule[part_name] = {
            'read_date': start_date + timedelta(days=part - 1),
            'reviews': []
        }

        # Calculate the review days for this part
        for interval in review_intervals:
            review_date = start_date + timedelta(days=part - 1 + interval)
            review_schedule[part_name]['reviews'].append({
                'interval': interval,
                'review_date': review_date
            })
    
    # Now generate the daily reading and review outputs
    output = []
    for day in range(1, DAYS_LEARN + 1):
        # Current part for the day
        current_part = f"(Part-{day})"
        output.append(f"Day {day}: {current_part}")

        # List all reviews due on this day
        for part_name, part_info in review_schedule.items():
            for review in part_info['reviews']:
                if review['review_date'].date() == (start_date + timedelta(days=day - 1)).date():
                    output.append(f"  Spaced repetition for {part_name} (it's been {review['interval']} days)")
    
    # Join all output lines
    return "\n".join(output)

# Generate the reading and review schedule
schedule = generate_reading_and_review_schedule()

# Print the result to the console
print(schedule)

# Copy the result to clipboard
pyperclip.copy(schedule)
print("\nThe schedule has been copied to the clipboard.")


# 3, Create the plan pdf from clipboard 


import fitz  # PyMuPDF
import pyperclip
import os

def create_pdf_from_clipboard(output_pdf_path):
    # Get clipboard content using pyperclip
    clipboard_text = pyperclip.paste()

    # Create a new PDF document
    pdf = fitz.open()

    # Page settings
    page_width = 595  # A4 width in points (210mm)
    page_height = 842  # A4 height in points (297mm)
    font_size = 12
    margin = 40  # Margin around the page
    text_position = (margin, margin)  # Starting position for the text

    # Page layout settings
    line_height = font_size * 1.4  # Adjust line height based on font size
    max_lines_per_page = (page_height - 2 * margin) // line_height  # Max lines per page considering margins

    # Split the clipboard content into lines
    lines = clipboard_text.split("\n")

    current_page = pdf.new_page(width=page_width, height=page_height)
    y_position = margin  # Start at the top of the page

    # Add text line by line
    for line in lines:
        if y_position + line_height > page_height - margin:  # If space is not enough, start a new page
            current_page = pdf.new_page(width=page_width, height=page_height)
            y_position = margin  # Reset the vertical position for the new page

        current_page.insert_text((text_position[0], y_position), line, fontsize=font_size)
        y_position += line_height  # Move to the next line

    # Save the PDF to the specified path
    pdf.save(output_pdf_path)
    pdf.close()

    print(f"PDF created successfully: {output_pdf_path}")


output_folder = r"G:\temp"
# Example usage:
output_filename = 'plans.pdf'
output_file_path = os.path.join(output_folder, output_filename)
create_pdf_from_clipboard(output_file_path)





# 4， do the resize if need

import fitz  # PyMuPDF

def resize_pdf_to_match(input_pdf, reference_pdf, output_pdf):
    # Open the reference PDF and get the size of the first page
    ref_doc = fitz.open(reference_pdf)
    ref_page_size = ref_doc[0].rect  # The size of the first page in the reference PDF
    ref_width = ref_page_size.width
    ref_height = ref_page_size.height
    ref_doc.close()  # Close the reference PDF

    # Open the input PDF
    input_doc = fitz.open(input_pdf)
    output_doc = fitz.open()  # Create a new PDF for the output

    for page in input_doc:
        # Create a new blank page with the reference size
        new_page = output_doc.new_page(width=ref_width, height=ref_height)
        
        # Scale and add the content of the input page to the new page
        scale_matrix = fitz.Matrix(
            ref_width / page.rect.width,
            ref_height / page.rect.height
        )
        new_page.show_pdf_page(new_page.rect, input_doc, page.number, scale_matrix)

    # Save the resized PDF to the output path
    output_doc.save(output_pdf)
    output_doc.close()
    input_doc.close()

    print(f"PDF resized successfully and saved to: {output_pdf}")

# Example usage
input_pdf = r"G:\temp\X2_1218.pdf"
reference_pdf = r"G:\temp\plans.pdf"
output_pdf = r"G:\temp\X2_1218__.pdf"

resize_pdf_to_match(input_pdf, reference_pdf, output_pdf)






# 5，Label the pdf


import fitz  # PyMuPDF


# Input and output file paths
input_pdf_path = r"G:\temp\X2_1218__.pdf"
output_pdf_path = r"G:\temp\X2_1218_2.pdf"



# Constants
ORIGINAL_PAGES = 1020  # Original book pages
ADDITIONAL_PAGES = 0  # Additional content is zero
DAYS_LEARN = 180  # Total days for learning

# Calculate total pages and pages per day
total_pages = ORIGINAL_PAGES + ADDITIONAL_PAGES
pages_per_day = total_pages // DAYS_LEARN
remainder_pages = total_pages % DAYS_LEARN

# Ensure at least one page is distributed per day
if pages_per_day <= 0:
    raise ValueError("Pages per day must be greater than 0. Check your inputs.")

# Print the calculated values
print(f"Total Pages: {total_pages}")
print(f"Pages per Day: {pages_per_day}")
print(f"Remainder Pages: {remainder_pages}")

# Open the input PDF
pdf = fitz.open(input_pdf_path)

# Loop through each page and add labels at the top-right corner
current_page = 0  # Track current page in the PDF

for day_num in range(1, DAYS_LEARN + 1):
    # Calculate how many pages to assign this day (handle remainder pages)
    if day_num <= remainder_pages:
        pages_today = pages_per_day + 1  # For the first 'remainder_pages' days, add one extra page
    else:
        pages_today = pages_per_day

    # Loop through the pages for the current day
    for _ in range(pages_today):
        if current_page < total_pages:
            page = pdf[current_page]
            part_number = day_num
            label_text = f"Part-{part_number}"

            # Get page dimensions
            rect = page.rect  # Page dimensions
            margin = 20  # Distance from the top-right corner

            # Calculate position for the label
            text_position = (rect.width - margin - 50, margin)  # Adjust -50 for text width

            # Define text properties
            font_size = 12
            color = (0, 0, 0)  # Black color

            # Add the label text to the page
            page.insert_text(text_position, label_text, fontsize=font_size, color=color)

            # Move to the next page
            current_page += 1

# Save the modified PDF
pdf.save(output_pdf_path)
pdf.close()

print(f"Labeled PDF saved to: {output_pdf_path}")








# 6, conbines multiple pdfs

import fitz  # PyMuPDF
import os

def combine_pdfs(pdf_paths, output_folder, output_filename):
    # Step 1: Create a new PDF where the combined result will be saved
    output_pdf = fitz.open()

    # Step 2: Loop through each PDF and append its pages to the output PDF
    for pdf_path in pdf_paths:
        pdf_document = fitz.open(pdf_path)  # Open the current PDF
        for page_num in range(pdf_document.page_count):
            output_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        pdf_document.close()

    # Step 3: Ensure the output folder exists, create it if not
    os.makedirs(output_folder, exist_ok=True)

    # Step 4: Define the combined PDF output path
    output_file_path = os.path.join(output_folder, output_filename)
    
    # Step 5: Save the combined PDF
    output_pdf.save(output_file_path)
    output_pdf.close()

    # Step 6: Print the absolute path of the combined output PDF
    print(f"PDFs have been successfully combined. The combined file is saved at:\n{output_file_path}")

# Example usage
pdf_paths = [
    r"G:\books\X_1113_redact(1-160).pdf",
    r"G:\books\X_1113_redact(161-596)_2.pdf",
]
output_folder = r"G:\books"
output_filename = "X_1113_v2"

# Call the function to combine PDFs
combine_pdfs(pdf_paths, output_folder, output_filename)

















import fitz  # PyMuPDF
import os
from pathlib import Path

def combine_pdfs(dir_path):
    # Step 1: Ask how many PDFs the user wants to combine
    num_pdfs = int(input("How many PDFs do you want to combine? "))
    
    # Step 2: Collect paths for each PDF
    pdf_paths = []
    for i in range(num_pdfs):
        pdf_path = input(f"Enter the path for PDF {i+1}: ").strip().strip('"')  # Remove quotes and spaces
        pdf_paths.append(pdf_path)
    
    # Step 3: Create a new PDF where the combined result will be saved
    output_pdf = fitz.open()

    # Step 4: Loop through each PDF and append its pages to the output PDF
    for pdf_path in pdf_paths:
        pdf_document = fitz.open(pdf_path)  # Open the current PDF
        for page_num in range(pdf_document.page_count):
            output_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        pdf_document.close()
    
    # Step 5: Define and save the combined PDF output path
    output_file_name = "combined_output.pdf"
    output_file_path = Path(dir_path, output_file_name)
    output_pdf.save(output_file_path)
    output_pdf.close()

    # Step 6: Print the absolute path of the combined output PDF
    print(f"PDFs have been successfully combined. The combined file is saved at:\n{output_file_path}")

# Call the function to combine PDFs
dir_path = Path(r"G:\books\1210t")
combine_pdfs(dir_path)

















##########################################################################

import fitz
import os

def combine_all_pdfs_in_directory(directory, output_filename):
    """
    Combine all PDF files in a given directory into a single PDF.

    Parameters:
        directory (str): The directory containing the PDF files to combine.
        output_filename (str): The name of the output combined PDF file.

    Returns:
        str: The full path to the combined PDF file.
    """
    # Ensure directory exists
    if not os.path.exists(directory):
        raise ValueError(f"The directory {directory} does not exist.")
    
    # Get a sorted list of all PDF files in the directory
    pdf_list = sorted([os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.pdf')])
    
    if not pdf_list:
        raise ValueError(f"No PDF files found in the directory {directory}.")
    
    # Full path for the output PDF
    output_pdf_path = os.path.join(directory, output_filename)
    
    # Create a new PDF document
    combined_pdf = fitz.open()
    
    # Iterate over each PDF in the list and add its pages to the combined PDF
    for pdf_file in pdf_list:
        with fitz.open(pdf_file) as pdf:
            for page_num in range(pdf.page_count):
                combined_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)
    
    # Save the combined PDF
    combined_pdf.save(output_pdf_path)
    combined_pdf.close()
    
    print(f"Combined PDF saved as: {output_pdf_path}")
    return output_pdf_path

# Example usage:
directory_path = r'G:\全部PPT'
output_filename = 'combined_output.pdf'
combined_pdf_path = combine_all_pdfs_in_directory(directory_path, output_filename)





##########################################################################













import fitz  # PyMuPDF
import os

def images_to_pdf(images_path, output_pdf_path):
    # Create a new PDF document
    pdf_document = fitz.open()

    # List all image files in the directory
    image_files = [f for f in os.listdir(images_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'))]
    image_files.sort()  # Optional: sort files by name to ensure order

    if not image_files:
        print("No images found in the directory.")
        return

    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        # Open the image file
        img_document = fitz.open(image_path)
        # Get the first page of the image document
        img_page = img_document.load_page(0)
        # Create a new PDF page with the same dimensions as the image
        pdf_page = pdf_document.new_page(width=img_page.rect.width, height=img_page.rect.height)
        # Insert the image into the PDF page
        pdf_page.insert_image(pdf_page.rect, filename=image_path)
        img_document.close()

    # Save the PDF
    pdf_document.save(output_pdf_path)
    pdf_document.close()

    print(f"Combined images into PDF and saved to '{output_pdf_path}'.")

if __name__ == "__main__":
    # Get paths from user input.
    images_path = input("Enter the path for images: ").strip().strip('"')
    output_pdf_path = input("Enter the path for the output PDF: ").strip().strip('"')

    images_to_pdf(images_path, os.path.join(output_pdf_path, "combined_images.pdf"))
















# important , final working version of removing chinese characters from pdf

import fitz  # PyMuPDF

def clean_pdf(input_pdf, output_pdf, remove_text):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf)

    # Loop through each page in the PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)

        # Search for the unwanted text and remove it
        text_instances = page.search_for(remove_text)

        for inst in text_instances:
            # Remove the found instances of the unwanted text by adding a redaction annotation
            page.add_redact_annot(inst)
        page.apply_redactions()  # Apply the redactions

    # Save the cleaned PDF with optimization and no incremental flag
    pdf_document.save(output_pdf, deflate=True)  # Deflate option for optimization

    print(f"Cleaned PDF saved as: {output_pdf}")

# Input and output PDF paths
input_pdf = r"C:\Users\recur\Desktop\django5 book.pdf"
output_pdf = r"C:\Users\recur\Desktop\cleaned_django5_book.pdf"

# Chinese characters to remove
remove_text = "最新资料最新资料"

# Call the function to clean the PDF
clean_pdf(input_pdf, output_pdf, remove_text)

