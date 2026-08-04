

import pandas as pd


buyers = pd.DataFrame(
    [
        {
            "buyer_id": 1,
            "name": "Ville de Lyon",
            "siret": "21690123100011",
        },
        {
            "buyer_id": 2,
            "name": "Métropole de Lyon",
            "siret": "20004697700012",
        },
    ]
)


suppliers = pd.DataFrame(
    [
        {
            "supplier_id": 1,
            "name": "Entreprise A",
            "siret": "12345678900011",
        },
        {
            "supplier_id": 2,
            "name": "Entreprise B",
            "siret": "98765432100022",
        },
    ]
)


contracts = pd.DataFrame(
    [
        {
            "contract_id": 1,
            "buyer_id": 1,
            "supplier_id": 1,
            "contract_value": 100000.00,
        },
        {
            "contract_id": 2,
            "buyer_id": 2,
            "supplier_id": 2,
            "contract_value": 250000.00,
        },
    ]
)

lots = pd.DataFrame(
    [
        {
            "lot_id": 1,
            "contract_id": 1,
            "description": "Construction",
            "value": 100000.00,
        },
        {
            "lot_id": 2,
            "contract_id": 2,
            "description": "Maintenance",
            "value": 250000.00,
        },
    ]
)

buyers.to_csv("data/raw/buyers.csv", sep=";")
suppliers.to_csv("data/raw/suppliers.csv", sep=";")
contracts.to_csv("data/raw/contracts.csv", sep=";")
lots.to_csv("data/raw/lots.csv", sep=";")

