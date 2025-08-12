import pytest

# DOCKER BASE TESTS
def test_base_1(client, db):
    res = client.get("/api/products")
    assert res.status_code == 200

def test_base_2(client, db):
    product_id = "PR11"
    res = client.get(f"/api/products/{product_id}/contributors")
    assert res.status_code == 200

def test_base_3(client, db):
    product_id = "PR11"
    res = client.get(f"/api/products/{product_id}/details")
    assert res.status_code == 200


# CUSTOM FUNC TESTS
"""
HARDCODED THE FOLLOWING:
[
    {
        "productId": "PR32",
        "productName": "Chlorine Scranton",
        "materialId": "M3",
        "plantId": "PL2"
    }
]
"""
def test_get_product_list_with_material_and_plant(client, db):
    res = client.get("/api/products?mat_id=M3&plant_id=PL2")
    assert res.status_code == 200
    items = res.json()

    assert len(items) == 1
    assert items[0]["productId"] == "PR32"
    assert items[0]["productName"] == "Chlorine Scranton"
    assert items[0]["materialId"] == "M3"
    assert items[0]["plantId"] == "PL2"

"""
HARDCODED THE FOLLOWING:
[
    {
        "productId": "PR11",
        "productName": "Acetone Manchester",
        "materialId": "M1",
        "plantId": "PL1"
    },
    {
        "productId": "PR12",
        "productName": "Acetone Scranton",
        "materialId": "M1",
        "plantId": "PL2"
    }
]
"""
def test_get_product_list_with_material_only(client, db):
    res = client.get("/api/products?mat_id=M1")
    assert res.status_code == 200
    items = res.json()

    assert len(items) == 2
    assert items[0]["productId"] == "PR11"
    assert items[0]["productName"] == "Acetone Manchester"
    assert items[0]["materialId"] == "M1"
    assert items[0]["plantId"] == "PL1"
    assert items[1]["productId"] == "PR12"
    assert items[1]["productName"] == "Acetone Scranton"
    assert items[1]["materialId"] == "M1"
    assert items[1]["plantId"] == "PL2"

"""
HARDCODED THE FOLLOWING:
[
    {
        "productId": "PR12",
        "productName": "Acetone Scranton",
        "materialId": "M1",
        "plantId": "PL2"
    },
    {
        "productId": "PR32",
        "productName": "Chlorine Scranton",
        "materialId": "M3",
        "plantId": "PL2"
    }
]
"""
def test_get_product_list_with_plant_only(client, db):
    res = client.get("/api/products?plant_id=PL2")
    assert res.status_code == 200
    items = res.json()

    assert len(items) == 2
    assert items[0]["productId"] == "PR12"
    assert items[0]["productName"] == "Acetone Scranton"
    assert items[0]["materialId"] == "M1"
    assert items[0]["plantId"] == "PL2"
    assert items[1]["productId"] == "PR32"
    assert items[1]["productName"] == "Chlorine Scranton"
    assert items[1]["materialId"] == "M3"
    assert items[1]["plantId"] == "PL2"

"""
HARDCODED THE FOLLOWING:
[
    {
        "productId": "PR11",
        "productName": "Acetone Manchester",
        "materialId": "M1",
        "plantId": "PL1"
    },
    {
        "productId": "PR12",
        "productName": "Acetone Scranton",
        "materialId": "M1",
        "plantId": "PL2"
    },
    {
        "productId": "PR21",
        "productName": "Butene Manchester",
        "materialId": "M2",
        "plantId": "PL1"
    },
    {
        "productId": "PR32",
        "productName": "Chlorine Scranton",
        "materialId": "M3",
        "plantId": "PL2"
    },
    {
        "productId": "PR41",
        "productName": "Diorite Manchester",
        "materialId": "M4",
        "plantId": "PL1"
    }
]
"""
def test_get_product_list_with_nothing(client, db):
    res = client.get("/api/products")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 5
    assert any(item["productId"] == "PR11" for item in items)
    assert any(item["productId"] == "PR12" for item in items)
    assert any(item["productId"] == "PR21" for item in items)
    assert any(item["productId"] == "PR32" for item in items)
    assert any(item["productId"] == "PR41" for item in items)

def test_get_product_list_with_invalid_material(client, db):
    res = client.get("/api/products?mat_id=M5")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 0

"""
HARDCODED THE FOLLOWING:
[
    {
        "purchaseId": "PU11",
        "purchaseName": "Acetone from Argentina",
        "materialId": "M1",
        "countryOfOriginId": "AR",
        "quantityInKg": 100.0,
        "emissionsValue": 1.0
    },
    {
        "purchaseId": "PU13",
        "purchaseName": "Acetone from Croatia",
        "materialId": "M1",
        "countryOfOriginId": "HR",
        "quantityInKg": 100.0,
        "emissionsValue": 3.0
    }
]
"""
def test_get_product_contributors(client, db):
    
    product_id = "PR11"
    
    res = client.get(f"/api/products/{product_id}/contributors")
    assert res.status_code == 200
    item = res.json()[0]

    assert item["purchaseId"] == "PU11"
    assert item["purchaseName"] == "Acetone from Argentina"
    assert item["materialId"] == "M1"
    assert item["countryOfOriginId"] == "AR"
    assert item["quantityInKg"] == 100.0
    assert item["emissionsValue"] == 1.0

"""
HARDCODED THE FOLLOWING:

{
    "productId": "PR11",
    "productName": "Acetone Manchester",
    "materialId": "M1",
    "plantId": "PL1",
    "quantityInKg": 200.0,
    "emissionsValue": 2.0
}
"""
def test_get_product_details_all_emissions_with_weight_average(client, db):
    product_id = "PR11"

    res = client.get(f"/api/products/{product_id}/details")
    assert res.status_code == 200

    assert res.json()["productId"] == "PR11"
    assert res.json()["productName"] == "Acetone Manchester"
    assert res.json()["materialId"] == "M1"
    assert res.json()["plantId"] == "PL1"
    assert res.json()["quantityInKg"] == 200.0
    assert res.json()["emissionsValue"] == 2.0

"""
HARDCODED THE FOLLOWING:

{
    "productId": "PR41",
    "productName": "Diorite Manchester",
    "materialId": "M4",
    "plantId": "PL1",
    "quantityInKg": 100.0,
    "emissionsValue": null
}
"""
def test_get_product_details_no_contributors(client, db):

    product_id = "PR41"

    res = client.get(f"/api/products/{product_id}/details")
    assert res.status_code == 200

    assert res.json()["productId"] == "PR41"
    assert res.json()["productName"] == "Diorite Manchester"
    assert res.json()["materialId"] == "M4"
    assert res.json()["plantId"] == "PL1"
    assert res.json()["quantityInKg"] == 100.0
    assert res.json()["emissionsValue"] is None

