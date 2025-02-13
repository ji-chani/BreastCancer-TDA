from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import numpy as np

def get_specificity(confusionMatrix, classes):
    label_lists = classes
    specificity = {}
    for l, label in enumerate(label_lists):
        tp, tn, fp, fn = 0, 0, 0, 0
        tp = confusionMatrix[l, l]
        fn = sum(confusionMatrix[l]) - tp
        for i in range(len(label_lists)):
            for j in range(len(label_lists)):
                if i == l or j == l:
                    continue
                else:
                    tn += confusionMatrix[i,j]
        for i in range(len(label_lists)):
            if i==l:
                continue
            else:
                fp += confusionMatrix[l][i]
        specificity[str(label)] = tn/(tn+fp)
    return specificity


def plot_metrics(predicted_labels, true_labels, measurements, title=None, save:bool=False):
    colors = ['#013A63', '#2A6F97', '#89C2D9']
    report = classification_report(true_labels, predicted_labels, output_dict=True)
    labels = np.unique(true_labels)
    metric_values = []
    xlabels = ['precision', 'recall', 'f1-score', 'specificity', 'accuracy']
    metrics = measurements.copy()
    metrics.remove('support')
    specificity = get_specificity(confusion_matrix(true_labels, predicted_labels, labels=labels), labels)
    for metric in metrics:
        if metric == 'accuracy':
            value = [report[metric]]
        elif metric == 'specificity':
            value = [specificity[str(clss)] for clss in labels]
        else:
            value = [report[str(clss)][metric] for clss in labels]
        metric_values.extend(value)

    # plot 4 eval metrics
    b = plt.bar(np.arange(len(metric_values[:-1])), metric_values[:-1], width=0.90, color=colors[:-1], edgecolor='black')
    plt.bar_label(b, fmt='%.4f', label_type='edge')

    # plot accuracy
    b2 = plt.bar([8.5], metric_values[-1], width=1.5, color=colors[-1], edgecolor='black')
    plt.bar_label(b2, fmt='%.4f', label_type='edge')

    # plot proxy legends
    handles = [plt.Rectangle((0,0),1,1, color=colors[lab]) for lab in labels] + [plt.Rectangle((0,0),1,1, color=colors[-1])]
    plt.legend(handles, ['benign', 'malignant', 'overall'])
    plt.ylim([0, 1.3])

    plt.xticks(np.arange(0.5, 9.5, step=2), xlabels, rotation='horizontal')
    plt.xlabel("Metrics")
    plt.ylabel("Values")
    if title is not None:
        plt.title(title)

    if save:
        plt.savefig('final_classification_result', dpi=500, transparent=True, format='png')