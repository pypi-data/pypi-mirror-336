# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
import requests
import time
from typing import Optional, Any
from .portfolio_analysis import PortfolioAnalysis

KUPALA_API_URL_TEST = 'https://gy3q1uyj68.execute-api.us-east-1.amazonaws.com/prod/value_portfolio'
KUPALA_API_URL = 'https://w08z5ckqt9.execute-api.us-east-1.amazonaws.com/prod/value_portfolio'

class KupalaVal:
    def __init__(self, api_key: str, vebose: bool = False):
        self._api_key = api_key
        self._verbose = vebose
        self._portfolio_analysis: Optional[PortfolioAnalysis] = None
        self._portfolio_input: list[dict] = []

    def _validate_and_clean(self) -> None :
        """
        Validates and cleans the input data.
        """
        if not self._portfolio_input:
            raise ValueError("Portfolio input data is not set.")
        
        required_columns = ["direction", "product"]
        header = self._portfolio_input[0].keys()

        missing_columns = [col for col in required_columns if col not in header]
        if missing_columns:
            raise ValueError(f'Missing required columns: {", ".join(missing_columns)}')

        for row in self._portfolio_input:
            row['fixed_rate'] = self._convert_fixed_rate( row.get('fixed_rate') )
            row['price_date'] = row.get('price_date', 'LATEST')

    def _call_api(self, msg:dict ) -> Any:
        headers = {
            'x-api-key': self._api_key,
            'Content-Type': 'application/json'
        }
        start = time.time()
        response = requests.post(KUPALA_API_URL, headers=headers, json=msg)
        if response.status_code == 403:
            raise PermissionError("403 Invalid API Key, get your API key from user settings tab of https://kupala-nich.com")
        elif response.status_code == 413:
            raise ValueError("413 Request too large, review limits in user settings tab of https://kupala-nich.com")
        elif response.status_code == 429:
            raise RuntimeError("429 Usage limit reached, review limits in user settings tab of https://kupala-nich.com")
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        if self._verbose:
            print(f"API call took {time.time() - start:.2f} seconds.")
        return response.json()
        
    def analyze(self, csv_file_path: Optional[str] = None, df:Optional[pd.DataFrame] = None ) -> Optional[PortfolioAnalysis]:
        """
        Analyzes the portfolio and returns instance of PortfolioAnalysis.
        """
        if csv_file_path is None and df is None:
            raise ValueError("Either csv_file_path or df must be provided.")
        if csv_file_path is not None:
            if not csv_file_path.endswith('.csv') or not os.path.isfile(csv_file_path):
                raise ValueError('The uploaded file is not a CSV file.')
            df = pd.read_csv(csv_file_path)

        if df is not None:
            df.replace([np.inf, -np.inf, np.nan], None, inplace=True)

            self._portfolio_input = df.to_dict(orient='records')
            if self._verbose:
                print(f"Loaded {len(self._portfolio_input)} positions from the CSV file.")
            self._validate_and_clean()
            if self._verbose:
                print("Validated and cleaned the input data.")

            data = self._call_api( { 'positions':self._portfolio_input})
            self._portfolio_analysis = PortfolioAnalysis( data, self._verbose )

        return self._portfolio_analysis

    def _convert_fixed_rate(self, value: Any) -> Any:
        if isinstance(value, str):
            value = value.strip().replace('%', '')
        if value in ['', None]:
            return None
        try:
            value = float(value)
        except ValueError:
            raise ValueError(f"Invalid fixed_rate value: {value}")
        return value / 100
