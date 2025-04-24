# Topological Insights and Hybrid Feature Extraction for Breast Cancer Detection: A Persistent Homology Classification Approach
This is the repository associated with the submitted AI Applications article (titled above) in PeerJ Computer Science. It consists of all codes used to implement the experiments in the article. The focus here is to utilize Persistent Homology Classification Algorithm (PHCA) [1], a novel computational topology-based classifier, and some computer vision technique for breast cancer mammography scans detection. To replicate results, follow through the replication process elaborate below.

## Required Packages and Versions
- **numpy**==2.1.2
- **matplotlib**==3.9.2
- **scikit-learn**==1.5.2
- **scikit-image**==0.24.0
- **ripser**==0.6.10
- **opencv-python**==4.10.0.84
- **tqdm**==4.66.6

All of these packages are indicated in the requirements.txt file. The ripser package works better for Python versions >3.7 and <= 3.10.10.

## Instructions for Replication

### Data Preparation
- Download the dataset from https://doi.org/10.5281/zenodo.14769221. You should be able to obtain 2 zip files: `BreastCancer_Benign.zip` and `BreastCancer_Malignant.zip`.
- Save downloaded files in a folder/directory. This folder will be your directory for later implementation.
- Extract the contents of each zip file. You should expect two folders: `BreastCancer_Benign` and `BreastCancer_Malignant`
- If the folders contain the images upon opening, you're all set. If not and you observe another folder with the same name as the one opened, move the "inner" folder to your directory. Upon moving, you won't be needing the now empty folders.

### Main Implementation (without cloning)
- Download all files from this repository. 
- Extract the contents of the `modules.zip` file. You should expect a `modules` folder which contains Python files: `__init__.py`, `classification.py`, `phca.py`, and `pixel_extraction.py`.
- Create a virtual environment and install all dependices from the `requirements.txt` file.(**Important Note**: Make sure to use Python version (>3.7, <=3.10.10) so that the _ripser_ package will work)
- Create a `prepared_data` folder in the directory. This will contain the test and train data and targets for later use.
- Run the `main.py` file. For first time implementation, make sure that the _extract_data_ and _extract_features_ global controls are set to _True_.
- After running the `main.py` file, you should expect a new file with name `PHCA_predicted_labels.npy`. This contains the true labels and predicted labels by PHCA.
- Run through the `generate_results.ipynb` Jupyter notebook to plot the results.

### Main Implementation (with cloning)
```
git clone 
```
## References
[1] 
