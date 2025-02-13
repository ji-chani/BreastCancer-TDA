import numpy as np
from modules import zip2array_filenames, extract_pixels, PersistentHomologyClassifier, plot_metrics
from sklearn.model_selection import train_test_split
from skimage.feature import hog
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

print("Initiating Classification of Breast Cancer Mammograms ------")
print()

# global controls
extract_data = False
extract_features = False

if extract_data:
    # ------- FILE EXTRACTION ------ 
    # Extract File Names
    breast_cancer = {'target_names': ['benign', 'malignant'], 'image_dim': (224, 224, 3)}
    classes = breast_cancer['target_names']
    zip_paths = ['BreastCancer_Benign.zip', 'BreastCancer_Malignant.zip']

    for idx,clss in enumerate(classes):
        breast_cancer[clss+'Paths'] = zip2array_filenames(zip_paths[idx], 'png')

    num_benign, num_malignant = len(breast_cancer['benignPaths']), len(breast_cancer['malignantPaths'])

    # Extract Pixels from Image File Names
    for c in classes:
        breast_cancer[c+'Pixels'] = [extract_pixels(img_path, grayscaled=True, flattened=True) for img_path in breast_cancer[c+'Paths']]

    # Organizing Data according the Pixels and Targets
    breast_cancer['data'], breast_cancer['target'] = [], []
    for idx, clss in enumerate(classes):
        new_data = [data for data in breast_cancer[clss+"Pixels"]]
        new_target = [idx for _ in breast_cancer[clss+"Pixels"]]

        breast_cancer['data'].extend(new_data)
        breast_cancer['target'].extend(new_target)

    # save breast_cancer dictionary into npy file
    np.save('breast_cancer_dataset.npy', breast_cancer)

else:
    # load breast_cancer dictionary into npy file
    breast_cancer = np.load('breast_cancer_dataset.npy', allow_pickle=True).item()
    classes = breast_cancer['target_names']


if extract_features:
    # ---------- DATA PREPARATION
    print("Preparing dataset ...")
    print()

    # reshaping data
    HEIGHT, WIDTH = 224, 224
    X, y = np.array(breast_cancer['data']), np.array(breast_cancer['target'])
    X = X.reshape(-1, HEIGHT, WIDTH)
    print(f"Data is reshaped. \n Dimension of each instance: {HEIGHT*WIDTH}")

    # data splitting
    train_size, test_size = 4800, 1200
    indices = np.arange(len(y))
    X_train, X_test, y_train, y_test = train_test_split(X, y, indices, train_size=train_size, test_size=test_size)
    print(f"Data is split. \n Train size: {y_train.shape[0]} \n Test size: {y_test.shape[0]}")

    # feature extraction
    print("Extracting features using HOG ...")
    X_train = np.array([hog(img, orientations=9, pixels_per_cell=(8,8), cells_per_block=(3,3)).flatten() for img in X_train])
    X_test = np.array([hog(img, orientations=9, pixels_per_cell=(8,8), cells_per_block=(3,3)).flatten() for img in X_test])
    print(f"Features extracted. \n Dimension of each instance: {X_test[0].shape[0]}")

    # dimension reduction
    print("Reducing dimensions using PCA ...")
    pca_model = PCA(0.95).fit(X_train)
    X_train, X_test = pca_model.transform(X_train), pca_model.transform(X_test)
    print(f"Dimension reduced. \n Dimension of each instance: {X_test[0].shape[0]}")

    print("Normalizing data ...")
    # feature scaling
    scaler = StandardScaler().fit(X_train)
    X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)
    print(f"Data normalized. \n Final dimension of each instance: {X_test[0].shape[0]}")

    np.save("prepared_data/train_data.npy", X_train)
    np.save("prepared_data/test_data.npy", X_test)
    np.save("prepared_data/train_target.npy", y_train)
    np.save("prepared_data/test_target.npy", y_test)
else:
    X_train = np.load("prepared_data/train_data.npy")
    X_test = np.load("prepared_data/test_data.npy")
    y_train = np.load("prepared_data/train_target.npy")
    y_test = np.load("prepared_data/test_target.npy")
    
print(f"Data ready for classification. \n Train size: {X_train.shape[0]} \n Test size: {X_test.shape[0]} \n Dimension: {X_test[0].shape[0]}")

# -------- CLASSIFICATION
print('Starting Validation --------------')
print('\n The PHCA model is learning from the data...')

method_labels = {'true_labels': [], 'phca': []}
phca_model = PersistentHomologyClassifier()
phca_model.fit(X_train, y_train)

print("Model finished learning.")
print()
print("The model is now predicting new data.")

method_labels['true_labels'].extend(y_test)
method_labels['phca'].extend(phca_model.predict(X_test))
print("\n PHCA model is finished predicting.")
np.save('PHCA_predicted_labels.npy', method_labels)

# --------- CLASSIFICATION REPORT
metrics = ['precision', 'recall', 'f1-score', 'specificity', 'support', 'accuracy']
report = classification_report(method_labels['true_labels'], method_labels['phca'])
print(report)
plot_metrics(predicted_labels=method_labels['phca'],
            true_labels=method_labels['true_labels'],
            measurements=metrics, save=True)