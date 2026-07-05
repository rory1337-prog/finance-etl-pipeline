import argparse
import pytest
from app.main import get_assets_to_process


def test_get_assets_to_process_all():
    args = argparse.Namespace(all=True, asset=None)
    assets = get_assets_to_process(args)
    assert len(assets) > 0


def test_get_assets_to_process_single_asset():
    args = argparse.Namespace(all=False, asset="BTC-USDT")
    assets = get_assets_to_process(args)
    assert len(assets) == 1
    assert assets[0]["symbol"] == "BTC-USDT"


def test_get_assets_to_process_unknown_asset():
    args = argparse.Namespace(all=False, asset="UNKNOWN-USDT")
    with pytest.raises(ValueError, match="Unknown asset"):
        get_assets_to_process(args)
