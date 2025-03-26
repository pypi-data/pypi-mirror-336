import asyncio
import inspect
import typing
from difflib import SequenceMatcher
from enum import Enum
from datetime import date

UnionType = type(str | None)
NoneType = type(None)

# first level is the type of input, second is expected output type
# JSON_CASTER[from][to]
JSON_CASTERS = {
    float: {
        NoneType: lambda _v, _d: None,
        float: lambda v, _d: v,
        str: lambda v, _d: str(v),
        int: lambda v, _d: int(v),
        bool: lambda v, _d: bool(v),
        date: lambda _v, d: cast_date_default(d),
    },
    int: {
        NoneType: lambda _v, _d: None,
        int: lambda v, _d: v,
        str: lambda v, _d: str(v),
        float: lambda v, _d: float(v),
        bool: lambda v, _d: bool(v),
        date: lambda _v, d: cast_date_default(d),
    },
    str: {
        NoneType: lambda _v, _d: None,
        str: lambda v, _d: v,
        int: lambda v, d: try_cast_or(v, int, d),
        float: lambda v, d: try_cast_or(v, float, d),
        bool: lambda v, d: try_cast_or(v, bool, d),
        date: lambda v, d: try_cast_or(v, date.fromisoformat, d, cast_date_default),
    },
    bool: {
        NoneType: lambda _v, _d: None,
        bool: lambda v, _d: v,
        str: lambda v, _d: str(v),
        int: lambda v, _d: int(v),
        float: lambda v, _d: float(v),
        date: lambda _v, d: cast_date_default(d),
    },
    NoneType: {
        NoneType: lambda _v, _d: None,
        bool: lambda _v, d: d,
        str: lambda _v, d: d,
        int: lambda _v, d: d,
        float: lambda _v, d: d,
        date: lambda _v, d: cast_date_default(d),
    },
}


def cast_date_default(v):
    # TODO: handle a way to have dynamic default like "today"
    return v


def identity(v):
    return v


def try_cast_or(v, cast_fn, default, default_caster=identity):
    try:
        return cast_fn(v)
    except Exception as err:
        print("couldn't cast to", cast_fn, "returning default", err)
        return default_caster(default)


def cast_json_type_to_fn_arg_type_or_default(v, target_type, default):
    v_type = type(v)
    caster = JSON_CASTERS.get(v_type, {}).get(target_type)
    if caster:
        return caster(v, default)
    else:
        print(
            "WARN: no caster found from", v_type, "to", target_type, "returning default"
        )
        return default


class FnArg:
    def __init__(self, name, index, type_, default_value):
        self.name = name
        self.index = index
        if type_ and typing.get_origin(type_) is UnionType:
            targs = typing.get_args(type_)
            ta, tb = targs
            if len(targs) == 2 and (ta is NoneType or tb is NoneType):
                self.type = ta if tb is NoneType else tb
                self._isinstance_type = targs
            else:
                raise ValueError("FnArg type Union can only be with None")
        else:
            # assert that it's a type
            assert type_ is None or isinstance(type_, type)
            self.type = type_

            if type_ is None:
                self._isinstance_type = object
            elif type_ is float:
                self._isinstance_type = (int, float)
            else:
                self._isinstance_type = type_

        self.default_value = default_value

    def cast_json_value_or_default(self, v):
        "cast a value that came from json, handles only int, float, bool, null, string"
        return cast_json_type_to_fn_arg_type_or_default(
            v, self.type, self.default_value
        )

    def __str__(self):
        return f"{self.name}[{self.index}]: {self.type} = {self.default_value}"


class ToolArg(FnArg):
    def __init__(self, name, index, type, default_value, label=None):
        super().__init__(name, index, type, default_value)
        self.docs = None
        self.label = label or name

    def __str__(self):
        return f"{self.label}[{self.index}]: {self.type} = {self.default_value}"

    def to_schema_info(self):
        type, default = type_to_schema_type(self.type, self.default_value)
        return {
            "type": type,
            "default": default,
            "description": self.docs,
        }

    def to_ui_info(self, toolbox):
        tag_value = toolbox.enum_class_to_wrapper.get(self.type)
        if tag_value:
            return {"prefix": self.label, "dtypeName": tag_value.id}
        else:
            return {"prefix": self.label}

    def apply_overrides(self, d):
        name = d.get("name")
        docs = d.get("docs")

        if name:
            self.label = name

        if docs:
            self.docs = docs


def type_to_schema_type(t, default):
    if t is float:
        return "number", default if default is not None else 0.0
    elif t is str:
        return "string", default if default is not None else ""
    elif t is bool:
        return "boolean", default if default is not None else False
    elif t is int:
        return "integer", default if default is not None else 0
    else:
        if not (isinstance(t, type) and issubclass(t, (Enum, DynEnum))):
            print("unknown type for schema", t, default)
        return "string", ""


class FnInfo:
    def __init__(self, fn, name, docs, args, return_type=None):
        self.fn = fn
        self.name = name
        self.docs = docs
        self.args = args
        self.return_type = return_type

    def __str__(self):
        return f"def {self.name}({', '.join([str(arg) for arg in self.args])}) -> {self.return_type}:\n\t{self.docs}"

    async def call_with_args(self, args_provider, info):
        args0 = [args_provider.provide_arg(arg, info) for arg in self.args]
        # await all items in arg that needs awaiting
        args = [await arg if inspect.isawaitable(arg) else arg for arg in args0]
        return self.fn(*args)

    @classmethod
    def make_arg(cls, name, i, arg_type, arg_default):
        return FnArg(name, i, arg_type, arg_default)

    @classmethod
    def from_function(cls, fn):
        fn_name = fn.__name__
        docs = fn.__doc__
        default_count = len(fn.__defaults__ or [])
        arg_names = fn.__code__.co_varnames[: fn.__code__.co_argcount]
        arg_types = {}
        arg_defaults = {}
        return_type = None

        args = []

        if fn.__defaults__:
            default_params = arg_names[-default_count:]
            for i, param in enumerate(default_params):
                arg_defaults[param] = fn.__defaults__[i]

        for param, annotation in fn.__annotations__.items():
            if param == "return":
                return_type = annotation
            else:
                arg_types[param] = annotation

        for i, name in enumerate(arg_names):
            arg_type = arg_types.get(name)
            arg_default = arg_defaults.get(name)
            args.append(cls.make_arg(name, i, arg_type, arg_default))

        return cls(fn, fn_name, docs, args, return_type)


class Tool(FnInfo):
    def __init__(self, fn, name, docs, args, return_type=None, examples=None):
        super().__init__(fn, name, docs, args, return_type)
        self.id = name
        self.examples = examples if examples is not None else []
        self.ui_prefix = name

    @classmethod
    def make_arg(cls, name, i, arg_type, arg_default):
        return ToolArg(name, i, arg_type, arg_default)

    def to_info(self, toolbox):
        args = [arg for arg in self.args if arg.type is not toolbox.State]
        return {
            "title": self.name,
            "description": self.docs,
            "schema": {"fields": {arg.name: arg.to_schema_info() for arg in args}},
            "ui": {
                "prefix": self.ui_prefix,
                "args": {arg.name: arg.to_ui_info(toolbox) for arg in args},
            },
            "examples": self.examples,
        }

    def apply_overrides(self, d):
        id = d.get("id")
        name = d.get("name")
        docs = d.get("docs")
        args = d.get("args")
        examples = d.get("examples")
        ui_prefix = d.get("ui_prefix")

        if id:
            self.id = id

        if name:
            self.name = name

        if docs:
            self.docs = docs

        if args:
            args_by_name = {arg.name: arg for arg in self.args}
            for name, info in args.items():
                arg = args_by_name.get(name)
                if arg:
                    if isinstance(info, dict):
                        arg.apply_overrides(info)
                    elif isinstance(info, str):
                        arg.apply_overrides({"name": info})
                    else:
                        print("bad tool argument info format for argument", name, info)

                else:
                    print("tool argument info for inexistent argument name", name)

        if examples:
            self.examples = examples

        if ui_prefix:
            self.ui_prefix = ui_prefix
        elif self.ui_prefix == self.id:
            self.ui_prefix = self.name


def basic_match_raw_tag_value(word, possibilities):
    s = SequenceMatcher()
    s.set_seq2(word)

    best_key_index = -1
    best_key_ratio = -1
    best_key_pair = None

    best_value_index = -1
    best_value_ratio = -1
    best_value_pair = None

    for i, pair in enumerate(possibilities):
        key, value = pair

        s.set_seq1(key)
        key_ratio = s.ratio()
        if key_ratio > best_key_ratio:
            best_key_ratio = key_ratio
            best_key_index = i
            best_key_pair = pair

        s.set_seq1(value)
        value_ratio = s.ratio()
        if value_ratio > best_value_ratio:
            best_value_ratio = value_ratio
            best_value_index = i
            best_value_pair = pair

    if best_key_ratio > best_value_ratio:
        return best_key_index, best_key_pair
    else:
        return best_value_index, best_value_pair


def to_seq_of_pairs(seq):
    for k, v in seq:
        yield (k, v)


def to_list_of_pairs(seq):
    return list(to_seq_of_pairs(seq))


class DynEnum:
    def __init__(self, key, label):
        self.key = key
        self.label = label

    def __eq__(self, other):
        return self.key == other.key and self.label == other.label

    @staticmethod
    def load():
        return []


class TagValue:
    def __init__(self, id, name, docs, icon=None):
        self.id = id
        self.name = name
        self.docs = docs
        self.icon = None
        self.closest_matcher = basic_match_raw_tag_value

    def __str__(self):
        return f"TagValue({self.id}, {self.name}, {self.docs})"

    def to_info(self, _toolbox):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.docs,
            "icon": self.icon,
        }

    async def from_raw_arg_value(self, v):
        return await self.closest_match(str(v))

    async def match_handler(self, info):
        value = info.get("value", "")
        return await self.closest_match(value)

    async def load_handler(self, _info):
        entries = to_list_of_pairs(await self.get_variants())
        return dict(entries=entries)

    async def closest_match(self, word):
        variant_pairs = to_seq_of_pairs(await self.get_variants())
        _, pair = self.closest_matcher(word, variant_pairs)
        return pair

    async def get_variants(self):
        return []

    def apply_overrides(self, d):
        id = d.get("id")
        name = d.get("name")
        docs = d.get("docs")
        icon = d.get("icon")
        matcher = d.get("matcher")

        if id:
            self.id = id

        if name:
            self.name = name

        if docs:
            self.docs = docs

        if icon:
            self.icon = icon

        if matcher:
            self.closest_matcher = matcher

    @classmethod
    def from_enum_class(cls, Class, overrides):
        id = Class.__name__
        name = id
        docs = Class.__doc__
        variants = []
        for variant in Class:
            variants.append(Variant.from_enum_variant(variant))

        e = FixedTagValue(id, name, docs, variants, Class)
        e.apply_overrides(overrides)

        return e

    @classmethod
    def from_dyn_enum_class(cls, Class, overrides, fn_arg_provider):
        id = Class.__name__
        name = id
        docs = Class.__doc__

        load_fn_info = FnInfo.from_function(Class.load)

        e = DynTagValue(
            id,
            name,
            docs,
            Class,
            lambda: load_fn_info.call_with_args(fn_arg_provider, {}),
        )
        e.apply_overrides(overrides)

        return e


class FixedTagValue(TagValue):
    def __init__(self, id, name, docs, variants, EnumClass):
        super().__init__(id, name, docs)
        self.EnumClass = EnumClass
        self.variants = variants

    async def from_raw_arg_value(self, v):
        v = await self.closest_match(str(v))
        if v:
            key, value = v
            return self.EnumClass.__members__.get(key)

        return None

    @property
    def match_handler_id(self):
        return f"enum::{self.id}::match"

    def to_info(self, _toolbox):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.docs,
            "icon": self.icon,
            "entries": [(v.name, v.value) for v in self.variants],
            "matchHandlerId": self.match_handler_id,
        }

    def get_handlers(self):
        return [
            (self.match_handler_id, self.match_handler),
        ]

    async def get_variants(self):
        return self.variants


class DynTagValue(TagValue):
    def __init__(self, id, name, docs, EnumClass, load_fn, cache=True):
        super().__init__(id, name, docs)
        self.EnumClass = EnumClass
        self.load_fn = load_fn
        self.cache = cache
        self._cached_variants = None

    async def from_raw_arg_value(self, v):
        v = await self.closest_match(str(v))
        if v:
            key, value = v
            return self.EnumClass(key, value)

        return None

    @property
    def match_handler_id(self):
        return f"enum::{self.id}::match"

    @property
    def load_handler_id(self):
        return f"enum::{self.id}::load_entries"

    async def get_variants(self):
        if self._cached_variants:
            return self._cached_variants

        variants = await maybe_await(await self.load_fn())

        if self.cache:
            self._cached_variants = variants

        return variants

    def get_handlers(self):
        return [
            (self.match_handler_id, self.match_handler),
            (self.load_handler_id, self.load_handler),
        ]

    def to_info(self, _toolbox):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.docs,
            "icon": self.icon,
            "matchHandlerId": self.match_handler_id,
            "loadEntriesHandlerId": self.load_handler_id,
        }


class Variant:
    def __init__(self, name, value, docs=None):
        self.name = name
        self.value = value
        self.docs = docs

    def __str__(self):
        return f"Variant({self.name}, {self.value}, {self.docs})"

    def __iter__(self):
        yield self.name
        yield self.value

    @classmethod
    def from_enum_variant(cls, variant):
        name = variant.name
        value = variant.value
        docs = None

        return cls(name, value, docs)


class EmptyState:
    "State class used when no state is provided"

    def setup(self):
        "method called to setup the state before start serving"
        pass


class Toolbox:
    def __init__(self, id, name, docs, state=None):
        self.id = id
        self.name = name
        self.docs = docs

        self.tools = []
        self.enums = []
        self.enum_class_to_wrapper = {}

        self.handlers = {}

        self.state = state if state is not None else EmptyState()
        self.State = self.state.__class__

    def __str__(self):
        if self.tools:
            tools = "\n\n" + "\n\n".join([str(tool) for tool in self.tools])
        else:
            tools = ""

        return f"Toolbox({self.id}, {self.name}, {self.docs}){tools}"

    def provide_arg(self, arg, info):
        if arg.type is self.State:
            return self.state
        else:
            v = info.get(arg.name)
            if isinstance(arg.type, type) and issubclass(arg.type, (Enum, DynEnum)):
                wrapper = self.enum_class_to_wrapper.get(arg.type)
                if wrapper:
                    # NOTE: This call is async and returns an awaitable
                    return wrapper.from_raw_arg_value(v)
                else:
                    print("enum class argument type not annotated?", arg)
                    return arg.default_value
            else:
                return arg.cast_json_value_or_default(v)

    async def setup(self):
        if hasattr(self.state, "setup"):
            if inspect.iscoroutinefunction(self.state.setup):
                await self.state.setup()
            else:
                self.state.setup()

    def add_enum(self, v):
        for id, handler in v.get_handlers():
            if id in self.handlers:
                print(f"WARN: duplicated handler for id '{id}, new for enum {v}")

            self.handlers[id] = handler

        self.enum_class_to_wrapper[v.EnumClass] = v
        self.enums.append(v)

    def enum(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            arg = args[0]
            if isinstance(arg, type) and issubclass(arg, Enum):
                self.add_enum(TagValue.from_enum_class(arg, {}))
            elif isinstance(arg, type) and issubclass(arg, DynEnum):
                self.add_enum(TagValue.from_dyn_enum_class(arg, {}, self))
            else:
                raise TypeError(
                    "The decorated class must inherit from enum.Enum or DynEnum"
                )

            return arg
        else:

            def wrapper(arg):
                if isinstance(arg, type) and issubclass(arg, Enum):
                    self.add_enum(TagValue.from_enum_class(arg, kwargs))
                elif isinstance(arg, type) and issubclass(arg, DynEnum):
                    self.add_enum(TagValue.from_dyn_enum_class(arg, kwargs, self))
                else:
                    raise TypeError(
                        "The decorated class must inherit from enum.Enum or DynEnum"
                    )

                return arg

            return wrapper

    def add_tool(self, tool):
        if tool.id in self.handlers:
            print(f"WARN: duplicated handler for id '{id}, new for tool {tool}")

        arg_provider = self
        self.handlers[tool.id] = lambda info: tool.call_with_args(arg_provider, info)

        self.tools.append(tool)

    def tool(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            func = args[0]
            t = Tool.from_function(func)
            self.add_tool(t)
            return func
        else:

            def wrapper(func):
                t = Tool.from_function(func)
                t.apply_overrides(kwargs)
                self.add_tool(t)
                return func

            return wrapper

    def build_tool_info(self):
        return {
            "ns": self.id,
            "title": self.name,
            "description": self.docs,
            "tools": {tool.id: tool.to_info(self) for tool in self.tools},
            "tagValues": {
                tag_value.id: tag_value.to_info(self) for tag_value in self.enums
            },
        }

    def handle_request(self, body):
        if not isinstance(body, dict):
            return res_error("BadRequestBody", "Bad Request Body")

        action = body.get("action", None)
        if action == "info":
            return self.handle_action_info()
        elif action == "request":
            op_name = body.get("opName", None)
            req_info = body.get("info", {})
            return self.handle_action_request(op_name, req_info)
        else:
            return res_error("UnknownAction", "Unknown Action", {"action": action})

    def handle_action_info(self):
        return self.build_tool_info()

    def handle_action_request(self, op_name, req_info):
        handler = self.handlers.get(op_name)
        if handler:
            return handler(req_info)
        else:
            return res_error("ToolNotFound", "Tool Not Found", {"opName": op_name})

    def to_fastapi_app(self):
        from fastapi import FastAPI, Request
        from fastapi.encoders import jsonable_encoder
        from fastapi.responses import JSONResponse

        app = FastAPI()
        tb = self

        @app.post("/")
        async def root_gd_handler(request: Request):
            body = await request.json()
            res = await maybe_await(tb.handle_request(body))
            try:
                return JSONResponse(content=jsonable_encoder(res), status_code=200)
            except Exception as err:
                print("Error encoding response", err, res)
                err_res = res_error("InternalError", "Internal Error", {})
                return JSONResponse(content=jsonable_encoder(err_res), status_code=500)

        return app

    def serve(self, host="127.0.0.1", port=8086):
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(self.setup())
        serve_uvicorn(self.to_fastapi_app(), host, port)


def res_error(code, reason, info=None):
    return {"ok": False, "code": code, "reason": reason, "info": info}


def serve_uvicorn(app, host="127.0.0.1", port=8086):
    import uvicorn

    return uvicorn.run(app, host=host, port=port)


async def maybe_await(v):
    if inspect.isawaitable(v):
        return await v
    else:
        return v
