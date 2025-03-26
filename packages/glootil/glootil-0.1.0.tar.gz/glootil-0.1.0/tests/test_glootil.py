import asyncio
from enum import Enum
from glootil import (
    Toolbox,
    DynEnum,
    DynTagValue,
    FixedTagValue,
    FnArg,
    NoneType,
    type_to_schema_type,
    basic_match_raw_tag_value,
    cast_json_type_to_fn_arg_type_or_default as cast_json,
)
from datetime import date

import pytest

all_months = [
    ("01", "January"),
    ("02", "February"),
    ("03", "March"),
    ("04", "April"),
    ("05", "May"),
    ("06", "June"),
    ("07", "July"),
    ("08", "August"),
    ("09", "September"),
    ("10", "October"),
    ("11", "November"),
    ("12", "December"),
]


def test_toolbox_constructor():
    t = Toolbox("math", "Math tools", "do operations on numbers")
    assert t.id == "math"
    assert t.name == "Math tools"
    assert t.docs == "do operations on numbers"


def test_tool_no_call_no_args():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def f():
        return None

    t = tb.tools[0]

    assert t.name == "f"
    assert t.docs is None
    assert len(t.args) == 0


def test_tool_no_call_no_annotations():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def add(a, b):
        return a + b

    t = tb.tools[0]

    assert t.name == "add"
    assert t.docs is None
    assert len(t.args) == 2

    a, b = t.args

    assert a.name == "a"
    assert a.index == 0
    assert a.type is None
    assert a.default_value is None

    assert b.name == "b"
    assert b.index == 1
    assert b.type is None
    assert b.default_value is None

    assert t.return_type is None


def test_tool_no_call():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def add(a: int, b: int = 0) -> int:
        "add two numbers together"
        return a + b

    t = tb.tools[0]

    assert t.name == "add"
    assert t.docs == "add two numbers together"
    assert len(t.args) == 2

    a, b = t.args

    assert a.name == "a"
    assert a.index == 0
    assert a.type is int
    assert a.default_value is None

    assert b.name == "b"
    assert b.index == 1
    assert b.type is int
    assert b.default_value == 0

    assert t.return_type is int


def test_tool_call_override_name_and_args():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool(
        name="substract", docs="my docs", args={"a": {"name": "Left"}, "b": "Right"}
    )
    def sub(a, b):
        return a - b

    t = tb.tools[0]

    assert t.name == "substract"
    assert t.docs == "my docs"
    assert len(t.args) == 2

    a, b = t.args

    assert a.label == "Left"
    assert b.label == "Right"


def test_enum_class():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Operation(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    assert len(tb.enums) == 1

    e = tb.enums[0]

    assert isinstance(e, FixedTagValue)
    assert e.name == "Operation"
    assert e.docs == "the operation to apply"
    assert len(e.variants) == 4

    add, sub, mul, div = e.variants

    assert add.name == "ADD"
    assert add.value == "add"

    assert sub.name == "SUB"
    assert sub.value == "sub"

    assert mul.name == "MUL"
    assert mul.value == "mul"

    assert div.name == "DIV"
    assert div.value == "div"

    assert e.to_info() == {
        "id": e.id,
        "name": e.name,
        "description": e.docs,
        "icon": e.icon,
        "entries": [(v.name, v.value) for v in e.variants],
        "matchHandlerId": f"enum::{e.id}::match",
    }


def test_empty_build_tool_info():
    tb = Toolbox("mytools", "My Tools", "some tools")

    assert tb.build_tool_info() == {
        "ns": "mytools",
        "title": "My Tools",
        "description": "some tools",
        "tools": {},
        "tagValues": {},
    }


def test_type_to_schema_type_int():
    assert type_to_schema_type(int, None) == ("integer", 0)
    assert type_to_schema_type(int, 42) == ("integer", 42)


def test_type_to_schema_type_float():
    assert type_to_schema_type(float, None) == ("number", 0.0)
    assert type_to_schema_type(float, 3.14) == ("number", 3.14)


def test_type_to_schema_type_str():
    assert type_to_schema_type(str, None) == ("string", "")
    assert type_to_schema_type(str, "hello") == ("string", "hello")


def test_type_to_schema_type_bool():
    assert type_to_schema_type(bool, None) == ("boolean", False)
    assert type_to_schema_type(bool, True) == ("boolean", True)


def test_type_to_schema_type_fallthrough():
    assert type_to_schema_type(list, None) == ("string", "")


def test_tool_all_types():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def all_types(
        a: int,
        b: float,
        c: bool,
        d: str,
        e: int = 10,
        f: float = 1.5,
        g: bool = True,
        h: str = "hi",
    ):
        pass

    t = tb.tools[0]

    assert t.to_info() == {
        "title": t.name,
        "description": t.docs,
        "schema": {
            "fields": {
                "a": {"type": "integer", "default": 0, "description": None},
                "b": {"type": "number", "default": 0.0, "description": None},
                "c": {"type": "boolean", "default": False, "description": None},
                "d": {"type": "string", "default": "", "description": None},
                "e": {"type": "integer", "default": 10, "description": None},
                "f": {"type": "number", "default": 1.5, "description": None},
                "g": {"type": "boolean", "default": True, "description": None},
                "h": {"type": "string", "default": "hi", "description": None},
            }
        },
        "ui": {
            "prefix": t.name,
            "args": {
                "a": {"prefix": "a"},
                "b": {"prefix": "b"},
                "c": {"prefix": "c"},
                "d": {"prefix": "d"},
                "e": {"prefix": "e"},
                "f": {"prefix": "f"},
                "g": {"prefix": "g"},
                "h": {"prefix": "h"},
            },
        },
        "examples": [],
    }


def test_toolbox_info():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool(examples=["Show all types"])
    def all_types(
        a: int,
        b: float,
        c: bool,
        d: str,
        e: int = 10,
        f: float = 1.5,
        g: bool = True,
        h: str = "hi",
    ):
        pass

    t = tb.tools[0]

    @tb.enum(id="CountryEnum", icon="flag")
    class Country(DynEnum):
        "A Country"

        @staticmethod
        def load():
            return [("ARG", "Argentina"), ("URU", "Uruguay")]

    e = tb.enums[0]

    assert tb.build_tool_info() == {
        "ns": "mytools",
        "title": "My Tools",
        "description": "some tools",
        "tools": {
            "all_types": {
                "title": t.name,
                "description": t.docs,
                "schema": {
                    "fields": {
                        "a": {"type": "integer", "default": 0, "description": None},
                        "b": {"type": "number", "default": 0.0, "description": None},
                        "c": {"type": "boolean", "default": False, "description": None},
                        "d": {"type": "string", "default": "", "description": None},
                        "e": {"type": "integer", "default": 10, "description": None},
                        "f": {"type": "number", "default": 1.5, "description": None},
                        "g": {"type": "boolean", "default": True, "description": None},
                        "h": {"type": "string", "default": "hi", "description": None},
                    }
                },
                "ui": {
                    "prefix": t.name,
                    "args": {
                        "a": {"prefix": "a"},
                        "b": {"prefix": "b"},
                        "c": {"prefix": "c"},
                        "d": {"prefix": "d"},
                        "e": {"prefix": "e"},
                        "f": {"prefix": "f"},
                        "g": {"prefix": "g"},
                        "h": {"prefix": "h"},
                    },
                },
                "examples": ["Show all types"],
            }
        },
        "tagValues": {
            "CountryEnum": {
                "id": e.id,
                "name": e.name,
                "description": e.docs,
                "icon": e.icon,
                "matchHandlerId": "enum::CountryEnum::match",
                "loadEntriesHandlerId": "enum::CountryEnum::load_entries",
            }
        },
    }


def test_basic_matcher_empty_pos():
    assert basic_match_raw_tag_value("", []) == (-1, None)


def test_basic_matcher_non_empty_pos_list():
    assert basic_match_raw_tag_value("a", [("b", "c")]) == (0, ("b", "c"))


def gen_one_posibility():
    yield ("b", "c")


def test_basic_matcher_non_empty_pos_gen():
    assert basic_match_raw_tag_value("a", gen_one_posibility()) == (0, ("b", "c"))


def gen_two_posibilities():
    yield ("b", "c")
    yield ("a", "a")


def test_basic_matcher_non_empty_pos_gen_2():
    assert basic_match_raw_tag_value("a", gen_two_posibilities()) == (1, ("a", "a"))


@pytest.mark.asyncio
async def test_enum_class_default_matcher():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Operation(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    e = tb.enums[0]

    assert await e.closest_match("ad") == ("ADD", "add")
    assert await e.closest_match("mu") == ("MUL", "mul")


@pytest.mark.asyncio
async def test_enum_class_custom_matcher():
    def matcher_always_first(_word, possibilities):
        return 0, next(iter(possibilities))

    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum(matcher=matcher_always_first)
    class Operation(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    e = tb.enums[0]

    assert e.closest_matcher == matcher_always_first
    assert await e.closest_match("") == ("ADD", "add")
    assert await e.closest_match("mul") == ("ADD", "add")


@pytest.mark.asyncio
async def test_tb_setup_with_sync_state_setup():
    class State:
        def __init__(self):
            self.v = None

        def setup(self):
            self.v = 42

    tb = Toolbox("mytools", "My Tools", "some tools", state=State())
    await tb.setup()
    assert tb.state.v == 42


@pytest.mark.asyncio
async def test_tb_setup_with_async_state_setup():
    class State:
        def __init__(self):
            self.v = None

        async def setup(self):
            await asyncio.sleep(0.010)
            self.v = 42

    tb = Toolbox("mytools", "My Tools", "some tools", state=State())
    await tb.setup()
    assert tb.state.v == 42


@pytest.mark.asyncio
async def test_tb_setup_with_no_state_setup():
    class State:
        def __init__(self):
            self.v = None

    tb = Toolbox("mytools", "My Tools", "some tools", state=State())
    await tb.setup()
    assert tb.state.v is None


@pytest.mark.asyncio
async def test_enum_class_match_handler():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Operation(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    e = tb.enums[0]

    assert tb.handlers[e.match_handler_id] == e.match_handler
    match_result = await e.match_handler(dict(value="ad"))
    assert match_result == ("ADD", "add")


def test_provide_arg_int():
    tb = Toolbox("mytools", "My Tools", "some tools")
    arg = FnArg("a", 0, int, 0)
    assert tb.provide_arg(arg, {}) == 0
    assert tb.provide_arg(arg, {"a": 5}) == 5
    assert tb.provide_arg(arg, {"a": 5.5}) == 5


def test_provide_arg_float():
    tb = Toolbox("mytools", "My Tools", "some tools")
    arg = FnArg("a", 0, float, 0)
    assert tb.provide_arg(arg, {}) == 0
    assert tb.provide_arg(arg, {"a": 5}) == 5
    assert tb.provide_arg(arg, {"a": 5.5}) == 5.5
    assert tb.provide_arg(arg, {"a": False}) == 0


def test_provide_arg_bool():
    tb = Toolbox("mytools", "My Tools", "some tools")
    arg = FnArg("a", 0, bool, False)
    assert tb.provide_arg(arg, {}) is False
    assert tb.provide_arg(arg, {"a": True}) is True
    assert tb.provide_arg(arg, {"a": 1}) is True
    assert tb.provide_arg(arg, {"a": 0}) is False


def test_provide_arg_str():
    tb = Toolbox("mytools", "My Tools", "some tools")
    arg = FnArg("a", 0, str, "hi")
    assert tb.provide_arg(arg, {}) == "hi"
    assert tb.provide_arg(arg, {"a": "hello"}) == "hello"
    assert tb.provide_arg(arg, {"a": ""}) == ""
    assert tb.provide_arg(arg, {"a": 0}) == "0"


@pytest.mark.asyncio
async def test_provide_arg_enum():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Color(Enum):
        RED = "Red"
        GREEN = "Green"
        BLUE = "Blue"

    arg = FnArg("a", 0, Color, Color.RED)
    assert await tb.provide_arg(arg, {}) == Color.RED
    assert await tb.provide_arg(arg, {"a": "BLUE"}) == Color.BLUE
    assert await tb.provide_arg(arg, {"a": "Blue"}) == Color.BLUE
    assert await tb.provide_arg(arg, {"a": "Bl"}) == Color.BLUE
    assert await tb.provide_arg(arg, {"a": "G"}) == Color.GREEN


@pytest.mark.asyncio
async def test_provide_arg_dyn_enum():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Color(DynEnum):
        @staticmethod
        def load():
            return [
                ("RED", "Red"),
                ("GREEN", "Green"),
                ("BLUE", "Blue"),
            ]

    RED = Color("RED", "Red")
    GREEN = Color("GREEN", "Green")
    BLUE = Color("BLUE", "Blue")

    arg = FnArg("a", 0, Color, RED)
    assert await tb.provide_arg(arg, {}) == RED
    assert await tb.provide_arg(arg, {"a": "BLUE"}) == BLUE
    assert await tb.provide_arg(arg, {"a": "Blue"}) == BLUE
    assert await tb.provide_arg(arg, {"a": "Bl"}) == BLUE
    assert await tb.provide_arg(arg, {"a": "G"}) == GREEN


def test_provide_arg_optional_str():
    tb = Toolbox("mytools", "My Tools", "some tools")
    arg = FnArg("a", 0, str | None, None)
    assert tb.provide_arg(arg, {}) is None
    assert tb.provide_arg(arg, {"a": "hello"}) == "hello"
    assert tb.provide_arg(arg, {"a": ""}) == ""
    assert tb.provide_arg(arg, {"a": 0}) == "0"


def test_provide_arg_optional_str_in_tool():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def f(a: str | None = "hi"):
        return a

    @tb.tool
    def g(a: None | str):
        return a

    t = tb.tools[0]
    arg = t.args[0]
    assert arg.type is str
    assert arg._isinstance_type == (str, type(None))

    t = tb.tools[1]
    arg = t.args[0]
    assert arg.type is str
    assert arg._isinstance_type == (type(None), str)


def test_dyn_enum_decoration_no_args():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Country(DynEnum):
        "A Country"

        @staticmethod
        def load():
            return [("ARG", "Argentina"), ("URU", "Uruguay")]

    assert len(tb.enums) == 1

    e = tb.enums[0]

    assert isinstance(e, DynTagValue)
    assert e.id == "Country"
    assert e.name == "Country"
    assert e.docs == "A Country"
    assert e.icon is None

    assert e.to_info() == {
        "id": e.id,
        "name": e.name,
        "description": e.docs,
        "icon": e.icon,
        "matchHandlerId": "enum::Country::match",
        "loadEntriesHandlerId": "enum::Country::load_entries",
    }


def test_dyn_enum_decoration_args():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum(id="CountryEnum", icon="flag")
    class Country(DynEnum):
        "A Country"

        @staticmethod
        def load():
            return [("ARG", "Argentina"), ("URU", "Uruguay")]

    assert len(tb.enums) == 1

    e = tb.enums[0]

    assert isinstance(e, DynTagValue)
    assert e.id == "CountryEnum"
    assert e.name == "Country"
    assert e.docs == "A Country"
    assert e.icon == "flag"

    assert e.to_info() == {
        "id": e.id,
        "name": e.name,
        "description": e.docs,
        "icon": e.icon,
        "matchHandlerId": "enum::CountryEnum::match",
        "loadEntriesHandlerId": "enum::CountryEnum::load_entries",
    }


@pytest.mark.asyncio
async def test_fn_enum_default_matcher():
    def matcher_always_first(_word, possibilities):
        return 0, next(iter(possibilities))

    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Month(DynEnum):
        @staticmethod
        def load():
            return all_months

    e = tb.enums[0]

    assert await e.closest_match("1") == ("01", "January")
    assert await e.closest_match("2") == ("02", "February")
    assert await e.closest_match("may") == ("05", "May")


@pytest.mark.asyncio
async def test_fn_enum_custom_matcher():
    def matcher_always_first(_word, possibilities):
        return 0, next(iter(possibilities))

    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum(matcher=matcher_always_first)
    class Month(DynEnum):
        @staticmethod
        def load():
            return all_months

    e = tb.enums[0]

    assert e.closest_matcher == matcher_always_first
    assert await e.closest_match("") == ("01", "January")
    assert await e.closest_match("02") == ("01", "January")
    assert await e.closest_match("May") == ("01", "January")


@pytest.mark.asyncio
async def test_dyn_enum_arg_provider_provides_state():
    class State:
        def get_variants(self):
            return all_months

    tb = Toolbox("mytools", "My Tools", "some tools", state=State())

    @tb.enum
    class Month(DynEnum):
        @staticmethod
        def load(name="Months", state: State | None = None):
            return state.get_variants() if state else []

    e = tb.enums[0]
    en = await e.get_variants()

    assert len(en) == len(all_months)
    assert en == all_months


@pytest.mark.asyncio
async def test_async_dyn_enum():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Month(DynEnum):
        "my enum description"

        @staticmethod
        async def load():
            await asyncio.sleep(0.010)
            return all_months

    assert len(tb.enums) == 1

    e = tb.enums[0]

    assert isinstance(e, DynTagValue)
    assert e.name == "Month"
    assert e.docs == "my enum description"
    assert e.icon is None
    en = await e.get_variants()
    assert len(en) == len(all_months)
    assert en == all_months


@pytest.mark.asyncio
async def test_dyn_enum_match_handler():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Operation(DynEnum):
        @staticmethod
        def load():
            return [
                ("ADD", "add"),
                ("SUB", "sub"),
                ("MUL", "mul"),
                ("DIV", "div"),
            ]

    e = tb.enums[0]

    assert tb.handlers[e.match_handler_id] == e.match_handler
    match_result = await e.match_handler(dict(value="ad"))
    assert match_result == ("ADD", "add")


def test_cast_json_from_int():
    assert cast_json(10, int, 0) == 10
    assert cast_json(10, float, 0.0) == 10.0
    assert cast_json(10, bool, False) is True
    assert cast_json(0, bool, True) is False
    assert cast_json(5, str, "") == "5"
    assert cast_json(5, date, None) is None


def test_cast_json_from_float():
    assert cast_json(10.5, float, 0) == 10.5
    assert cast_json(10.5, int, 0) == 10
    assert cast_json(10.5, bool, False) is True
    assert cast_json(0.0, bool, True) is False
    assert cast_json(5.5, str, "") == "5.5"
    assert cast_json(5, date, None) is None


def test_cast_json_from_bool():
    assert cast_json(True, bool, None) is True
    assert cast_json(False, bool, None) is False
    assert cast_json(True, int, 0) == 1
    assert cast_json(False, int, 1) == 0
    assert cast_json(True, float, 0) == 1.0
    assert cast_json(False, float, 1) == 0.0
    assert cast_json(True, str, "") == "True"
    assert cast_json(False, str, "") == "False"
    assert cast_json(True, date, None) is None


def test_cast_json_from_none():
    assert cast_json(None, NoneType, 10) is None
    assert cast_json(None, int, 10) == 10
    assert cast_json(None, float, 5.0) == 5.0
    assert cast_json(None, bool, True) is True
    assert cast_json(None, str, "nope") == "nope"
    assert cast_json(None, date, None) is None


def test_cast_json_from_str():
    assert cast_json("10.5", float, 0.0) == 10.5
    assert cast_json("10", int, 0) == 10
    assert cast_json("", bool, True) is False
    assert cast_json("whatev", bool, False) is True
    assert cast_json("hi", str, "") == "hi"
    assert cast_json("2025-03-25", date, None) == date(2025, 3, 25)
