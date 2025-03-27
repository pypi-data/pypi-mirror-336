# -*- coding: utf-8 -*-
# tools.py
# Copyright (c) 2025 zedmoster

import logging
from typing import List
from mcp.server.fastmcp import Context

logger = logging.getLogger("RevitTools")


def call_func(ctx: Context, method: str = "CallFunc", params: List[str] = None) -> str:
    """
    调用Revit函数服务，当前支持清理重复元素功能，遵循JSON-RPC 2.0规范。

    特性:
    - 支持批量函数调用（当前仅实现ClearDuplicates）
    - 自动去重处理相同函数调用
    - 事务化操作确保数据一致性
    - 严格遵循JSON-RPC 2.0规范

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"CallFunc"
        params (List[Dict[str, List[str]]]): 函数调用参数列表，每个字典应包含:
            - "func": ["函数名1", "函数名2"] (当前仅支持["ClearDuplicates"])

    返回:
        str: JSON-RPC 2.0格式的响应字符串，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [被删除元素的ID列表],
                "id": request_id
            }
            失败时: 标准JSON-RPC错误响应

    错误代码:
        -32600: 无效请求（参数验证失败）
        -32602: 不支持的功能（调用未实现的函数）
        -32603: 内部错误
        -32700: 解析错误（参数格式错误）

    示例:
        >>> # 清理重复元素
        >>> response = call_func(ctx, params=[{"func": ["ClearDuplicates"]}])
        >>> print(response)
        '{"jsonrpc": "2.0", "result": [123456, 789012], "id": 1}'
    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数不能为空列表")

        if not all(isinstance(param, dict) for param in params):
            raise ValueError("每个参数应为字典类型")

        validated_params = []
        for param in params:
            if "func" not in param:
                raise ValueError("每个参数必须包含'func'字段")

            if not isinstance(param["func"], list):
                raise ValueError("'func'字段应为字符串列表")

            if not all(isinstance(f, str) for f in param["func"]):
                raise ValueError("'func'列表中的所有项应为字符串")

            validated_params.append({"func": param["func"]})

        # 执行函数调用
        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result_data = revit.send_command(method, validated_params)
        return result_data

    except Exception as e:
        logging.error(f"API调用失败: {str(e)}", exc_info=True)
        return "[]"  # 返回空的JSON数组


def find_elements(ctx: Context, method: str = "FindElements", params: List[dict[str, object]] = None) -> str:
    """
    在Revit中按类别查找元素，返回匹配的元素ID列表，遵循JSON-RPC 2.0规范。

    特性:
    - 支持按类别ID和类别名称查找（推荐使用categoryId）
    - 可指定是否只查找实例元素
    - 支持批量多个查询条件
    - 严格遵循JSON-RPC 2.0规范
    - 详细的错误处理和日志记录

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"FindElements"
        params (List[Dict[str, Union[int, str, bool]]]): 查询条件列表，每个字典包含:
            - categoryId (int, optional): 内置类别ID（推荐使用）
            - categoryName (str, optional): 类别名称（可能受语言版本影响）
            - isInstance (bool, optional): 是否只查找实例（默认为True）
        request_id (int): 请求标识符，默认为1

    返回:
        str: JSON-RPC 2.0格式的响应字符串，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [匹配的元素ID列表],
                "id": request_id
            }
            失败时: 标准JSON-RPC错误响应

    错误代码:
        -32600: 无效请求（参数验证失败）
        -32602: 类别未找到（无效的categoryId或categoryName）
        -32603: 内部错误
        -32700: 解析错误（参数格式错误）

    示例:
        >>> # 按类别ID查找
        >>> response = find_elements(ctx, params=[{"categoryId": -2000011}])

        >>> # 组合条件查找
        >>> response = find_elements(ctx, params=[
        ...     {"categoryId": -2000011, "isInstance": True},
        ...     {"categoryId": -2000240, "categoryName": "标高"}
        ... ])
        >>> print(response)
        '{"jsonrpc": "2.0", "result": [123456, 789012], "id": 1}'
    """
    try:
        # 参数验证
        if not isinstance(params, list) or not all(isinstance(param, dict) for param in params):
            raise ValueError("参数必须为字典列表")

        validated_params = []
        for param in params:
            validated_param = {}

            # 验证categoryId
            if "categoryId" in param:
                if not isinstance(param["categoryId"], int):
                    raise ValueError("categoryId必须是整数")
                validated_param["categoryId"] = param["categoryId"]

            # 验证categoryName
            if "categoryName" in param:
                if not isinstance(param["categoryName"], str):
                    raise ValueError("categoryName必须是字符串")
                validated_param["categoryName"] = param["categoryName"]

            # 验证isInstance（默认为True）
            validated_param["isInstance"] = param.get("isInstance", True)
            if not isinstance(validated_param["isInstance"], bool):
                raise ValueError("isInstance必须是布尔值")

            # 至少需要categoryId或categoryName之一
            if "categoryId" not in validated_param and "categoryName" not in validated_param:
                raise ValueError("必须提供categoryId或categoryName")

            validated_params.append(validated_param)

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, validated_params)
        return result

    except Exception as e:
        logger.error(f"查找元素时发生错误：{str(e)}", exc_info=True)
        return []


def update_elements(ctx: Context, method: str = "UpdateElements", params: list[dict[str, str]] = None) -> str:
    """
    批量更新Revit元素参数值，遵循JSON-RPC 2.0规范，支持事务处理。

    特性:
    - 支持混合格式元素ID（整数/字符串）
    - 自动参数值类型转换
    - 详细的错误报告和元素级状态跟踪
    - 严格遵循JSON-RPC 2.0规范

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"UpdateElements"
        params (List[Dict[str, Union[int, str]]]): 更新参数列表，每个字典必须包含:
            - elementId (Union[int, str]): 要更新的元素ID
            - parameterName (str): 参数名称（区分大小写）
            - parameterValue (str): 参数新值

    返回:
        str: JSON-RPC 2.0格式的响应字符串，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [成功更新的元素ID列表],
                "id": request_id
            }
            失败时: {
                "jsonrpc": "2.0",
                "error": {
                    "code": 错误代码,
                    "message": 错误描述,
                    "data": 错误详情
                },
                "id": request_id
            }

    错误代码:
        -32600 (Invalid Request): 参数验证失败
        -32602 (Invalid Params): 无效参数（元素不存在/参数不存在等）
        -32603 (Internal Error): 内部处理错误
        -32700 (Parse Error): 参数解析错误

    示例:
        >>> # 批量更新元素参数
        >>> response = update_elements(ctx, params=[
        ...     {"elementId": 123456, "parameterName": "Comments", "parameterValue": "Test"},
        ...     {"elementId": "789012", "parameterName": "Height", "parameterValue": "3000"}
        ... ])
        >>> print(response)
        '{"jsonrpc":"2.0","result":[123456,789012],"id":1}'

        >>> # 错误情况示例
        >>> response = update_elements(ctx, params=[{"elementId":999999,"parameterName":"InvalidParam","parameterValue":"X"}])
        >>> print(response)
        '{"jsonrpc":"2.0","error":{"code":-32602,"message":"参数无效","data":"参数'InvalidParam'不存在"},"id":1}'

    事务说明:
        所有更新操作在Revit事务组中执行，任一更新失败自动跳过。
    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数列表不能为空")

        validated_params = []
        for param in params:
            if not all(key in param for key in ['elementId', 'parameterName', 'parameterValue']):
                raise ValueError("每个参数字典必须包含elementId、parameterName和parameterValue")

            # 构造验证后的参数（保持原始格式）
            validated_param = {
                "elementId": str(param["elementId"]),  # 统一转为字符串以匹配服务器处理
                "parameterName": str(param["parameterName"]),
                "parameterValue": str(param["parameterValue"])
            }
            validated_params.append(validated_param)

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, validated_params)
        return result

    except Exception as e:
        error_msg = f"更新元素失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


def delete_elements(ctx: Context, method: str = "DeleteElements", params: List[dict[str, str]] = None) -> str:
    """
    批量删除Revit元素，支持字典格式参数，严格遵循服务器实现规范。

    特性:
    - 完全匹配服务器参数处理逻辑
    - 支持字典列表格式参数，每个字典包含elementId键
    - 自动处理整数和字符串格式的elementId
    - 事务化操作确保数据一致性
    - 详细的错误处理和日志记录

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"DeleteElements"
        params (List[Dict[str, Union[int, str]]]): 删除参数列表，每个字典必须包含:
            - elementId (Union[int, str]): 要删除的元素ID

    返回:
        str: JSON-RPC 2.0格式的响应字符串，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [成功删除的元素ID列表],
                "id": request_id
            }

    示例:
        >>> # 删除多个元素（混合格式）
        >>> response = delete_elements(ctx, params=[
        ...     {"elementId": 5943},
        ...     {"elementId": "5913"},
        ...     {"elementId": 212831}
        ... ])
        >>> print(response)
        '{"jsonrpc":"2.0","result":[5943,5913,212831],"id":1}'
    """
    try:
        # 参数验证：确保params为整型元素ID列表
        if not params or not all(isinstance(el_id, int) for el_id in params):
            raise ValueError("参数错误：'params' 应为整型元素ID列表。")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"删除元素时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def show_elements(ctx: Context, method: str = "ShowElements", params: List[dict[str, str]] = None) -> str:
    """
    在Revit视图中高亮显示指定元素，支持批量操作并遵循JSON-RPC 2.0规范。

    特性:
    - 支持批量显示多个元素
    - 自动处理整数和字符串格式的元素ID
    - 元素自动缩放至视图中心并高亮显示
    - 严格的参数验证和错误处理
    - 完全匹配服务器端实现逻辑

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"ShowElements"
        params (List[Dict[str, Union[int, str]]]): 元素参数列表，每个字典必须包含:
            - elementId (Union[int, str]): 要显示的元素ID

    返回:
        str: JSON-RPC 2.0格式的响应字符串，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [成功显示的元素ID列表],
                "id": request_id
            }
            失败时: {
                "jsonrpc": "2.0",
                "error": {
                    "code": 错误代码,
                    "message": 错误描述,
                    "data": 错误详情
                },
                "id": request_id
            }

    错误代码:
        -32600 (Invalid Request): 参数验证失败
        -32602 (Invalid Params): 无效元素ID或元素不存在
        -32603 (Internal Error): 内部处理错误
        -32700 (Parse Error): 参数解析错误

    示例:
        >>> # 显示多个元素
        >>> response = show_elements(ctx, params=[
        ...     {"elementId": 212781},
        ...     {"elementId": "212792"}
        ... ])
        >>> print(response)
        '{"jsonrpc":"2.0","result":[212781,212792],"id":1}'

    视图操作:
        成功调用后，元素将在当前视图中:
        1. 自动缩放至视图中心
        2. 高亮显示
        3. 被添加到当前选择集
    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数列表不能为空")

        validated_params = []
        for param in params:
            if "elementId" not in param:
                raise ValueError("每个参数必须包含elementId字段")

            # 转换elementId为字符串（匹配服务器处理逻辑）
            try:
                element_id = str(param["elementId"])
                validated_params.append({"elementId": element_id})
            except Exception:
                raise ValueError(f"无效的元素ID格式: {param['elementId']}")

        # 执行显示操作
        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result_data = revit.send_command(method, validated_params)
        return result_data

    except Exception as e:
        logger.error(f"显示元素时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def parameter_elements(ctx: Context, method: str = "ParameterElements", params: List[dict[str, str]] = None) -> str:
    """
    获取Revit元素的参数信息，支持批量查询和特定参数查询，遵循JSON-RPC 2.0规范。

    特性:
    - 支持批量查询多个元素的参数
    - 可查询特定参数或元素所有参数
    - 返回参数哈希码、名称和值的完整信息
    - 完善的错误处理机制

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"ParameterElements"
        params (List[Dict]): 查询参数列表，每个字典包含:
            - elementId (Union[int, str]): 要查询的元素ID
            - parameterName (str, optional): 要查询的特定参数名称

    返回:
        dict: JSON-RPC 2.0格式的响应，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": {
                    "elementId1": [
                        {
                            "hashCode": int,
                            "parameterName": str,
                            "parameterValue": str,
                        }
                    ],
                    ...
                },
                "id": request_id
            }
            失败时: {
                "jsonrpc": "2.0",
                "error": {
                    "code": int,
                    "message": str,
                    "data": any
                },
                "id": request_id
            }

    示例:
        # 查询多个元素的参数
        response = parameter_elements(ctx, params=[
            {"elementId": 212792, "parameterName": "注释"},  # 获取特定参数
            {"elementId": 212781}  # 获取所有参数
        ])

        # 输出示例
        {
            "jsonrpc": "2.0",
            "result": {
                "212792": [
                    {
                        "hashCode": 12345,
                        "parameterName": "注释",
                        "parameterValue": "示例注释",
                    }
                ],
                "212781": [
                    {
                        "hashCode": 23456,
                        "parameterName": "长度",
                        "parameterValue": "5000",
                    },
                    ...
                ]
            },
            "id": 1
        }
    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数错误：'params'不能为空")

        for param in params:
            if "elementId" not in param:
                raise ValueError("每个参数字典必须包含'elementId'")
            if not isinstance(param["elementId"], (int, str)):
                raise ValueError("'elementId'必须是整数或字符串")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"获取元素参数时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def get_location(ctx: Context, method: str = "GetLocations", params: List[dict[str, str]] = None) -> dict:
    """
    获取Revit元素的位置信息，支持点和曲线元素，遵循JSON-RPC 2.0规范。

    特性:
    - 支持批量查询多个元素的位置
    - 自动处理单位转换（英尺转毫米）
    - 支持点位置和曲线位置（直线和圆弧）
    - 完善的错误处理机制

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"GetLocation"
        params (List[Dict]): 查询参数列表，每个字典包含:
            - elementId (Union[int, str]): 要查询的元素ID

    返回:
        dict: JSON-RPC 2.0格式的响应，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": {
                    "elementId1": [
                        {
                            "X": float,  # X坐标（毫米）
                            "Y": float,  # Y坐标（毫米）
                            "Z": float   # Z坐标（毫米）
                        },
                        ...
                    ],
                    ...
                },
                "id": request_id
            }
            失败时: {
                "jsonrpc": "2.0",
                "error": {
                    "code": int,
                    "message": str,
                    "data": any
                },
                "id": request_id
            }

    错误代码:
        -32600: 无效请求
        -32602: 无效参数（元素不存在等）
        -32603: 内部错误
        -32700: 解析错误

    示例:
        # 查询多个元素的位置
        response = get_location(ctx, params=[
            {"elementId": 123456},
            {"elementId": "789012"}
        ])

        # 输出示例（XYZ元素）
        {
            "jsonrpc": "2.0",
            "result": {
                "123456": [
                    {"X": 1000.0, "Y": 2000.0, "Z": 0.0}
                ]
            },
            "id": 1
        }

        # 输出示例（Line元素）
        {
            "jsonrpc": "2.0",
            "result": {
                "789012": [
                    {"X": 0.0, "Y": 0.0, "Z": 0.0},
                    {"X": 5000.0, "Y": 0.0, "Z": 0.0}
                ]
            },
            "id": 1
        }
        # 输出示例（Arc元素）
        {
            "jsonrpc": "2.0",
            "result": {
                "789012": [
                    {"X": 0.0, "Y": 0.0, "Z": 0.0},
                    {"X": 5000.0, "Y": 0.0, "Z": 0.0}
                    {"X": 2500.0, "Y": 1200, "Z": 0.0}
                ]
            },
            "id": 1
        }

        用途:找到定位后可用于创建门窗这种带有主体的族,族插入点就可以通过这个计算出来

    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数错误：'params'不能为空")

        validated_params = []
        for param in params:
            if "elementId" not in param:
                raise ValueError("每个参数字典必须包含'elementId'")
            if not isinstance(param["elementId"], (int, str)):
                raise ValueError("'elementId'必须是整数或字符串")

            validated_params.append({
                "elementId": str(param["elementId"])  # 统一转为字符串以匹配服务器处理
            })

        from .server import get_Revit_connection
        revit = get_Revit_connection()

        # 发送请求并获取响应
        response = revit.send_command(method, validated_params)
        return response

    except ValueError as ve:
        error_response = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32602,  # Invalid params
                "message": f"无效参数: {str(ve)}",
                "data": params
            },
            "id": ctx.request_id if hasattr(ctx, "request_id") else 1
        }
        ctx.logger.error(f"参数验证失败: {str(ve)}")
        return error_response

    except Exception as e:
        error_response = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,  # Internal error
                "message": f"内部错误: {str(e)}",
                "data": params
            },
            "id": ctx.request_id if hasattr(ctx, "request_id") else 1
        }
        ctx.logger.error(f"获取元素位置时发生错误: {str(e)}", exc_info=True)
        return error_response


def create_levels(ctx: Context, method: str = "CreateLevels", params: List[dict[str, any]] = None) -> str:
    """
    在Revit中创建标高，支持批量创建，遵循JSON-RPC 2.0规范。

    特性:
    - 支持批量创建多个标高
    - 自动处理单位转换（毫米转英尺）
    - 自动处理标高名称冲突
    - 完善的错误处理机制

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"CreateLevels"
        params (List[Dict]): 标高参数列表，每个字典包含:
            - elevation (float): 标高高度（毫米）
            - name (str, optional): 标高名称（可选，默认为"Level_{elevation}"）

    返回:
        dict: JSON-RPC 2.0格式的响应，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [elementId1, elementId2, ...],
                "id": request_id
            }
            失败时: {
                "jsonrpc": "2.0",
                "error": {
                    "code": int,
                    "message": str,
                    "data": any
                },
                "id": request_id
            }

    示例:
        # 创建多个标高
        response = create_levels(ctx, params=[
            {"elevation": 8000, "name": "Level_3"},
            {"elevation": 12000}  # 自动生成名称"Level_12000"
        ])

        # 输出示例
        {
            "jsonrpc": "2.0",
            "result": [212792, 212793],
            "id": 1
        }
    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数错误：'params'不能为空")

        validated_params = []
        for param in params:
            if "elevation" not in param:
                raise ValueError("每个参数字典必须包含'elevation'")

            if not isinstance(param["elevation"], (int, float)):
                raise ValueError("'elevation'必须是数字")

            # 构建标准化参数
            validated_param = {
                "elevation": float(param["elevation"])
            }

            # 可选参数处理
            if "name" in param:
                if not isinstance(param["name"], str):
                    raise ValueError("'name'必须是字符串")
                validated_param["name"] = param["name"]

            validated_params.append(validated_param)

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, validated_params)
        return result

    except Exception as e:
        logger.error(f"创建标高时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def create_grids(ctx: Context, method: str = "CreateGrids", params: List[dict[str, any]] = None) -> str:
    """
    在Revit中创建轴网，支持直线轴网和弧线轴网，遵循JSON-RPC 2.0规范。

    特性:
    - 支持批量创建多个轴网
    - 支持直线轴网和弧线轴网创建
    - 自动处理单位转换（毫米转英尺）
    - 自动处理轴网名称冲突
    - 完善的错误处理机制

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"CreateGrids"
        params (List[Dict]): 轴网参数列表，每个字典包含:
            - startX (float): 起点X坐标（毫米）
            - startY (float): 起点Y坐标（毫米）
            - endX (float): 终点X坐标（毫米）
            - endY (float): 终点Y坐标（毫米）
            - name (str, optional): 轴网名称（可选）
            - centerX (float, optional): 弧线轴网的圆心X坐标（毫米）
            - centerY (float, optional): 弧线轴网的圆心Y坐标（毫米）

    返回:
        dict: JSON-RPC 2.0格式的响应，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [elementId1, elementId2, ...],
                "id": request_id
            }
            失败时: {
                "jsonrpc": "2.0",
                "error": {
                    "code": int,
                    "message": str,
                    "data": any
                },
                "id": request_id
            }

    示例:
        # 创建直线轴网和弧线轴网
        response = create_grids(ctx, params=[
            {
                "name": "Grid_A",
                "startX": 0,
                "startY": 0,
                "endX": 10000,
                "endY": 0
            },
            {
                "name": "Grid_B",
                "startX": 5000,
                "startY": 0,
                "endX": 5000,
                "endY": 10000,
                "centerX": 5000,
                "centerY": 5000
            }
        ])

        # 输出示例
        {
            "jsonrpc": "2.0",
            "result": [212801, 212802],
            "id": 1
        }
    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数错误：'params'不能为空")

        validated_params = []
        for param in params:
            # 必需参数检查
            required_params = ["startX", "startY", "endX", "endY"]
            for p in required_params:
                if p not in param:
                    raise ValueError(f"缺少必需参数: '{p}'")
                if not isinstance(param[p], (int, float)):
                    raise ValueError(f"'{p}'必须是数字")

            # 构建标准化参数
            validated_param = {
                "startX": float(param["startX"]),
                "startY": float(param["startY"]),
                "endX": float(param["endX"]),
                "endY": float(param["endY"])
            }

            # 可选参数处理
            if "name" in param:
                if not isinstance(param["name"], str):
                    raise ValueError("'name'必须是字符串")
                validated_param["name"] = param["name"]

            # 弧线参数检查（必须同时存在或不存在）
            has_centerX = "centerX" in param
            has_centerY = "centerY" in param
            if has_centerX != has_centerY:
                raise ValueError("centerX和centerY必须同时提供或同时省略")

            if has_centerX:
                if not isinstance(param["centerX"], (int, float)) or not isinstance(param["centerY"], (int, float)):
                    raise ValueError("centerX和centerY必须是数字")
                validated_param["centerX"] = float(param["centerX"])
                validated_param["centerY"] = float(param["centerY"])

            validated_params.append(validated_param)

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, validated_params)
        return result

    except Exception as e:
        logger.error(f"创建轴网时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def create_walls(ctx: Context, method: str = "CreateWalls", params: List[dict[str, any]] = None) -> str:
    """
    在Revit中创建墙体，支持批量创建，遵循JSON-RPC 2.0规范。

    特性:
    - 支持批量创建多个墙体
    - 自动处理单位转换（毫米转英尺）
    - 自动创建或匹配符合厚度的墙类型
    - 支持指定标高或使用默认标高
    - 完善的错误处理机制

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"CreateWalls"
        params (List[Dict]): 墙体参数列表，每个字典包含:
            - startX (float): 起点X坐标（毫米）
            - startY (float): 起点Y坐标（毫米）
            - endX (float): 终点X坐标（毫米）
            - endY (float): 终点Y坐标（毫米）
            - height (float): 墙体高度（毫米）
            - width (float): 墙体厚度（毫米）
            - elevation (float, optional): 墙体底部标高（毫米，默认为0）

    返回:
        dict: JSON-RPC 2.0格式的响应，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [elementId1, elementId2, ...],
                "id": request_id
            }
            失败时: {
                "jsonrpc": "2.0",
                "error": {
                    "code": int,
                    "message": str,
                    "data": any
                },
                "id": request_id
            }

    示例:
        # 创建多个墙体
        response = create_walls(ctx, params=[
            {
                "startX": 0,
                "startY": 0,
                "endX": 5000,
                "endY": 0,
                "height": 3000,
                "width": 200
            },
            {
                "startX": 5000,
                "startY": 0,
                "endX": 5000,
                "endY": 5000,
                "height": 3000,
                "width": 200,
                "elevation": 1000
            }
        ])

        # 输出示例
        {
            "jsonrpc": "2.0",
            "result": [212901, 212902],
            "id": 1
        }
    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数错误：'params'不能为空")

        validated_params = []
        for param in params:
            # 必需参数检查
            required_params = ["startX", "startY", "endX", "endY", "height", "width"]
            for p in required_params:
                if p not in param:
                    raise ValueError(f"缺少必需参数: '{p}'")
                if not isinstance(param[p], (int, float)):
                    raise ValueError(f"'{p}'必须是数字")

            # 构建标准化参数
            validated_param = {
                "startX": float(param["startX"]),
                "startY": float(param["startY"]),
                "endX": float(param["endX"]),
                "endY": float(param["endY"]),
                "height": float(param["height"]),
                "width": float(param["width"])
            }

            # 可选参数处理
            if "elevation" in param:
                if not isinstance(param["elevation"], (int, float)):
                    raise ValueError("'elevation'必须是数字")
                validated_param["elevation"] = float(param["elevation"])

            validated_params.append(validated_param)

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, validated_params)
        return result

    except Exception as e:
        logger.error(f"创建墙体时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def create_rooms(ctx: Context, method: str = "CreateRooms", params: List[dict[str, str]] = None) -> dict:
    """
    在指定标高上创建房间，遵循JSON-RPC 2.0规范。

    特性:
    - 支持批量在多个标高上创建房间
    - 自动验证标高元素有效性
    - 事务化操作确保数据一致性
    - 完善的错误处理机制

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"CreateRooms"
        params (List[Dict]): 标高参数列表，每个字典包含:
            - elementId (Union[int, str]): 标高元素ID

    返回:
        dict: JSON-RPC 2.0格式的响应，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [创建的房间元素ID列表],
                "id": request_id
            }
            失败时: {
                "jsonrpc": "2.0",
                "error": {
                    "code": int,
                    "message": str,
                    "data": any
                },
                "id": request_id
            }

    错误代码:
        -32600: 无效请求
        -32602: 无效参数（元素不是标高或无效）
        -32603: 内部错误
        -32700: 解析错误

    示例:
        # 在多个标高上创建房间
        response = create_rooms(ctx, params=[
            {"elementId": 123456},  # 标高1的ID
            {"elementId": "789012"}  # 标高2的ID
        ])

        # 输出示例
        {
            "jsonrpc": "2.0",
            "result": [212801, 212802, 212803],  # 创建的房间ID列表
            "id": 1
        }

    注意:
        1. 会在指定标高的所有封闭区域创建房间
        2. 返回的房间ID列表顺序与创建顺序一致
        3. 如果标高没有封闭区域，则不会创建房间但也不会报错
    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数错误：'params'不能为空")

        validated_params = []
        for param in params:
            if "elementId" not in param:
                raise ValueError("每个参数字典必须包含'elementId'")
            if not isinstance(param["elementId"], (int, str)):
                raise ValueError("'elementId'必须是整数或字符串")

            # 统一转为字符串以匹配服务器处理
            validated_params.append({
                "elementId": str(param["elementId"])
            })

        from .server import get_Revit_connection
        revit = get_Revit_connection()

        # 发送请求并获取响应
        response = revit.send_command(method, validated_params)
        return response

    except ValueError as ve:
        error_response = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32602,  # Invalid params
                "message": f"无效参数: {str(ve)}",
                "data": params
            },
            "id": ctx.request_id if hasattr(ctx, "request_id") else 1
        }
        ctx.logger.error(f"参数验证失败: {str(ve)}")
        return error_response

    except Exception as e:
        error_response = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,  # Internal error
                "message": f"内部错误: {str(e)}",
                "data": params
            },
            "id": ctx.request_id if hasattr(ctx, "request_id") else 1
        }
        ctx.logger.error(f"创建房间时发生错误: {str(e)}", exc_info=True)
        return error_response


def create_floors(ctx: Context, method: str = "CreateFloors", params: List[dict[str, any]] = None) -> str:
    """
    在Revit中创建楼板，支持批量创建，遵循JSON-RPC 2.0规范。

    特性:
    - 支持批量创建多个楼板
    - 自动处理单位转换（毫米转英尺）
    - 自动匹配楼板类型或使用默认类型
    - 支持结构楼板和非结构楼板
    - 自动根据z值标高确定楼层
    - 完善的错误处理机制

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"CreateFloors"
        params (List[Dict]): 楼板参数列表，每个字典包含:
            - boundaryPoints (List[Dict]): 楼板边界点列表，每个点包含:
                - x (float): X坐标（毫米）
                - y (float): Y坐标（毫米）
                - z (float): Z坐标（毫米）
            - floorTypeName (str, optional): 楼板类型名称（可选）
            - structural (bool, optional): 是否为结构楼板（默认为False）

    返回:
        dict: JSON-RPC 2.0格式的响应，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [elementId1, elementId2, ...],
                "id": request_id
            }
            失败时: {
                "jsonrpc": "2.0",
                "error": {
                    "code": int,
                    "message": str,
                    "data": any
                },
                "id": request_id
            }

    示例:
        # 创建多个楼板
        response = create_floors(ctx, params=[
            {
                "boundaryPoints": [
                    {"x": 0, "y": 0, "z": 0},
                    {"x": 5000, "y": 0, "z": 0},
                    {"x": 5000, "y": 5000, "z": 0},
                    {"x": 0, "y": 5000, "z": 0},
                    {"x": 0, "y": 0, "z": 0}
                ],
                "floorTypeName": "常规 - 150mm",
                "structural": True
            },
            {
                "boundaryPoints": [
                    {"x": 0, "y": 0, "z": 3000},
                    {"x": 5000, "y": 0, "z": 3000},
                    {"x": 5000, "y": 5000, "z": 3000},
                    {"x": 0, "y": 5000, "z": 3000},
                    {"x": 0, "y": 0, "z": 3000}
                ],
                "floorTypeName": "常规 - 200mm"
            }
        ])

        # 输出示例
        {
            "jsonrpc": "2.0",
            "result": [213001, 213002],
            "id": 1
        }
    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数错误：'params'不能为空")

        validated_params = []
        for param in params:
            # 必需参数检查
            if "boundaryPoints" not in param:
                raise ValueError("缺少必需参数: 'boundaryPoints'")

            if not isinstance(param["boundaryPoints"], list) or len(param["boundaryPoints"]) < 3:
                raise ValueError("'boundaryPoints'必须包含至少3个点的列表")

            # 验证每个边界点
            validated_points = []
            for point in param["boundaryPoints"]:
                if not isinstance(point, dict):
                    raise ValueError("边界点必须是字典格式")

                for coord in ["x", "y", "z"]:
                    if coord not in point:
                        raise ValueError(f"边界点缺少坐标: '{coord}'")
                    if not isinstance(point[coord], (int, float)):
                        raise ValueError(f"坐标'{coord}'必须是数字")

                validated_points.append({
                    "x": float(point["x"]),
                    "y": float(point["y"]),
                    "z": float(point["z"])
                })

            # 构建标准化参数
            validated_param = {
                "boundaryPoints": validated_points
            }

            # 可选参数处理
            if "floorTypeName" in param:
                if not isinstance(param["floorTypeName"], str):
                    raise ValueError("'floorTypeName'必须是字符串")
                validated_param["floorTypeName"] = param["floorTypeName"]

            if "structural" in param:
                if not isinstance(param["structural"], bool):
                    raise ValueError("'structural'必须是布尔值")
                validated_param["structural"] = param["structural"]

            validated_params.append(validated_param)

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, validated_params)
        return result

    except Exception as e:
        logger.error(f"创建楼板时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def create_family_instances(ctx: Context, method: str = "CreateFamilyInstances",
                            params: List[dict[str, any]] = None) -> str:
    """
    在Revit中创建族实例，支持多种放置方式，遵循JSON-RPC 2.0规范。

    特性:
    - 支持批量创建多个族实例
    - 自动处理单位转换（毫米转英尺）
    - 支持多种放置类型：
        - 基于标高放置
        - 基于视图放置
        - 基于工作平面放置
        - 基于宿主放置
        - 基于曲线放置
    - 支持旋转和偏移
    - 自动匹配族类型和类别
    - 完善的错误处理机制

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): JSON-RPC方法名，默认为"CreateFamilyInstances"
        params (List[Dict]): 族实例参数列表，每个字典包含:
            - categoryName (str): 族类别名称（如"OST_Walls","OST_Doors", "墙", "门", "结构框架"等）
            - name (str): 族类型名称
            - startX (float): 起点X坐标（毫米）
            - startY (float): 起点Y坐标（毫米）
            - startZ (float): 起点Z坐标（毫米）
            - familyName (str, optional): 族名称（可选，用于更精确匹配）
            - endX (float, optional): 终点X坐标（毫米，默认等于startX）
            - endY (float, optional): 终点Y坐标（毫米，默认等于startY）
            - endZ (float, optional): 终点Z坐标（毫米，默认等于startZ）
            - hostId (str, optional): 宿主元素ID（可选）
            - viewName (str, optional): 视图名称（可选）
            - rotationAngle (float, optional): 旋转角度（度，默认0）
            - offset (float, optional): 偏移距离（毫米，默认0）

    返回:
        dict: JSON-RPC 2.0格式的响应，结构为:
            成功时: {
                "jsonrpc": "2.0",
                "result": [elementId1, elementId2, ...],
                "id": request_id
            }
            失败时: {
                "jsonrpc": "2.0",
                "error": {
                    "code": int,
                    "message": str,
                    "data": any
                },
                "id": request_id
            }

    示例:
        # 创建多个族实例
        response = create_family_instances(ctx, params=[
            # 基于标高的门
            {
                "categoryName": "窗",
                "name": "0406 x 0610mm",
                "startX": 1000,
                "startY": 2000,
                "startZ": 0,
                "hostid": 225535,
                "level": "标高 1",
            },
            # 基于视图的家具
            {
                "categoryName": "OST_Furniture",
                "name": "办公桌",
                "startX": 3000,
                "startY": 4000,
                "startZ": 0,
                "viewName": "标高 1",
                "rotationAngle": 90
            },
            # 基于曲线的梁
            {
                "categoryName": "OST_StructuralFraming",
                "name": "H型钢梁",
                "startX": 0,
                "startY": 0,
                "startZ": 3000,
                "endX": 5000,
                "endY": 0,
                "endZ": 3000
            }
        ])

        # 输出示例
        {
            "jsonrpc": "2.0",
            "result": [213101, 213102, 213103],
            "id": 1
        }
    """
    try:
        # 参数验证
        if not params:
            raise ValueError("参数错误：'params'不能为空")

        validated_params = []
        for param in params:
            # 必需参数检查
            required_params = ["categoryName", "name", "startX", "startY", "startZ"]
            for p in required_params:
                if p not in param:
                    raise ValueError(f"缺少必需参数: '{p}'")
                if p in ["startX", "startY", "startZ"] and not isinstance(param[p], (int, float)):
                    raise ValueError(f"'{p}'必须是数字")
                if p in ["categoryName", "name"] and not isinstance(param[p], str):
                    raise ValueError(f"'{p}'必须是字符串")

            # 构建标准化参数
            validated_param = {
                "categoryName": param["categoryName"],
                "name": param["name"],
                "startX": float(param["startX"]),
                "startY": float(param["startY"]),
                "startZ": float(param["startZ"])
            }

            # 可选参数处理
            optional_params = {
                "familyName": str,
                "endX": (int, float),
                "endY": (int, float),
                "endZ": (int, float),
                "hostId": str,
                "viewName": str,
                "rotationAngle": (int, float),
                "offset": (int, float)
            }

            for param_name, param_type in optional_params.items():
                if param_name in param:
                    if not isinstance(param[param_name], param_type):
                        raise ValueError(f"'{param_name}'必须是{param_type.__name__}")
                    validated_param[param_name] = param[param_name]

            # 设置默认值
            if "endX" not in validated_param:
                validated_param["endX"] = validated_param["startX"]
            if "endY" not in validated_param:
                validated_param["endY"] = validated_param["startY"]
            if "endZ" not in validated_param:
                validated_param["endZ"] = validated_param["startZ"]
            if "rotationAngle" not in validated_param:
                validated_param["rotationAngle"] = 0

            validated_params.append(validated_param)
        from .server import get_Revit_connection
        revit = get_Revit_connection()

        # 构建调用方法的参数
        result = revit.send_command(method, validated_params)

        return result
    except Exception as e:
        logger.error(f"创建族实例时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"
