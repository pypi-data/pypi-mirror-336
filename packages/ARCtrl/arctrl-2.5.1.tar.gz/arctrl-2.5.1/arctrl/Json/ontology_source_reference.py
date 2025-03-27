from __future__ import annotations
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.string_ import replace
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, resize_array, IGetters)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from ..Core.ontology_source_reference import OntologySourceReference
from .comment import (encoder as encoder_1, decoder as decoder_1, ISAJson_encoder as ISAJson_encoder_1)
from .context.rocrate.isa_ontology_source_reference_context import context_jsonvalue
from .decode import Decode_uri
from .encode import (try_include, try_include_seq)

__A_ = TypeVar("__A_")

def encoder(osr: OntologySourceReference) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], osr: Any=osr) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2080(value: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr2079(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2079()

    def _arrow2082(value_2: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr2081(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2081()

    def _arrow2084(value_4: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr2083(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2083()

    def _arrow2086(value_6: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr2085(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr2085()

    def _arrow2087(comment: Comment, osr: Any=osr) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("description", _arrow2080, osr.Description), try_include("file", _arrow2082, osr.File), try_include("name", _arrow2084, osr.Name), try_include("version", _arrow2086, osr.Version), try_include_seq("comments", _arrow2087, osr.Comments)]))
    class ObjectExpr2088(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], osr: Any=osr) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2088()


def _arrow2094(get: IGetters) -> OntologySourceReference:
    def _arrow2089(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("description", Decode_uri)

    def _arrow2090(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("file", string)

    def _arrow2091(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("name", string)

    def _arrow2092(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("version", string)

    def _arrow2093(__unit: None=None) -> Array[Comment] | None:
        arg_9: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("comments", arg_9)

    return OntologySourceReference(_arrow2089(), _arrow2090(), _arrow2091(), _arrow2092(), _arrow2093())


decoder: Decoder_1[OntologySourceReference] = object(_arrow2094)

def ROCrate_genID(o: OntologySourceReference) -> str:
    match_value: str | None = o.File
    if match_value is None:
        match_value_1: str | None = o.Name
        if match_value_1 is None:
            return "#DummyOntologySourceRef"

        else: 
            return "#OntologySourceRef_" + replace(match_value_1, " ", "_")


    else: 
        return match_value



def ROCrate_encoder(osr: OntologySourceReference) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], osr: Any=osr) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2098(__unit: None=None, osr: Any=osr) -> IEncodable:
        value: str = ROCrate_genID(osr)
        class ObjectExpr2097(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2097()

    class ObjectExpr2099(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], osr: Any=osr) -> Any:
            return helpers_1.encode_string("OntologySourceReference")

    def _arrow2101(value_2: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr2100(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2100()

    def _arrow2103(value_4: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr2102(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr2102()

    def _arrow2105(value_6: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr2104(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_6)

        return ObjectExpr2104()

    def _arrow2107(value_8: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr2106(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_8)

        return ObjectExpr2106()

    def _arrow2108(comment: Comment, osr: Any=osr) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2098()), ("@type", ObjectExpr2099()), try_include("description", _arrow2101, osr.Description), try_include("file", _arrow2103, osr.File), try_include("name", _arrow2105, osr.Name), try_include("version", _arrow2107, osr.Version), try_include_seq("comments", _arrow2108, osr.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr2109(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], osr: Any=osr) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr2109()


def _arrow2115(get: IGetters) -> OntologySourceReference:
    def _arrow2110(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("description", Decode_uri)

    def _arrow2111(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("file", string)

    def _arrow2112(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("name", string)

    def _arrow2113(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("version", string)

    def _arrow2114(__unit: None=None) -> Array[Comment] | None:
        arg_9: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("comments", arg_9)

    return OntologySourceReference(_arrow2110(), _arrow2111(), _arrow2112(), _arrow2113(), _arrow2114())


ROCrate_decoder: Decoder_1[OntologySourceReference] = object(_arrow2115)

def ISAJson_encoder(id_map: Any | None, osr: OntologySourceReference) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, osr: Any=osr) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2119(value: str, id_map: Any=id_map, osr: Any=osr) -> IEncodable:
        class ObjectExpr2118(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2118()

    def _arrow2121(value_2: str, id_map: Any=id_map, osr: Any=osr) -> IEncodable:
        class ObjectExpr2120(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2120()

    def _arrow2123(value_4: str, id_map: Any=id_map, osr: Any=osr) -> IEncodable:
        class ObjectExpr2122(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2122()

    def _arrow2125(value_6: str, id_map: Any=id_map, osr: Any=osr) -> IEncodable:
        class ObjectExpr2124(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr2124()

    def _arrow2126(comment: Comment, id_map: Any=id_map, osr: Any=osr) -> IEncodable:
        return ISAJson_encoder_1(id_map, comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("description", _arrow2119, osr.Description), try_include("file", _arrow2121, osr.File), try_include("name", _arrow2123, osr.Name), try_include("version", _arrow2125, osr.Version), try_include_seq("comments", _arrow2126, osr.Comments)]))
    class ObjectExpr2127(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], id_map: Any=id_map, osr: Any=osr) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2127()


ISAJson_decoder: Decoder_1[OntologySourceReference] = decoder

__all__ = ["encoder", "decoder", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_decoder"]

