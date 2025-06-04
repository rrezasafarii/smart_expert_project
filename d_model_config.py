# d_model_config.py
"""
Configuration file for Smart Expert Project - Model Settings.
Supports: XGBoost, LightGBM, CatBoost, Random Forest, Gradient Boosting, Neural Network, SVM, Logistic Regression, Linear Regression, KNN
Tasks: Classification & Regression
"""

# Random seed for reproducibility
RANDOM_SEED = 42

# Train/Test split ratio
TEST_SIZE = 0.25  # 25% Test, 75% Train

# Task Type: "classification" or "regression"
TASK_TYPE = "classification"  # or "regression"

# Model type: Select one
# Options: "xgboost", "lightgbm", "catboost", "random_forest", "gradient_boosting", "neural_network", "svm", "logistic_regression", "linear_regression", "knn"
MODEL_TYPE = "xgboost"

# Common parameters (for all models)
COMMON_PARAMS = {
    "random_state": RANDOM_SEED,
}

# XGBoost hyperparameters
XGBOOST_PARAMS = {
    "n_estimators": 200,
    "learning_rate": 0.05,
    "max_depth": 6,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "binary:logistic" if TASK_TYPE == "classification" else "reg:squarederror",
    "random_state": RANDOM_SEED,
}

# LightGBM hyperparameters
LIGHTGBM_PARAMS = {
    "n_estimators": 200,
    "learning_rate": 0.05,
    "num_leaves": 31,
    "boosting_type": "gbdt",
    "objective": "binary" if TASK_TYPE == "classification" else "regression",
    "random_state": RANDOM_SEED,
}

# CatBoost hyperparameters
CATBOOST_PARAMS = {
    "iterations": 200,
    "learning_rate": 0.05,
    "depth": 6,
    "loss_function": "Logloss" if TASK_TYPE == "classification" else "RMSE",
    "random_seed": RANDOM_SEED,
    "verbose": False,
}

# Random Forest hyperparameters
RANDOM_FOREST_PARAMS = {
    "n_estimators": 100,
    "max_depth": 10,
    "min_samples_split": 2,
    "random_state": RANDOM_SEED,
}

# Gradient Boosting hyperparameters
GRADIENT_BOOSTING_PARAMS = {
    "n_estimators": 100,
    "learning_rate": 0.1,
    "max_depth": 3,
    "random_state": RANDOM_SEED,
}

# Neural Network (MLP) hyperparameters
NEURAL_NETWORK_PARAMS = {
    "hidden_layer_sizes": (100, 50),
    "activation": "relu",
    "solver": "adam",
    "alpha": 0.0001,
    "batch_size": "auto",
    "learning_rate_init": 0.001,
    "max_iter": 200,
    "random_state": RANDOM_SEED,
}

# SVM hyperparameters
SVM_PARAMS = {
    "C": 1.0,
    "kernel": "rbf",
    "gamma": "scale",
}

# Logistic Regression hyperparameters
LOGISTIC_REGRESSION_PARAMS = {
    "solver": "lbfgs",
    "max_iter": 200,
    "random_state": RANDOM_SEED,
}

# Linear Regression hyperparameters
LINEAR_REGRESSION_PARAMS = {
    # No hyperparameters for basic Linear Regression in sklearn
}

# K-Nearest Neighbors hyperparameters
KNN_PARAMS = {
    "n_neighbors": 5,
    "weights": "uniform",
}

# Early Stopping settings (for models that support it)
EARLY_STOPPING_ROUNDS = 10
