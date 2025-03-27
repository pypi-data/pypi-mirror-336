from setuptools import setup, find_packages

setup(
    name="forecast_sdk",
    version="0.1.0",
    description="A time series forecasting SDK using XGBoost and ARIMA",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "xgboost",
        "scikit-learn",
        "statsmodels",
        "python-dateutil",
        "streamlit",
        # Optionally add "scikit-optimize" if you need Bayesian Optimization
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
