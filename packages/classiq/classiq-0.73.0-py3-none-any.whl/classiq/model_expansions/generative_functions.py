from collections.abc import Mapping
from sys import exc_info
from types import TracebackType
from typing import TYPE_CHECKING, Any

from classiq.interface.exceptions import (
    ClassiqExpansionError,
)
from classiq.interface.generator.expressions.proxies.classical.classical_proxy import (
    ClassicalProxy,
)
from classiq.interface.generator.expressions.proxies.classical.qmod_struct_instance import (
    QmodStructInstance,
)
from classiq.interface.generator.expressions.proxies.classical.utils import (
    get_proxy_type,
)
from classiq.interface.generator.functions.type_name import Struct
from classiq.interface.helpers.datastructures import get_sdk_compatible_python_object
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    PositionalArg,
    QuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)
from classiq.interface.model.quantum_statement import QuantumStatement

from classiq.model_expansions.closure import (
    FunctionClosure,
    GenerativeClosure,
)
from classiq.model_expansions.scope import Evaluated, QuantumSymbol
from classiq.qmod.generative import generative_mode_context, set_frontend_interpreter
from classiq.qmod.model_state_container import QMODULE
from classiq.qmod.qmod_parameter import CParamStruct, create_param
from classiq.qmod.qmod_variable import _create_qvar_for_qtype
from classiq.qmod.quantum_expandable import (
    QTerminalCallable,
)
from classiq.qmod.quantum_function import QFunc
from classiq.qmod.semantics.annotation.call_annotation import resolve_function_calls

if TYPE_CHECKING:
    from classiq.model_expansions.interpreters.generative_interpreter import (
        GenerativeInterpreter,
    )


def _unwrap_traceback_frame(e: Exception) -> Exception:
    fallback_error = ClassiqExpansionError(str(e))
    traceback = exc_info()[2]
    if traceback is None:
        return fallback_error
    back_frame = traceback.tb_frame.f_back
    if back_frame is None:
        return fallback_error
    back_tb = TracebackType(
        tb_next=None,
        tb_frame=back_frame,
        tb_lasti=back_frame.f_lasti,
        tb_lineno=back_frame.f_lineno,
    )
    return e.with_traceback(back_tb)


def translate_ast_arg_to_python_qmod(param: PositionalArg, evaluated: Evaluated) -> Any:
    if isinstance(param, PortDeclaration):
        quantum_symbol = evaluated.as_type(QuantumSymbol)
        return _create_qvar_for_qtype(
            quantum_symbol.quantum_type, quantum_symbol.handle
        )
    if isinstance(param, QuantumOperandDeclaration):
        if not param.is_list or not param.is_generative:
            return QTerminalCallable(param)
        inner_decl = param.model_copy(update={"is_list": False})
        func_list: list[FunctionClosure] = evaluated.as_type(list)
        return [
            QTerminalCallable(inner_decl, index_=idx) for idx in range(len(func_list))
        ]
    classical_value = evaluated.value
    if isinstance(classical_value, QmodStructInstance):
        return CParamStruct(
            expr=param.name,
            struct_type=Struct(name=classical_value.struct_declaration.name),
            qmodule=QMODULE,
        )
    if isinstance(classical_value, ClassicalProxy):
        return create_param(
            str(classical_value.handle), get_proxy_type(classical_value), QMODULE
        )

    return get_sdk_compatible_python_object(classical_value)


class _InterpreterExpandable(QFunc):
    def __init__(self, interpreter: "GenerativeInterpreter"):
        super().__init__(lambda: None)
        self._interpreter = interpreter

    def append_statement_to_body(self, stmt: QuantumStatement) -> None:
        current_operation = self._interpreter._builder._operations[-1]
        dummy_function = NativeFunctionDefinition(
            name=current_operation.name,
            positional_arg_declarations=current_operation.positional_arg_declarations,
            body=self._interpreter._builder._current_statements + [stmt],
        )
        declarative_functions = {
            name: func
            for name, func in self._qmodule.native_defs.items()
            if name not in self._interpreter._top_level_scope
        }
        self._interpreter.update_declarative_functions(
            declarative_functions, self._qmodule
        )
        self._interpreter.update_generative_functions(
            self._qmodule.generative_functions
        )
        func_decls = self._get_function_declarations()
        for dec_func in declarative_functions.values():
            resolve_function_calls(dec_func, func_decls)
        resolve_function_calls(dummy_function, func_decls)
        stmt = dummy_function.body[-1]
        with generative_mode_context(False):
            self._interpreter.emit_statement(stmt)

    def _get_function_declarations(self) -> Mapping[str, QuantumFunctionDeclaration]:
        scope_func_decls: dict[str, QuantumFunctionDeclaration] = {}
        for name, evaluated in self._interpreter._builder.current_scope.items():
            value = evaluated.value
            if isinstance(value, FunctionClosure):
                scope_func_decls[name] = QuantumFunctionDeclaration(
                    name=name,
                    positional_arg_declarations=value.positional_arg_declarations,
                )
            elif (
                isinstance(value, list)
                and len(value) > 0
                and isinstance(value[0], FunctionClosure)
            ):
                scope_func_decls[name] = QuantumFunctionDeclaration(
                    name=name,
                    positional_arg_declarations=value[0].positional_arg_declarations,
                )
        return (
            nameables_to_dict(self._interpreter._get_function_declarations())
            | scope_func_decls
        )


def emit_generative_statements(
    interpreter: "GenerativeInterpreter",
    operation: GenerativeClosure,
    args: list[Evaluated],
) -> None:
    python_qmod_args = [
        translate_ast_arg_to_python_qmod(param, arg)
        for param, arg in zip(operation.positional_arg_declarations, args)
    ]
    with _InterpreterExpandable(interpreter):
        set_frontend_interpreter(interpreter)
        for block_name, generative_function in operation.generative_blocks.items():
            with (
                interpreter._builder.block_context(block_name),
                generative_mode_context(True),
            ):
                generative_function._py_callable(*python_qmod_args)
