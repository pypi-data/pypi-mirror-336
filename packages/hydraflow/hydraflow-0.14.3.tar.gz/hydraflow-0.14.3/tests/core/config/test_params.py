import json
from dataclasses import dataclass, field

import pytest
from omegaconf import ListConfig, OmegaConf

from hydraflow.core.config import _is_param, iter_params


@pytest.mark.parametrize("value", (1, "string", 3.14, True))
def test_is_param_with_simple_values(value):
    assert _is_param(value) is True


def test_is_param_with_dictconfig_containing_simple_values():
    dict_conf = OmegaConf.create({"a": 1, "b": "string", "c": 3.14, "d": True})
    assert _is_param(dict_conf) is False


def test_is_param_with_listconfig_containing_simple_values():
    list_conf = OmegaConf.create([1, "string", 3.14, True])
    assert _is_param(list_conf) is True


def test_is_param_with_listconfig_containing_nested_dictconfig():
    nested_list_conf = OmegaConf.create([1, {"a": 1}, 3.14])
    assert _is_param(nested_list_conf) is False


def test_is_param_with_listconfig_containing_nested_listconfig():
    nested_list_conf_2 = OmegaConf.create([1, [2, 3], 3.14])
    assert _is_param(nested_list_conf_2) is False


def test_is_param_with_empty_dictconfig():
    empty_dict_conf = OmegaConf.create({})
    assert _is_param(empty_dict_conf) is False


def test_is_param_with_empty_listconfig():
    empty_list_conf = OmegaConf.create([])
    assert _is_param(empty_list_conf) is True


def test_is_param_with_none():
    assert _is_param(None) is True


def test_is_param_with_complex_nested_structure():
    complex_conf = OmegaConf.create({"a": [1, {"b": 2}], "c": {"d": 3}})
    assert _is_param(complex_conf) is False


def test_iter_params_with_none():
    assert not list(iter_params(None))


def test_iter_params():
    conf = OmegaConf.create({"k": "v", "l": [1, {"a": "1", "b": "2", 3: "c"}]})
    it = iter_params(conf)
    assert next(it) == ("k", "v")
    assert next(it) == ("l.0", 1)
    assert next(it) == ("l.1.a", "1")
    assert next(it) == ("l.1.b", "2")
    assert next(it) == ("l.1.3", "c")


@dataclass
class Size:
    x: int = 1
    y: int = 2


@dataclass
class Db:
    name: str = "name"
    port: int = 100


@dataclass
class Store:
    items: list[str] = field(default_factory=lambda: ["a", "b"])


@dataclass
class Config:
    size: Size = field(default_factory=Size)
    db: Db = field(default_factory=Db)
    store: Store = field(default_factory=Store)


@pytest.fixture
def cfg():
    return Config()


def test_config(cfg: Config):
    assert cfg.size.x == 1
    assert cfg.db.name == "name"
    assert cfg.store.items == ["a", "b"]


def test_iter_params_from_config(cfg):
    it = iter_params(cfg)
    assert next(it) == ("size.x", 1)
    assert next(it) == ("size.y", 2)
    assert next(it) == ("db.name", "name")
    assert next(it) == ("db.port", 100)
    assert next(it) == ("store.items", ["a", "b"])


def test_iter_params_with_empty_config():
    empty_cfg = Config(
        size=Size(x=0, y=0),
        db=Db(name="", port=0),
        store=Store(items=[]),
    )
    it = iter_params(empty_cfg)
    assert next(it) == ("size.x", 0)
    assert next(it) == ("size.y", 0)
    assert next(it) == ("db.name", "")
    assert next(it) == ("db.port", 0)
    assert next(it) == ("store.items", [])


def test_iter_params_with_nested_config():
    @dataclass
    class Nested:
        level1: Config = field(default_factory=Config)

    nested_cfg = Nested()
    it = iter_params(nested_cfg)
    assert next(it) == ("level1.size.x", 1)
    assert next(it) == ("level1.size.y", 2)
    assert next(it) == ("level1.db.name", "name")
    assert next(it) == ("level1.db.port", 100)
    assert next(it) == ("level1.store.items", ["a", "b"])


def test_iter_params_with_mixed_types_in_list():
    @dataclass
    class MixedStore:
        items: list = field(default_factory=lambda: ["a", 1, {"key": "value"}])

    mixed_cfg = MixedStore()
    it = iter_params(mixed_cfg)
    assert next(it) == ("items.0", "a")
    assert next(it) == ("items.1", 1)
    assert next(it) == ("items.2.key", "value")


def test_iter_params_dotlist():
    it = iter_params(["a=1", "b.c=2", "d.e=[1,2,3]"])
    assert next(it) == ("a", "1")
    assert next(it) == ("b.c", "2")
    assert next(it) == ("d.e", "[1,2,3]")


@pytest.mark.parametrize("type_", [int, float])
@pytest.mark.parametrize("s", ["[1, 2, 3]", "[1.0, 2.0, 3.0]"])
def test_list_config(type_, s):
    a = [type_(x) for x in [1, 2, 3]]
    b = OmegaConf.create(a)
    assert isinstance(b, ListConfig)
    t = OmegaConf.create(json.loads(s))
    assert b == t
    assert a == t


@pytest.mark.parametrize("s", ['["a", "b", "c"]'])
def test_list_config_str(s):
    a = ["a", "b", "c"]
    b = OmegaConf.create(a)
    assert isinstance(b, ListConfig)
    t = OmegaConf.create(json.loads(s))
    assert b == t
