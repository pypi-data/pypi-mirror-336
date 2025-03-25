from clustervis import ensemble_classifier_plot, base_classifier_plot

import matplotlib.pyplot as plt

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

# Define the necessary variables for the subplots
n_knns = len(bag.estimators_)  # Number of KNN classifiers in the bagging ensemble
fig, axes = plt.subplots(1, n_knns, figsize=(n_knns * 5, 5))  # Create a horizontal grid for KNN plots

# First, plot the decision boundaries for the ensemble (Bagging) in a separate plot
# We will create a separate axis for this plot to avoid it getting mixed with the KNN plots.
fig_ensemble, ax_ensemble = plt.subplots(figsize=(10, 5))
ensemble_classifier_plot(X, bag, colors, resolution, 'Bagging Classifier', show=True, ax=ax_ensemble)

# Now, use clustervis to plot the decision boundaries for the base classifiers (KNN)
for i, base_estimator in enumerate(bag.estimators_):
    base_classifier_plot(X, base_estimator, colors, resolution, f'KNN #{i+1}', show=True, ax=axes[i])

# Adjust layout for tight spacing in the KNN plots
plt.tight_layout()