"""Sqlite dataset."""

import sqlite3
from collections.abc import Generator

import pandas as pd
import torch
from torch.utils.data import IterableDataset


class SqliteDataset(IterableDataset[torch.Tensor]):
    """Plain sqlite dataset."""

    def __init__(self, filename: str, table_name: str, query: str, chunk_size: int = 10000) -> None:
        """Init class.

        Args:
            filename: Sqlite database name.
            table_name: Table name for sqlite database. query parameter should contain table_name.
            query: SELECT query to get generator.
            chunk_size: Sqlite fetchmany size. Defaults to 10000.

        Examples:
            ```python
            dataset = SqliteDataset("file.db", "data", "SELECT * FROM data")
            ```
        """
        super().__init__()
        self.filename = filename
        self.table_name = table_name
        self.query = query
        self.chunk_size = chunk_size

        self.conn = sqlite3.connect(self.filename)
        self.conn.isolation_level = None  # Auto commit

    def insert(self, data: pd.DataFrame) -> None:
        """Insert pandas dataframe to database.

        Args:
            data: Pandas dataframe.

        Examples:
            ```python
            df = pd.DataFrame()
            df["data"] = [1,2,3]
            dataset = SqliteDataset("file.db", "data", "SELECT * FROM data")
            dataset.insert(df)
            ```

        Raises:
            ValueError: if dataframe has missing values.
            TypeError: if invalid data is passed
        """
        if isinstance(data, pd.DataFrame):
            if data.isna().to_numpy().any():
                raise ValueError("Found NA/NAN values. Check df.data.isna()")
        else:
            raise TypeError("data must be pd.DataFrame.")
        data.to_sql(name=self.table_name, con=self.conn, if_exists="append", index=False)

    def __iter__(self) -> Generator[torch.Tensor]:
        """Returns torch tensor data.

        Yields:
            Generator: torch.Tensor data.

        Examples:
            ```python
            df = pd.DataFrame()
            df["data"] = [1,2,3]
            dataset = SqliteDataset("file.db", "data", "SELECT * FROM data")
            dataset.insert(df)
            for row in dataset:
                print(row)
            ```
        """
        cursor = self.conn.cursor()
        cursor.execute(self.query)

        while True:
            if not (chunk := cursor.fetchmany(self.chunk_size)):
                cursor.close()
                break
            tensor = torch.tensor(chunk)
            yield from tensor

    def __len__(self) -> int:
        """Calculate the total number of data.

        Raises:
            ValueError: if the query result is not number.

        Returns:
            int: The value of COUNT(*) query result.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        count = cursor.fetchone()[0]
        cursor.close()

        if isinstance(count, int):
            return count
        else:
            raise ValueError("Sqlite cannot count rows due to unknown error.")


class RollingSqliteDataset(SqliteDataset):
    """Rolling sqlite dataset for time series model like LSTM or Transformer."""

    def __init__(self, filename: str, table_name: str, query: str, window: int, chunk_size: int = 10000) -> None:
        """Init class.

        Args:
            filename: Sqlite database name.
            table_name: Table name for sqlite database. query parameter should contain table_name.
            query: SELECT query to get generator.
            window: Rolling value.
            chunk_size: Sqlite fetchmany size. Defaults to 10000.

        Examples:
            ```python
            dataset = SqliteDataset("file.db", "data", "SELECT * FROM data", 2)
            ```
        """
        super().__init__(filename=filename, table_name=table_name, query=query, chunk_size=chunk_size)
        self.window = window

    def __iter__(self) -> Generator[torch.Tensor]:
        """Returns rolled torch tensor data.

        Yields:
            Generator: torch.Tensor data.

        Examples:
            ```python
            df = pd.DataFrame()
            df["data"] = [1,2,3]
            dataset = SqliteDataset("file.db", "data", "SELECT * FROM data", 2)
            dataset.insert(df)
            for row in dataset:
                print(row)
            ```
        """
        cursor = self.conn.cursor()
        cursor.execute(self.query)

        while True:
            if not (chunk := cursor.fetchmany(self.chunk_size)):
                cursor.close()
                break
            tensor = torch.tensor(chunk)
            rolled_tensor = tensor.unfold(0, self.window, 1)
            # Basically trasformer layer like nn.Transformer takes tensors with shape of (batch_size, window, features).
            # So chunk is transposed to have shape of (window, features).
            transposed_chunk = rolled_tensor.transpose(1, 2)
            yield from transposed_chunk
