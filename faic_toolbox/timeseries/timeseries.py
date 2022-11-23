from typing import Tuple

import numpy as np
import pandas as pd


class Timeserie:
    def __init__(self, df: pd.DataFrame, test_proportion: float = 0.25) -> None:
        """Build a timeserie dataframe

        Args:
            df (pd.DataFrame): dataframe holding training and testing data
            test_proportion (float, optional): test proportion of the dataset, test set will be composed of the test_proportion*100 % last values. Defaults to 0.25.
        """
        self.df = df
        self.test_proportion = test_proportion

    def train_test_split(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split training and testing set

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Training and Testing DataFrame
        """
        train_size = 1 - int(self.df.shape[0] * self.test_proportion)
        self.train_df = self.df.iloc[:train_size, :]
        self.test_df = self.df.iloc[train_size:, :]

        return self.train_df, self.test_df

    @staticmethod
    def _get_window(df, x_features, y_features, lookback, predict_head):

        x = []
        y = []

        X = df[x_features].values
        Y = df[y_features].values

        for i in range(0, X.shape[0] - predict_head - lookback):
            x.append(X[i : i + lookback][np.newaxis, ...])
            y.append(Y[i + lookback : i + lookback + predict_head][np.newaxis, ...])

        x = np.vstack(x)
        y = np.vstack(y)

        return x, y

    def get_training(self, x_features, y_features, lookback, predict_head):
        return Timeserie._get_window(
            self.train_df, x_features, y_features, lookback, predict_head
        )

    def get_testing(self, x_features, y_features, lookback, predict_head):
        return Timeserie._get_window(
            self.test_df, x_features, y_features, lookback, predict_head
        )
