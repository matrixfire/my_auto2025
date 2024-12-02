
#####################################################################################################################
import random  # Importing the random module for generating random numbers
from PIL import Image, ImageEnhance, ImageDraw  # Importing necessary classes from the PIL library for image processing
import os  # Importing the os module for interacting with the operating system
import shutil  # Importing the shutil module for file operations
from datetime import datetime

def randomize_factor(base_factor, variability=0.2, min_value=0.8):
    """
    Generate a random factor based on a base factor and a variability range.
    Ensures that the resulting factor does not lead to white or near-white pixels.

    :param base_factor: The base factor to start with.
    :param variability: The maximum amount of random variation (+/-) to apply.
    :param min_value: Minimum value to avoid high factors that result in white or near-white.
    :return: A randomly adjusted factor.
    """
    random_adjustment = random.uniform(-variability, variability)  # Generate a random adjustment within the variability range
    factor = base_factor + random_adjustment  # Calculate the new factor by adding the adjustment to the base factor
    return max(factor, min_value)  # Ensure the factor is not below the minimum value


def change_background_color_randomly(image_path, output_path, base_red_factor=1.0, base_green_factor=1.0, base_blue_factor=1.0, base_brightness_factor=1.0, variability=0.5):
    """
    Modify the background color by adjusting the RGB channels and brightness with added randomness.
    Ensures that the image does not become white or near-white.

    :param image_path: Path to the original background image.
    :param output_path: Path where the modified image will be saved.
    :param base_red_factor: Base multiplier for the red channel (1.0 means no change).
    :param base_green_factor: Base multiplier for the green channel (1.0 means no change).
    :param base_blue_factor: Base multiplier for the blue channel (1.0 means no change).
    :param base_brightness_factor: Base multiplier for brightness (1.0 means no change).
    :param variability: The maximum amount of random variation (+/-) to apply to each factor.
    """
    red_factor = randomize_factor(base_red_factor, variability)  # Randomize the red factor
    green_factor = randomize_factor(base_green_factor, variability)  # Randomize the green factor
    blue_factor = randomize_factor(base_blue_factor, variability)  # Randomize the blue factor
    brightness_factor = randomize_factor(base_brightness_factor, variability)  # Randomize the brightness factor
    
    image = Image.open(image_path).convert("RGB")  # Open the image and convert it to RGB mode
    
    r, g, b = image.split()  # Split the image into its red, green, and blue channels
    
    r = r.point(lambda i: i * red_factor)  # Adjust the red channel
    g = g.point(lambda i: i * green_factor)  # Adjust the green channel
    b = b.point(lambda i: i * blue_factor)  # Adjust the blue channel
    
    modified_image = Image.merge("RGB", (r, g, b))  # Merge the adjusted channels back into an image
    
    if brightness_factor != 1.0:
        enhancer = ImageEnhance.Brightness(modified_image)  # Create a brightness enhancer
        modified_image = enhancer.enhance(brightness_factor)  # Adjust the brightness
    
    modified_image = ensure_no_white(modified_image)  # Ensure no white pixels in the image
    
    modified_image.save(output_path, format="PNG")  # Save the modified image


def ensure_no_white(image):
    """
    Adjust the image to ensure that no pixel is fully white or near-white.
    
    :param image: The PIL Image object to process.
    :return: The processed PIL Image object.
    """
    width, height = image.size  # Get the dimensions of the image
    pixels = image.load()  # Load the pixel data of the image
    
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]  # Get the RGB values of the pixel
            if r > 240 and g > 240 and b > 240:  # Check if the pixel is near-white
                pixels[x, y] = (r - 30, g - 30, b - 30)  # Adjust the pixel to make it less white
    
    return image  # Return the adjusted image


def copy_and_rename_images(source_paths, destination_folder, prefix="Reobrix-"):
    """
    Copy images to a destination folder and rename them with a specified prefix.
    
    :param source_paths: List of paths to the source images.
    :param destination_folder: Path to the destination folder.
    :param prefix: Prefix to be added to the new file names.
    :return: List of new file paths.
    """
    new_paths = []  # Initialize a list to store the new file paths
    
    os.makedirs(destination_folder, exist_ok=True)  # Create the destination folder if it doesn't exist
    
    for source_path in source_paths:
        original_filename = os.path.basename(source_path)  # Get the original file name
        file_name, file_extension = os.path.splitext(original_filename)  # Split the file name and extension
        
        new_filename = f"{prefix}{file_name}{file_extension}"  # Create the new file name with the prefix
        new_path = os.path.join(destination_folder, new_filename)  # Create the new file path
        
        shutil.copy2(source_path, new_path)  # Copy the file to the new path
        new_paths.append(new_path)  # Add the new path to the list
    
    return new_paths  # Return the list of new file paths


def calculate_square_frame(background_size, size_fraction=0.5, position="left"):
    """
    Calculate the size and position of the square frame based on the background size.
    
    :param background_size: Tuple of (width, height) for the background image.
    :param size_fraction: Fraction of the smaller side of the background used as the size of the square.
    :param position: Position of the square frame ("left" or "right").
    :return: Tuple containing (x, y, size) where (x, y) is the top-left corner of the square and size is the side length of the square.
    """
    bg_width, bg_height = background_size  # Get the width and height of the background
    
    smaller_side = min(bg_width, bg_height)  # Determine the smaller side of the background
    square_size = int(smaller_side * size_fraction)  # Calculate the size of the square
    margin = (bg_height - square_size) // 2  # Calculate the margin
    
    if position == "left":
        x = margin  # Set the x-coordinate for the left position
    elif position == "right":
        x = bg_width - margin - square_size  # Set the x-coordinate for the right position
    elif position == "middle":
        x = (bg_width - square_size) // 2  # Set the x-coordinate for the middle position
    else:
        raise ValueError("Invalid position argument. Use 'left' or 'right'.")  # Raise an error for invalid position
    
    y = margin  # Set the y-coordinate
    
    return (x, y, square_size)  # Return the coordinates and size of the square


def resize_and_rotate_overlay_image(overlay_image, target_size, angle):
    """
    Resize the overlay image to the target size and rotate it by a specified angle.
    
    :param overlay_image: PIL Image object for the overlay image.
    :param target_size: Tuple of (width, height) for the target size.
    :param angle: Angle to rotate the image (in degrees, counterclockwise).
    :return: Resized and rotated PIL Image object.
    """
    overlay_resized = overlay_image.resize(target_size, Image.LANCZOS)  # Resize the overlay image
    overlay_rotated = overlay_resized.rotate(angle, expand=True)  # Rotate the resized image
    
    return overlay_rotated  # Return the resized and rotated image


def overlay_images(background_path, overlay_path, output_path, scale_factor=0.8, size_fraction=0.5, position="left", angle=0, draw_border=False):
    """
    Overlay one image on top of another, with optional rotation, and save the result.
    
    :param background_path: Path to the background image.
    :param overlay_path: Path to the overlay image.
    :param output_path: Path where the resulting image will be saved.
    :param scale_factor: Fraction of the square size used to scale the overlay image.
    :param size_fraction: Fraction of the smaller side of the background used as the size of the square.
    :param position: Position of the square frame ("left" or "right").
    :param angle: Angle to rotate the overlay image (in degrees, counterclockwise).
    :param draw_border: Boolean indicating whether to draw a red border around the square frame.
    """
    background = Image.open(background_path).convert("RGBA")  # Open the background image and convert to RGBA mode
    overlay = Image.open(overlay_path).convert("RGBA")  # Open the overlay image and convert to RGBA mode
    
    bg_width, bg_height = background.size  # Get the dimensions of the background image
    
    x, y, square_size = calculate_square_frame((bg_width, bg_height), size_fraction, position)  # Calculate the square frame
    
    overlay_aspect_ratio = overlay.width / overlay.height  # Calculate the aspect ratio of the overlay image
    if overlay_aspect_ratio > 1:
        target_size = (int(square_size * scale_factor), int(square_size * scale_factor / overlay_aspect_ratio))  # Calculate target size for wide images
    else:
        target_size = (int(square_size * scale_factor * overlay_aspect_ratio), int(square_size * scale_factor))  # Calculate target size for tall images
    
    overlay_transformed = resize_and_rotate_overlay_image(overlay, target_size, angle)  # Resize and rotate the overlay image
    
    overlay_x = x + (square_size - overlay_transformed.width) // 2  # Calculate the x-coordinate for the overlay
    overlay_y = y + (square_size - overlay_transformed.height) // 2  # Calculate the y-coordinate for the overlay
    
    temp_image = Image.new("RGBA", background.size)  # Create a new temporary image with the same size as the background
    temp_image.paste(overlay_transformed, (overlay_x, overlay_y), overlay_transformed)  # Paste the transformed overlay onto the temporary image
    
    combined = Image.alpha_composite(background, temp_image)  # Combine the background and temporary images
    
    if draw_border:
        draw = ImageDraw.Draw(combined)  # Create a drawing context
        border_color = "red"  # Set the border color
        border_width = 5  # Set the border width
        draw.rectangle([x, y, x + square_size, y + square_size], outline=border_color, width=border_width)  # Draw the border
    
    combined.save(output_path, format="PNG")  # Save the combined image


# Example usage
background_image_path = "G:/x/t2/background1.png"  # Path to the background image
rand_background_image_path = "G:/x/t2/random_background.png"  # Path to save the randomly modified background image

# Apply random color adjustments
change_background_color_randomly(background_image_path, rand_background_image_path, base_red_factor=1, base_green_factor=1, base_blue_factor=1, base_brightness_factor=1.1, variability=0.3)

overlay_image_path1 = r"G:\产品图\22011\PNG\1.png"
overlay_image_path2 = r"G:\产品图\22011\尺寸图\2.jpg"

destination_folder = "G:/x/t2/"  # Path to the destination folder

intermediate_image_path = os.path.join(destination_folder, "intermediate_image.png")  # Path for the intermediate image

current_date = datetime.now().strftime("%m-%d")
final_output_image_path = os.path.join(destination_folder, f"Reobrix-{current_date}-{random.randint(1, 100)}.png")  # Final output path

new_image_paths = copy_and_rename_images([overlay_image_path1, overlay_image_path2], destination_folder)  # Copy and rename the overlay images

# First overlay operation (left side)
overlay_images(rand_background_image_path, overlay_image_path1, intermediate_image_path, scale_factor=0.8, size_fraction=0.8, position="left", angle=0, draw_border=False)

# Second overlay operation (right side) on the intermediate image
overlay_images(intermediate_image_path, overlay_image_path2, final_output_image_path, scale_factor=0.8, size_fraction=0.6, position="right", angle=0, draw_border=False)






















from PIL import Image

def add_logo(background_path, logo_path, output_path, position="top-left", size_fraction=0.2, margin_fraction=0.05):
    """
    Add a logo to the background image at one of the four corners.
    
    :param background_path: Path to the background image.
    :param logo_path: Path to the logo image.
    :param output_path: Path where the final image will be saved.
    :param position: Corner position for the logo ("top-left", "top-right", "bottom-left", "bottom-right").
    :param size_fraction: The fraction of the smaller side of the background that the logo should occupy.
    :param margin_fraction: The fraction of the smaller side used as a margin from the border.
    """
    # Load the background and logo images
    background = Image.open(background_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    
    # Get background dimensions
    bg_width, bg_height = background.size
    smaller_side = min(bg_width, bg_height)
    
    # Resize logo to occupy the specified fraction of the smaller side
    logo_size = int(smaller_side * size_fraction)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    
    # Calculate margin
    margin = int(smaller_side * margin_fraction)
    
    # Determine logo position
    if position == "top-left":
        x = margin
        y = margin
    elif position == "top-right":
        x = bg_width - logo_size - margin
        y = margin
    elif position == "bottom-left":
        x = margin
        y = bg_height - logo_size - margin
    elif position == "bottom-right":
        x = bg_width - logo_size - margin
        y = bg_height - logo_size - margin
    else:
        raise ValueError("Invalid position: choose from 'top-left', 'top-right', 'bottom-left', 'bottom-right'")
    
    # Paste the logo onto the background
    background.paste(logo, (x, y), logo)
    
    # Save the final image
    background.save(output_path, format="PNG")

# Example usage
background_image_path =r"G:\x\t2\新产品\微信图片_20240926174546.jpg"
logo_image_path = "G:/x/logo.png"
output_image_path = r"C:\Users\Administrator\Desktop\with_logo.png"

# Add the logo to the top-left corner by default
add_logo(background_image_path, logo_image_path, output_image_path, position="top-left", size_fraction=0.1)

# Add the logo to the bottom-right corner
# add_logo(background_image_path, logo_image_path, output_image_path, position="top-left", size_fraction=0.1)









