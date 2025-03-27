import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.parser import parse
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
import xgboost as xgb
from sklearn.metrics import mean_absolute_percentage_error
from statsmodels.tsa.arima.model import ARIMA
# Optional: for Bayesian optimization
try:
    from skopt import BayesSearchCV
except ImportError:
    BayesSearchCV = None

class ForecastPipeline:
    def __init__(self, xgb_params=None, fine_tune_method="None", period_option="Daily", forecast_value=10):
        if xgb_params is None:
            xgb_params = {
                "base_score": 0.5,
                "booster": "gbtree",
                "objective": "reg:squarederror",
                "n_estimators": 500,
                "learning_rate": 0.01,
                "max_depth": 5,
                "min_child_weight": 5,
                "reg_lambda": 10,
                "reg_alpha": 5
            }
        self.xgb_params = xgb_params
        self.fine_tune_method = fine_tune_method
        self.period_option = period_option
        self.forecast_value = forecast_value

    # --- Utility Functions ---
    @staticmethod
    def robust_parse_date(val):
        s = str(val).strip()
        if not s:
            return pd.NaT
        if s.isdigit() and len(s) == 8:
            try:
                dt = datetime.strptime(s, '%Y%m%d')
                if dt.year < 1900 or dt.year > 2100:
                    return pd.NaT
                return dt
            except Exception:
                return pd.NaT
        if not any(delim in s for delim in ['-', '/', '.']):
            return pd.NaT
        try:
            dt = parse(s, fuzzy=True)
            if dt.year < 1900 or dt.year > 2100:
                return pd.NaT
            return dt
        except Exception:
            return pd.NaT

    @staticmethod
    def detect_datetime_column(df, selected_cols, threshold=0.8):
        best_col = None
        best_ratio = 0
        for col in selected_cols:
            if not pd.api.types.is_object_dtype(df[col]):
                continue
            parsed = df[col].apply(ForecastPipeline.robust_parse_date)
            ratio = parsed.notnull().mean()
            if ratio > best_ratio:
                best_ratio = ratio
                best_col = col
        return (best_col, best_ratio) if best_ratio >= threshold else (None, best_ratio)

    @staticmethod
    def add_time_features(df, datetime_col):
        df['year'] = df[datetime_col].dt.year
        df['month'] = df[datetime_col].dt.month
        df['day'] = df[datetime_col].dt.day
        df['weekday'] = df[datetime_col].dt.weekday
        df['hour'] = df[datetime_col].dt.hour
        df['minute'] = df[datetime_col].dt.minute
        df['second'] = df[datetime_col].dt.second
        df['week_number'] = df[datetime_col].dt.isocalendar().week.astype(int)
        df['is_month_start'] = df[datetime_col].dt.is_month_start.astype(int)
        df['is_month_end'] = df[datetime_col].dt.is_month_end.astype(int)
        df['quarter'] = df[datetime_col].dt.quarter
        return df

    @staticmethod
    def create_time_features(df, datetime_col, target_col, default_lags=[1, 2], default_rolling=[3, 5]):
        df = ForecastPipeline.add_time_features(df, datetime_col)
        for lag in default_lags:
            df[f'lag_{lag}'] = df[target_col].shift(lag)
        for window in default_rolling:
            df[f'rolling_mean_{window}'] = df[target_col].rolling(window=window).mean()
        return df

    # --- Main Pipeline Method ---
    def run(self, df, feature_cols, target_col):
        # 1. Detect datetime column.
        datetime_col, best_ratio = self.detect_datetime_column(df, feature_cols)
        if datetime_col is None:
            raise ValueError("Could not detect a datetime column among the selected features.")

        # 2. Remove additional datetime-like columns.
        datetime_threshold = 0.8
        additional_features = [col for col in feature_cols if col != datetime_col and 
                               df[col].apply(self.robust_parse_date).notnull().mean() < datetime_threshold]

        # 3. Convert datetime column.
        df[datetime_col] = df[datetime_col].apply(self.robust_parse_date)
        if df[datetime_col].isnull().any():
            raise ValueError("Datetime conversion error: Some dates could not be parsed.")
        cols_order = [datetime_col] + [col for col in df.columns if col != datetime_col]
        df = df[cols_order]

        # 4. Process additional features.
        X_features = df[additional_features].copy() if additional_features else pd.DataFrame()
        cat_cols = X_features.select_dtypes(include=['object']).columns.tolist()
        num_cols = [col for col in X_features.columns if col not in cat_cols]
        encoders = {}
        for col in cat_cols:
            le = LabelEncoder()
            X_features[col] = le.fit_transform(X_features[col])
            encoders[col] = le
        if num_cols:
            scaler = StandardScaler()
            X_features_scaled_num = pd.DataFrame(scaler.fit_transform(X_features[num_cols]), columns=num_cols)
        else:
            X_features_scaled_num = pd.DataFrame()
        X_features_scaled_cat = X_features[cat_cols].copy() if cat_cols else pd.DataFrame()
        if not X_features_scaled_cat.empty and not X_features_scaled_num.empty:
            X_features_processed = pd.concat([X_features_scaled_cat, X_features_scaled_num], axis=1)
        elif not X_features_scaled_cat.empty:
            X_features_processed = X_features_scaled_cat.copy()
        else:
            X_features_processed = X_features_scaled_num.copy()

        # 5. Prepare target.
        y = df[target_col].copy()

        # 6. Combine datetime, processed features, and target.
        data = pd.concat([df[[datetime_col]], X_features_processed, y], axis=1)

        # 7. Create time features.
        data = self.create_time_features(data, datetime_col, target_col)
        data.dropna(inplace=True)

        X_full = data.drop(columns=[datetime_col, target_col])
        y_full = data[target_col]
        X_train, X_test, y_train, y_test = train_test_split(X_full, y_full, test_size=0.2, random_state=42)

        # 8. Train the XGBoost model.
        model = xgb.XGBRegressor(**self.xgb_params)
        if self.fine_tune_method != "None":
            param_grid = {
                "max_depth": [3, 5, 7],
                "learning_rate": [0.01, 0.05, 0.1],
                "n_estimators": [100, 300, 500],
                "min_child_weight": [1, 3, 5],
                "reg_lambda": [0, 10, 20],
                "reg_alpha": [0, 5, 10]
            }
            if self.fine_tune_method == "Grid Search":
                model_search = GridSearchCV(model, param_grid, cv=3, n_jobs=-1, verbose=1)
            elif self.fine_tune_method == "Random Search":
                model_search = RandomizedSearchCV(model, param_grid, cv=3, n_iter=10, n_jobs=-1, verbose=1, random_state=42)
            elif self.fine_tune_method == "Bayesian Optimization":
                if BayesSearchCV is None:
                    raise ImportError("Bayesian Optimization requires scikit-optimize. Please install it.")
                model_search = BayesSearchCV(model, param_grid, cv=3, n_iter=15, n_jobs=-1, verbose=1, random_state=42)
            else:
                model_search = None

            if model_search is not None:
                model_search.fit(X_train, y_train)
                model = model_search.best_estimator_
            else:
                model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=True)
        else:
            model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=True)

        # 9. Forecast exogenous features using ARIMA.
        exog_feats = [col for col in X_full.columns if col not in ['lag_1','lag_2']]
        exog_forecasts = {}
        for feat in exog_feats:
            try:
                series = data[feat].dropna()
                arima_model = ARIMA(series, order=(1,1,1)).fit()
                forecast_series = arima_model.forecast(steps=self.forecast_value)
                exog_forecasts[feat] = forecast_series.values
            except Exception:
                exog_forecasts[feat] = np.repeat(data[feat].iloc[-1], self.forecast_value)

        # 10. Recursive Forecasting.
        last_row = data.iloc[-1]
        start_date = data[datetime_col].iloc[-1]
        if self.period_option == 'Hourly':
            freq = 'H'
        elif self.period_option == 'Daily':
            freq = 'D'
        elif self.period_option == '5 Minutes':
            freq = '5T'
        elif self.period_option == 'Monthly':
            freq = 'M'
        elif self.period_option == 'Yearly':
            freq = 'Y'
        else:
            freq = 'H'
        future_dates = pd.date_range(start=start_date, periods=self.forecast_value+1, freq=freq)[1:]

        recursive_preds = []
        current_features = last_row.drop([datetime_col, target_col]).copy()
        step = 0
        for dt in future_dates:
            next_pred = model.predict(current_features.values.reshape(1, -1))[0]
            recursive_preds.append(next_pred)
            new_features = current_features.copy()
            if 'lag_1' in new_features.index and 'lag_2' in new_features.index:
                new_features['lag_2'] = current_features['lag_1']
                new_features['lag_1'] = next_pred
            for feat in exog_feats:
                new_features[feat] = exog_forecasts[feat][step]
            current_features = new_features.copy()
            step += 1

        # 11. Build forecast DataFrame.
        future_df = pd.DataFrame({datetime_col: future_dates})
        future_df["forecast"] = recursive_preds
        actual_range = data[target_col].iloc[-self.forecast_value:].values
        if len(actual_range) != self.forecast_value:
            actual_range = np.repeat(data[target_col].iloc[-1], self.forecast_value)
        future_df["actual"] = actual_range

        # 12. Final display: only datetime and forecast.
        display_df = future_df[[datetime_col, "forecast"]].copy()
        preds_train = model.predict(X_train)
        mape = mean_absolute_percentage_error(y_train, preds_train)

        return display_df, mape
