
#################################################
# HolAdo (Holistic Automation do)
#
# (C) Copyright 2021-2025 by Eric Klumpp
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.
#################################################

from builtins import object
import logging
from holado_value.common.tools.value_types import ValueTypes
from holado_core.common.exceptions.technical_exception import TechnicalException
import re
import importlib
from holado_core.common.tools.converters.converter import Converter
import types
from holado_core.common.tools.tools import Tools
from holado_multitask.multithreading.reflection import traceback
from holado_scripting.common.tools.evaluate_parameters import EvaluateParameters
from holado.holado_config import Config
from holado_multitask.multitasking.multitask_manager import MultitaskManager
from holado_python.standard_library.typing import Typing
from holado.common.handlers.undefined import undefined_value

logger = logging.getLogger(__name__)


class ExpressionEvaluator(object):

    def __init__(self):
        self.__dynamic_text_manager = None
        self.__text_interpreter = None
        self.__unique_value_manager = None
        self.__variable_manager = None
        
        # self.__modules_already_imported = []
        
    def initialize(self, dynamic_text_manager, unique_value_manager, text_interpreter, variable_manager):
        self.__dynamic_text_manager = dynamic_text_manager
        self.__text_interpreter = text_interpreter
        self.__unique_value_manager = unique_value_manager
        self.__variable_manager = variable_manager
            
    def evaluate_expression(self, expression, unescape_string_method=None, eval_params=EvaluateParameters.default(), log_level=logging.DEBUG):
        value_type, value, value_to_eval = self.extract_expression_information(expression, unescape_string_method)
        if value_to_eval is not undefined_value:
            res = self.evaluate_expression_of_information(value_type, value_to_eval, eval_params=eval_params)
        else:
            res = value
        if Tools.do_log(logger, log_level):
            logger.log(log_level, f"Evaluate expression [{expression}] => ({value_type}, {value}, '{value_to_eval}') => [{res}] (type: {Typing.get_object_class_fullname(res)})    (with evaluate parameters: {eval_params})")
        return res

    def evaluate_python_expression(self, expression, eval_params=EvaluateParameters.default(), log_level=logging.DEBUG):
        res = self.evaluate_expression_of_information(ValueTypes.Symbol, expression, eval_params=eval_params)
        if Tools.do_log(logger, log_level):
            logger.log(log_level, f"Evaluate python expression [{expression}] => [{res}] (type: {Typing.get_object_class_fullname(res)})    (with evaluate parameters: {eval_params})")
        return res

    def extract_expression_information(self, expression, unescape_string_method=None, log_level=logging.TRACE):  # @UndefinedVariable
        res = self.__extract_expression_information(expression, unescape_string_method=unescape_string_method)
        if Tools.do_log(logger, log_level):
            logger.log(log_level, f"Extract expression information [{expression}] => {res}")
        return res

    def __extract_expression_information(self, expression, unescape_string_method=None):
        if isinstance(expression, str):
            return self.__extract_expression_information_str(expression, unescape_string_method = unescape_string_method)
        else:
            return self.__extract_value_information(expression)

    def __extract_expression_information_str(self, expression, unescape_string_method=None):
        if unescape_string_method is None:
            from holado_test.scenario.step_tools import StepTools
            unescape_string_method = StepTools.unescape_string
            
        try:
            expr_content = expression.strip()

            # Manage usual types    
            if expr_content == Config.NONE_SYMBOL:
                return (ValueTypes.Null, None, undefined_value)
            elif expr_content == Config.NOT_APPLICABLE_SYMBOL:
                return (ValueTypes.NotApplicable, undefined_value, undefined_value)
            elif Converter.is_boolean(expr_content):
                return (ValueTypes.Boolean, Converter.to_boolean(expr_content), undefined_value)
            elif Converter.is_integer(expr_content):
                return (ValueTypes.Integer, int(expr_content), undefined_value)
            elif Converter.is_float(expr_content):
                return (ValueTypes.Float, float(expr_content), undefined_value)
            
            # Manage strings
            for end_sym, val_type in [(Config.DYNAMIC_SYMBOL, ValueTypes.DynamicString), 
                                      (Config.THREAD_DYNAMIC_SYMBOL, ValueTypes.ThreadDynamicString), 
                                      (Config.UNIQUE_SYMBOL, ValueTypes.UniqueString), 
                                      ("", ValueTypes.String)]:
                if expr_content.startswith("'") and expr_content.endswith("'" + end_sym):
                    text = expr_content[1:-1-len(end_sym)]
                    if unescape_string_method is not None:
                        text = unescape_string_method(text)
                    return (val_type, undefined_value, text)
                
            # # Manage evaluated values
            # try:
            #     value_evaluated = eval(expr_content)
            #     evaluated = True
            # except (SyntaxError, NameError, ValueError):
            #     evaluated = False
            # if evaluated:
            #     if isinstance(value_evaluated, bool):
            #         value_type = ValueTypes.Boolean
            #     elif isinstance(value_evaluated, int):
            #         value_type = ValueTypes.Integer
            #     elif isinstance(value_evaluated, float):
            #         value_type = ValueTypes.Float
            #     elif isinstance(value_evaluated, str):
            #         value_type = ValueTypes.String
            #     else:
            #         value_type = ValueTypes.Generic
            #     return (value_type, value_evaluated)
            
            # Else consider content as a symbol
            return (ValueTypes.Symbol, undefined_value, expr_content)
        except Exception as exc:
            raise TechnicalException(f"Error while extracting expression information in expression [{expression}] (type: {Typing.get_object_class_fullname(expression)})") from exc

    def extract_value_information(self, value):
        return self.__extract_value_information(value)

    def __extract_value_information(self, value):
        if value is undefined_value:
            return (ValueTypes.Undefined, undefined_value, undefined_value)
        elif value is None:
            return (ValueTypes.Null, None, undefined_value)
        elif isinstance(value, bool):
            return (ValueTypes.Boolean, value, undefined_value)
        elif isinstance(value, int):
            return (ValueTypes.Integer, value, undefined_value)
        elif isinstance(value, float):
            return (ValueTypes.Float, value, undefined_value)
        elif isinstance(value, str):
            return (ValueTypes.String, value, undefined_value)
        else:
            return (ValueTypes.Generic, value, undefined_value)
        
    def evaluate_expression_of_information(self, value_type, value, eval_params=EvaluateParameters.default()):
        if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
            logger.trace(f"Evaluating expression of information ({value_type.name}, {value}, {eval_params})")
        res = self.__evaluate_expression_of_information(value_type, value, eval_params=eval_params)
        if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
            logger.trace(f"Evaluate expression of information ({value_type.name}, {value}) => [{res}] (type: {Typing.get_object_class_fullname(res)})    (with evaluate parameters: {eval_params})")
        return res
        
    def __evaluate_expression_of_information(self, value_type, value, eval_params=EvaluateParameters.default()):
        if value_type in [ValueTypes.Null]:
            return None
        elif value_type in [ValueTypes.Boolean, ValueTypes.Integer, ValueTypes.Float, ValueTypes.Generic]:
            return value
        elif value_type in [ValueTypes.String, ValueTypes.DynamicString, ValueTypes.ThreadDynamicString, ValueTypes.UniqueString]:
            return self.__evaluate_expression_of_information_string(value_type, value, eval_params=eval_params)
        elif value_type in [ValueTypes.Symbol]:
            return self.__evaluate_expression_of_information_symbol(value, eval_params=eval_params)
        else:
            return value
        
    def __evaluate_expression_of_information_string(self, value_type, value, eval_params=EvaluateParameters.default_without_raise()):
        if eval_params.do_interpret:
            res = self.__text_interpreter.interpret(value, eval_params=eval_params)
        else:
            res = value
            
        if isinstance(res, bytes):
            res = res.decode('utf-8')
        elif not isinstance(res, str):
            res = str(res)
            
        if value_type == ValueTypes.DynamicString:
            return self.__dynamic_text_manager.get(res)
        elif value_type == ValueTypes.ThreadDynamicString:
            return self.__dynamic_text_manager.get(res, scope=MultitaskManager.get_thread_id())
        elif value_type == ValueTypes.UniqueString:
            return res + self.__unique_value_manager.new_string(padding_length=Config.unique_string_padding_length)
        else:
            return res
        
    def __evaluate_expression_of_information_symbol(self, value, eval_params=EvaluateParameters.default()):
        if logger.isEnabledFor(logging.TRACE):  # @UndefinedVariable
            logger.trace(f"Evaluating symbol ([{value}], {eval_params})")
        res = value
        
        # Replace explicit interpret parts
        if eval_params.do_interpret and isinstance(res, str):
            res, _, is_evaluated = self.__evaluate_interpret_expression(res, eval_params=eval_params)
            if is_evaluated:
                # If symbol is already evaluated, stop evaluation process
                if logger.isEnabledFor(logging.TRACE):  # @UndefinedVariable
                    logger.trace(f"Evaluate symbol [{value}]  =>  [{res}] (type: {Typing.get_object_class_fullname(res)})    (after interpret, with evaluate parameters: {eval_params})")
                return res
            # if logger.isEnabledFor(logging.TRACE):  # @UndefinedVariable
            #     logger.trace(f"Evaluate symbol [{value}] - after interpret:  [{res}] (type: {Typing.get_object_class_fullname(res)})    (with evaluate parameters: {eval_params})")
        
        # Evaluate variable expression
        # Note: if an eval must be done after interpret, variable shouldn't be evaluated unless it can makes failing eval
        if eval_params.do_eval_variable and isinstance(res, str) and len(res) > 0:
            result, is_evaluated = self.__evaluate_variable_expression(res, eval_params=eval_params)
            if is_evaluated:
                # If symbol is a variable expression, don't evaluate the result of the variable
                if logger.isEnabledFor(logging.TRACE):  # @UndefinedVariable
                    logger.trace(f"Evaluate symbol [{value}]  =>  [{result}] (type: {Typing.get_object_class_fullname(result)})    (after variable evaluation, with evaluate parameters: {eval_params})")
                return result
        
        # Evaluate expression
        # if eval_params.do_eval and (isinstance(res, str) or isinstance(res, bytes)):    # Commented as it doesn't work currently with bytes
        if eval_params.do_eval and isinstance(res, str):
            res = self.__evaluate_expression(res, locals_={}, eval_params=eval_params)
            
        # logger.debug(f"Evaluate symbol [{value}] => [{res}] (type: {Typing.get_object_class_fullname(res)})")
        if logger.isEnabledFor(logging.TRACE):  # @UndefinedVariable
            logger.trace(f"Evaluate symbol [{value}]  =>  [{res}] (type: {Typing.get_object_class_fullname(res)})    (after full evaluation, with evaluate parameters: {eval_params})")
        return res
        
    def __evaluate_interpret_expression(self, value, eval_params=EvaluateParameters.default()):
        result, is_interpreted, is_evaluated = value, False, False
        
        nb_sections = self.__text_interpreter.get_number_of_sections(value)
        if nb_sections > 0:
            # If eval is authorized, and many sections exists, prefer interpret sections and eval result
            if eval_params.do_eval and nb_sections > 1:
                result, locals_ = self.__text_interpreter._interpret_sections(value, eval_params=eval_params)
                if result != value:
                    result = self.__evaluate_expression(result, locals_, eval_params=eval_params)
                    is_evaluated = True
            else:
                result = self.__text_interpreter.interpret(value, eval_params=eval_params)
            is_interpreted = result != value
        
        # Manage recursive interpret, only in case of first interpret and if it wasn't evaluated
        if eval_params.do_interpret_recursively and is_interpreted and not is_evaluated and isinstance(result, str):
            new_result, new_is_interpreted, new_is_evaluated = self.__evaluate_interpret_expression(result, eval_params.with_raise_on_interpret_error(False))
            if new_is_interpreted:
                result = new_result
                is_evaluated = new_is_evaluated
        
        return result, is_interpreted, is_evaluated
        
    def __evaluate_variable_expression(self, value, eval_params=EvaluateParameters.default()):
        is_evaluated, result = False, None
        
        if self.__variable_manager.exists_variable(value):
            result = self.__variable_manager.get_variable_value(value)
            is_evaluated = True
        elif self.__variable_manager.is_variable_expression(value):
            try:
                result = self.__variable_manager.eval_variable_expression(value)
            except Exception as exc:
                if eval_params.raise_on_variable_eval_error:
                    raise exc
                else:
                    # logger.error(f"Error while evaluating variable expression [{value}]: {exc}")
                    logger.error(f"Error while evaluating variable expression [{value}]: {Tools.represent_exception(exc)}\n -> traceback:\n{traceback.represent_stack(indent=4)}")
            else:
                is_evaluated = True
        
        # Manage recursive evaluation, only in case of first variable evaluation
        if eval_params.do_eval_variable_recursively and is_evaluated and isinstance(result, str) and result != value:
            new_result, new_is_evaluated = self.__evaluate_variable_expression(result, eval_params.with_raise_on_variable_eval_error(False))
            if new_is_evaluated:
                result = new_result
        
        return result, is_evaluated
        
    def __evaluate_expression(self, value, locals_, eval_params=EvaluateParameters.default()):
        res = value
        while True:
            try:
                result = None
                if isinstance(value, str):
                    # Try first by replacing double semicolon
                    try:
                        txt_to_eval = value.replace("{{", "{").replace("}}", "}")
                        result = eval(txt_to_eval, globals(), locals_)
                    except SyntaxError as exc:
                        # Retry without replacing double semicolon
                        pass
                    
                if result is None:
                    result = eval(value, globals(), locals_)
            except NameError as exc:
                # logger.trace(f"Error while expression evaluation:\n    exception: {Tools.represent_exception(exc)}\n    globals: {globals()}\n    locals: {locals_}")
                # In case the name concerns a library, try to import the library
                m = re.match(r"name '(.*)' is not defined", str(exc))
                is_imported = False
                if m:
                    module_name = m.group(1)
                    is_imported = self.__import_module(module_name, locals_)
                    
                # If no import is done
                if not is_imported:
                    if Tools.do_log(logger, logging.DEBUG):
                        logger.debug(f"Error while evaluating expression [{value}]: {exc}")
                    break
            except Exception as exc:
                if eval_params.raise_on_eval_error:
                    raise exc
                else:
                    if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
                        logger.trace(f"Error while evaluating expression [{value}]: {Tools.represent_exception(exc)}")
                    elif Tools.do_log(logger, logging.DEBUG):
                        if isinstance(exc, SyntaxError):
                            logger.debug(f"Error while evaluating expression [{value}]: {repr(exc)}")
                        else:
                            logger.debug(f"Error while evaluating expression [{value}]: [{Typing.get_object_class_fullname(exc)}] {exc}")
                break
            else:
                if not isinstance(result, types.ModuleType):
                    res = result
                break
            
        # logger.debug(f"Evaluate [{value}] => [{res}] (type: {Typing.get_object_class_fullname(res)})")
        return res
    
    # def __import_module(self, module_name, locals_):
    #     res = False
    #
    #     if module_name in locals_:
    #         raise TechnicalException(f"Module '{module_name}' is already imported (locals_: {locals_})")
    #
    #     if module_name not in self.__modules_already_imported:
    #         if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
    #             logger.trace(f"Importing module '{module_name}'")
    #         try:
    #             module = importlib.import_module(module_name)
    #             locals_[module_name] = module
    #         except Exception as exc2:
    #             if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
    #                 logger.trace(f"Failed to import module '{module_name}': {exc2}")
    #         else:
    #             if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
    #                 logger.trace(f"Imported module '{module_name}' for expression evaluation")
    #             res = True
    #         finally:
    #             self.__modules_already_imported.append(module_name)
    #     else:
    #         if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
    #             logger.trace(f"Skip import of module '{module_name}' since it was already imported")
    #
    #     return res
    def __import_module(self, module_name, locals_):
        res = False
        
        if module_name in locals_:
            if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
                logger.trace(f"Skip import of module '{module_name}' since it was already imported")
        else:
            if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
                logger.trace(f"Importing module '{module_name}'")
            try:
                module = importlib.import_module(module_name)
                locals_[module_name] = module
            except Exception as exc2:
                if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
                    logger.trace(f"Failed to import module '{module_name}': {exc2}")
            else:
                if Tools.do_log(logger, logging.TRACE):  # @UndefinedVariable
                    logger.trace(f"Imported module '{module_name}' for expression evaluation")
                res = True
                
        return res
    
    def extract_string_value(self, expression, unescape_string_method=None, log_level=logging.DEBUG):
        value_type, value_str, value_to_eval = self.extract_expression_information(expression, unescape_string_method)
        if value_type in [ValueTypes.String, ValueTypes.DynamicString, ValueTypes.ThreadDynamicString, ValueTypes.UniqueString]:
            if value_to_eval is not undefined_value:
                res = value_to_eval
            else:
                res = value_str
        else:
            res = expression
        if Tools.do_log(logger, log_level):
            logger.debug(f"Extract string value [{expression}] => ({value_type}, '{value_str}') => [{res}] (type: {Typing.get_object_class_fullname(res)})")
        return res

