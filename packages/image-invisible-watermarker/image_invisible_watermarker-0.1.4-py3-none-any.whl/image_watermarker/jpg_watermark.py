import piexif, io
from PIL import Image

def add_watermark_jpeg(image_bytes, watermark_text):
    """
    Adds a watermark to a JPEG image by embedding the watermark text into the EXIF metadata.

    Args:
        image_bytes (bytes or str): The byte stream of the JPEG image data or the file path.
        watermark_text (str): The watermark text to be embedded.

    Returns:
         bytes: The modified byte stream of the JPEG image with the watermark.
    """
    try:
        # If a file path is provided, read the bytes from file
        if isinstance(image_bytes, str):
            with open(image_bytes, "rb") as f:
                image_bytes = f.read()

        # Load image from bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Check if EXIF data exists; if not, create an empty EXIF dictionary
        try:
            exif_dict = piexif.load(image.info['exif'])
        except KeyError:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}

        # Ensure "0th" dictionary is present, then add watermark text
        exif_dict["0th"][piexif.ImageIFD.Artist] = watermark_text.encode()  # Encode text as bytes

        # Save image with new metadata to bytes
        exif_bytes = piexif.dump(exif_dict)
        output_bytes = io.BytesIO()
        image.save(output_bytes, format='JPEG', exif=exif_bytes)
        output_bytes.seek(0)
        return output_bytes.getvalue()
    except Exception as e:
        print(f"An error occurred while adding watermark: {e}")
        return e


def check_watermark_jpeg(image_bytes, watermark_text):
    """
    Checks if a JPEG image contains the specified watermark text in its EXIF metadata.

    Args:
        image_bytes (bytes): The byte stream of the JPEG image data.
        watermark_text (str): The expected watermark text.

    Returns:
        bool: True if the watermark is found, False otherwise.
    """
    try:
        # If a file path is provided, read the bytes from file
        if isinstance(image_bytes, str):
            with open(image_bytes, "rb") as f:
                image_bytes = f.read()

        # Load image from bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Attempt to extract EXIF metadata; if missing, return False
        try:
            exif_data = piexif.load(image.info['exif'])
        except KeyError:
            return False  # No EXIF data means no watermark

        # Extract and decode watermark text
        stored_watermark = exif_data.get("0th", {}).get(piexif.ImageIFD.Artist, b"").decode()
        return stored_watermark == watermark_text, stored_watermark
    except Exception as e:
        print(f"An error occurred while checking watermark: {e}")
        return e