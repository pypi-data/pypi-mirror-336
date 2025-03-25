from clustervis import show_ensemble_classifier_plot, show_base_classifier_plot

from sklearn.ensemble import BaggingClassifier
from sklearn.datasets import make_blobs
from sklearn.neighbors import KNeighborsClassifier

# Generate synthetic data
X, y = make_blobs(n_samples=300, centers=4, random_state=0, cluster_std=1.0)

# Define some colors for each class
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow

# Define the resolution of the plots
resolution = 100

# Initialize the base classifier and bagging ensemble
clf = KNeighborsClassifier(n_neighbors=3)
bag = BaggingClassifier(clf, n_estimators=8, max_samples=0.05, random_state=1)
bag.fit(X, y)

# Use clustervis to plot the decision boundaries for the ensemble (Bagging)
show_ensemble_classifier_plot(X, bag, colors, resolution, 'Bagging Classifier')

# Declare the necessary variables for plotting side by side
n_knns = len(bag.estimators_)  # Number of KNN classifiers in the bagging ensemble
fig, axes = plt.subplots(1, n_knns, figsize=(n_knns * 5, 5))  # Create a horizontal grid for KNN plots

# Use clustervis to plot the decision boundaries for the base classifiers (KNN)
for t, base_estimator in enumerate(bag.estimators_):
    show_base_classifier_plot(X, base_estimator, colors, resolution, f'KNN #{t+1}')