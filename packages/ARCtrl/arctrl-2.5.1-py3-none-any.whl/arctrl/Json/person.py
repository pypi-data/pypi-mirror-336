from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.array_ import map as map_2
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import (map, default_arg)
from ..fable_modules.fable_library.seq import (map as map_1, try_pick)
from ..fable_modules.fable_library.string_ import (replace, split, join)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, resize_array, IGetters, IRequiredGetter, map as map_3, array as array_3)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from ..Core.conversion import (Person_setCommentFromORCID, Person_setOrcidFromComments)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from .comment import (encoder as encoder_1, decoder as decoder_1, ROCrate_encoderDisambiguatingDescription, ROCrate_decoderDisambiguatingDescription)
from .context.rocrate.isa_organization_context import context_jsonvalue
from .context.rocrate.isa_person_context import (context_jsonvalue as context_jsonvalue_1, context_minimal_json_value)
from .decode import Decode_objectNoAdditionalProperties
from .encode import (try_include, try_include_seq)
from .idtable import encode
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm)

__A_ = TypeVar("__A_")

def encoder(person: Person) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], person: Any=person) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2276(value: str, person: Any=person) -> IEncodable:
        class ObjectExpr2275(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2275()

    def _arrow2278(value_2: str, person: Any=person) -> IEncodable:
        class ObjectExpr2277(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2277()

    def _arrow2280(value_4: str, person: Any=person) -> IEncodable:
        class ObjectExpr2279(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2279()

    def _arrow2282(value_6: str, person: Any=person) -> IEncodable:
        class ObjectExpr2281(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr2281()

    def _arrow2284(value_8: str, person: Any=person) -> IEncodable:
        class ObjectExpr2283(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_8)

        return ObjectExpr2283()

    def _arrow2286(value_10: str, person: Any=person) -> IEncodable:
        class ObjectExpr2285(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_10)

        return ObjectExpr2285()

    def _arrow2288(value_12: str, person: Any=person) -> IEncodable:
        class ObjectExpr2287(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_12)

        return ObjectExpr2287()

    def _arrow2290(value_14: str, person: Any=person) -> IEncodable:
        class ObjectExpr2289(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_14)

        return ObjectExpr2289()

    def _arrow2292(value_16: str, person: Any=person) -> IEncodable:
        class ObjectExpr2291(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_16)

        return ObjectExpr2291()

    def _arrow2293(oa: OntologyAnnotation, person: Any=person) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow2294(comment: Comment, person: Any=person) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("firstName", _arrow2276, person.FirstName), try_include("lastName", _arrow2278, person.LastName), try_include("midInitials", _arrow2280, person.MidInitials), try_include("orcid", _arrow2282, person.ORCID), try_include("email", _arrow2284, person.EMail), try_include("phone", _arrow2286, person.Phone), try_include("fax", _arrow2288, person.Fax), try_include("address", _arrow2290, person.Address), try_include("affiliation", _arrow2292, person.Affiliation), try_include_seq("roles", _arrow2293, person.Roles), try_include_seq("comments", _arrow2294, person.Comments)]))
    class ObjectExpr2295(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any], person: Any=person) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_9.encode_object(arg)

    return ObjectExpr2295()


def _arrow2307(get: IGetters) -> Person:
    def _arrow2296(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("orcid", string)

    def _arrow2297(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("lastName", string)

    def _arrow2298(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("firstName", string)

    def _arrow2299(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("midInitials", string)

    def _arrow2300(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("email", string)

    def _arrow2301(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("phone", string)

    def _arrow2302(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("fax", string)

    def _arrow2303(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("address", string)

    def _arrow2304(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("affiliation", string)

    def _arrow2305(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_19: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("roles", arg_19)

    def _arrow2306(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_21)

    return Person(_arrow2296(), _arrow2297(), _arrow2298(), _arrow2299(), _arrow2300(), _arrow2301(), _arrow2302(), _arrow2303(), _arrow2304(), _arrow2305(), _arrow2306())


decoder: Decoder_1[Person] = object(_arrow2307)

def ROCrate_genID(p: Person) -> str:
    def chooser(c: Comment, p: Any=p) -> str | None:
        match_value: str | None = c.Name
        match_value_1: str | None = c.Value
        (pattern_matching_result, n, v) = (None, None, None)
        if match_value is not None:
            if match_value_1 is not None:
                pattern_matching_result = 0
                n = match_value
                v = match_value_1

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            if True if (True if (n == "orcid") else (n == "Orcid")) else (n == "ORCID"):
                return v

            else: 
                return None


        elif pattern_matching_result == 1:
            return None


    orcid: str | None = try_pick(chooser, p.Comments)
    if orcid is None:
        match_value_1: str | None = p.EMail
        if match_value_1 is None:
            match_value_2: str | None = p.FirstName
            match_value_3: str | None = p.MidInitials
            match_value_4: str | None = p.LastName
            (pattern_matching_result_1, fn, ln, mn, fn_1, ln_1, ln_2, fn_2) = (None, None, None, None, None, None, None, None)
            if match_value_2 is None:
                if match_value_3 is None:
                    if match_value_4 is not None:
                        pattern_matching_result_1 = 2
                        ln_2 = match_value_4

                    else: 
                        pattern_matching_result_1 = 4


                else: 
                    pattern_matching_result_1 = 4


            elif match_value_3 is None:
                if match_value_4 is None:
                    pattern_matching_result_1 = 3
                    fn_2 = match_value_2

                else: 
                    pattern_matching_result_1 = 1
                    fn_1 = match_value_2
                    ln_1 = match_value_4


            elif match_value_4 is not None:
                pattern_matching_result_1 = 0
                fn = match_value_2
                ln = match_value_4
                mn = match_value_3

            else: 
                pattern_matching_result_1 = 4

            if pattern_matching_result_1 == 0:
                return (((("#" + replace(fn, " ", "_")) + "_") + replace(mn, " ", "_")) + "_") + replace(ln, " ", "_")

            elif pattern_matching_result_1 == 1:
                return (("#" + replace(fn_1, " ", "_")) + "_") + replace(ln_1, " ", "_")

            elif pattern_matching_result_1 == 2:
                return "#" + replace(ln_2, " ", "_")

            elif pattern_matching_result_1 == 3:
                return "#" + replace(fn_2, " ", "_")

            elif pattern_matching_result_1 == 4:
                return "#EmptyPerson"


        else: 
            return match_value_1


    else: 
        return orcid



def ROCrate_Affiliation_encoder(affiliation: str) -> IEncodable:
    class ObjectExpr2309(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            return helpers.encode_string("Organization")

    def _arrow2311(__unit: None=None, affiliation: Any=affiliation) -> IEncodable:
        value_1: str = replace(("#Organization_" + affiliation) + "", " ", "_")
        class ObjectExpr2310(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr2310()

    class ObjectExpr2312(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            return helpers_2.encode_string(affiliation)

    values: FSharpList[tuple[str, IEncodable]] = of_array([("@type", ObjectExpr2309()), ("@id", _arrow2311()), ("name", ObjectExpr2312()), ("@context", context_jsonvalue)])
    class ObjectExpr2313(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_3))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping, values)
            return helpers_3.encode_object(arg)

    return ObjectExpr2313()


def _arrow2314(get: IGetters) -> str:
    object_arg: IRequiredGetter = get.Required
    return object_arg.Field("name", string)


ROCrate_Affiliation_decoder: Decoder_1[str] = object(_arrow2314)

def ROCrate_encoder(oa: Person) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2318(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2317(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2317()

    class ObjectExpr2319(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Person")

    def _arrow2321(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2320(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2320()

    def _arrow2323(value_4: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2322(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr2322()

    def _arrow2325(value_6: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2324(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_6)

        return ObjectExpr2324()

    def _arrow2327(value_8: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2326(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_8)

        return ObjectExpr2326()

    def _arrow2329(value_10: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2328(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_10)

        return ObjectExpr2328()

    def _arrow2331(value_12: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2330(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_12)

        return ObjectExpr2330()

    def _arrow2333(value_14: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2332(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_14)

        return ObjectExpr2332()

    def _arrow2335(value_16: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2334(IEncodable):
            def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
                return helpers_9.encode_string(value_16)

        return ObjectExpr2334()

    def _arrow2336(affiliation: str, oa: Any=oa) -> IEncodable:
        return ROCrate_Affiliation_encoder(affiliation)

    def _arrow2337(oa_1: OntologyAnnotation, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow2338(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoderDisambiguatingDescription(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2318()), ("@type", ObjectExpr2319()), try_include("orcid", _arrow2321, oa.ORCID), try_include("firstName", _arrow2323, oa.FirstName), try_include("lastName", _arrow2325, oa.LastName), try_include("midInitials", _arrow2327, oa.MidInitials), try_include("email", _arrow2329, oa.EMail), try_include("phone", _arrow2331, oa.Phone), try_include("fax", _arrow2333, oa.Fax), try_include("address", _arrow2335, oa.Address), try_include("affiliation", _arrow2336, oa.Affiliation), try_include_seq("roles", _arrow2337, oa.Roles), try_include_seq("comments", _arrow2338, oa.Comments), ("@context", context_jsonvalue_1)]))
    class ObjectExpr2339(IEncodable):
        def Encode(self, helpers_10: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_10))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_10.encode_object(arg)

    return ObjectExpr2339()


def _arrow2351(get: IGetters) -> Person:
    def _arrow2340(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("orcid", string)

    def _arrow2341(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("lastName", string)

    def _arrow2342(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("firstName", string)

    def _arrow2343(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("midInitials", string)

    def _arrow2344(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("email", string)

    def _arrow2345(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("phone", string)

    def _arrow2346(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("fax", string)

    def _arrow2347(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("address", string)

    def _arrow2348(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("affiliation", ROCrate_Affiliation_decoder)

    def _arrow2349(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_19: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_ROCrate_decoderDefinedTerm)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("roles", arg_19)

    def _arrow2350(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoderDisambiguatingDescription)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_21)

    return Person(_arrow2340(), _arrow2341(), _arrow2342(), _arrow2343(), _arrow2344(), _arrow2345(), _arrow2346(), _arrow2347(), _arrow2348(), _arrow2349(), _arrow2350())


ROCrate_decoder: Decoder_1[Person] = object(_arrow2351)

def ROCrate_encodeAuthorListString(author_list: str) -> IEncodable:
    def encode_single(name: str, author_list: Any=author_list) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], name: Any=name) -> tuple[str, IEncodable] | None:
            def mapping_1(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping_1, tupled_arg[1])

        class ObjectExpr2353(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], name: Any=name) -> Any:
                return helpers.encode_string("Person")

        def _arrow2355(value_1: str, name: Any=name) -> IEncodable:
            class ObjectExpr2354(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_1)

            return ObjectExpr2354()

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@type", ObjectExpr2353()), try_include("name", _arrow2355, name), ("@context", context_minimal_json_value)]))
        class ObjectExpr2356(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], name: Any=name) -> Any:
                def mapping_2(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_2, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr2356()

    def mapping(s: str, author_list: Any=author_list) -> str:
        return s.strip()

    values_2: Array[IEncodable] = map_2(encode_single, map_2(mapping, split(author_list, ["\t" if (author_list.find("\t") >= 0) else (";" if (author_list.find(";") >= 0) else ",")], None, 0), None), None)
    class ObjectExpr2357(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], author_list: Any=author_list) -> Any:
            def mapping_3(v_3: IEncodable) -> __A_:
                return v_3.Encode(helpers_3)

            arg_1: Array[__A_] = map_2(mapping_3, values_2, None)
            return helpers_3.encode_array(arg_1)

    return ObjectExpr2357()


def ctor(v: Array[str]) -> str:
    return join(", ", v)


def _arrow2359(get: IGetters) -> str:
    def _arrow2358(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("name", string)

    return default_arg(_arrow2358(), "")


ROCrate_decodeAuthorListString: Decoder_1[str] = map_3(ctor, array_3(object(_arrow2359)))

ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "firstName", "lastName", "midInitials", "email", "phone", "fax", "address", "affiliation", "roles", "comments", "@type", "@context"])

def ISAJson_encoder(id_map: Any | None, person: Person) -> IEncodable:
    def f(person_1: Person, id_map: Any=id_map, person: Any=person) -> IEncodable:
        person_2: Person = Person_setCommentFromORCID(person_1)
        def chooser(tupled_arg: tuple[str, IEncodable | None], person_1: Any=person_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2365(value: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2364(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2364()

        def _arrow2369(value_2: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2367(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2367()

        def _arrow2373(value_4: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2372(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_4)

            return ObjectExpr2372()

        def _arrow2376(value_6: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2375(IEncodable):
                def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_3.encode_string(value_6)

            return ObjectExpr2375()

        def _arrow2378(value_8: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2377(IEncodable):
                def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_4.encode_string(value_8)

            return ObjectExpr2377()

        def _arrow2381(value_10: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2380(IEncodable):
                def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_5.encode_string(value_10)

            return ObjectExpr2380()

        def _arrow2384(value_12: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2383(IEncodable):
                def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_6.encode_string(value_12)

            return ObjectExpr2383()

        def _arrow2388(value_14: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2387(IEncodable):
                def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_7.encode_string(value_14)

            return ObjectExpr2387()

        def _arrow2393(value_16: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2392(IEncodable):
                def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_8.encode_string(value_16)

            return ObjectExpr2392()

        def _arrow2394(oa: OntologyAnnotation, person_1: Any=person_1) -> IEncodable:
            return OntologyAnnotation_encoder(oa)

        def _arrow2395(comment: Comment, person_1: Any=person_1) -> IEncodable:
            return encoder_1(comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2365, ROCrate_genID(person_2)), try_include("firstName", _arrow2369, person_2.FirstName), try_include("lastName", _arrow2373, person_2.LastName), try_include("midInitials", _arrow2376, person_2.MidInitials), try_include("email", _arrow2378, person_2.EMail), try_include("phone", _arrow2381, person_2.Phone), try_include("fax", _arrow2384, person_2.Fax), try_include("address", _arrow2388, person_2.Address), try_include("affiliation", _arrow2393, person_2.Affiliation), try_include_seq("roles", _arrow2394, person_2.Roles), try_include_seq("comments", _arrow2395, person_2.Comments)]))
        class ObjectExpr2396(IEncodable):
            def Encode(self, helpers_9: IEncoderHelpers_1[Any], person_1: Any=person_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_9.encode_object(arg)

        return ObjectExpr2396()

    if id_map is not None:
        def _arrow2397(p_1: Person, id_map: Any=id_map, person: Any=person) -> str:
            return ROCrate_genID(p_1)

        return encode(_arrow2397, f, person, id_map)

    else: 
        return f(person)



def _arrow2408(get: IGetters) -> Person:
    def _arrow2398(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("lastName", string)

    def _arrow2399(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("firstName", string)

    def _arrow2400(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("midInitials", string)

    def _arrow2401(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("email", string)

    def _arrow2402(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("phone", string)

    def _arrow2403(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("fax", string)

    def _arrow2404(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("address", string)

    def _arrow2405(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("affiliation", string)

    def _arrow2406(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_17: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("roles", arg_17)

    def _arrow2407(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return Person_setOrcidFromComments(Person(None, _arrow2398(), _arrow2399(), _arrow2400(), _arrow2401(), _arrow2402(), _arrow2403(), _arrow2404(), _arrow2405(), _arrow2406(), _arrow2407()))


ISAJson_decoder: Decoder_1[Person] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2408)

__all__ = ["encoder", "decoder", "ROCrate_genID", "ROCrate_Affiliation_encoder", "ROCrate_Affiliation_decoder", "ROCrate_encoder", "ROCrate_decoder", "ROCrate_encodeAuthorListString", "ROCrate_decodeAuthorListString", "ISAJson_allowedFields", "ISAJson_encoder", "ISAJson_decoder"]

