from __future__ import annotations
from collections.abc import Callable
from typing import Any
from .fable_modules.fable_library.array_ import (choose, try_pick, exactly_one, map, filter, iterate, exists, fold, concat, contains as contains_2, append as append_1)
from .fable_modules.fable_library.async_ import run_synchronously
from .fable_modules.fable_library.async_builder import (Async, singleton)
from .fable_modules.fable_library.list import FSharpList
from .fable_modules.fable_library.map import of_seq as of_seq_1
from .fable_modules.fable_library.map_util import add_to_dict
from .fable_modules.fable_library.option import (value as value_2, default_arg, map as map_2, bind)
from .fable_modules.fable_library.reflection import (TypeInfo, class_type)
from .fable_modules.fable_library.result import FSharpResult_2
from .fable_modules.fable_library.seq import (to_array, contains, delay, append, singleton as singleton_1, map as map_1, iterate as iterate_1, try_find, find, empty, collect, to_list)
from .fable_modules.fable_library.set import (of_seq, contains as contains_1, union_many, FSharpSet__Contains)
from .fable_modules.fable_library.string_ import (starts_with_exact, replace, join, to_fail, printf, to_text)
from .fable_modules.fable_library.types import Array
from .fable_modules.fable_library.util import (string_hash, IEnumerable_1, compare_primitives, curry2, safe_hash, to_enumerable)
from .fable_modules.fs_spreadsheet.Cells.fs_cells_collection import Dictionary_tryGet
from .fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from .fable_modules.thoth_json_core.types import IEncodable
from .Contract.arc import try_isaread_contract_from_path
from .Contract.arc_assay import (ARCtrl_ArcAssay__ArcAssay_tryFromReadContract_Static_7570923F, ARCtrl_ArcAssay__ArcAssay_ToDeleteContract, ARCtrl_ArcAssay__ArcAssay_ToCreateContract_6FCE9E49, ARCtrl_ArcAssay__ArcAssay_ToUpdateContract)
from .Contract.arc_investigation import (ARCtrl_ArcInvestigation__ArcInvestigation_tryFromReadContract_Static_7570923F, ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract)
from .Contract.arc_study import (ARCtrl_ArcStudy__ArcStudy_tryFromReadContract_Static_7570923F, ARCtrl_ArcStudy__ArcStudy_ToUpdateContract, ARCtrl_ArcStudy__ArcStudy_ToCreateContract_6FCE9E49)
from .Contract.contract import (Contract, DTOType, DTO)
from .Contract.datamap import (ARCtrl_DataMap__DataMap_tryFromReadContractForAssay_Static, ARCtrl_DataMap__DataMap_tryFromReadContractForStudy_Static, ARCtrl_DataMap__DataMap_ToCreateContractForStudy_Z721C83C5, ARCtrl_DataMap__DataMap_ToUpdateContractForStudy_Z721C83C5, ARCtrl_DataMap__DataMap_ToCreateContractForAssay_Z721C83C5, ARCtrl_DataMap__DataMap_ToUpdateContractForAssay_Z721C83C5)
from .Contract.git import (Init_createInitContract_6DFDD678, gitattributes_contract, gitignore_contract, Init_createAddRemoteContract_Z721C83C5, Clone_createCloneContract_5000466F)
from .Contract.validation_packages_config import (ValidationPackagesConfigHelper_ConfigFilePath, ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toCreateContract_Static_724DAE55, ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toDeleteContract_Static_724DAE55, ValidationPackagesConfigHelper_ReadContract, ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_tryFromReadContract_Static_7570923F)
from .Core.arc_types import (ArcAssay, ArcStudy, ArcInvestigation)
from .Core.data import Data
from .Core.data_context import DataContext
from .Core.data_map import (DataMap, DataMap__get_DataContexts, DataMap__set_StaticHash_Z524259A4, DataMap__get_StaticHash)
from .Core.Helper.identifier import (Study_fileNameFromIdentifier, Study_datamapFileNameFromIdentifier, Assay_fileNameFromIdentifier, Assay_datamapFileNameFromIdentifier)
from .Core.Table.arc_table import ArcTable
from .Core.Table.arc_tables import ArcTables
from .Core.Table.composite_cell import CompositeCell
from .Core.Table.composite_column import CompositeColumn
from .FileSystem.file_system import FileSystem
from .FileSystem.file_system_tree import FileSystemTree
from .FileSystem.path import (get_assay_folder_path, get_study_folder_path)
from .Json.encode import default_spaces
from .Spreadsheet.arc_assay import ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F
from .Spreadsheet.arc_investigation import ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF
from .Spreadsheet.arc_study import ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522
from .Spreadsheet.data_map import to_fs_workbook
from .ValidationPackages.validation_packages_config import ValidationPackagesConfig
from .ContractIO.contract_io import full_fill_contract_batch_async
from .ContractIO.file_system_helper import get_all_file_paths_async
from .fable_modules.thoth_json_python.decode import Decode_fromString
from .fable_modules.thoth_json_python.encode import to_string
from .rocrate_io import (ROCrate_get_decoderDeprecated, ROCrate_get_decoder, ROCrate_encoder_8A8D439)

def ARCAux_getArcAssaysFromContracts(contracts: Array[Contract]) -> Array[ArcAssay]:
    def chooser(c: Contract, contracts: Any=contracts) -> ArcAssay | None:
        return ARCtrl_ArcAssay__ArcAssay_tryFromReadContract_Static_7570923F(c)

    return choose(chooser, contracts, None)


def ARCAux_getAssayDataMapFromContracts(assay_identifier: str, contracts: Array[Contract]) -> DataMap | None:
    def chooser(c: Contract, assay_identifier: Any=assay_identifier, contracts: Any=contracts) -> DataMap | None:
        return ARCtrl_DataMap__DataMap_tryFromReadContractForAssay_Static(assay_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getArcStudiesFromContracts(contracts: Array[Contract]) -> Array[tuple[ArcStudy, FSharpList[ArcAssay]]]:
    def chooser(c: Contract, contracts: Any=contracts) -> tuple[ArcStudy, FSharpList[ArcAssay]] | None:
        return ARCtrl_ArcStudy__ArcStudy_tryFromReadContract_Static_7570923F(c)

    return choose(chooser, contracts, None)


def ARCAux_getStudyDataMapFromContracts(study_identifier: str, contracts: Array[Contract]) -> DataMap | None:
    def chooser(c: Contract, study_identifier: Any=study_identifier, contracts: Any=contracts) -> DataMap | None:
        return ARCtrl_DataMap__DataMap_tryFromReadContractForStudy_Static(study_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getArcInvestigationFromContracts(contracts: Array[Contract]) -> ArcInvestigation:
    def chooser(c: Contract, contracts: Any=contracts) -> ArcInvestigation | None:
        return ARCtrl_ArcInvestigation__ArcInvestigation_tryFromReadContract_Static_7570923F(c)

    return exactly_one(choose(chooser, contracts, None))


def ARCAux_updateFSByISA(isa: ArcInvestigation | None, fs: FileSystem) -> FileSystem:
    pattern_input: tuple[Array[ArcStudy], Array[ArcAssay]]
    if isa is None:
        pattern_input = ([], [])

    else: 
        inv: ArcInvestigation = isa
        pattern_input = (to_array(inv.Studies), to_array(inv.Assays))

    assays_folder: FileSystemTree
    def mapping(a: ArcAssay, isa: Any=isa, fs: Any=fs) -> FileSystemTree:
        return FileSystemTree.create_assay_folder(a.Identifier, a.DataMap is not None)

    assays_1: Array[FileSystemTree] = map(mapping, pattern_input[1], None)
    assays_folder = FileSystemTree.create_assays_folder(assays_1)
    studies_folder: FileSystemTree
    def mapping_1(s: ArcStudy, isa: Any=isa, fs: Any=fs) -> FileSystemTree:
        return FileSystemTree.create_study_folder(s.Identifier, s.DataMap is not None)

    studies_1: Array[FileSystemTree] = map(mapping_1, pattern_input[0], None)
    studies_folder = FileSystemTree.create_studies_folder(studies_1)
    investigation: FileSystemTree = FileSystemTree.create_investigation_file()
    tree_1: FileSystem
    tree: FileSystemTree = FileSystemTree.create_root_folder([investigation, assays_folder, studies_folder])
    tree_1 = FileSystem.create(tree = tree)
    return fs.Union(tree_1)


def ARCAux_updateFSByCWL(cwl: None | None, fs: FileSystem) -> FileSystem:
    workflows: FileSystemTree = FileSystemTree.create_workflows_folder([])
    runs: FileSystemTree = FileSystemTree.create_runs_folder([])
    tree_1: FileSystem
    tree: FileSystemTree = FileSystemTree.create_root_folder([workflows, runs])
    tree_1 = FileSystem.create(tree = tree)
    return fs.Union(tree_1)


def _expr3684() -> TypeInfo:
    return class_type("ARCtrl.ARC", None, ARC)


class ARC:
    def __init__(self, isa: ArcInvestigation | None=None, cwl: None | None=None, fs: FileSystem | None=None) -> None:
        self.cwl: None | None = cwl
        self._isa: ArcInvestigation | None = isa
        self._cwl: None | None = self.cwl
        self._fs: FileSystem = ARCAux_updateFSByCWL(self.cwl, ARCAux_updateFSByISA(isa, default_arg(fs, FileSystem.create(tree = FileSystemTree(1, "", [])))))

    @property
    def ISA(self, __unit: None=None) -> ArcInvestigation | None:
        this: ARC = self
        return this._isa

    @ISA.setter
    def ISA(self, new_isa: ArcInvestigation | None=None) -> None:
        this: ARC = self
        this._isa = new_isa
        this.UpdateFileSystem()

    @property
    def CWL(self, __unit: None=None) -> None | None:
        this: ARC = self
        return this.cwl

    @property
    def FileSystem(self, __unit: None=None) -> FileSystem:
        this: ARC = self
        return this._fs

    @FileSystem.setter
    def FileSystem(self, fs: FileSystem) -> None:
        this: ARC = self
        this._fs = fs

    def TryWriteAsync(self, arc_path: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetWriteContracts())

    def TryUpdateAsync(self, arc_path: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetUpdateContracts())

    @staticmethod
    def try_load_async(arc_path: str) -> Async[FSharpResult_2[ARC, Array[str]]]:
        def _arrow3596(__unit: None=None) -> Async[FSharpResult_2[ARC, Array[str]]]:
            def _arrow3595(_arg: Array[str]) -> Async[FSharpResult_2[ARC, Array[str]]]:
                arc: ARC = ARC.from_file_paths(to_array(_arg))
                contracts: Array[Contract] = arc.GetReadContracts()
                def _arrow3594(_arg_1: FSharpResult_2[Array[Contract], Array[str]]) -> Async[FSharpResult_2[ARC, Array[str]]]:
                    ful_filled_contracts: FSharpResult_2[Array[Contract], Array[str]] = _arg_1
                    if ful_filled_contracts.tag == 1:
                        return singleton.Return(FSharpResult_2(1, ful_filled_contracts.fields[0]))

                    else: 
                        arc.SetISAFromContracts(ful_filled_contracts.fields[0])
                        return singleton.Return(FSharpResult_2(0, arc))


                return singleton.Bind(full_fill_contract_batch_async(arc_path, contracts), _arrow3594)

            return singleton.Bind(get_all_file_paths_async(arc_path), _arrow3595)

        return singleton.Delay(_arrow3596)

    def GetAssayRemoveContracts(self, assay_identifier: str) -> Array[Contract]:
        this: ARC = self
        isa: ArcInvestigation
        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            raise Exception("Cannot remove assay from null ISA value.")

        else: 
            def _arrow3599(__unit: None=None) -> bool:
                i: ArcInvestigation = match_value
                class ObjectExpr3598:
                    @property
                    def Equals(self) -> Callable[[str, str], bool]:
                        def _arrow3597(x: str, y: str) -> bool:
                            return x == y

                        return _arrow3597

                    @property
                    def GetHashCode(self) -> Callable[[str], int]:
                        return string_hash

                return contains(assay_identifier, i.AssayIdentifiers, ObjectExpr3598())

            if _arrow3599():
                i_1: ArcInvestigation = match_value
                isa = i_1

            else: 
                raise Exception("ARC does not contain assay with given name")


        assay: ArcAssay = isa.GetAssay(assay_identifier)
        studies: Array[ArcStudy] = assay.StudiesRegisteredIn
        isa.RemoveAssay(assay_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        assay_folder_path: str = get_assay_folder_path(assay_identifier)
        def predicate(p: str) -> bool:
            return not starts_with_exact(p, assay_folder_path)

        filtered_paths: Array[str] = filter(predicate, paths)
        this.SetFilePaths(filtered_paths)
        def _arrow3602(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow3601(__unit: None=None) -> IEnumerable_1[Contract]:
                def _arrow3600(__unit: None=None) -> IEnumerable_1[Contract]:
                    return map_1(ARCtrl_ArcStudy__ArcStudy_ToUpdateContract, studies)

                return append(singleton_1(ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract(isa)), delay(_arrow3600))

            return append(singleton_1(ARCtrl_ArcAssay__ArcAssay_ToDeleteContract(assay)), delay(_arrow3601))

        return to_array(delay(_arrow3602))

    def TryRemoveAssayAsync(self, arc_path: str, assay_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetAssayRemoveContracts(assay_identifier))

    def GetAssayRenameContracts(self, old_assay_identifier: str, new_assay_identifier: str) -> Array[Contract]:
        this: ARC = self
        isa: ArcInvestigation
        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            raise Exception("Cannot rename assay in null ISA value.")

        else: 
            def _arrow3605(__unit: None=None) -> bool:
                i: ArcInvestigation = match_value
                class ObjectExpr3604:
                    @property
                    def Equals(self) -> Callable[[str, str], bool]:
                        def _arrow3603(x: str, y: str) -> bool:
                            return x == y

                        return _arrow3603

                    @property
                    def GetHashCode(self) -> Callable[[str], int]:
                        return string_hash

                return contains(old_assay_identifier, i.AssayIdentifiers, ObjectExpr3604())

            if _arrow3605():
                i_1: ArcInvestigation = match_value
                isa = i_1

            else: 
                raise Exception("ARC does not contain assay with given name")


        isa.RenameAssay(old_assay_identifier, new_assay_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        old_assay_folder_path: str = get_assay_folder_path(old_assay_identifier)
        new_assay_folder_path: str = get_assay_folder_path(new_assay_identifier)
        def mapping(p: str) -> str:
            return replace(p, old_assay_folder_path, new_assay_folder_path)

        renamed_paths: Array[str] = map(mapping, paths, None)
        this.SetFilePaths(renamed_paths)
        def _arrow3607(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow3606(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton_1(Contract.create_rename(old_assay_folder_path, new_assay_folder_path)), delay(_arrow3606))

        return to_array(delay(_arrow3607))

    def TryRenameAssayAsync(self, arc_path: str, old_assay_identifier: str, new_assay_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetAssayRenameContracts(old_assay_identifier, new_assay_identifier))

    def GetStudyRemoveContracts(self, study_identifier: str) -> Array[Contract]:
        this: ARC = self
        isa: ArcInvestigation
        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            raise Exception("Cannot remove study from null ISA value.")

        else: 
            isa = match_value

        isa.RemoveStudy(study_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        study_folder_path: str = get_study_folder_path(study_identifier)
        def predicate(p: str) -> bool:
            return not starts_with_exact(p, study_folder_path)

        filtered_paths: Array[str] = filter(predicate, paths)
        this.SetFilePaths(filtered_paths)
        return [Contract.create_delete(study_folder_path), ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract(isa)]

    def TryRemoveStudyAsync(self, arc_path: str, study_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetStudyRemoveContracts(study_identifier))

    def GetStudyRenameContracts(self, old_study_identifier: str, new_study_identifier: str) -> Array[Contract]:
        this: ARC = self
        isa: ArcInvestigation
        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            raise Exception("Cannot rename study in null ISA value.")

        else: 
            def _arrow3610(__unit: None=None) -> bool:
                i: ArcInvestigation = match_value
                class ObjectExpr3609:
                    @property
                    def Equals(self) -> Callable[[str, str], bool]:
                        def _arrow3608(x: str, y: str) -> bool:
                            return x == y

                        return _arrow3608

                    @property
                    def GetHashCode(self) -> Callable[[str], int]:
                        return string_hash

                return contains(old_study_identifier, i.StudyIdentifiers, ObjectExpr3609())

            if _arrow3610():
                i_1: ArcInvestigation = match_value
                isa = i_1

            else: 
                raise Exception("ARC does not contain study with given name")


        isa.RenameStudy(old_study_identifier, new_study_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        old_study_folder_path: str = get_study_folder_path(old_study_identifier)
        new_study_folder_path: str = get_study_folder_path(new_study_identifier)
        def mapping(p: str) -> str:
            return replace(p, old_study_folder_path, new_study_folder_path)

        renamed_paths: Array[str] = map(mapping, paths, None)
        this.SetFilePaths(renamed_paths)
        def _arrow3612(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow3611(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton_1(Contract.create_rename(old_study_folder_path, new_study_folder_path)), delay(_arrow3611))

        return to_array(delay(_arrow3612))

    def TryRenameStudyAsync(self, arc_path: str, old_study_identifier: str, new_study_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetStudyRenameContracts(old_study_identifier, new_study_identifier))

    def WriteAsync(self, arc_path: str) -> Async[None]:
        this: ARC = self
        def _arrow3614(__unit: None=None) -> Async[None]:
            def _arrow3613(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not write ARC, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryWriteAsync(arc_path), _arrow3613)

        return singleton.Delay(_arrow3614)

    def UpdateAsync(self, arc_path: str) -> Async[None]:
        this: ARC = self
        def _arrow3616(__unit: None=None) -> Async[None]:
            def _arrow3615(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not update ARC, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryUpdateAsync(arc_path), _arrow3615)

        return singleton.Delay(_arrow3616)

    def RemoveAssayAsync(self, arc_path: str, assay_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow3618(__unit: None=None) -> Async[None]:
            def _arrow3617(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not remove assay, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRemoveAssayAsync(arc_path, assay_identifier), _arrow3617)

        return singleton.Delay(_arrow3618)

    def RenameAssayAsync(self, arc_path: str, old_assay_identifier: str, new_assay_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow3620(__unit: None=None) -> Async[None]:
            def _arrow3619(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not rename assay, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRenameAssayAsync(arc_path, old_assay_identifier, new_assay_identifier), _arrow3619)

        return singleton.Delay(_arrow3620)

    def RemoveStudyAsync(self, arc_path: str, study_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow3622(__unit: None=None) -> Async[None]:
            def _arrow3621(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not remove study, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRemoveStudyAsync(arc_path, study_identifier), _arrow3621)

        return singleton.Delay(_arrow3622)

    def RenameStudyAsync(self, arc_path: str, old_study_identifier: str, new_study_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow3624(__unit: None=None) -> Async[None]:
            def _arrow3623(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not rename study, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRenameStudyAsync(arc_path, old_study_identifier, new_study_identifier), _arrow3623)

        return singleton.Delay(_arrow3624)

    @staticmethod
    def load_async(arc_path: str) -> Async[ARC]:
        def _arrow3626(__unit: None=None) -> Async[ARC]:
            def _arrow3625(_arg: FSharpResult_2[ARC, Array[str]]) -> Async[ARC]:
                result: FSharpResult_2[ARC, Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not load ARC, failed with the following errors %s"))(appended)
                    return singleton.Return(ARC())

                else: 
                    return singleton.Return(result.fields[0])


            return singleton.Bind(ARC.try_load_async(arc_path), _arrow3625)

        return singleton.Delay(_arrow3626)

    def Write(self, arc_path: str) -> None:
        this: ARC = self
        run_synchronously(this.WriteAsync(arc_path))

    def Update(self, arc_path: str) -> None:
        this: ARC = self
        run_synchronously(this.UpdateAsync(arc_path))

    def RemoveAssay(self, arc_path: str, assay_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RemoveAssayAsync(arc_path, assay_identifier))

    def RenameAssay(self, arc_path: str, old_assay_identifier: str, new_assay_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RenameAssayAsync(arc_path, old_assay_identifier, new_assay_identifier))

    def RemoveStudy(self, arc_path: str, study_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RemoveStudyAsync(arc_path, study_identifier))

    def RenameStudy(self, arc_path: str, old_study_identifier: str, new_study_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RenameStudyAsync(arc_path, old_study_identifier, new_study_identifier))

    @staticmethod
    def load(arc_path: str) -> ARC:
        return run_synchronously(ARC.load_async(arc_path))

    def MakeDataFilesAbsolute(self, __unit: None=None) -> None:
        this: ARC = self
        class ObjectExpr3627:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        files_paths: Any = of_seq(this.FileSystem.Tree.ToFilePaths(), ObjectExpr3627())
        def check_existence_from_root(p: str) -> bool:
            return contains_1(p, files_paths)

        def update_column_option(data_name_function: Callable[[Data], str], col: CompositeColumn | None=None) -> None:
            (pattern_matching_result, col_2) = (None, None)
            if col is not None:
                def _arrow3628(__unit: None=None, data_name_function: Any=data_name_function, col: Any=col) -> bool:
                    col_1: CompositeColumn = col
                    return col_1.Header.IsDataColumn

                if _arrow3628():
                    pattern_matching_result = 0
                    col_2 = col

                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1

            if pattern_matching_result == 0:
                def action(c: CompositeCell, data_name_function: Any=data_name_function, col: Any=col) -> None:
                    if c.AsData.FilePath is not None:
                        new_file_path: str = data_name_function(c.AsData)
                        c.AsData.FilePath = new_file_path


                iterate(action, col_2.Cells)

            elif pattern_matching_result == 1:
                pass


        def update_table(data_name_function_1: Callable[[Data], str], t: ArcTable) -> None:
            update_column_option(data_name_function_1, t.TryGetInputColumn())
            update_column_option(data_name_function_1, t.TryGetOutputColumn())

        def update_data_map(data_name_function_2: Callable[[Data], str], dm: DataMap) -> None:
            def action_1(c_1: DataContext, data_name_function_2: Any=data_name_function_2, dm: Any=dm) -> None:
                if c_1.FilePath is not None:
                    new_file_path_1: str = data_name_function_2(c_1)
                    c_1.FilePath = new_file_path_1


            iterate_1(action_1, DataMap__get_DataContexts(dm))

        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            pass

        else: 
            inv: ArcInvestigation = match_value
            def action_3(s: ArcStudy) -> None:
                def f(d: Data, s: Any=s) -> str:
                    return d.GetAbsolutePathForStudy(s.Identifier, check_existence_from_root)

                source_1: Array[ArcTable] = s.Tables
                iterate_1(curry2(update_table)(f), source_1)
                if s.DataMap is not None:
                    update_data_map(f, value_2(s.DataMap))


            iterate_1(action_3, inv.Studies)
            def action_5(a: ArcAssay) -> None:
                def f_1(d_1: Data, a: Any=a) -> str:
                    return d_1.GetAbsolutePathForAssay(a.Identifier, check_existence_from_root)

                source_3: Array[ArcTable] = a.Tables
                iterate_1(curry2(update_table)(f_1), source_3)
                if a.DataMap is not None:
                    update_data_map(f_1, value_2(a.DataMap))


            iterate_1(action_5, inv.Assays)


    @staticmethod
    def from_file_paths(file_paths: Array[str]) -> ARC:
        return ARC(None, None, FileSystem.from_file_paths(file_paths))

    def SetFilePaths(self, file_paths: Array[str]) -> None:
        this: ARC = self
        tree: FileSystemTree = FileSystemTree.from_file_paths(file_paths)
        this._fs = FileSystem(tree, this._fs.History)

    def GetReadContracts(self, __unit: None=None) -> Array[Contract]:
        this: ARC = self
        return choose(try_isaread_contract_from_path, this._fs.Tree.ToFilePaths(), None)

    def SetISAFromContracts(self, contracts: Array[Contract]) -> None:
        this: ARC = self
        investigation: ArcInvestigation = ARCAux_getArcInvestigationFromContracts(contracts)
        def mapping(tuple: tuple[ArcStudy, FSharpList[ArcAssay]]) -> ArcStudy:
            return tuple[0]

        studies: Array[ArcStudy] = map(mapping, ARCAux_getArcStudiesFromContracts(contracts), None)
        assays: Array[ArcAssay] = ARCAux_getArcAssaysFromContracts(contracts)
        def action(ai: str) -> None:
            def predicate(a: ArcAssay, ai: Any=ai) -> bool:
                return a.Identifier == ai

            if not exists(predicate, assays):
                investigation.DeleteAssay(ai)


        iterate(action, investigation.AssayIdentifiers)
        def action_1(si: str) -> None:
            def predicate_1(s: ArcStudy, si: Any=si) -> bool:
                return s.Identifier == si

            if not exists(predicate_1, studies):
                investigation.DeleteStudy(si)


        iterate(action_1, investigation.StudyIdentifiers)
        def action_2(study: ArcStudy) -> None:
            def predicate_2(s_1: ArcStudy, study: Any=study) -> bool:
                return s_1.Identifier == study.Identifier

            registered_study_opt: ArcStudy | None = try_find(predicate_2, investigation.Studies)
            if registered_study_opt is None:
                investigation.AddStudy(study)

            else: 
                registered_study: ArcStudy = registered_study_opt
                registered_study.UpdateReferenceByStudyFile(study, True)

            datamap: DataMap | None = ARCAux_getAssayDataMapFromContracts(study.Identifier, contracts)
            if study.DataMap is None:
                study.DataMap = datamap

            study.StaticHash = study.GetLightHashCode() or 0

        iterate(action_2, studies)
        def action_3(assay: ArcAssay) -> None:
            def predicate_3(a_1: ArcAssay, assay: Any=assay) -> bool:
                return a_1.Identifier == assay.Identifier

            registered_assay_opt: ArcAssay | None = try_find(predicate_3, investigation.Assays)
            if registered_assay_opt is None:
                investigation.AddAssay(assay)

            else: 
                registered_assay: ArcAssay = registered_assay_opt
                registered_assay.UpdateReferenceByAssayFile(assay, True)

            def predicate_4(a_2: ArcAssay, assay: Any=assay) -> bool:
                return a_2.Identifier == assay.Identifier

            assay_1: ArcAssay = find(predicate_4, investigation.Assays)
            updated_tables: ArcTables
            array_6: Array[ArcStudy] = assay_1.StudiesRegisteredIn
            def folder(tables: ArcTables, study_1: ArcStudy, assay: Any=assay) -> ArcTables:
                return ArcTables.update_reference_tables_by_sheets(ArcTables(study_1.Tables), tables, False)

            updated_tables = fold(folder, ArcTables(assay_1.Tables), array_6)
            datamap_1: DataMap | None = ARCAux_getAssayDataMapFromContracts(assay_1.Identifier, contracts)
            if assay_1.DataMap is None:
                assay_1.DataMap = datamap_1

            assay_1.Tables = updated_tables.Tables

        iterate(action_3, assays)
        def action_4(a_3: ArcAssay) -> None:
            a_3.StaticHash = a_3.GetLightHashCode() or 0

        iterate_1(action_4, investigation.Assays)
        def action_5(s_2: ArcStudy) -> None:
            s_2.StaticHash = s_2.GetLightHashCode() or 0

        iterate_1(action_5, investigation.Studies)
        investigation.StaticHash = investigation.GetLightHashCode() or 0
        this.ISA = investigation

    def UpdateFileSystem(self, __unit: None=None) -> None:
        this: ARC = self
        new_fs: FileSystem
        fs: FileSystem = ARCAux_updateFSByISA(this._isa, this._fs)
        new_fs = ARCAux_updateFSByCWL(this._cwl, fs)
        this._fs = new_fs

    def GetWriteContracts(self, __unit: None=None) -> Array[Contract]:
        this: ARC = self
        workbooks: Any = dict([])
        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            add_to_dict(workbooks, "isa.investigation.xlsx", (DTOType(2), ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF(ArcInvestigation.create("MISSING_IDENTIFIER_"))))

        else: 
            inv: ArcInvestigation = match_value
            add_to_dict(workbooks, "isa.investigation.xlsx", (DTOType(2), ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF(inv)))
            inv.StaticHash = inv.GetLightHashCode() or 0
            def action(s: ArcStudy) -> None:
                s.StaticHash = s.GetLightHashCode() or 0
                add_to_dict(workbooks, Study_fileNameFromIdentifier(s.Identifier), (DTOType(1), ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522(s)))
                if s.DataMap is not None:
                    dm: DataMap = value_2(s.DataMap)
                    DataMap__set_StaticHash_Z524259A4(dm, safe_hash(dm))
                    add_to_dict(workbooks, Study_datamapFileNameFromIdentifier(s.Identifier), (DTOType(3), to_fs_workbook(dm)))


            iterate_1(action, inv.Studies)
            def action_1(a: ArcAssay) -> None:
                a.StaticHash = a.GetLightHashCode() or 0
                add_to_dict(workbooks, Assay_fileNameFromIdentifier(a.Identifier), (DTOType(0), ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F(a)))
                if a.DataMap is not None:
                    dm_1: DataMap = value_2(a.DataMap)
                    DataMap__set_StaticHash_Z524259A4(dm_1, safe_hash(dm_1))
                    add_to_dict(workbooks, Assay_datamapFileNameFromIdentifier(a.Identifier), (DTOType(3), to_fs_workbook(dm_1)))


            iterate_1(action_1, inv.Assays)

        def mapping(fp: str) -> Contract:
            match_value_1: tuple[DTOType, FsWorkbook] | None = Dictionary_tryGet(fp, workbooks)
            if match_value_1 is None:
                return Contract.create_create(fp, DTOType(8))

            else: 
                wb: FsWorkbook = match_value_1[1]
                dto: DTOType = match_value_1[0]
                return Contract.create_create(fp, dto, DTO(0, wb))


        return map(mapping, this._fs.Tree.ToFilePaths(True), None)

    def GetUpdateContracts(self, __unit: None=None) -> Array[Contract]:
        this: ARC = self
        match_value: ArcInvestigation | None = this.ISA
        def _arrow3629(__unit: None=None) -> bool:
            inv: ArcInvestigation = match_value
            return inv.StaticHash == 0

        def _arrow3630(__unit: None=None) -> Array[Contract]:
            inv_1: ArcInvestigation = match_value
            return this.GetWriteContracts()

        def _arrow3644(__unit: None=None) -> Array[Contract]:
            inv_2: ArcInvestigation = match_value
            def _arrow3643(__unit: None=None) -> IEnumerable_1[Contract]:
                hash_1: int = inv_2.GetLightHashCode() or 0
                def _arrow3642(__unit: None=None) -> IEnumerable_1[Contract]:
                    inv_2.StaticHash = hash_1 or 0
                    def _arrow3635(s: ArcStudy) -> IEnumerable_1[Contract]:
                        hash_2: int = s.GetLightHashCode() or 0
                        def _arrow3634(__unit: None=None) -> IEnumerable_1[Contract]:
                            s.StaticHash = hash_2 or 0
                            match_value_1: DataMap | None = s.DataMap
                            (pattern_matching_result, dm_2, dm_3) = (None, None, None)
                            if match_value_1 is not None:
                                if DataMap__get_StaticHash(match_value_1) == 0:
                                    pattern_matching_result = 0
                                    dm_2 = match_value_1

                                else: 
                                    def _arrow3633(__unit: None=None) -> bool:
                                        dm_1: DataMap = match_value_1
                                        return DataMap__get_StaticHash(dm_1) != safe_hash(dm_1)

                                    if _arrow3633():
                                        pattern_matching_result = 1
                                        dm_3 = match_value_1

                                    else: 
                                        pattern_matching_result = 2



                            else: 
                                pattern_matching_result = 2

                            if pattern_matching_result == 0:
                                def _arrow3631(__unit: None=None) -> IEnumerable_1[Contract]:
                                    DataMap__set_StaticHash_Z524259A4(dm_2, safe_hash(dm_2))
                                    return empty()

                                return append(singleton_1(ARCtrl_DataMap__DataMap_ToCreateContractForStudy_Z721C83C5(dm_2, s.Identifier)), delay(_arrow3631))

                            elif pattern_matching_result == 1:
                                def _arrow3632(__unit: None=None) -> IEnumerable_1[Contract]:
                                    DataMap__set_StaticHash_Z524259A4(dm_3, safe_hash(dm_3))
                                    return empty()

                                return append(singleton_1(ARCtrl_DataMap__DataMap_ToUpdateContractForStudy_Z721C83C5(dm_3, s.Identifier)), delay(_arrow3632))

                            elif pattern_matching_result == 2:
                                return empty()


                        return append(ARCtrl_ArcStudy__ArcStudy_ToCreateContract_6FCE9E49(s, True) if (s.StaticHash == 0) else (singleton_1(ARCtrl_ArcStudy__ArcStudy_ToUpdateContract(s)) if (s.StaticHash != hash_2) else empty()), delay(_arrow3634))

                    def _arrow3641(__unit: None=None) -> IEnumerable_1[Contract]:
                        def _arrow3640(a: ArcAssay) -> IEnumerable_1[Contract]:
                            hash_3: int = a.GetLightHashCode() or 0
                            def _arrow3639(__unit: None=None) -> IEnumerable_1[Contract]:
                                a.StaticHash = hash_3 or 0
                                match_value_2: DataMap | None = a.DataMap
                                (pattern_matching_result_1, dm_6, dm_7) = (None, None, None)
                                if match_value_2 is not None:
                                    if DataMap__get_StaticHash(match_value_2) == 0:
                                        pattern_matching_result_1 = 0
                                        dm_6 = match_value_2

                                    else: 
                                        def _arrow3638(__unit: None=None) -> bool:
                                            dm_5: DataMap = match_value_2
                                            return DataMap__get_StaticHash(dm_5) != safe_hash(dm_5)

                                        if _arrow3638():
                                            pattern_matching_result_1 = 1
                                            dm_7 = match_value_2

                                        else: 
                                            pattern_matching_result_1 = 2



                                else: 
                                    pattern_matching_result_1 = 2

                                if pattern_matching_result_1 == 0:
                                    def _arrow3636(__unit: None=None) -> IEnumerable_1[Contract]:
                                        DataMap__set_StaticHash_Z524259A4(dm_6, safe_hash(dm_6))
                                        return empty()

                                    return append(singleton_1(ARCtrl_DataMap__DataMap_ToCreateContractForAssay_Z721C83C5(dm_6, a.Identifier)), delay(_arrow3636))

                                elif pattern_matching_result_1 == 1:
                                    def _arrow3637(__unit: None=None) -> IEnumerable_1[Contract]:
                                        DataMap__set_StaticHash_Z524259A4(dm_7, safe_hash(dm_7))
                                        return empty()

                                    return append(singleton_1(ARCtrl_DataMap__DataMap_ToUpdateContractForAssay_Z721C83C5(dm_7, a.Identifier)), delay(_arrow3637))

                                elif pattern_matching_result_1 == 2:
                                    return empty()


                            return append(ARCtrl_ArcAssay__ArcAssay_ToCreateContract_6FCE9E49(a, True) if (a.StaticHash == 0) else (singleton_1(ARCtrl_ArcAssay__ArcAssay_ToUpdateContract(a)) if (a.StaticHash != hash_3) else empty()), delay(_arrow3639))

                        return collect(_arrow3640, inv_2.Assays)

                    return append(collect(_arrow3635, inv_2.Studies), delay(_arrow3641))

                return append(singleton_1(ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract(inv_2)) if (inv_2.StaticHash != hash_1) else empty(), delay(_arrow3642))

            return to_array(delay(_arrow3643))

        return (_arrow3630() if _arrow3629() else _arrow3644()) if (match_value is not None) else this.GetWriteContracts()

    def GetGitInitContracts(self, branch: str | None=None, repository_address: str | None=None, default_gitignore: bool | None=None) -> Array[Contract]:
        default_gitignore_1: bool = default_arg(default_gitignore, False)
        def _arrow3648(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow3647(__unit: None=None) -> IEnumerable_1[Contract]:
                def _arrow3646(__unit: None=None) -> IEnumerable_1[Contract]:
                    def _arrow3645(__unit: None=None) -> IEnumerable_1[Contract]:
                        return singleton_1(Init_createAddRemoteContract_Z721C83C5(value_2(repository_address))) if (repository_address is not None) else empty()

                    return append(singleton_1(gitignore_contract) if default_gitignore_1 else empty(), delay(_arrow3645))

                return append(singleton_1(gitattributes_contract), delay(_arrow3646))

            return append(singleton_1(Init_createInitContract_6DFDD678(branch)), delay(_arrow3647))

        return to_array(delay(_arrow3648))

    @staticmethod
    def get_clone_contract(remote_url: str, merge: bool | None=None, branch: str | None=None, token: tuple[str, str] | None=None, nolfs: bool | None=None) -> Contract:
        return Clone_createCloneContract_5000466F(remote_url, merge, branch, token, nolfs)

    def Copy(self, __unit: None=None) -> ARC:
        this: ARC = self
        def mapping(i: ArcInvestigation) -> ArcInvestigation:
            return i.Copy()

        isa_copy: ArcInvestigation | None = map_2(mapping, this._isa)
        fs_copy: FileSystem = this._fs.Copy()
        return ARC(isa_copy, this._cwl, fs_copy)

    def GetRegisteredPayload(self, IgnoreHidden: bool | None=None) -> FileSystemTree:
        this: ARC = self
        def mapping_1(isa: ArcInvestigation) -> Array[ArcStudy]:
            return isa.Studies[:]

        def mapping(i: ArcInvestigation) -> ArcInvestigation:
            return i.Copy()

        registered_studies: Array[ArcStudy] = default_arg(map_2(mapping_1, map_2(mapping, this._isa)), [])
        def mapping_2(s: ArcStudy) -> Array[ArcAssay]:
            return s.RegisteredAssays[:]

        registered_assays: Array[ArcAssay] = concat(map(mapping_2, registered_studies, None), None)
        class ObjectExpr3649:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        def mapping_3(s_1: ArcStudy) -> Any:
            study_foldername: str = ((("" + "studies") + "/") + s_1.Identifier) + ""
            def _arrow3656(__unit: None=None, s_1: Any=s_1) -> IEnumerable_1[str]:
                def _arrow3655(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow3654(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow3653(table: ArcTable) -> IEnumerable_1[str]:
                            def _arrow3652(kv: Any) -> IEnumerable_1[str]:
                                text_value: str = kv[1].ToFreeTextCell().AsFreeText
                                def _arrow3651(__unit: None=None) -> IEnumerable_1[str]:
                                    def _arrow3650(__unit: None=None) -> IEnumerable_1[str]:
                                        return singleton_1(((((("" + study_foldername) + "/") + "protocols") + "/") + text_value) + "")

                                    return append(singleton_1(((((("" + study_foldername) + "/") + "resources") + "/") + text_value) + ""), delay(_arrow3650))

                                return append(singleton_1(text_value), delay(_arrow3651))

                            return collect(_arrow3652, table.Values)

                        return collect(_arrow3653, s_1.Tables)

                    return append(singleton_1(((("" + study_foldername) + "/") + "README.md") + ""), delay(_arrow3654))

                return append(singleton_1(((("" + study_foldername) + "/") + "isa.study.xlsx") + ""), delay(_arrow3655))

            class ObjectExpr3657:
                @property
                def Compare(self) -> Callable[[str, str], int]:
                    return compare_primitives

            return of_seq(to_list(delay(_arrow3656)), ObjectExpr3657())

        class ObjectExpr3658:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        def mapping_4(a: ArcAssay) -> Any:
            assay_foldername: str = ((("" + "assays") + "/") + a.Identifier) + ""
            def _arrow3665(__unit: None=None, a: Any=a) -> IEnumerable_1[str]:
                def _arrow3664(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow3663(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow3662(table_1: ArcTable) -> IEnumerable_1[str]:
                            def _arrow3661(kv_1: Any) -> IEnumerable_1[str]:
                                text_value_1: str = kv_1[1].ToFreeTextCell().AsFreeText
                                def _arrow3660(__unit: None=None) -> IEnumerable_1[str]:
                                    def _arrow3659(__unit: None=None) -> IEnumerable_1[str]:
                                        return singleton_1(((((("" + assay_foldername) + "/") + "protocols") + "/") + text_value_1) + "")

                                    return append(singleton_1(((((("" + assay_foldername) + "/") + "dataset") + "/") + text_value_1) + ""), delay(_arrow3659))

                                return append(singleton_1(text_value_1), delay(_arrow3660))

                            return collect(_arrow3661, table_1.Values)

                        return collect(_arrow3662, a.Tables)

                    return append(singleton_1(((("" + assay_foldername) + "/") + "README.md") + ""), delay(_arrow3663))

                return append(singleton_1(((("" + assay_foldername) + "/") + "isa.assay.xlsx") + ""), delay(_arrow3664))

            class ObjectExpr3666:
                @property
                def Compare(self) -> Callable[[str, str], int]:
                    return compare_primitives

            return of_seq(to_list(delay(_arrow3665)), ObjectExpr3666())

        class ObjectExpr3667:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        class ObjectExpr3668:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        include_files: Any = union_many(to_enumerable([of_seq(to_enumerable(["isa.investigation.xlsx", "README.md"]), ObjectExpr3649()), union_many(map(mapping_3, registered_studies, None), ObjectExpr3658()), union_many(map(mapping_4, registered_assays, None), ObjectExpr3667())]), ObjectExpr3668())
        ignore_hidden: bool = default_arg(IgnoreHidden, True)
        fs_copy: FileSystem = this._fs.Copy()
        def binder(tree_1: FileSystemTree) -> FileSystemTree | None:
            if ignore_hidden:
                def _arrow3669(n_1: str, tree_1: Any=tree_1) -> bool:
                    return not starts_with_exact(n_1, ".")

                return FileSystemTree.filter_folders(_arrow3669)(tree_1)

            else: 
                return tree_1


        def _arrow3671(__unit: None=None) -> FileSystemTree | None:
            tree: FileSystemTree
            def predicate(p: str) -> bool:
                if True if starts_with_exact(p, "workflows") else starts_with_exact(p, "runs"):
                    return True

                else: 
                    return FSharpSet__Contains(include_files, p)


            paths: Array[str] = filter(predicate, FileSystemTree.to_file_paths()(fs_copy.Tree))
            tree = FileSystemTree.from_file_paths(paths)
            def _arrow3670(n: str) -> bool:
                return not starts_with_exact(n, ".")

            return FileSystemTree.filter_files(_arrow3670)(tree) if ignore_hidden else tree

        return default_arg(bind(binder, _arrow3671()), FileSystemTree.from_file_paths([]))

    def GetAdditionalPayload(self, IgnoreHidden: bool | None=None) -> FileSystemTree:
        this: ARC = self
        ignore_hidden: bool = default_arg(IgnoreHidden, True)
        class ObjectExpr3672:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        registered_payload: Any = of_seq(FileSystemTree.to_file_paths()(this.GetRegisteredPayload()), ObjectExpr3672())
        def binder(tree_1: FileSystemTree) -> FileSystemTree | None:
            if ignore_hidden:
                def _arrow3673(n_1: str, tree_1: Any=tree_1) -> bool:
                    return not starts_with_exact(n_1, ".")

                return FileSystemTree.filter_folders(_arrow3673)(tree_1)

            else: 
                return tree_1


        def _arrow3675(__unit: None=None) -> FileSystemTree | None:
            tree: FileSystemTree
            def predicate(p: str) -> bool:
                return not FSharpSet__Contains(registered_payload, p)

            paths: Array[str] = filter(predicate, FileSystemTree.to_file_paths()(this._fs.Copy().Tree))
            tree = FileSystemTree.from_file_paths(paths)
            def _arrow3674(n: str) -> bool:
                return not starts_with_exact(n, ".")

            return FileSystemTree.filter_files(_arrow3674)(tree) if ignore_hidden else tree

        return default_arg(bind(binder, _arrow3675()), FileSystemTree.from_file_paths([]))

    @staticmethod
    def DefaultContracts() -> Any:
        class ObjectExpr3676:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        return of_seq_1(to_enumerable([(".gitignore", gitignore_contract), (".gitattributes", gitattributes_contract)]), ObjectExpr3676())

    @staticmethod
    def from_deprecated_rocrate_json_string(s: str) -> ARC:
        try: 
            s_1: str = replace(s, "bio:additionalProperty", "sdo:additionalProperty")
            def _arrow3677(__unit: None=None) -> ArcInvestigation:
                match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(ROCrate_get_decoderDeprecated(), s_1)
                if match_value.tag == 1:
                    raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

                else: 
                    return match_value.fields[0]


            return ARC(_arrow3677())

        except Exception as ex:
            arg_1: str = str(ex)
            return to_fail(printf("Could not parse deprecated ARC-RO-Crate metadata: \n%s"))(arg_1)


    @staticmethod
    def from_rocrate_json_string(s: str) -> ARC:
        try: 
            def _arrow3678(__unit: None=None) -> ArcInvestigation:
                match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(ROCrate_get_decoder(), s)
                if match_value.tag == 1:
                    raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

                else: 
                    return match_value.fields[0]


            return ARC(_arrow3678())

        except Exception as ex:
            arg_1: str = str(ex)
            return to_fail(printf("Could not parse ARC-RO-Crate metadata: \n%s"))(arg_1)


    def ToROCrateJsonString(self, spaces: int | None=None) -> str:
        this: ARC = self
        this.MakeDataFilesAbsolute()
        value: IEncodable = ROCrate_encoder_8A8D439(value_2(this._isa))
        return to_string(default_spaces(spaces), value)

    @staticmethod
    def to_rocrate_json_string(spaces: int | None=None) -> Callable[[ARC], str]:
        def _arrow3679(obj: ARC) -> str:
            return obj.ToROCrateJsonString(spaces)

        return _arrow3679

    def GetValidationPackagesConfigWriteContract(self, vpc: ValidationPackagesConfig) -> Contract:
        this: ARC = self
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        class ObjectExpr3681:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow3680(x: str, y: str) -> bool:
                    return x == y

                return _arrow3680

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains_2(ValidationPackagesConfigHelper_ConfigFilePath, paths, ObjectExpr3681()):
            file_paths: Array[str] = append_1([ValidationPackagesConfigHelper_ConfigFilePath], paths, None)
            this.SetFilePaths(file_paths)

        return ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toCreateContract_Static_724DAE55(vpc)

    def GetValidationPackagesConfigDeleteContract(self, vpc: ValidationPackagesConfig) -> Contract:
        this: ARC = self
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        class ObjectExpr3683:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow3682(x: str, y: str) -> bool:
                    return x == y

                return _arrow3682

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if contains_2(ValidationPackagesConfigHelper_ConfigFilePath, paths, ObjectExpr3683()):
            def predicate(p: str) -> bool:
                return not (p == ValidationPackagesConfigHelper_ConfigFilePath)

            file_paths: Array[str] = filter(predicate, paths)
            this.SetFilePaths(file_paths)

        return ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toDeleteContract_Static_724DAE55(vpc)

    def GetValidationPackagesConfigReadContract(self, __unit: None=None) -> Contract:
        return ValidationPackagesConfigHelper_ReadContract

    def GetValidationPackagesConfigFromReadContract(self, contract: Contract) -> ValidationPackagesConfig | None:
        return ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_tryFromReadContract_Static_7570923F(contract)


ARC_reflection = _expr3684

def ARC__ctor_79978BA1(isa: ArcInvestigation | None=None, cwl: None | None=None, fs: FileSystem | None=None) -> ARC:
    return ARC(isa, cwl, fs)


__all__ = ["ARCAux_getArcAssaysFromContracts", "ARCAux_getAssayDataMapFromContracts", "ARCAux_getArcStudiesFromContracts", "ARCAux_getStudyDataMapFromContracts", "ARCAux_getArcInvestigationFromContracts", "ARCAux_updateFSByISA", "ARCAux_updateFSByCWL", "ARC_reflection"]

