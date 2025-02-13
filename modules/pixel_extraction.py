import zipfile
import cv2

# extract filenames of images from zip file
def zip2array_filenames(zip_path: str, file_extension:str):
    """
    Converts a zipped filenames into a dictionary.
    Removes the path of the folder where the filenames are saved.

    Parameter
    -------
    zipPath: path of zip file
    fileExtension: extension of the files to extract

    Return
    -------
    fileNames: array of filenames (str)
    """

    file_folder_names = []
    with zipfile.ZipFile(zip_path, "r") as zip:
        for file_info in zip.infolist():
            file_folder_names.append(file_info.filename)

    file_names = [f for f in file_folder_names if f.endswith(file_extension)]
    return file_names


# extract pixels from image through filenames
def extract_pixels(img_path:str, grayscaled:bool=True, flattened:bool=True):
    """
    Extracts flattened pixels of grayscaled image (True) and
    original dimensions of image.

    Parameter
    --------
    imgPath: path of image

    Returns
    --------
    image: flattened image pixels
    """
    image = cv2.imread(img_path)
    if grayscaled:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # dimensions = image.shape
    if flattened:
        return image.flatten()
    else:
        return image
