from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (of_array, FSharpList)
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (one_of, map, string, int_1, decimal, object, IRequiredGetter, IOptionalGetter, IGetters)
from ...fable_modules.thoth_json_core.types import (Decoder_1, IEncodable, IEncoderHelpers_1)
from ...ROCrate.ldobject import LDValue
from ..encode import date_time

__A_ = TypeVar("__A_")

def _arrow1857(value: str) -> Any:
    return value


def _arrow1858(value_1: int) -> Any:
    return value_1


def _arrow1859(value_2: Decimal) -> Any:
    return value_2


generic_decoder: Decoder_1[Any] = one_of(of_array([map(_arrow1857, string), map(_arrow1858, int_1), map(_arrow1859, decimal)]))

def generic_encoder(value: Any=None) -> IEncodable:
    if str(type(value)) == "<class \'str\'>":
        class ObjectExpr1860(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1860()

    elif str(type(value)) == "<class \'int\'>":
        class ObjectExpr1861(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_1.encode_signed_integral_number(value)

        return ObjectExpr1861()

    elif str(type(value)) == "<class \'bool\'>":
        class ObjectExpr1862(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_2.encode_bool(value)

        return ObjectExpr1862()

    elif str(type(value)) == "<class \'float\'>":
        class ObjectExpr1863(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_3.encode_decimal_number(value)

        return ObjectExpr1863()

    elif isinstance(value, datetime):
        return date_time(value)

    else: 
        raise Exception("Unknown type")



def _arrow1866(decoders: IGetters) -> LDValue:
    def _arrow1864(__unit: None=None) -> Any:
        object_arg: IRequiredGetter = decoders.Required
        return object_arg.Field("@value", generic_decoder)

    def _arrow1865(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = decoders.Optional
        return object_arg_1.Field("@type", string)

    return LDValue(_arrow1864(), _arrow1865())


decoder: Decoder_1[LDValue] = object(_arrow1866)

def encoder(v: LDValue) -> IEncodable:
    def _arrow1868(__unit: None=None, v: Any=v) -> IEncodable:
        value: str = v.ValueType
        class ObjectExpr1867(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1867()

    values: FSharpList[tuple[str, IEncodable]] = of_array([("@value", generic_encoder(v.Value)), ("@type", _arrow1868())])
    class ObjectExpr1869(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], v: Any=v) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr1869()


__all__ = ["generic_decoder", "generic_encoder", "decoder", "encoder"]

