"""Test SqliteDataset."""

import pandas as pd
import torch

from src.torchsqlite.dataset import RollingSqliteDataset, SqliteDataset


def test_dataset_len(sample_dataset: SqliteDataset, sample_dataframe: pd.DataFrame) -> None:
    """Test __len__.

    The length of db should be equal to the length of dataframe.
    """
    assert len(sample_dataset) == len(sample_dataframe)


def test_dataset_lter(sample_dataset: SqliteDataset) -> None:
    """Test __iter__ of SqliteDataset.

    The row should have torch.Tensor type and data.
    """
    for row in sample_dataset:
        assert isinstance(row, torch.Tensor) and row.shape[0] > 0


def test_rolling_dataset_lter(sample_rolling_dataset: RollingSqliteDataset) -> None:
    """Test __iter__ of RollingSqliteDataset.

    The row should have torch.Tensor type and the first dimension should have the same value of window.
    """
    for row in sample_rolling_dataset:
        assert isinstance(row, torch.Tensor) and row.shape[0] == sample_rolling_dataset.window
