import uuid

from ephemerista.assets import _asset_id


def test_asset_id(lunar_scenario):
    expected = uuid.UUID("8c8e6427-7012-495b-b83a-214e220c5e74")
    asset = lunar_scenario["CEBR"]
    assert _asset_id(asset) == expected
    assert _asset_id(asset.asset_id) == expected
