from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.date import (today, to_string)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList, unzip, empty)
from ..fable_modules.fable_library.option import (map, default_arg)
from ..fable_modules.fable_library.seq import (map as map_1, concat)
from ..fable_modules.fable_library.seq2 import distinct_by
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (IEnumerable_1, string_hash)
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, resize_array, IGetters, list_1 as list_1_1)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.arc_types import (ArcAssay, ArcStudy, ArcInvestigation)
from ..Core.comment import Comment
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.ontology_source_reference import OntologySourceReference
from ..Core.person import Person
from ..Core.publication import Publication
from ..Core.Table.composite_cell import CompositeCell
from .assay import (encoder as encoder_4, decoder as decoder_6, encoder_compressed as encoder_compressed_1, decoder_compressed as decoder_compressed_1)
from .comment import (encoder as encoder_6, decoder as decoder_8, ROCrate_encoder as ROCrate_encoder_5, ROCrate_decoder as ROCrate_decoder_5, ISAJson_encoder as ISAJson_encoder_5, ISAJson_decoder as ISAJson_decoder_5)
from .context.rocrate.isa_investigation_context import context_jsonvalue
from .context.rocrate.rocrate_context import (conforms_to_jsonvalue, context_jsonvalue as context_jsonvalue_1)
from .decode import Decode_objectNoAdditionalProperties
from .encode import (try_include, try_include_seq)
from .ontology_source_reference import (encoder as encoder_1, decoder as decoder_3, ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_2)
from .person import (encoder as encoder_3, decoder as decoder_5, ROCrate_encoder as ROCrate_encoder_3, ROCrate_decoder as ROCrate_decoder_4, ISAJson_encoder as ISAJson_encoder_3, ISAJson_decoder as ISAJson_decoder_4)
from .publication import (encoder as encoder_2, decoder as decoder_4, ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_3, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_3)
from .study import (encoder as encoder_5, decoder as decoder_7, encoder_compressed as encoder_compressed_2, decoder_compressed as decoder_compressed_2, ROCrate_encoder as ROCrate_encoder_4, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_4, ISAJson_decoder as ISAJson_decoder_1)

__A_ = TypeVar("__A_")

def encoder(inv: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], inv: Any=inv) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3127(__unit: None=None, inv: Any=inv) -> IEncodable:
        value: str = inv.Identifier
        class ObjectExpr3126(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3126()

    def _arrow3129(value_1: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr3128(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3128()

    def _arrow3131(value_3: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr3130(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr3130()

    def _arrow3133(value_5: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr3132(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr3132()

    def _arrow3135(value_7: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr3134(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr3134()

    def _arrow3136(osr: OntologySourceReference, inv: Any=inv) -> IEncodable:
        return encoder_1(osr)

    def _arrow3137(oa: Publication, inv: Any=inv) -> IEncodable:
        return encoder_2(oa)

    def _arrow3138(person: Person, inv: Any=inv) -> IEncodable:
        return encoder_3(person)

    def _arrow3139(assay: ArcAssay, inv: Any=inv) -> IEncodable:
        return encoder_4(assay)

    def _arrow3140(study: ArcStudy, inv: Any=inv) -> IEncodable:
        return encoder_5(study)

    def _arrow3142(value_9: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr3141(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_9)

        return ObjectExpr3141()

    def _arrow3143(comment: Comment, inv: Any=inv) -> IEncodable:
        return encoder_6(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow3127()), try_include("Title", _arrow3129, inv.Title), try_include("Description", _arrow3131, inv.Description), try_include("SubmissionDate", _arrow3133, inv.SubmissionDate), try_include("PublicReleaseDate", _arrow3135, inv.PublicReleaseDate), try_include_seq("OntologySourceReferences", _arrow3136, inv.OntologySourceReferences), try_include_seq("Publications", _arrow3137, inv.Publications), try_include_seq("Contacts", _arrow3138, inv.Contacts), try_include_seq("Assays", _arrow3139, inv.Assays), try_include_seq("Studies", _arrow3140, inv.Studies), try_include_seq("RegisteredStudyIdentifiers", _arrow3142, inv.RegisteredStudyIdentifiers), try_include_seq("Comments", _arrow3143, inv.Comments)]))
    class ObjectExpr3144(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], inv: Any=inv) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr3144()


def _arrow3157(get: IGetters) -> ArcInvestigation:
    def _arrow3145(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow3146(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("Title", string)

    def _arrow3147(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("Description", string)

    def _arrow3148(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("SubmissionDate", string)

    def _arrow3149(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("PublicReleaseDate", string)

    def _arrow3150(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_11: Decoder_1[Array[OntologySourceReference]] = resize_array(decoder_3)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("OntologySourceReferences", arg_11)

    def _arrow3151(__unit: None=None) -> Array[Publication] | None:
        arg_13: Decoder_1[Array[Publication]] = resize_array(decoder_4)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("Publications", arg_13)

    def _arrow3152(__unit: None=None) -> Array[Person] | None:
        arg_15: Decoder_1[Array[Person]] = resize_array(decoder_5)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("Contacts", arg_15)

    def _arrow3153(__unit: None=None) -> Array[ArcAssay] | None:
        arg_17: Decoder_1[Array[ArcAssay]] = resize_array(decoder_6)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("Assays", arg_17)

    def _arrow3154(__unit: None=None) -> Array[ArcStudy] | None:
        arg_19: Decoder_1[Array[ArcStudy]] = resize_array(decoder_7)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("Studies", arg_19)

    def _arrow3155(__unit: None=None) -> Array[str] | None:
        arg_21: Decoder_1[Array[str]] = resize_array(string)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("RegisteredStudyIdentifiers", arg_21)

    def _arrow3156(__unit: None=None) -> Array[Comment] | None:
        arg_23: Decoder_1[Array[Comment]] = resize_array(decoder_8)
        object_arg_11: IOptionalGetter = get.Optional
        return object_arg_11.Field("Comments", arg_23)

    return ArcInvestigation(_arrow3145(), _arrow3146(), _arrow3147(), _arrow3148(), _arrow3149(), _arrow3150(), _arrow3151(), _arrow3152(), _arrow3153(), _arrow3154(), _arrow3155(), _arrow3156())


decoder: Decoder_1[ArcInvestigation] = object(_arrow3157)

def encoder_compressed(string_table: Any, oa_table: Any, cell_table: Any, inv: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3161(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        value: str = inv.Identifier
        class ObjectExpr3160(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3160()

    def _arrow3163(value_1: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr3162(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3162()

    def _arrow3165(value_3: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr3164(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr3164()

    def _arrow3167(value_5: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr3166(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr3166()

    def _arrow3169(value_7: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr3168(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr3168()

    def _arrow3170(osr: OntologySourceReference, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_1(osr)

    def _arrow3171(oa: Publication, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_2(oa)

    def _arrow3172(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_3(person)

    def _arrow3173(assay: ArcAssay, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_compressed_1(string_table, oa_table, cell_table, assay)

    def _arrow3174(study: ArcStudy, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_compressed_2(string_table, oa_table, cell_table, study)

    def _arrow3176(value_9: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr3175(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_9)

        return ObjectExpr3175()

    def _arrow3177(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_6(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow3161()), try_include("Title", _arrow3163, inv.Title), try_include("Description", _arrow3165, inv.Description), try_include("SubmissionDate", _arrow3167, inv.SubmissionDate), try_include("PublicReleaseDate", _arrow3169, inv.PublicReleaseDate), try_include_seq("OntologySourceReferences", _arrow3170, inv.OntologySourceReferences), try_include_seq("Publications", _arrow3171, inv.Publications), try_include_seq("Contacts", _arrow3172, inv.Contacts), try_include_seq("Assays", _arrow3173, inv.Assays), try_include_seq("Studies", _arrow3174, inv.Studies), try_include_seq("RegisteredStudyIdentifiers", _arrow3176, inv.RegisteredStudyIdentifiers), try_include_seq("Comments", _arrow3177, inv.Comments)]))
    class ObjectExpr3178(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr3178()


def decoder_compressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcInvestigation]:
    def _arrow3191(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcInvestigation:
        def _arrow3179(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow3180(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("Title", string)

        def _arrow3181(__unit: None=None) -> str | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("Description", string)

        def _arrow3182(__unit: None=None) -> str | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("SubmissionDate", string)

        def _arrow3183(__unit: None=None) -> str | None:
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("PublicReleaseDate", string)

        def _arrow3184(__unit: None=None) -> Array[OntologySourceReference] | None:
            arg_11: Decoder_1[Array[OntologySourceReference]] = resize_array(decoder_3)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("OntologySourceReferences", arg_11)

        def _arrow3185(__unit: None=None) -> Array[Publication] | None:
            arg_13: Decoder_1[Array[Publication]] = resize_array(decoder_4)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("Publications", arg_13)

        def _arrow3186(__unit: None=None) -> Array[Person] | None:
            arg_15: Decoder_1[Array[Person]] = resize_array(decoder_5)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("Contacts", arg_15)

        def _arrow3187(__unit: None=None) -> Array[ArcAssay] | None:
            arg_17: Decoder_1[Array[ArcAssay]] = resize_array(decoder_compressed_1(string_table, oa_table, cell_table))
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("Assays", arg_17)

        def _arrow3188(__unit: None=None) -> Array[ArcStudy] | None:
            arg_19: Decoder_1[Array[ArcStudy]] = resize_array(decoder_compressed_2(string_table, oa_table, cell_table))
            object_arg_9: IOptionalGetter = get.Optional
            return object_arg_9.Field("Studies", arg_19)

        def _arrow3189(__unit: None=None) -> Array[str] | None:
            arg_21: Decoder_1[Array[str]] = resize_array(string)
            object_arg_10: IOptionalGetter = get.Optional
            return object_arg_10.Field("RegisteredStudyIdentifiers", arg_21)

        def _arrow3190(__unit: None=None) -> Array[Comment] | None:
            arg_23: Decoder_1[Array[Comment]] = resize_array(decoder_8)
            object_arg_11: IOptionalGetter = get.Optional
            return object_arg_11.Field("Comments", arg_23)

        return ArcInvestigation(_arrow3179(), _arrow3180(), _arrow3181(), _arrow3182(), _arrow3183(), _arrow3184(), _arrow3185(), _arrow3186(), _arrow3187(), _arrow3188(), _arrow3189(), _arrow3190())

    return object(_arrow3191)


def ROCrate_genID(i: ArcInvestigation) -> str:
    return "./"


def ROCrate_encoder(oa: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3195(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr3194(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3194()

    class ObjectExpr3196(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Investigation")

    class ObjectExpr3197(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_2.encode_string("Investigation")

    def _arrow3199(__unit: None=None, oa: Any=oa) -> IEncodable:
        value_3: str = oa.Identifier
        class ObjectExpr3198(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_3)

        return ObjectExpr3198()

    def _arrow3201(__unit: None=None, oa: Any=oa) -> IEncodable:
        value_4: str = ArcInvestigation.FileName()
        class ObjectExpr3200(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_4)

        return ObjectExpr3200()

    def _arrow3203(value_5: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3202(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_5)

        return ObjectExpr3202()

    def _arrow3205(value_7: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3204(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_7)

        return ObjectExpr3204()

    def _arrow3207(value_9: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3206(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_9)

        return ObjectExpr3206()

    def _arrow3210(__unit: None=None, oa: Any=oa) -> IEncodable:
        def _arrow3208(__unit: None=None) -> str:
            copy_of_struct: Any = today()
            return to_string(copy_of_struct, "yyyy-MM-dd")

        value_12: str = default_arg(oa.PublicReleaseDate, _arrow3208())
        class ObjectExpr3209(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_12)

        return ObjectExpr3209()

    def _arrow3211(osr: OntologySourceReference, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_1(osr)

    def _arrow3212(oa_1: Publication, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_2(oa_1)

    def _arrow3213(oa_2: Person, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_3(oa_2)

    def _arrow3214(s: ArcStudy, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_4(None, s)

    def _arrow3215(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_5(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow3195()), ("@type", ObjectExpr3196()), ("additionalType", ObjectExpr3197()), ("identifier", _arrow3199()), ("filename", _arrow3201()), try_include("title", _arrow3203, oa.Title), try_include("description", _arrow3205, oa.Description), try_include("submissionDate", _arrow3207, oa.SubmissionDate), ("publicReleaseDate", _arrow3210()), try_include_seq("ontologySourceReferences", _arrow3211, oa.OntologySourceReferences), try_include_seq("publications", _arrow3212, oa.Publications), try_include_seq("people", _arrow3213, oa.Contacts), try_include_seq("studies", _arrow3214, oa.Studies), try_include_seq("comments", _arrow3215, oa.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr3216(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_9.encode_object(arg)

    return ObjectExpr3216()


def _arrow3228(get: IGetters) -> ArcInvestigation:
    identifier: str
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("identifier", string)
    identifier = create_missing_identifier() if (match_value is None) else match_value
    def _arrow3217(__unit: None=None) -> FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]] | None:
        arg_3: Decoder_1[FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]]] = list_1_1(ROCrate_decoder_1)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("studies", arg_3)

    pattern_input: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(default_arg(_arrow3217(), empty()))
    studies_raw: FSharpList[ArcStudy] = pattern_input[0]
    def projection(a: ArcAssay) -> str:
        return a.Identifier

    class ObjectExpr3219:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow3218(x: str, y: str) -> bool:
                return x == y

            return _arrow3218

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    assays: Array[ArcAssay] = list(distinct_by(projection, concat(pattern_input[1]), ObjectExpr3219()))
    studies: Array[ArcStudy] = list(studies_raw)
    def mapping(a_1: ArcStudy) -> str:
        return a_1.Identifier

    study_identifiers: Array[str] = list(map_1(mapping, studies_raw))
    def _arrow3220(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("title", string)

    def _arrow3221(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow3222(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("submissionDate", string)

    def _arrow3223(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("publicReleaseDate", string)

    def _arrow3224(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_13: Decoder_1[Array[OntologySourceReference]] = resize_array(ROCrate_decoder_2)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("ontologySourceReferences", arg_13)

    def _arrow3225(__unit: None=None) -> Array[Publication] | None:
        arg_15: Decoder_1[Array[Publication]] = resize_array(ROCrate_decoder_3)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_15)

    def _arrow3226(__unit: None=None) -> Array[Person] | None:
        arg_17: Decoder_1[Array[Person]] = resize_array(ROCrate_decoder_4)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_17)

    def _arrow3227(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoder_5)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return ArcInvestigation(identifier, _arrow3220(), _arrow3221(), _arrow3222(), _arrow3223(), _arrow3224(), _arrow3225(), _arrow3226(), assays, studies, study_identifiers, _arrow3227())


ROCrate_decoder: Decoder_1[ArcInvestigation] = object(_arrow3228)

def ROCrate_encodeRoCrate(oa: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3232(value: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3231(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3231()

    def _arrow3234(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3233(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr3233()

    def _arrow3235(oa_1: ArcInvestigation, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder(oa_1)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@type", _arrow3232, "CreativeWork"), try_include("@id", _arrow3234, "ro-crate-metadata.json"), try_include("about", _arrow3235, oa), ("conformsTo", conforms_to_jsonvalue), ("@context", context_jsonvalue_1)]))
    class ObjectExpr3236(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_2.encode_object(arg)

    return ObjectExpr3236()


ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "filename", "identifier", "title", "description", "submissionDate", "publicReleaseDate", "ontologySourceReferences", "publications", "people", "studies", "comments", "@type", "@context"])

def ISAJson_encoder(id_map: Any | None, inv: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, inv: Any=inv) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3240(__unit: None=None, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        value: str = ROCrate_genID(inv)
        class ObjectExpr3239(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3239()

    def _arrow3242(__unit: None=None, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        value_1: str = ArcInvestigation.FileName()
        class ObjectExpr3241(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3241()

    def _arrow3244(__unit: None=None, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        value_2: str = inv.Identifier
        class ObjectExpr3243(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr3243()

    def _arrow3246(value_3: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3245(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_3)

        return ObjectExpr3245()

    def _arrow3248(value_5: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3247(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_5)

        return ObjectExpr3247()

    def _arrow3250(value_7: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3249(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_7)

        return ObjectExpr3249()

    def _arrow3252(value_9: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3251(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_9)

        return ObjectExpr3251()

    def _arrow3253(osr: OntologySourceReference, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_1(id_map, osr)

    def _arrow3254(oa: Publication, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_2(id_map, oa)

    def _arrow3255(person: Person, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_3(id_map, person)

    def _arrow3256(s: ArcStudy, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_4(id_map, None, s)

    def _arrow3257(comment: Comment, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_5(id_map, comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow3240()), ("filename", _arrow3242()), ("identifier", _arrow3244()), try_include("title", _arrow3246, inv.Title), try_include("description", _arrow3248, inv.Description), try_include("submissionDate", _arrow3250, inv.SubmissionDate), try_include("publicReleaseDate", _arrow3252, inv.PublicReleaseDate), try_include_seq("ontologySourceReferences", _arrow3253, inv.OntologySourceReferences), try_include_seq("publications", _arrow3254, inv.Publications), try_include_seq("people", _arrow3255, inv.Contacts), try_include_seq("studies", _arrow3256, inv.Studies), try_include_seq("comments", _arrow3257, inv.Comments)]))
    class ObjectExpr3258(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any], id_map: Any=id_map, inv: Any=inv) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_7))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_7.encode_object(arg)

    return ObjectExpr3258()


def _arrow3275(get: IGetters) -> ArcInvestigation:
    identifer: str
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("identifier", string)
    identifer = create_missing_identifier() if (match_value is None) else match_value
    def _arrow3260(__unit: None=None) -> FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]] | None:
        arg_3: Decoder_1[FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]]] = list_1_1(ISAJson_decoder_1)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("studies", arg_3)

    pattern_input: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(default_arg(_arrow3260(), empty()))
    studies_raw: FSharpList[ArcStudy] = pattern_input[0]
    def projection(a: ArcAssay) -> str:
        return a.Identifier

    class ObjectExpr3262:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow3261(x: str, y: str) -> bool:
                return x == y

            return _arrow3261

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    assays: Array[ArcAssay] = list(distinct_by(projection, concat(pattern_input[1]), ObjectExpr3262()))
    studies: Array[ArcStudy] = list(studies_raw)
    def mapping(a_1: ArcStudy) -> str:
        return a_1.Identifier

    study_identifiers: Array[str] = list(map_1(mapping, studies_raw))
    def _arrow3264(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("title", string)

    def _arrow3266(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow3267(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("submissionDate", string)

    def _arrow3268(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("publicReleaseDate", string)

    def _arrow3270(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_13: Decoder_1[Array[OntologySourceReference]] = resize_array(ISAJson_decoder_2)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("ontologySourceReferences", arg_13)

    def _arrow3271(__unit: None=None) -> Array[Publication] | None:
        arg_15: Decoder_1[Array[Publication]] = resize_array(ISAJson_decoder_3)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_15)

    def _arrow3272(__unit: None=None) -> Array[Person] | None:
        arg_17: Decoder_1[Array[Person]] = resize_array(ISAJson_decoder_4)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_17)

    def _arrow3274(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = resize_array(ISAJson_decoder_5)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return ArcInvestigation(identifer, _arrow3264(), _arrow3266(), _arrow3267(), _arrow3268(), _arrow3270(), _arrow3271(), _arrow3272(), assays, studies, study_identifiers, _arrow3274())


ISAJson_decoder: Decoder_1[ArcInvestigation] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow3275)

__all__ = ["encoder", "decoder", "encoder_compressed", "decoder_compressed", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ROCrate_encodeRoCrate", "ISAJson_allowedFields", "ISAJson_encoder", "ISAJson_decoder"]

