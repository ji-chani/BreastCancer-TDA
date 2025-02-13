## Instructions for Replication

### Data Preparation
- Download the dataset from https://doi.org/10.5281/zenodo.14769221. You should be able to obtain 2 zip files: `BreastCancer_Benign.zip` and `BreastCancer_Malignant.zip`.
- Save downloaded files in a folder/directory. This folder will be your directory for later implementation.
- Extract the contents of each zip file. You should expect two folders: `BreastCancer_Benign` and `BreastCancer_Malignant`
- If the folders contain the images upon opening, you're all set. If not and you observe another folder with the same name as the one opened, move the "inner" folder to your directory. Upon moving, you won't be needing the now empty folders.

### Main Implementation
- Create a virtual environment and install all dependices from the `requirements.txt` file.(**Important Note**: Make sure to use Python version (>3.7, <=3.10.10) so that the _ripser_ package will work)
- Create a `prepared_data` folder in the directory. This will contain the test and train data and targets for later use.
- Run the `main.py` file. For first time implementation, make sure that the _extract_data_ global controls are set to _True_.
- If you want to skip the data extraction process, set _extract_data_ to _False_ and make sure that you have the `breast_cancer_dataset.npy` in your directory. File is also available in this repository.
- After running the `main.py` file, you should expect a new file with name `PHCA_predicted_labels.npy`. This contains the true labels and predicted labels by PHCA.
- Run through the `generate_results.ipynb` Jupyter notebook to plot the results.
