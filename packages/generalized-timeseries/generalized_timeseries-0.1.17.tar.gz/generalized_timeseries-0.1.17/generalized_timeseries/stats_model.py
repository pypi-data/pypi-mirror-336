#!/usr/bin/env python3
# stats_model.py

import logging as l

# handle data transformation and preparation tasks
import pandas as pd

# import model specific libraries
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model

# type hinting
from typing import Dict, Any, Tuple
from generalized_timeseries import data_processor

class ModelARIMA:
    """
    Applies the ARIMA (AutoRegressive Integrated Moving Average) model on all columns of a DataFrame.

    Attributes:
        data (pd.DataFrame): The input data on which ARIMA models will be applied.
        order (Tuple[int, int, int]): The (p, d, q) order of the ARIMA model.
        steps (int): The number of steps to forecast.
        models (Dict[str, ARIMA]): A dictionary to store ARIMA models for each column.
        fits (Dict[str, ARIMA]): A dictionary to store fitted ARIMA models for each column.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        order: Tuple[int, int, int] = (1, 1, 1),
        steps: int = 5,
    ) -> None:
        """
        Initializes the ARIMA model with the given data, order, and steps.

        Args:
            data (pd.DataFrame): The input data for the ARIMA model.
            order (Tuple[int, int, int]): The (p, d, q) order of the ARIMA model.
            steps (int): The number of steps to forecast.
        """
        ascii_banner = """
        \n
        \t> ARIMA <\n"""
        l.info(ascii_banner)
        self.data = data
        self.order = order
        self.steps = steps
        self.models: Dict[str, ARIMA] = {}  # Store models for each column
        self.fits: Dict[str, ARIMA] = {}  # Store fits for each column

    def fit(self) -> Dict[str, ARIMA]:
        """
        Fits an ARIMA model to each column in the dataset.

        Returns:
            Dict[str, ARIMA]: A dictionary where the keys are column names and the values are the
                fitted ARIMA models for each column.
        """
        for column in self.data.columns:
            model = ARIMA(self.data[column], order=self.order)
            self.fits[column] = model.fit()
        return self.fits

    def summary(self) -> Dict[str, str]:
        """
        Returns the model summaries for all columns.

        Returns:
            Dict[str, str]: A dictionary containing the model summaries for each column.
        """
        summaries = {}
        for column, fit in self.fits.items():
            summaries[column] = str(fit.summary())
        return summaries

    def forecast(self) -> Dict[str, float]:
        """
        Generates forecasts for each fitted model.

        Returns:
            Dict[str, float]: A dictionary where the keys are the column names and the values
                are the forecasted values for the first step.
        """
        forecasts = {}
        for column, fit in self.fits.items():
            forecasts[column] = fit.forecast(steps=self.steps).iloc[0]
        return forecasts


def run_arima(
    df_stationary: pd.DataFrame,
    p: int = 1,
    d: int = 1,
    q: int = 1,
    forecast_steps: int = 5,
) -> Tuple[Dict[str, object], Dict[str, float]]:
    """
    Runs an ARIMA model on stationary time series data.
    
    This function fits ARIMA(p,d,q) models to each column in the provided DataFrame
    and generates forecasts for the specified number of steps ahead. It performs minimal
    logging to display only core information about the model and forecasts.
    
    Args:
        df_stationary (pd.DataFrame): The DataFrame with stationary time series data
        p (int): Autoregressive lag order, default=1
        d (int): Degree of differencing, default=1
        q (int): Moving average lag order, default=1
        forecast_steps (int): Number of steps to forecast, default=5
        
    Returns:
        Tuple[Dict[str, object], Dict[str, float]]: 
            - First element: Dictionary of fitted ARIMA models for each column
            - Second element: Dictionary of forecasted values for each column
    """
    l.info(f"\n## Running ARIMA(p={p}, d={d}, q={q})")
    
    # Ensure data is properly prepared
    df_stationary = data_processor.prepare_timeseries_data(df_stationary)
    
    model_arima = ModelFactory.create_model(
        model_type="ARIMA",
        data=df_stationary,
        order=(p, d, q),
        steps=forecast_steps,
    )
    arima_fit = model_arima.fit()
    
    # Log only core model information instead of full summary
    l.info(f"## ARIMA model fitted to columns: {list(arima_fit.keys())}")
    
    # Generate and log forecast values concisely
    arima_forecast = model_arima.forecast()
    l.info(f"## ARIMA {forecast_steps}-step forecast values:")
    for col, value in arima_forecast.items():
        l.info(f"   {col}: {value:.4f}")

    return arima_fit, arima_forecast


class ModelGARCH:
    """
    Represents a GARCH model for time series data.

    Attributes:
        data (pd.DataFrame): The input time series data.
        p (int): The order of the GARCH model for the lag of the squared residuals.
        q (int): The order of the GARCH model for the lag of the conditional variance.
        dist (str): The distribution to use for the GARCH model (e.g., 'normal', 't').
        models (Dict[str, arch_model]): A dictionary to store models for each column of the data.
        fits (Dict[str, arch_model]): A dictionary to store fitted models for each column of the data.
    """

    def __init__(
        self, data: pd.DataFrame, p: int = 1, q: int = 1, dist: str = "normal"
    ) -> None:
        """
        Initializes the GARCH model with the given parameters.

        Args:
            data (pd.DataFrame): The input data for the GARCH model.
            p (int): The order of the GARCH model.
            q (int): The order of the ARCH model.
            dist (str): The distribution to be used in the model (e.g., 'normal', 't').
        """
        ascii_banner = """
        \n\t> GARCH <\n"""
        l.info(ascii_banner)
        self.data = data
        self.p = p
        self.q = q
        self.dist = dist
        self.models: Dict[str, arch_model] = {}  # Store models for each column
        self.fits: Dict[str, arch_model] = {}  # Store fits for each column

    def fit(self) -> Dict[str, arch_model]:
        """
        Fits a GARCH model to each column of the data.

        Returns:
            Dict[str, arch_model]: A dictionary where the keys are column names and the values
                are the fitted GARCH models.
        """
        for column in self.data.columns:
            model = arch_model(
                self.data[column], vol="Garch", p=self.p, q=self.q, dist=self.dist
            )
            self.fits[column] = model.fit(disp="off")
        return self.fits

    def summary(self) -> Dict[str, str]:
        """
        Returns the model summaries for all columns.

        Returns:
            Dict[str, str]: A dictionary containing the model summaries for each column.
        """
        summaries = {}
        for column, fit in self.fits.items():
            summaries[column] = str(fit.summary())
        return summaries

    def forecast(self, steps: int) -> Dict[str, float]:
        """
        Generates forecasted variance for each fitted model.

        Args:
            steps (int): The number of steps ahead to forecast.

        Returns:
            Dict[str, float]: A dictionary where keys are column names and values are the forecasted variances for the specified horizon.
        """
        forecasts = {}
        for column, fit in self.fits.items():
            forecasts[column] = fit.forecast(horizon=steps).variance.iloc[-1]
        return forecasts


class ModelFactory:
    """
    Factory class for creating instances of different statistical models.

    Methods:
        create_model(model_type: str, **kwargs) -> Any:
            Static method that creates and returns an instance of a model based on the provided model_type.
    """

    @staticmethod
    def create_model(
        model_type: str,
        data: pd.DataFrame,
        # ARIMA parameters with defaults
        order: Tuple[int, int, int] = (1, 1, 1),
        steps: int = 5,
        # GARCH parameters with defaults
        p: int = 1,
        q: int = 1,
        dist: str = "normal",
    ) -> Any:
        """
        Creates and returns a statistical model based on the specified type.

        Args:
            model_type (str): The type of model to create. Supported values are "arima" and "garch".
            **kwargs: Additional keyword arguments to pass to the model constructor.

        Returns:
            Any: An instance of the specified model type.

        Raises:
            ValueError: If the specified model type is not supported.
        """
        l.info(f"Creating model type: {model_type}")
        if model_type.lower() == "arima":
            return ModelARIMA(data=data, order=order, steps=steps)
        elif model_type.lower() == "garch":
            return ModelGARCH(data=data, p=p, q=q, dist=dist)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

def run_garch(
    df_stationary: pd.DataFrame,
    p: int = 1,
    q: int = 1,
    dist: str = "normal",
    forecast_steps: int = 5,
) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """
    Runs the GARCH model on the provided stationary DataFrame.
    
    This function fits GARCH(p,q) models to each column in the provided DataFrame 
    and generates volatility forecasts. It performs minimal logging to display only 
    core information about the model and forecasts.
    
    Args:
        df_stationary (pd.DataFrame): The stationary time series data for GARCH modeling
        p (int): The GARCH lag order, default=1
        q (int): The ARCH lag order, default=1
        dist (str): The error distribution - 'normal', 't', etc., default="normal"
        forecast_steps (int): The number of steps to forecast, default=5
        
    Returns:
        Tuple[Dict[str, Any], Dict[str, float]]: 
            - First element: Dictionary of fitted GARCH models for each column
            - Second element: Dictionary of forecasted volatility values for each column
    """
    l.info(f"\n## Running GARCH(p={p}, q={q}, dist={dist})")
    
    # Ensure data is properly prepared for time series analysis
    try:
        df_stationary = data_processor.prepare_timeseries_data(df_stationary)
    except Exception as e:
        l.error(f"Error preparing data for GARCH model: {e}")
        raise ValueError(f"Failed to prepare data for GARCH model: {str(e)}")
    
    # Check if we have enough data points for GARCH modeling (need at least p+q+1)
    min_points = p + q + 1
    if len(df_stationary) < min_points:
        raise ValueError(f"GARCH model requires at least {min_points} data points, but only {len(df_stationary)} provided")
    
    # Verify data has variance (GARCH won't work on constant data)
    for col in df_stationary.columns:
        if df_stationary[col].std() == 0:
            l.warning(f"Column {col} has zero variance, GARCH modeling may fail")
    
    # Create and fit the GARCH model
    try:
        model_garch = ModelFactory.create_model(
            model_type="GARCH",
            data=df_stationary,
            p=p,
            q=q,
            dist=dist,
        )
        garch_fit = model_garch.fit()
        
        # Log only core model information instead of full summary
        l.info(f"## GARCH model fitted to columns: {list(garch_fit.keys())}")
        
        # Generate and log forecast values concisely
        garch_forecast = model_garch.forecast(steps=forecast_steps)
        l.info(f"## GARCH {forecast_steps}-step volatility forecast:")
        for col, value in garch_forecast.items():
            if hasattr(value, 'iloc'):
                value_str = ', '.join(f"{v:.6f}" for v in value)
                l.info(f"   {col}: [{value_str}]")
            else:
                l.info(f"   {col}: {value:.6f}")
        
        return garch_fit, garch_forecast
    
    except Exception as e:
        l.error(f"Error during GARCH model fitting or forecasting: {e}")
        raise RuntimeError(f"GARCH model failed: {str(e)}")
