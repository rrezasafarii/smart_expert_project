# b_model_trainer.py
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Import model configs
from b_config.d_model_config import (
    RANDOM_SEED, TEST_SIZE, TASK_TYPE, MODEL_TYPE,
    XGBOOST_PARAMS, LIGHTGBM_PARAMS, CATBOOST_PARAMS,
    RANDOM_FOREST_PARAMS, GRADIENT_BOOSTING_PARAMS, NEURAL_NETWORK_PARAMS,
    SVM_PARAMS, LOGISTIC_REGRESSION_PARAMS, LINEAR_REGRESSION_PARAMS, KNN_PARAMS,
    EARLY_STOPPING_ROUNDS
)

# Import ML models
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from catboost import CatBoostClassifier, CatBoostRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.svm import SVC, SVR
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

# ===> Generate Placeholder Dataset (GLOBAL) ✅
from sklearn.datasets import make_classification, make_regression

if TASK_TYPE == "classification":
    X, y = make_classification(
        n_samples=1000, n_features=20, n_classes=2, random_state=RANDOM_SEED
    )
else:
    X, y = make_regression(
        n_samples=1000, n_features=20, noise=0.1, random_state=RANDOM_SEED
    )

# ===> Functions Start from Here
def get_model():
    if MODEL_TYPE == "xgboost":
        return XGBClassifier(**XGBOOST_PARAMS) if TASK_TYPE == "classification" else XGBRegressor(**XGBOOST_PARAMS)
    elif MODEL_TYPE == "lightgbm":
        return LGBMClassifier(**LIGHTGBM_PARAMS) if TASK_TYPE == "classification" else LGBMRegressor(**LIGHTGBM_PARAMS)
    elif MODEL_TYPE == "catboost":
        return CatBoostClassifier(**CATBOOST_PARAMS) if TASK_TYPE == "classification" else CatBoostRegressor(**CATBOOST_PARAMS)
    elif MODEL_TYPE == "random_forest":
        return RandomForestClassifier(**RANDOM_FOREST_PARAMS) if TASK_TYPE == "classification" else RandomForestRegressor(**RANDOM_FOREST_PARAMS)
    elif MODEL_TYPE == "gradient_boosting":
        return GradientBoostingClassifier(**GRADIENT_BOOSTING_PARAMS) if TASK_TYPE == "classification" else GradientBoostingRegressor(**GRADIENT_BOOSTING_PARAMS)
    elif MODEL_TYPE == "neural_network":
        return MLPClassifier(**NEURAL_NETWORK_PARAMS) if TASK_TYPE == "classification" else MLPRegressor(**NEURAL_NETWORK_PARAMS)
    elif MODEL_TYPE == "svm":
        return SVC(**SVM_PARAMS) if TASK_TYPE == "classification" else SVR(**SVM_PARAMS)
    elif MODEL_TYPE == "logistic_regression":
        return LogisticRegression(**LOGISTIC_REGRESSION_PARAMS)
    elif MODEL_TYPE == "linear_regression":
        return LinearRegression()
    elif MODEL_TYPE == "knn":
        return KNeighborsClassifier(**KNN_PARAMS) if TASK_TYPE == "classification" else KNeighborsRegressor(**KNN_PARAMS)
    else:
        raise ValueError(f"Unsupported MODEL_TYPE: {MODEL_TYPE}")

def evaluate(y_true, y_pred):
    if TASK_TYPE == "classification":
        acc = accuracy_score(y_true, y_pred)
        print(f"🔎 Accuracy: {acc:.4f}")
        return acc
    else:  # regression
        mse = mean_squared_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        print(f"🔎 MSE: {mse:.4f}")
        print(f"🔎 R2 Score: {r2:.4f}")
        return mse, r2

def train(X, y):
    # Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED
    )

    # Normalize features for Neural Networks or SVMs
    if MODEL_TYPE in ["neural_network", "svm"]:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    model = get_model()

    print(f"🚀 Training {MODEL_TYPE} model for {TASK_TYPE} task...")
    model.fit(X_train, y_train)
    print("✅ Training completed.")

    y_pred = model.predict(X_test)

    print("📊 Evaluation Results:")
    evaluate(y_test, y_pred)

    return model

# no need for if __name__ == "__main__" part now
