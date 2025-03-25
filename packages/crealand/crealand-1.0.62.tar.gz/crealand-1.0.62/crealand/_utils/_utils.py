import re
import inspect
from typing import (
    Any, 
    Union, 
    Callable, 
    List, 
    Tuple, 
    Set, 
    Dict, 
    get_origin, 
    get_args, 
    _GenericAlias, 
    Literal
)
from functools import wraps
from crealand._apis import _constants
from crealand._utils import _logger_setup

_logger = _logger_setup.setup_logger()

def check_out_of_range(
    func_name, 
    arg_name, 
    arg_value, 
    arg_range_type
):
    cons_dict = arg_range_type.__dict__
    for attr in cons_dict.keys():
        if not attr.startswith("_") and cons_dict[attr] == arg_value:
            return

    raise TypeError(get_out_of_range_error_info(
        func_name, arg_name, arg_value, arg_range_type))

def get_out_of_range_error_info(
    func_name, 
    arg_name, 
    arg_value, 
    arg_range_type, 
    escape=False
):
    cons_name = arg_range_type.__name__
    if escape:
        return re.escape(func_name + '(): The "' + arg_name + 
            '" argument must be in the range of ' + cons_name + 
            ", but got '" + str(arg_value)) + "'"
    else:
        return f'{func_name}(): The "{arg_name}" argument \
must be in the range of {cons_name}, but got \'{arg_value}\''

def check_compare_operator(
    func_name, 
    arg_name, 
    arg_value
):
    cmp_dict = _constants.CompareOperator.__dict__
    for attr in cmp_dict.keys():
        if not attr.startswith("_") and cmp_dict[attr] == arg_value:
            return

    raise TypeError(get_compare_operator_error_info(
        func_name, arg_name, arg_value))

def get_compare_operator_error_info(
    func_name, 
    arg_name, 
    arg_value, 
    escape=False
):
    cmp_dict = _constants.CompareOperator.__dict__
    cmp_opt_list = [cmp_dict[attr] for attr in cmp_dict.keys() 
        if not attr.startswith("_")]
    if escape:
        return re.escape(func_name + '(): The "' + arg_name + 
            '" argument must be in the range of ' + str(cmp_opt_list) + 
            ", but got '" + str(arg_value)) + "'"
    else:
        return f'{func_name}(): The "{arg_name}" argument \
must be in the range of {cmp_opt_list}, but got \'{arg_value}\''

def check_three_dimensions(
    func_name, 
    arg_name, 
    arg_value
):
    if len(arg_value) != 3:
        raise TypeError(get_three_dimensions_error_info(
            func_name, arg_name, arg_value))
    
def get_three_dimensions_error_info(
    func_name, 
    arg_name, 
    arg_value, 
    escape=False
):
    if escape:
        return re.escape(func_name + '(): The "' + arg_name + 
            '" argument must have three dimensions, but got ' 
            + str(arg_value))
    else:
        return f'{func_name}(): The "{arg_name}" argument \
must have three dimensions, but got {arg_value}'

def check_attachment_id(
    func_name, 
    arg_name, 
    arg_value
):
    if len(arg_value) < 1 or len(arg_value) > 2:
        raise TypeError(get_attachment_id_error_info(
            func_name, arg_name, arg_value))
    
def get_attachment_id_error_info(
    func_name, 
    arg_name, 
    arg_value, 
    escape=False
):
    if escape:
        return re.escape(func_name + '(): The "' + arg_name + 
            '" argument can only have one or two elements, but got ' 
            + str(arg_value))
    else:
        return f'{func_name}(): The "{arg_name}" argument \
can only have one or two elements, but got {arg_value}'

def over_args_error_info(
    func_name, 
    func_args_num, 
    given_args_num, 
    escape=False
):
    if escape:
        return re.escape(func_name + "() takes " + str(func_args_num) + 
            " positional arguments but " + str(given_args_num) 
            + " were given")
    else:
        return f"{func_name}() takes {func_args_num} \
positional arguments but {given_args_num} were given"

def miss_args_error_info(
    func_name, 
    miss_args_num, 
    miss_arg_list, 
    escape=False
):
    if escape:
        return re.escape(func_name + "() missing " + str(miss_args_num) + 
            " required positional arguments: " + ", ".join(miss_arg_list))
    else:
        return f"{func_name}() missing {miss_args_num} \
required positional arguments: {', '.join(miss_arg_list)}"

def wrong_type_arg_error_info(
    func_name, 
    arg_name, 
    arg_correct_type, 
    arg_wrong_type, 
    escape=False
):
    if escape:
        return re.escape(func_name + '(): The "' + arg_name + 
            '" argument must be of type ' + str(arg_correct_type) + 
            ", but got " + str(arg_wrong_type))
    else:
        return f'{func_name}(): The "{arg_name}" argument \
must be of type {arg_correct_type}, but got {arg_wrong_type}'

def Handle_point(value: tuple):
    result = {"id": value[0]}
    if len(value) == 2:
        result["name"] = value[1]
    return result

def check_type(func):
    def is_instance_of(value, annotation):
        if annotation is Any:
            return True
        if get_origin(annotation) is Union:
            return any(is_instance_of(value, t) for t in get_args(annotation))
        elif annotation is Callable:
            return callable(value)
        elif get_origin(annotation) in (List, Tuple, Set, Dict,Literal):
            if get_origin(annotation) is Literal:
                return value in get_args(annotation)
            if not isinstance(value, get_origin(annotation)):
                return False
            if not get_args(annotation):  # 如果没有指定元素类型，直接返回 True
                return True
            if get_origin(annotation) is dict:
                key_type, value_type = get_args(annotation)
                return all(is_instance_of(k, key_type) 
                    and is_instance_of(v, value_type) for k, v in value.items())
            else:
                element_type = get_args(annotation)[0]
                return all(is_instance_of(item, element_type) for item in value)
        elif isinstance(annotation, type):
            return isinstance(value, annotation)
        elif isinstance(annotation, _GenericAlias):
            origin = get_origin(annotation)
            args = get_args(annotation)
            if origin is None:
                return False
            if not isinstance(value, origin):
                return False
            if args:
                if origin is dict:
                    key_type, value_type = args
                    return all(is_instance_of(k, key_type) 
                        and is_instance_of(v, value_type) for k, v in value.items())
                elif origin in (list, tuple, set):
                    element_type = args[0]
                    if get_origin(annotation) is Union:
                        return any(is_instance_of(item, element_type) for item in value)
                    else:
                        return all(is_instance_of(item, element_type) for item in value)
            return True
        return False
    
    @wraps(func)
    def inner(*args, **kwargs):
        # 获取原始函数
        original_func = func
        if isinstance(original_func, (staticmethod, classmethod)):
            original_func = original_func.__func__
        
        # 获取函数的类型注解
        annotations = original_func.__annotations__

        # 获取函数的签名信息
        parameters = inspect.signature(original_func).parameters

        # 获取函数的参数名称
        arg_names = list(parameters.keys())

        # 检查位置参数数量
        given_args = list(args) + list(kwargs.values())
        if len(given_args) > len(arg_names):
            raise TypeError(over_args_error_info(
                func_name=original_func.__name__, 
                func_args_num=len(arg_names), 
                given_args_num=len(args)
            ))

        # 检查是否有未传递的必需参数
        required_params = [name for name in arg_names 
            if parameters[name].default == inspect.Parameter.empty]
        if len(given_args) < len(required_params):
            raise TypeError(miss_args_error_info(
                func_name=original_func.__name__, 
                miss_args_num=len(required_params) - len(given_args), 
                miss_arg_list=required_params[len(given_args):]
            ))

        # 检查位置参数
        for i, arg in enumerate(given_args):
            param_name = arg_names[i]
            if param_name in annotations:
                annotation = annotations[param_name]
                if not is_instance_of(arg, annotation):
                    raise TypeError(wrong_type_arg_error_info(
                        func_name=original_func.__name__, 
                        arg_name=param_name, 
                        arg_correct_type=annotation, 
                        arg_wrong_type=type(arg)
                    ))

        return original_func(*args, **kwargs)

    return inner

def raise_error(func,err,data):
    if err > 0:
        raise Exception(f"Error occurred:func {func} {err}, {data}")
    else:
        _logger.info(f"Error occurred:func {func} {err}, {data}")