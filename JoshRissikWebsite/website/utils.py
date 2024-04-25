from werkzeug.utils import secure_filename
import os

def format_price(price):
    if isinstance(price, (int, float)):
        return "{:,.0f}".format(price)  # Format as integer with commas for thousands separators
    else:
        return price

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_image(file, upload_folder, allowed_extensions, filename=None):
    if file and allowed_file(file.filename, allowed_extensions):
        if not filename:
            filename = secure_filename(file.filename)
        else:
            filename = secure_filename(filename)

        # Ensure that the upload directory exists; create it if not
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return filename
    return None

def delete_image_by_filename(filename, upload_folder):
    """
    Delete an image file from the specified upload folder based on its filename.

    Args:
        filename (str): The filename of the image to be deleted.
        upload_folder (str): The path to the upload folder where the image is stored.

    Returns:
        bool: True if the file was successfully deleted, False otherwise.
    """
    file_path = os.path.join(upload_folder, filename)

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            print(f"File '{filename}' does not exist in '{upload_folder}'.")
            return False
    except OSError as e:
        print(f"Error deleting file '{filename}': {e}")
        return False
