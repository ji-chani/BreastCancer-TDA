from tqdm import tqdm
import numpy as np
import ripser
import copy

import warnings
warnings.filterwarnings('ignore')

class PersistentHomologyClassifier:
    def __init__(self, dim=0):
        self.dim = dim

    def fit(self, X_train, y_train):
        self.byclass_data = by_class_data(X_train, y_train)
        self.PD_byclass = get_persistence_diagram(self.byclass_data, self.dim)

    def predict(self, X_test):
        y_pred = []
        for _, x_new in enumerate(tqdm(X_test)):
            self.byclass_data_plus = update_data(self.byclass_data, x_new)
            self.PD_byclass_plus = get_persistence_diagram(self.byclass_data_plus, self.dim)
            self.selected_class = class_category_selector(self.PD_byclass, self.PD_byclass_plus, self.dim)
            y_pred.append(self.selected_class)
        return y_pred

def by_class_data(X, y):
    byclass_data = {clss: [] for clss in set(y)}
    for i in range(len(X)):
        byclass_data[y[i]].append(X[i])
    return byclass_data

def get_persistence_diagram(data:dict, dim:int):
    return {key: ripser.ripser(np.array(data[key]), maxdim=dim)['dgms'] for key in data.keys()}

def update_data(data:dict, x_new:list):
    data_plus = copy.deepcopy(data)
    for clss in data_plus.keys():
        data_plus[clss].append(x_new)
    return data_plus

def get_lifespan(PD:list, dim:int):
    total_lifespan = 0
    for d in range(0, dim+1):
        births, deaths = PD[d][:,0], PD[d][:,1]
        births, deaths = births[np.isfinite(deaths)], deaths[np.isfinite(deaths)]  # remove inf values
        total_lifespan += np.sum(deaths)- np.sum(births)
    return total_lifespan

def class_category_selector(orig_PD:dict, new_PD:dict, dim:int):
    scores = {}
    for clss in orig_PD.keys():
        orig_lspan, new_lspan = get_lifespan(orig_PD[clss], dim), get_lifespan(new_PD[clss], dim)
        scores[clss] = abs(new_lspan - orig_lspan)
    return min(scores, key=scores.get)