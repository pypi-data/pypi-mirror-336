# filepath: c:\Users\wel\Documents\Portfolio\image_watermarking\image_watermarker\image_watermarker\avif_watermark.py
import os

def add_watermark_avif_heic_heif(file_bytes, watermark_text):
    """
    Adds a watermark to an AVIF image by appending the watermark text to the file bytes.
    """
    try:
        # If file_bytes is a file path or not already bytes, convert it to bytes
        if isinstance(file_bytes, str):
            if not os.path.exists(file_bytes):
                print(f"File {file_bytes} does not exist.")
                return None
            with open(file_bytes, "rb") as f:
                file_bytes = f.read()
        elif not isinstance(file_bytes, bytes):
            file_bytes = str(file_bytes).encode("utf-8")

        if not file_bytes:
            print("The input file appears to be empty.")
            return None

        # Create a custom watermark in bytes.
        watermark_marker = b"WM_START"
        watermark_bytes = watermark_marker + watermark_text.encode("utf-8") + b"WM_END"

        # Append the watermark to the file bytes
        modified_bytes = file_bytes + watermark_bytes

        # Optionally, print byte lengths for debugging
        print(f"Original file size: {len(file_bytes)} bytes")
        print(f"Watermark size: {len(watermark_bytes)} bytes")
        print(f"Modified file size: {len(modified_bytes)} bytes")

        return modified_bytes
    except Exception as e:
        print(f"Error adding watermark: {e}")
        return None

def extract_watermark_avif_heic_heif(file_bytes, watermark_text):
    """
    Extracts a watermark from an AVIF image by searching for the watermark text in the file bytes.

    Args:
        file_bytes (bytes): The byte stream of the AVIF image data.

    Returns:
        str or None: The extracted watermark text if found, otherwise None.
    """
    try:

        # If file_bytes is a file path, read the bytes first
        if isinstance(file_bytes, str):
            with open(file_bytes, "rb") as f:
                file_bytes = f.read()

        # Look for the watermark markers
        start_marker = b"WM_START"
        end_marker = b"WM_END"
        start_index = file_bytes.find(start_marker)
        end_index = file_bytes.find(end_marker)

        if start_index != -1 and end_index != -1:
            start_index += len(start_marker)
            watermark = file_bytes[start_index:end_index].decode("utf-8")

            return watermark == watermark_text, watermark
        else:
            print("No watermark found.")
            return None
    except Exception as e:
        print(f"Error verifying watermark: {e}")
        return e