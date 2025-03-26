# -*- coding: utf-8 -*-
# tools.py
# Copyright (c) 2025 zedmoster

import logging
from typing import List
from mcp.server.fastmcp import Context

logger = logging.getLogger("RevitTools")


def call_func(ctx: Context, method: str = "CallFunc", params: List[str] = None) -> str:
    """
    异步调用指定的Revit API函数并执行操作

    参数组合规则:
    - 通用调用: 只需指定method名称
    - 特殊方法:
        * "ClearDuplicates": 清除重复元素(无需额外参数)

    参数:
        ctx (Context): FastMCP上下文对象
        method (str): 要调用的方法名称，支持:
            - "CallFunc": 通用调用(默认)
            - "ClearDuplicates": 清除重复元素
        params (List[str], optional): 参数列表

    返回:
        str: 受影响的元素ID列表

    异常:
        ValueError: 当参数类型不正确时
        Exception: 执行过程中发生错误时记录日志

    示例:
        # 清除重复元素
        deleted_ids = call_func(ctx, "CallFunc", "ClearDuplicates")
    """
    try:
        # 参数验证：确保params为字符串列表或为None
        if params is not None and (not isinstance(params, list) or not all(isinstance(param, str) for param in params)):
            raise ValueError("参数错误：'params' 应为字符串列表或 None。")

        # 获取Revit连接实例
        from .server import get_Revit_connection
        revit = get_Revit_connection()

        # 发送命令并等待结果
        result = revit.send_command(method, params or [])
        # 返回执行结果
        return result

    except Exception as e:
        # 记录异常信息，并返回空列表
        logging.error(f"call_func 发生错误：{str(e)}", exc_info=True)
        return []


def find_elements(ctx: Context, method: str = "FindElements", params: List[dict[str, object]] = None) -> str:
    """
    查找Revit元素

    参数组合规则:
    - 按类别ID查找: {"categoryId": int}
    - 按类别名称查找: {"categoryName": str}
    - 组合查找: 
        {
            "categoryId": int,
            "categoryName": str,
            "isInstance": bool
        }

    参数:
        ctx (Context): FastMCP上下文
        method (str): 方法名称(默认"FindElements")
        params (List[Dict[str, object]], optional): 查询条件列表

    返回:
        str: 匹配的元素ID列表

    示例:
        # 按类别名称查找
        elements = find_elements(ctx, "FindElements", params=[{"categoryName": "墙"}])
    """
    try:
        # 参数验证：确保params为字典列表
        if not isinstance(params, list) or not all(isinstance(param, dict) for param in params):
            raise ValueError("参数错误：'params' 应为字典列表。")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"查找元素时发生错误：{str(e)}", exc_info=True)
        return []


def update_elements(ctx: Context, method: str = "UpdateElements", params: list[dict[str, str]] = None) -> str:
    """
    更新Revit模型中元素的参数。
    默认返回中文响应信息（"zh"）。

    参数：
    - ctx (Context): 当前FastMCP上下文。
    - method (str): 要调用的Revit API方法，默认为 "UpdateElements"。
    - params (List[dict[str, str]]): 包含更新数据的字典列表，每个字典包括：
        - elementId (int或str): 要更新的元素ID。
        - parameterName (str): 要更新的参数名称。
        - parameterValue (str): 新的参数值。

    返回：
    - str: 表示成功或失败的结果消息。
    """
    try:
        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"更新元素时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def delete_elements(ctx: Context, method: str = "DeleteElements", params: List[dict[str, str]] = None) -> str:
    """
    根据元素ID删除Revit模型中的元素。
    默认返回中文响应信息（"zh"）。

    参数：
    - ctx (Context): 当前FastMCP上下文。
    - method (str): 要调用的Revit API方法，默认为 "DeleteElements"。
    - params (List[int]): 包含要删除的元素ID的列表。

    返回：
    - str: 表示成功或失败的结果消息。
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
    在Revit视图中显示指定的元素。
    默认返回中文响应信息（"zh"）。

    参数：
    - ctx (Context): 当前FastMCP上下文。
    - method (str): 要调用的Revit API方法，默认为 "ShowElements"。
    - params (List[dict[str, str]]): 包含要显示元素ID的字典列表，每个字典包括：
        - elementId (int或str): 要显示的元素ID。

    返回：
    - str: 表示成功或失败的结果消息。
    """
    try:
        # 参数验证：确保params为包含'elementId'的字典列表
        if not params or not all(isinstance(param.get("elementId"), (int, str)) for param in params):
            raise ValueError("参数错误：'params' 应为包含 'elementId'（int或str）的字典列表。")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"显示元素时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def parameter_elements(ctx: Context, method: str = "ParameterElements", params: List[dict[str, str]] = None) -> str:
    """
    获取指定Revit元素的参数名称和值。
    默认返回中文响应信息（"zh"）。单位都是适用毫米作为单位!

    参数：
    - ctx (Context): 当前FastMCP上下文。
    - method (str): 要调用的Revit API方法，默认为 "ParameterElements"。
    - params (List[dict[str, str]]): 包含查询参数的字典列表，每个字典包括：
        - elementId (int或str): 要查询的Revit元素ID。
        - parameterName (str, 可选): 指定要查询的参数名称，如不提供则返回所有参数。

    示例用法：
    - 查询某个元素的所有参数：
        [{ "elementId": 123456 }]
    - 查询某个元素的特定参数：
        [{ "elementId": 123456, "parameterName": "Comments" }]

    返回：
    - str: 包含格式化参数数据的结果消息，或操作失败时的错误消息。
    """
    try:
        # 参数验证：确保params为包含'elementId'的字典列表
        if not params or not all(isinstance(param.get("elementId"), (int, str)) for param in params):
            raise ValueError("参数错误：'params' 应为包含 'elementId'（int或str）的字典列表。")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"获取元素参数时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def create_levels(ctx: Context, method: str = "CreateLevels", params: List[dict[str, any]] = None) -> str:
    """
    使用MCP创建Revit标高。

    参数：
    - ctx (Context): 当前FastMCP上下文。
    - method (str): 要调用的Revit API方法，默认为 "CreateLevels"。
    - params (List[dict[str, any]]): 包含标高数据的字典列表，每个字典包括：
        - name (str): 标高名称。
        - elevation (float): 标高的高度，单位为毫米。

    示例用法：
        [
            {"name": "Level_3", "elevation": 8000},
            {"name": "Level_4", "elevation": 12000}
        ]

    返回：
    - str: 包含操作结果的消息。
    """
    try:
        if not params or not all(isinstance(param.get("name"), str) and isinstance(param.get("elevation"), (int, float)) for param in params):
            raise ValueError(
                "参数错误：'params' 应为包含有效 'name' 和 'elevation' 的字典列表。")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"创建标高时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def create_grids(ctx: Context, method: str = "CreateGrids", params: List[dict[str, any]] = None) -> str:
    """
    使用MCP创建Revit轴网。

    参数：
    - ctx (Context): 当前FastMCP上下文。
    - method (str): 要调用的Revit API方法，默认为 "CreateGrids"。
    - params (List[dict[str, any]]): 包含轴网数据的字典列表，每个字典包括：
        - name (str): 轴网名称。
        - startX (float): 起点X坐标。（单位：mm）
        - startY (float): 起点Y坐标。（单位：mm）
        - endX (float): 终点X坐标。（单位：mm）
        - endY (float): 终点Y坐标。（单位：mm）
        - centerX (float, 可选): 弧线轴网的圆心X坐标。（单位：mm）
        - centerY (float, 可选): 弧线轴网的圆心Y坐标。（单位：mm）

    返回：
    - str: 包含操作结果的消息。
    """
    try:
        if not params or not all(isinstance(param.get("name"), str) and isinstance(param.get("startX"), (int, float)) and isinstance(param.get("startY"), (int, float)) and isinstance(param.get("endX"), (int, float)) and isinstance(param.get("endY"), (int, float)) for param in params):
            raise ValueError(
                "参数错误：'params' 应为包含有效 'name', 'startX', 'startY', 'endX' 和 'endY' 的字典列表。")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"创建轴网时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def create_walls(ctx: Context, method: str = "CreateWalls", params: List[dict[str, any]] = None) -> str:
    """
    使用MCP创建Revit墙体。

    参数：
    - ctx (Context): 当前FastMCP上下文。
    - method (str): 要调用的Revit API方法，默认为 "CreateWalls"。
    - params (List[dict[str, any]]): 包含墙体数据的字典列表，每个字典包括：
        - startX (float): 墙体起点X坐标。（单位：mm）
        - startY (float): 墙体起点Y坐标。（单位：mm）
        - endX (float): 墙体终点X坐标。（单位：mm）
        - endY (float): 墙体终点Y坐标。（单位：mm）
        - height (float): 墙体高度。（单位：mm）
        - width (float): 墙体厚度。（单位：mm）
        - elevation (float, 可选): 墙体标高，默认为0。（单位：mm）

    返回：
    - str: 包含操作结果的消息。
    """
    try:
        if not params or not all(isinstance(param.get("startX"), (int, float)) and isinstance(param.get("startY"), (int, float)) and isinstance(param.get("endX"), (int, float)) and isinstance(param.get("endY"), (int, float)) and isinstance(param.get("height"), (int, float)) and isinstance(param.get("width"), (int, float)) for param in params):
            raise ValueError(
                "参数错误：'params' 应为包含有效 'startX', 'startY', 'endX', 'endY', 'height' 和 'width' 的字典列表。")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"创建墙体时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def create_floors(ctx: Context, method: str = "CreateFloors", params: List[dict[str, any]] = None) -> str:
    """
    使用MCP创建Revit楼板。

    参数：
    - ctx (Context): 当前FastMCP上下文。
    - method (str): 要调用的Revit API方法，默认为 "CreateFloors"。
    - params (List[dict[str, any]]): 包含楼板数据的字典列表，每个字典包括：
        - boundaryPoints (List[dict[str, float]]): 楼板边界点的坐标。（单位：mm）
        - floorTypeName (str): 楼板类型名称。
        - structural (bool): 是否为结构楼板。

    示例用法：
        [
            {
                "boundaryPoints": [
                    {"x": 0.0, "y": 0.0, "z": 0.0},
                    {"x": 3000.0, "y": 0.0, "z": 0.0},
                    {"x": 3000.0, "y": 3000.0, "z": 0.0},
                    {"x": 0.0, "y": 3000.0, "z": 0.0},
                    {"x": 0.0, "y": 0.0, "z": 0.0}
                ],
                "floorTypeName": "常规 - 150mm",
                "structural": True
            }
        ]

    返回：
    - str: 包含操作结果的消息。
    """
    try:
        if not params or not all(isinstance(param.get("boundaryPoints"), list) and isinstance(param.get("floorTypeName"), str) for param in params):
            raise ValueError(
                "参数错误：'params' 应为包含有效 'boundaryPoints' 和 'floorTypeName' 的字典列表。")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"创建楼板时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"


def create_family_instances(ctx: Context, method: str = "CreateFamilyInstances", params: List[dict[str, any]] = None) -> str:
    """
    使用MCP在Revit中创建族实例。

    参数：
    - ctx (Context): 当前FastMCP上下文。
    - method (str): 要调用的Revit API方法，默认为 "CreateFamilyInstances"。
    - params (List[dict[str, any]]): 包含族实例数据的字典列表，每个字典包括：
        - categoryName (str): 族所属类别名称。
        - startX (float): 起点X坐标（单位：mm）。
        - startY (float): 起点Y坐标（单位：mm）。
        - startZ (float): 起点Z坐标（单位：mm）。
        - name (str): 族符号名称。
        - familyName (str, 可选): 族名称。
        - endX (float, 可选): 终点X坐标（单位：mm）。
        - endY (float, 可选): 终点Y坐标（单位：mm）。
        - endZ (float, 可选): 终点Z坐标（单位：mm）。
        - hostId (str, 可选): 族实例的宿主元素ID。
        - viewName (str, 可选): 视图名称。
        - rotationAngle (float, 可选): 旋转角度（单位：度）。
        - offset (float, 可选): 偏移距离（单位：mm）。

    返回：
    - str: 操作结果消息。
    """
    try:
        if not params or not all(isinstance(param.get("categoryName"), str) and 
                                 isinstance(param.get("startX"), (int, float)) and 
                                 isinstance(param.get("startY"), (int, float)) and 
                                 isinstance(param.get("startZ"), (int, float)) and 
                                 isinstance(param.get("name"), str) for param in params):
            raise ValueError("参数错误：'params' 应为包含有效 'categoryName', 'startX', 'startY', 'startZ', 'name' 的字典列表。")

        from .server import get_Revit_connection
        revit = get_Revit_connection()

        # 构建调用方法的参数
        result = revit.send_command(method, params)

        return result
    except Exception as e:
        logger.error(f"创建族实例时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"
