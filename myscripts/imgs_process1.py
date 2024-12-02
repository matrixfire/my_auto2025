from PIL import Image
import os

# Define the default directory
DEFAULT_DIR = r"C:\Users\Administrator\Desktop\temp_img\ttt"

def create_background_image(width, height, color=(35, 35, 35), output_filename="background.png", gradient=False):
    """
    Creates a solid or slightly gradient color background image and saves it to the specified directory.

    Parameters:
    - width (int): The width of the image in pixels.
    - height (int): The height of the image in pixels.
    - color (tuple): A tuple representing the RGB color (default is (35, 35, 35)).
    - output_filename (str): The name of the file where the image will be saved.
    - gradient (bool): If True, applies a slight gradient effect to the image.
    """
    # Validate color
    if not all(0 <= c <= 255 for c in color):
        raise ValueError("Color values must be between 0 and 255.")
    
    # Create a new image with the given width and height
    image = Image.new('RGB', (width, height))
    
    if gradient:
        # Create a gradient effect
        for y in range(height):
            for x in range(width):
                # Apply a gradient based on the x position
                gradient_color = (
                    color[0] + int((x / width) * 20) % 256,
                    color[1] + int((y / height) * 20) % 256,
                    color[2] + int(((x + y) / (width + height)) * 20) % 256
                )
                image.putpixel((x, y), gradient_color)
    else:
        # Fill the image with the solid color
        for x in range(width):
            for y in range(height):
                image.putpixel((x, y), color)
    
    # Save the image to the specified directory
    output_path = os.path.join(DEFAULT_DIR, output_filename)
    image.save(output_path)
    print(f"Image saved as {output_path}")

# Example usage
create_background_image(800, 600, gradient=True)




def merge_and_save_images_corrected_lt_whole(base_image_path, second_image_path_lt, factor=0.7):
    """
    Resizes each image in `second_image_path_lt` to a height that is `factor` percent of the base image's height,
    ensuring all images are the same size. Each image's width-to-height ratio must be within 10% of 3/4. 
    Images are pasted side by side, with equal spacing from the base image's borders. The final image 
    is saved as a new file with "updated_" prefixed to the original base image file name.

    Parameters:
    - base_image_path (str): Path to the base image.
    - second_image_path_lt (list of str): List of paths to images to be resized and merged.
    - factor (float): The height factor for resizing the second images relative to the base image height.
    """
    from PIL import Image
    import os

    # Open the base image
    with Image.open(base_image_path) as base_img:
        base_width, base_height = base_img.size
        print(f"Base image size: {base_img.size}")

        # Calculate the resize height for all images
        resize_height = int(base_height * factor)
        
        # Initialize variables for pasting images
        total_width = 0
        images_resized = []
        valid_ratios = True

        # Process each image in the list
        for second_image_path in second_image_path_lt:
            with Image.open(second_image_path) as second_img:
                ratio = second_img.width / second_img.height
                
                # Check if the image ratio is within the acceptable range
                if not (0.675 <= ratio <= 0.825):
                    print(f"Image {second_image_path} ratio {ratio:.2f} is out of the acceptable range.")
                    valid_ratios = False
                    continue

                # Calculate the width to resize the image to maintain the correct height
                resize_width = int(resize_height * second_img.width / second_img.height)
                second_img_resized = second_img.resize((resize_width, resize_height))
                images_resized.append(second_img_resized)
                total_width += resize_width

        # If any image had an invalid ratio, exit the function
        if not valid_ratios:
            return
        
        # Calculate the starting x position for centering images
        spacing = (base_width - total_width) // 2
        
        # Paste the resized images side by side
        current_x = spacing
        for img in images_resized:
            base_img.paste(img, (current_x, (base_height - resize_height) // 2))
            current_x += img.width

        # Save the modified image as a new file
        new_base_image_path = os.path.join(os.path.dirname(base_image_path), "updated_" + os.path.basename(base_image_path))
        base_img.save(new_base_image_path)
        print(f"Modified image saved as {new_base_image_path}")
