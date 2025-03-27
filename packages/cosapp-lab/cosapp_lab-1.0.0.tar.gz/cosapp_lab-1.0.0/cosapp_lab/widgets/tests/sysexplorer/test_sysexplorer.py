import pytest
from cosapp_lab.widgets import SysExplorer
from pathlib import Path
from unittest.mock import MagicMock
from cosapp_lab.widgets.chartwidget.chart_component import ChartElement


@pytest.fixture
def template_root():
    return Path(__file__).parent


def test_SysExplorer_init_single_system(SystemFactory):
    s = SystemFactory("simple")
    x = SysExplorer(s)
    assert "SysExplorer" in x.title
    assert x.chart_template == {}


def test_SysExplorer_init_multiple_systems(SystemFactory):
    a = SystemFactory("simple")
    b = SystemFactory("simple")
    x = SysExplorer([a, b])
    assert "SysExplorer" in x.title
    assert a.name not in x.title
    assert b.name not in x.title
    assert x.chart_template == {}
    assert x.sys_data.system_name == "chart_viewer"


def test_SysExplorer_init_load_template(SystemFactory, template_root):
    s = SystemFactory("simple")
    template_path = template_root / "template.json"
    x = SysExplorer(s, template=str(template_path))
    assert x.chart_template["chart_template"]["modelJson"] == {}
    assert "template.json" in x.chart_template["template_path"]


def test_SysExplorer_init_load_empty_template(SystemFactory, template_root):
    s = SystemFactory("simple")
    template_path = template_root / "empty_template.json"
    with pytest.raises(KeyError, match="Required keys \['modelJson'\] not found"):
        SysExplorer(s, template=str(template_path))


def test_SysExplorer_init_load_wrong_template(SystemFactory, template_root):
    s = SystemFactory("simple")
    template_path = template_root / "empty_template1.json"
    with pytest.raises(FileNotFoundError, match="No such template file"):
        SysExplorer(s, template=str(template_path))


def test_SysExplorer_init_component(SystemFactory):
    s = SystemFactory("simple")
    x = SysExplorer(s)
    assert "ChartElement" in x._BaseWidget__component
    assert "Controller" in x._BaseWidget__component
    assert "GeometryView" in x._BaseWidget__component
    assert len(x._BaseWidget__component) == len(x.computed_callbacks)
    assert len(x._BaseWidget__component) == len(x.msg_handlers)


def test_SysExplorer_init_value(SystemFactory):
    s = SystemFactory("simple")
    x = SysExplorer(s)
    assert x.system_config["mode"] == "run"
    assert x.system_config["enableEdit"]
    assert "simple" in x.system_config["root_name"]
    assert x._system() is s


def test_SysExplorer__init_data(SystemFactory):
    s = SystemFactory("simple")
    x = SysExplorer(s)

    assert x.system_dict[s.name] == {
        "__class__": "conftest.Simple",
        "inputs": {
            "inwards.inw": -1,
            "simple_in.number": 1,
            "simple_in.vector": None,
            "simple_in.matrix": None,
        },
        "subsystems": [],
    }
    assert x._system_list == [s.name]
    assert x._driver_list[s.name] == ["None"]
    assert x.systemGraphData[s.name] == {
        "inPort": ["inwards", "modevars_in", "simple_in"],
        "outPort": ["outwards", "modevars_out", "simple_out"],
        "connections": [],
    }


def test_computed_notification(SystemFactory):
    s = SystemFactory("simple")
    x = SysExplorer(s)
    x.computed_callbacks[0] = MagicMock()
    s.run_drivers()
    x.computed_callbacks[0].assert_called()


def test_register(SystemFactory):
    s = SystemFactory("simple")
    x = SysExplorer(s)
    with pytest.raises(KeyError, match="Component 'ChartElement' already registered"):
        x.register(ChartElement)
