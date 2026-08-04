# load data as csv
from data.raw.create_dummy_data import buyers, suppliers, contracts, lots

# load the sql database engine
from Connector import engine

"""
Here the data is already taken into a pandas dataframe form
So it will be easy to construct the sql database
"""

def load_data():

    buyers.to_sql(
        "buyers",
        engine,
        if_exists="replace",
        index=False,
    )

    suppliers.to_sql(
        "suppliers",
        engine,
        if_exists="replace",
        index=False,
    )

    contracts.to_sql(
        "contracts",
        engine,
        if_exists="replace",
        index=False,
    )

    lots.to_sql(
        "lots",
        engine,
        if_exists="replace",
        index=False,
    )
        
if __name__ == "__main__":
    load_data()