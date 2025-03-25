from PIL import Image
import numpy as np
import io

from image_watermarker.utilities import text_to_binary, binary_to_text

def add_watermark_png(image, watermark_text):
    """
    Adds a watermark to a PNG image by embedding the watermark text into the alpha channel's LSB.

    Args:
        image (bytes, Image, or str): The image data (either bytes, Image object, or file path).
        watermark_text (str): The watermark text to be embedded.
        output_path (str, optional): The path to save the watermarked image.

    Returns:
        bytes or None: The modified byte stream of the PNG image with the watermark or None if output_path is provided.
    """
    try:
        # Open the image if a file path is provided
        if isinstance(image, str):
            image = Image.open(image)
        elif isinstance(image, bytes):
            image = Image.open(io.BytesIO(image))

        # Convert image to RGBA to access alpha channel
        image = image.convert('RGBA')
        img_array = np.array(image)

        # Convert watermark text to binary
        watermark_binary = text_to_binary(watermark_text)
        binary_index = 0
        height, width = img_array.shape[:2]

        # Embed binary watermark into the alpha channel
        for y in range(height):
            for x in range(width):
                if binary_index < len(watermark_binary):
                    # Modify the LSB of the alpha channel to store the watermark bit
                    alpha_pixel = img_array[y, x, 3]
                    lsb_bit = int(watermark_binary[binary_index])
                    img_array[y, x, 3] = (alpha_pixel & 0xFE) | lsb_bit
                    binary_index += 1
                else:
                    break
            if binary_index >= len(watermark_binary):
                break

        # Save or return image with watermark in alpha channel
        watermarked_img = Image.fromarray(img_array, 'RGBA')
        output_bytes = io.BytesIO()
        watermarked_img.save(output_bytes, format="PNG")
        return output_bytes.getvalue()
    except Exception as e:
        print(f"An error occurred: {e}")
        return e

def check_watermark_png(image, watermark_text):
    """Check if the watermark text is embedded in the alpha channel."""
    try:
        # Convert bytes to an Image if necessary
        if isinstance(image, str):
            image = Image.open(image)
        elif isinstance(image, bytes):
            image = Image.open(io.BytesIO(image))

        # Ensure the image is in RGBA format to access the alpha channel
        img_array = np.array(image.convert('RGBA'))

        watermark_binary = text_to_binary(watermark_text)
        extracted_binary = ''

        height, width = img_array.shape[:2]
        binary_index = 0

        for y in range(height):
            for x in range(width):
                if binary_index < len(watermark_binary):
                    # Extract LSB from the alpha channel
                    lsb_value = img_array[y, x, 3] & 1
                    extracted_binary += str(lsb_value)
                    binary_index += 1
                else:
                    break
            if binary_index >= len(watermark_binary):
                break

        extracted_text = binary_to_text(extracted_binary)
        return extracted_text == watermark_text, extracted_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return e