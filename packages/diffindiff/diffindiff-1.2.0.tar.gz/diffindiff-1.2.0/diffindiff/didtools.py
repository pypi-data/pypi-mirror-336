# -------------------------------------------------------------------------------
# Name:        didtools (diffindiff)
# Purpose:     Creating data for Difference-in-Differences Analysis
# Author:      Thomas Wieland (geowieland@googlemail.com)
# Version:     1.2.0
# Last update: 2025-03-25 19:27
# Copyright (c) 2025 Thomas Wieland
#-------------------------------------------------------------------------------


import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from sklearn.ensemble import BaggingRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_percentage_error, mean_squared_error, root_mean_squared_error


def check_columns(
    df: pd.DataFrame, 
    columns: list
    ):

    missing_columns = [col for col in columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"DataFrame '{df.__class__.__name__}' does not contain column(s): {', '.join(missing_columns)}")

def is_balanced(
    data,
    unit_col,
    time_col,
    outcome_col,
    other_cols = None
    ):

    unit_freq = data[unit_col].nunique()
    time_freq = data[time_col].nunique()
    unitxtime = unit_freq*time_freq

    if other_cols is None:
        cols_relevant = [unit_col, time_col, outcome_col]
    else:
        cols_relevant = [unit_col, time_col, outcome_col] + other_cols

    data_relevant = data[cols_relevant]

    if unitxtime != len(data_relevant.notna()):
        return False
    else:
        return True

def is_binary(
    data,
    treatment_col
    ):
    
    if data[treatment_col].nunique() == 2:
        if data[treatment_col].isin([0, 1]).all():
            return True
        else:
            return False
    else:
        return False

def is_missing(
    data,
    drop_missing: bool = True,
    missing_replace_by_zero: bool = False
    ):

    missing_outcome = data.isnull().any()
    missing_outcome_var = any(missing_outcome == True)

    if missing_outcome_var:
        missing_true_vars = [name for name, value in missing_outcome.items() if value]
    else:
        missing_true_vars = []

    if drop_missing and not missing_replace_by_zero:
        data = data.dropna(subset = missing_true_vars)
        
    if missing_replace_by_zero:
        data[missing_true_vars] = data[missing_true_vars].fillna(0)

    return [
        missing_outcome_var, 
        missing_true_vars, 
        data
        ]

def is_simultaneous(
    data,
    unit_col,
    time_col,
    treatment_col
    ):

    data_isnotreatment = is_notreatment(data, unit_col, treatment_col)
    treatment_group = data_isnotreatment[1]
    data_TG = data[data[unit_col].isin(treatment_group)]

    data_TG_pivot = data_TG.pivot_table (index = time_col, columns = unit_col, values = treatment_col)

    col_identical = (data_TG_pivot.nunique(axis=1) == 1).all()

    return col_identical

def is_notreatment(
    data,
    unit_col,
    treatment_col
    ):

    data_relevant = data[[unit_col, treatment_col]]

    treatment_timepoints = data_relevant.groupby(unit_col).sum(treatment_col)
    treatment_timepoints = treatment_timepoints.reset_index()

    no_treatment = (treatment_timepoints[treatment_col] == 0).any()

    treatment_group = treatment_timepoints.loc[treatment_timepoints[treatment_col] > 0, unit_col]
    control_group = treatment_timepoints.loc[treatment_timepoints[treatment_col] == 0, unit_col]

    return [
        no_treatment, 
        treatment_group, 
        control_group
        ]

def is_parallel(
    data,
    unit_col,
    time_col,
    treatment_col,
    outcome_col,
    pre_post = False,
    alpha = 0.05
    ):

    if pre_post:
        return None
    
    modeldata_isnotreatment = is_notreatment(
        data = data,
        unit_col = unit_col,
        treatment_col = treatment_col
        )    
    if not modeldata_isnotreatment:
        return None
    
    treatment_group = modeldata_isnotreatment[1]
    first_day_of_treatment = min(data[(data[unit_col].isin(treatment_group)) & (data[treatment_col] == 1)][time_col])

    data_test = data[data[time_col] < first_day_of_treatment].copy()
    data_test["TG"] = 0
    data_test.loc[data_test[unit_col].isin(treatment_group), "TG"] = 1
    
    if "date_counter" not in data_test.columns:
        data_test = date_counter(
            df = data_test,
            date_col = time_col, 
            new_col = "date_counter"
            )
    data_test["TG_x_t"] = data_test["TG"]*data_test["date_counter"]

    test_ols_model = ols(f'{outcome_col} ~ TG + date_counter + TG_x_t', data = data_test).fit()
    coef_TG_x_t_p = test_ols_model.pvalues["TG_x_t"]

    if coef_TG_x_t_p < alpha:
        parallel = False
    else:
        parallel = True

    return [
        parallel, 
        test_ols_model
        ]

def date_counter(
        df,
        date_col, 
        new_col = "date_counter"
        ):
    
    dates = df[date_col].unique()

    date_counter = pd.DataFrame({
       'date': dates,
        new_col: range(1, len(dates) + 1)
        })

    df = df.merge(
        date_counter,
        left_on = date_col,
        right_on = "date")
    
    return df

def unique(data):
    if data is None or (isinstance(data, (list, np.ndarray, pd.Series, pd.DataFrame)) and len(data) == 0):
        return []
    
    if isinstance(data, pd.DataFrame):
        values = data.values.ravel()

    elif isinstance(data, pd.Series):
        values = data.values.ravel()

    elif isinstance(data, np.ndarray):
        values = data.ravel()

    elif isinstance(data, list):
        values = data

    elif isinstance(data, set):
        values = list(data)

    else:
        raise TypeError(f"Unsupported data type: {type(data)}")
    
    unique_values = list(np.unique(values))
    return unique_values

def model_wrapper(
    y,
    X,
    model_type: str,
    test_size = 0.2,
    train_size = None,
    model_n_estimators = 1000,
    model_max_features = 0.9,
    model_min_samples_split = 2,
    rf_max_depth = None,
    gb_iterations = 100,
    gb_max_depth = 3,
    gb_learning_rate = 0.1,
    knn_n_neighbors = 5,
    svr_kernel = "rbf",
    xgb_learning_rate = 0.1,
    lgbm_learning_rate = 0.1,
    random_state = 71
    ):
    if model_type not in ["ols", "olsbg", "dtbg", "rf", "gb", "knn", "svr", "xgb", "lgbm", "catboost"]:
        raise ValueError("Please enter a valid model type")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, 
        y, 
        test_size = test_size,
        train_size = train_size,
        random_state = random_state
    )
    
    model = None
    y_pred = None

    if model_type == "ols":
        model = LinearRegression()    
    elif model_type == "olsbg":
        model = BaggingRegressor(
            estimator = LinearRegression(),
            n_estimators = model_n_estimators,         
            random_state = random_state
        )         
    elif model_type == "dtbg":
        model = BaggingRegressor(
            estimator = DecisionTreeRegressor(),
            n_estimators =model_n_estimators,         
            random_state = random_state
        )    
    elif model_type == "rf":
        model = RandomForestRegressor(
            n_estimators = model_n_estimators, 
            max_features = model_max_features,
            min_samples_split = model_min_samples_split,
            max_depth = rf_max_depth,
            random_state = random_state
        )
    elif model_type == "gb":
        model = GradientBoostingRegressor(
            learning_rate = gb_learning_rate,
            n_estimators = gb_iterations, 
            max_features = model_max_features,
            min_samples_split = model_min_samples_split,
            max_depth = gb_max_depth,
            random_state = random_state
        )
    elif model_type == "knn":
        model = KNeighborsRegressor(n_neighbors=knn_n_neighbors)
    elif model_type == "svr":
        model = SVR(kernel=svr_kernel)
    elif model_type == "xgb":
        model = XGBRegressor(
            learning_rate = xgb_learning_rate,
            n_estimators = gb_iterations,
            random_state = random_state
        )
    elif model_type == "lgbm":
        model = LGBMRegressor(
            learning_rate = lgbm_learning_rate,
            n_estimators = gb_iterations,
            random_state = random_state
        )
        
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    metrics = {
        "r2_score": r2_score(y_test, y_pred),
        "mape": mean_absolute_percentage_error(y_test, y_pred),
        "mse": mean_squared_error(y_test, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred))
        }

    return [
        y_pred,
        model,
        metrics
        ]
    
def treatment_times(
    data,
    unit_col,
    time_col,
    treatment_col
    ):
    
    check_columns(
        df = data,
        columns = [unit_col, time_col, treatment_col]
        )
    
    units = unique(data[unit_col])
    
    units_tt = pd.DataFrame(columns = [unit_col, "treatment_min", "treatment_max"])
    
    for unit in units:
        
        data_unit_tt = data[(data[unit_col] == unit) & (data[treatment_col] == 1)]
        
        if data_unit_tt.empty:
            continue
        
        treatment_min = min(data_unit_tt[time_col])
        treatment_max = max(data_unit_tt[time_col])
        
        units_tt = pd.concat(
            [units_tt, pd.DataFrame({unit_col: [unit], "treatment_min": [treatment_min], "treatment_max": [treatment_max]})],
            ignore_index=True
        )
        
    return units_tt