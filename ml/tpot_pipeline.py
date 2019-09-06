import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
import tpot_model

# NOTE: Make sure that the class is labeled 'target' in the data file
training_features, testing_features, training_target, testing_target = tpot_model.load_keiba_data()

# Average CV score on the training set was:0.7445685169564654
exported_pipeline = make_pipeline(
    StackingEstimator(estimator=GaussianNB()),
    MultinomialNB(alpha=100.0, fit_prior=False)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)

tpot_model.pickle_pipeline(exported_pipeline)
