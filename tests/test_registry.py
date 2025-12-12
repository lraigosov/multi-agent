import sys
from pathlib import Path

# Ensure src is on path for local runs and CI
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from multiagent.registry import registry


def test_domains_registered():
    keys = {d.key for d in registry.get_domains()}
    assert "marketing" in keys
    assert "sst" in keys


def test_crews_and_flows_discoverable():
    marketing_crews = registry.list_crews("marketing")
    sst_crews = registry.list_crews("sst")
    marketing_flows = registry.list_flows("marketing")
    sst_flows = registry.list_flows("sst")

    assert marketing_crews, "Se esperaban crews en marketing"
    assert sst_crews, "Se esperaban crews en sst"
    assert marketing_flows, "Se esperaban flows en marketing"
    assert sst_flows, "Se esperaban flows en sst"
