"""
Flexitricity data toolkit is a set of utility functions for loading data, and
optionally, also for interactive with data sources via SQL.

For distribution reasons `flex_dtk` is open source, but it's unlikely to be of
actual value outside the organisation.

To get up and running with `flex_dtk` you can pip install the package with:

```bash
pip install "flex_dtk[interactive]"
```

or, if you don't want to include the interactive (jupyter notebook, duckdb)
dependencies, simply:

```bash
pip install flex_dtk
```

For all functionality to work, you'll need some additional set up too:

- Azure credentials set up on your machine, this is easiest done by raising
 ticket for Azure CLI to be installed and set up on your machine.

- An MSSQL driver installed (most likely 17 or 18) in order to access the Azure
SQL database.

(You don't need a postgres driver, since `flex_dtk` uses precompiled binaries
from the `pyscopg2-binary` library).

`flex_dtk` is organised into four modules:
- datalake (functions for loading data from the datalake)
- warehouse (functions for loading data from the SQL warehouse)
- trading_db (functions for loading data from the trading database)
- interactive (optional module for interacting with the above data-sources using SQL)
"""

from flex_dtk._version import __version__  # noqa
