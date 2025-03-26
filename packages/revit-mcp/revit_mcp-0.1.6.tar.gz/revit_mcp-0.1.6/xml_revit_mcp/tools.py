# -*- coding: utf-8 -*-
# tools.py
# Copyright (c) 2025 zedmoster

import logging
from typing import List
from mcp.server.fastmcp import Context

logger = logging.getLogger("RevitTools")


def call_func(ctx: Context, method: str = "CallFunc", params: List[str] = None) -> List[int]:
    """
    异步调用指定的函数，并根据给定的方法和参数执行操作。
    默认返回中文响应信息（"zh"）。

    此函数用于执行不同的Revit API功能，例如 "ClearDuplicates"，
    根据所提供的方法名称发送命令给Revit，并异步执行操作，
    返回受影响的元素ID列表。

    支持的功能：
    - "ClearDuplicates": 清除位于相同位置的重复元素，防止在日程中重复计数，
      适用于意外叠加的同一族实例。

    参数：
    - ctx (Context): 当前FastMCP上下文，用于管理Revit操作。
    - method (str): 要调用的函数名称，默认为 "CallFunc"。
    - params (List[str]): 调用函数所需的参数列表，对于 "ClearDuplicates" 无需额外参数。

    返回：
    - List[int]: 受函数调用影响的元素ID列表（如 "ClearDuplicates" 返回被删除元素的ID）。

    异常：
    - 如果params不是字符串列表，则抛出ValueError异常。
    - 执行过程中出错时记录异常并返回空列表。
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


def find_elements(ctx: Context, method: str = "FindElements", params: List[dict[str, object]] = None) -> List[int]:
    """
    根据类别ID或类别名称查找Revit场景中的元素。
    默认返回中文响应信息（"zh"）。

    参数：
    - ctx (Context): 当前FastMCP上下文，用于管理Revit操作。
    - method (str): 要调用的Revit API方法，默认为 "FindElements"。
    - params (List[dict[str, object]]): 包含搜索条件的字典列表，
      例如：
        - categoryId (int, 可选)：要搜索的类别ID。
        - categoryName (str, 可选)：要搜索的类别名称。
        - isInstance (bool, 可选)：是否搜索实例或类型。

    返回：
    - List[int]: 匹配的元素ID列表。
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
    默认返回中文响应信息（"zh"）。

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


def create_elements(ctx: Context, method: str, params: List[dict[str, object]] = None) -> str:
    """
    创建Revit场景中的各种类型元素。
    默认返回中文响应信息（"zh"）。

    参数：
    - ctx (Context): 当前FastMCP上下文。
    - method (str): 用于创建元素的Revit API方法。
        支持的方法包括：
        - "CreateLevels": 创建标高
        - "CreateGrids": 创建轴网
        - "CreateWalls": 创建墙体
        - "CreateFamilyInstances": 创建族实例
        - "CreateFloors": 创建楼板
    - params (List[dict[str, object]]): 包含创建参数的字典列表，不同方法所需的必选和可选参数如下：

    **创建标高（CreateLevels）**
    - name (str): 标高名称。
    - elevation (float): 标高的高程值。
      *无可选参数。*

    **创建轴网（CreateGrids）**
    - name (str): 轴网名称。
    - startX, startY, endX, endY (float): 轴网起点和终点的坐标。
    - centerX, centerY (float, 可选): 用于创建弧形轴网的中心坐标。
      *创建弧形轴网时需提供centerX和centerY，对于直线轴网可省略此参数。*

    **创建墙体（CreateWalls）**
    - startX, startY, endX, endY (float): 墙体起点和终点的坐标。
    - height (float): 墙体高度。
    - width (float): 墙体厚度。
    - elevation (float, 可选): 墙体基础高程，默认为0。
      *如需在特定高度放置墙体，可指定elevation参数。*

    **创建楼板（CreateFloors）**
    - boundaryPoints (List[dict[str, float]]): 表示楼板边界的点列表（x, y坐标）。
    - floorTypeName (str, 可选): 楼板类型名称，如未指定则使用默认类型。
    - structural (bool, 可选): 是否为结构性楼板，默认为False。
      *如需特定楼板类型或结构性楼板，可分别使用floorTypeName和structural参数。*

    **创建族实例（CreateFamilyInstances）**
    - categoryName (str): 族实例所属类别（如 "Doors", "Windows", "Furniture"）。
    - startX, startY, startZ (float): 族实例插入点的坐标。
    - name (str): 族实例名称。如果未提供，将从项目中获取可选族类型供用户选择。
    - 可选参数：
      - familyName (str, 可选): 指定族类型，如未提供则使用项目默认族类型。
      - endX, endY, endZ (float, 可选): 对于线性族，需提供起点和终点。
      - hostId (int, 可选): **对于依赖宿主的族（如门窗），必须提供宿主元素ID。**
      - viewName (str, 可选): 插入族实例的视图名称，默认为当前视图。
      - rotationAngle (float, 可选): 族实例旋转角度（以弧度为单位）。
      - offset (float, 可选): 用于调整插入点的偏移量。
      *对于需要依赖宿主的族（如门窗），必须提供hostId；如需调整族实例位置，可指定rotationAngle或offset参数。*

    返回：
    - str: 表示成功或失败的结果消息。
    """
    try:
        # 参数验证：确保params为字典列表
        if not isinstance(params, list) or not all(isinstance(param, dict) for param in params):
            raise ValueError("参数错误：'params' 应为字典列表。")

        valid_methods = ["CreateWalls", "CreateFamilyInstances", "CreateFloors", "CreateGrids", "CreateLevels"]
        if method not in valid_methods:
            raise ValueError(f"参数错误：无效的方法 '{method}'。支持的方法有：{', '.join(valid_methods)}")

        # 验证各方法所需的必选参数
        required_params = {
            "CreateLevels": ["name", "elevation"],
            "CreateGrids": ["name", "startX", "startY", "endX", "endY"],
            "CreateWalls": ["startX", "startY", "endX", "endY", "height", "width"],
            "CreateFloors": ["boundaryPoints"],
            "CreateFamilyInstances": ["categoryName", "startX", "startY", "startZ", "name"],
        }

        missing_keys = []
        for param in params:
            if method in required_params:
                missing_keys += [key for key in required_params[method] if key not in param]

        if missing_keys:
            raise ValueError(f"缺少 {method} 所需的参数：{', '.join(set(missing_keys))}")

        # 针对 "CreateGrids" 进行特殊处理，确保结构正确
        if method == "CreateGrids":
            for param in params:
                if "centerX" in param and "centerY" in param:
                    # 弧形轴网：需要centerX和centerY，同时必须提供startX, startY, endX, endY
                    if "startX" not in param or "startY" not in param or "endX" not in param or "endY" not in param:
                        raise ValueError("弧形轴网缺少必要参数：必须提供 startX, startY, endX, endY。")
                else:
                    # 直线轴网：只需提供startX, startY, endX, endY
                    if "startX" not in param or "startY" not in param or "endX" not in param or "endY" not in param:
                        raise ValueError("直线轴网缺少必要参数：必须提供 startX, startY, endX, endY。")

        # 针对创建标高（CreateLevels）的特殊处理
        if method == "CreateLevels":
            for param in params:
                if "name" not in param or "elevation" not in param:
                    raise ValueError("创建标高时缺少必要参数：必须提供 name 和 elevation。")

        # 发送命令到Revit进行处理
        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"创建元素时发生错误：{str(e)}", exc_info=True)
        return f"错误：{str(e)}"
