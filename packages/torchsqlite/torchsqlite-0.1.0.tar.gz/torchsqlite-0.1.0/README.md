# Torchsqlite
**Sqlite based dataset for torch.**

## 1. Basic Usage
```python
import pandas as pd
from torch.utils.data import DataLoader

from torchsqlite import SqliteDataset

df = pd.DataFrame()
df["time"] = [1,2]
df["data1"] = [2,4]
df["data2"] = [20,40]

table_name = "data"
query = f"SELECT data1, data2 FROM {table_name} ORDER BY time"

dataset = SqliteDataset(filename="train.db", table_name=table_name, query=query)
for row in dataset:
    print(row)

# [2, 20]
# [4, 40]

dataloader = DataLoader(dataset, batch_size=2)
for batch in dataloader:
    print(batch)
# [[2, 20], [4, 40]]
```

## 2. Rolling dataset(usually for time series)
```python
import pandas as pd
from torch.utils.data import DataLoader

from torchsqlite import RollingSqliteDataset

df = pd.DataFrame()
df["time"] = [1,2]
df["data1"] = [2,4]
df["data2"] = [20,40]

table_name = "data"
query = f"SELECT data1, data2 FROM {table_name} ORDER BY time"

dataset = RollingSqliteDataset(filename="train.db", table_name=table_name, query=query, window=2)
for row in dataset:
    print(row)

dataloader = DataLoader(dataset, batch_size=2)
for batch in dataloader:
    print(batch)
```
