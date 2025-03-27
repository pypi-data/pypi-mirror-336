from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.array_ import (fold, append)
from ..fable_modules.fable_library.async_builder import (singleton, Async)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import curry2
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from ..Contract.contract import (Contract, DTOType, DTO as DTO_2)
from ..FileSystem.path import combine
from ..cross_async import (catch_with, start_sequential)
from .file_system_helper import (read_file_xlsx_async, read_file_text_async, ensure_directory_of_file_async, write_file_text_async, write_file_xlsx_async, rename_file_or_directory_async, delete_file_or_directory_async)

def fulfill_read_contract_async(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e_1: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow3443(__unit: None=None, e_1: Any=e_1) -> str:
            arg_4: str = str(e_1)
            return to_text(printf("Error reading contract %s: %s"))(c.Path)(arg_4)

        return FSharpResult_2(1, _arrow3443())

    def _arrow3449(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        def _arrow3446(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
            match_value: DTOType | None = c.DTOType
            (pattern_matching_result,) = (None,)
            if match_value is not None:
                if match_value.tag == 0:
                    pattern_matching_result = 0

                elif match_value.tag == 2:
                    pattern_matching_result = 0

                elif match_value.tag == 1:
                    pattern_matching_result = 0

                elif match_value.tag == 3:
                    pattern_matching_result = 0

                elif match_value.tag == 8:
                    pattern_matching_result = 1

                else: 
                    pattern_matching_result = 2


            else: 
                pattern_matching_result = 2

            if pattern_matching_result == 0:
                path: str = combine(base_path, c.Path)
                def _arrow3444(_arg: FsWorkbook) -> Async[FSharpResult_2[Contract, str]]:
                    return singleton.Return(FSharpResult_2(0, Contract(c.Operation, c.Path, c.DTOType, DTO_2(0, _arg))))

                return singleton.Bind(read_file_xlsx_async(path), _arrow3444)

            elif pattern_matching_result == 1:
                path_1: str = combine(base_path, c.Path)
                def _arrow3445(_arg_1: str) -> Async[FSharpResult_2[Contract, str]]:
                    return singleton.Return(FSharpResult_2(0, Contract(c.Operation, c.Path, c.DTOType, DTO_2(1, _arg_1))))

                return singleton.Bind(read_file_text_async(path_1), _arrow3445)

            elif pattern_matching_result == 2:
                return singleton.Return(FSharpResult_2(1, to_text(printf("Contract %s is neither an ISA nor a freetext contract"))(c.Path)))


        def _arrow3448(_arg_2: Exception) -> Async[FSharpResult_2[Contract, str]]:
            def _arrow3447(__unit: None=None) -> str:
                arg_2: str = str(_arg_2)
                return to_text(printf("Error reading contract %s: %s"))(c.Path)(arg_2)

            return singleton.Return(FSharpResult_2(1, _arrow3447()))

        return singleton.TryWith(singleton.Delay(_arrow3446), _arrow3448)

    return catch_with(f, singleton.Delay(_arrow3449))


def fullfill_contract_batch_async_by(contract_f: Callable[[str, Contract], Async[FSharpResult_2[Contract, str]]], base_path: str, cs: Array[Contract]) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
    def _arrow3451(__unit: None=None, contract_f: Any=contract_f, base_path: Any=base_path, cs: Any=cs) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        def _arrow3450(_arg: Array[FSharpResult_2[Contract, str]]) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
            def folder(acc: FSharpResult_2[Array[Contract], Array[str]], cr: FSharpResult_2[Contract, str]) -> FSharpResult_2[Array[Contract], Array[str]]:
                copy_of_struct: FSharpResult_2[Array[Contract], Array[str]] = acc
                if copy_of_struct.tag == 1:
                    copy_of_struct_1: FSharpResult_2[Contract, str] = cr
                    if copy_of_struct_1.tag == 1:
                        return FSharpResult_2(1, append(copy_of_struct.fields[0], [copy_of_struct_1.fields[0]], None))

                    else: 
                        return FSharpResult_2(1, copy_of_struct.fields[0])


                else: 
                    copy_of_struct_2: FSharpResult_2[Contract, str] = cr
                    if copy_of_struct_2.tag == 1:
                        return FSharpResult_2(1, [copy_of_struct_2.fields[0]])

                    else: 
                        return FSharpResult_2(0, append(copy_of_struct.fields[0], [copy_of_struct_2.fields[0]], None))



            res: FSharpResult_2[Array[Contract], Array[str]] = fold(folder, FSharpResult_2(0, []), _arg)
            return singleton.Return(res)

        return singleton.Bind(start_sequential(curry2(contract_f)(base_path), cs), _arrow3450)

    return singleton.Delay(_arrow3451)


def fulfill_write_contract_async(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e_1: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow3452(__unit: None=None, e_1: Any=e_1) -> str:
            arg_4: str = str(e_1)
            return to_text(printf("Error writing contract %s: %s"))(c.Path)(arg_4)

        return FSharpResult_2(1, _arrow3452())

    def _arrow3462(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        def _arrow3459(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
            match_value: DTO_2 | None = c.DTO
            if match_value is None:
                path_2: str = combine(base_path, c.Path)
                def _arrow3454(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow3453(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_text_async(path_2, ""), _arrow3453)

                return singleton.Bind(ensure_directory_of_file_async(path_2), _arrow3454)

            elif match_value.tag == 1:
                t: str = match_value.fields[0]
                path: str = combine(base_path, c.Path)
                def _arrow3456(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow3455(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_text_async(path, t), _arrow3455)

                return singleton.Bind(ensure_directory_of_file_async(path), _arrow3456)

            elif match_value.tag == 0:
                wb: Any = match_value.fields[0]
                path_1: str = combine(base_path, c.Path)
                def _arrow3458(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow3457(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_xlsx_async(path_1, wb), _arrow3457)

                return singleton.Bind(ensure_directory_of_file_async(path_1), _arrow3458)

            else: 
                return singleton.Return(FSharpResult_2(1, to_text(printf("Contract %s is not an ISA contract"))(c.Path)))


        def _arrow3461(_arg_6: Exception) -> Async[FSharpResult_2[Contract, str]]:
            def _arrow3460(__unit: None=None) -> str:
                arg_2: str = str(_arg_6)
                return to_text(printf("Error writing contract %s: %s"))(c.Path)(arg_2)

            return singleton.Return(FSharpResult_2(1, _arrow3460()))

        return singleton.TryWith(singleton.Delay(_arrow3459), _arrow3461)

    return catch_with(f, singleton.Delay(_arrow3462))


def fulfill_update_contract_async(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e_1: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow3463(__unit: None=None, e_1: Any=e_1) -> str:
            arg_4: str = str(e_1)
            return to_text(printf("Error updating contract %s: %s"))(c.Path)(arg_4)

        return FSharpResult_2(1, _arrow3463())

    def _arrow3473(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        def _arrow3470(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
            match_value: DTO_2 | None = c.DTO
            if match_value is None:
                path_2: str = combine(base_path, c.Path)
                def _arrow3465(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow3464(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_text_async(path_2, ""), _arrow3464)

                return singleton.Bind(ensure_directory_of_file_async(path_2), _arrow3465)

            elif match_value.tag == 1:
                t: str = match_value.fields[0]
                path: str = combine(base_path, c.Path)
                def _arrow3467(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow3466(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_text_async(path, t), _arrow3466)

                return singleton.Bind(ensure_directory_of_file_async(path), _arrow3467)

            elif match_value.tag == 0:
                wb: Any = match_value.fields[0]
                path_1: str = combine(base_path, c.Path)
                def _arrow3469(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow3468(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_xlsx_async(path_1, wb), _arrow3468)

                return singleton.Bind(ensure_directory_of_file_async(path_1), _arrow3469)

            else: 
                return singleton.Return(FSharpResult_2(1, to_text(printf("Contract %s is not an ISA contract"))(c.Path)))


        def _arrow3472(_arg_6: Exception) -> Async[FSharpResult_2[Contract, str]]:
            def _arrow3471(__unit: None=None) -> str:
                arg_2: str = str(_arg_6)
                return to_text(printf("Error updating contract %s: %s"))(c.Path)(arg_2)

            return singleton.Return(FSharpResult_2(1, _arrow3471()))

        return singleton.TryWith(singleton.Delay(_arrow3470), _arrow3472)

    return catch_with(f, singleton.Delay(_arrow3473))


def fullfill_rename_contract_async(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e_1: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow3474(__unit: None=None, e_1: Any=e_1) -> str:
            arg_5: str = str(e_1)
            return to_text(printf("Error renaming contract %s: %s"))(c.Path)(arg_5)

        return FSharpResult_2(1, _arrow3474())

    def _arrow3479(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        def _arrow3476(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
            match_value: DTO_2 | None = c.DTO
            (pattern_matching_result, t_2) = (None, None)
            if match_value is not None:
                if match_value.tag == 1:
                    if match_value.fields[0] == c.Path:
                        pattern_matching_result = 0

                    else: 
                        pattern_matching_result = 1
                        t_2 = match_value.fields[0]


                else: 
                    pattern_matching_result = 2


            else: 
                pattern_matching_result = 2

            if pattern_matching_result == 0:
                return singleton.Return(FSharpResult_2(1, to_text(printf("Rename Contract %s old and new Path are the same"))(c.Path)))

            elif pattern_matching_result == 1:
                new_path: str = combine(base_path, t_2)
                old_path: str = combine(base_path, c.Path)
                def _arrow3475(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    return singleton.Return(FSharpResult_2(0, c))

                return singleton.Bind(rename_file_or_directory_async(old_path, new_path), _arrow3475)

            elif pattern_matching_result == 2:
                return singleton.Return(FSharpResult_2(1, to_text(printf("Rename Contract %s does not contain new Path"))(c.Path)))


        def _arrow3478(_arg_1: Exception) -> Async[FSharpResult_2[Contract, str]]:
            def _arrow3477(__unit: None=None) -> str:
                arg_3: str = str(_arg_1)
                return to_text(printf("Error renaming contract %s: %s"))(c.Path)(arg_3)

            return singleton.Return(FSharpResult_2(1, _arrow3477()))

        return singleton.TryWith(singleton.Delay(_arrow3476), _arrow3478)

    return catch_with(f, singleton.Delay(_arrow3479))


def fullfill_delete_contract_async(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e_1: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow3480(__unit: None=None, e_1: Any=e_1) -> str:
            arg_3: str = str(e_1)
            return to_text(printf("Error deleting contract %s: %s"))(c.Path)(arg_3)

        return FSharpResult_2(1, _arrow3480())

    def _arrow3485(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        def _arrow3482(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
            path: str = combine(base_path, c.Path)
            def _arrow3481(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                return singleton.Return(FSharpResult_2(0, c))

            return singleton.Bind(delete_file_or_directory_async(path), _arrow3481)

        def _arrow3484(_arg_1: Exception) -> Async[FSharpResult_2[Contract, str]]:
            def _arrow3483(__unit: None=None) -> str:
                arg_1: str = str(_arg_1)
                return to_text(printf("Error deleting contract %s: %s"))(c.Path)(arg_1)

            return singleton.Return(FSharpResult_2(1, _arrow3483()))

        return singleton.TryWith(singleton.Delay(_arrow3482), _arrow3484)

    return catch_with(f, singleton.Delay(_arrow3485))


def full_fill_contract(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow3486(__unit: None=None, e: Any=e) -> str:
            arg_2: str = str(e)
            return to_text(printf("Error fulfilling contract %s: %s"))(c.Path)(arg_2)

        return FSharpResult_2(1, _arrow3486())

    def _arrow3487(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        match_value: str = c.Operation
        return singleton.ReturnFrom(fulfill_read_contract_async(base_path, c)) if (match_value == "READ") else (singleton.ReturnFrom(fulfill_write_contract_async(base_path, c)) if (match_value == "CREATE") else (singleton.ReturnFrom(fulfill_update_contract_async(base_path, c)) if (match_value == "UPDATE") else (singleton.ReturnFrom(fullfill_delete_contract_async(base_path, c)) if (match_value == "DELETE") else (singleton.ReturnFrom(fullfill_rename_contract_async(base_path, c)) if (match_value == "RENAME") else singleton.Return(FSharpResult_2(1, to_text(printf("Operation %A not supported"))(c.Operation)))))))

    return catch_with(f, singleton.Delay(_arrow3487))


def full_fill_contract_batch_async(base_path: str, cs: Array[Contract]) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
    def _arrow3488(base_path_1: str, c: Contract, base_path: Any=base_path, cs: Any=cs) -> Async[FSharpResult_2[Contract, str]]:
        return full_fill_contract(base_path_1, c)

    return fullfill_contract_batch_async_by(_arrow3488, base_path, cs)


__all__ = ["fulfill_read_contract_async", "fullfill_contract_batch_async_by", "fulfill_write_contract_async", "fulfill_update_contract_async", "fullfill_rename_contract_async", "fullfill_delete_contract_async", "full_fill_contract", "full_fill_contract_batch_async"]

