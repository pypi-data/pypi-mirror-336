# -*- coding: utf-8 -*-
# prompt.py
# Copyright (c) 2025 zedmoster

import mcp.types as types

PROMPTS = {
    "CallFunc": types.Prompt(
        name="CallFunc",
        description="根据给定参数异步调用指定函数。",
        arguments=[
            types.PromptArgument(
                name="func",
                description=(
                    "要调用的函数名称。支持的函数：'ClearDuplicates'。"
                    "使用 'ClearDuplicates' 清除相同位置的重复元素，防止在日程中多次计数。"
                    "此功能适用于不小心将同一族实例叠放的情况。"
                ),
                required=True
            ),
        ],
    ),

    "FindElements": types.Prompt(
        name="FindElements",
        description="在Revit场景中查找元素。",
        arguments=[
            types.PromptArgument(
                name="categoryName",
                description="要搜索的类别名称（必填）。",
                required=True
            ),
            types.PromptArgument(
                name="categoryId",
                description="要搜索的类别ID（可选）。"
            ),
            types.PromptArgument(
                name="isInstance",
                description="是否搜索实例或类型（可选）。",
                required=False
            )
        ],
    ),
    "UpdateElements": types.Prompt(
        name="UpdateElements",
        description="更新Revit元素的参数。",
        arguments=[
            types.PromptArgument(
                name="elementId",
                description="要更新的元素ID。",
                required=True
            ),
            types.PromptArgument(
                name="parameterName",
                description="要更新的参数名称。",
                required=True
            ),
            types.PromptArgument(
                name="parameterValue",
                description="参数的新值。",
                required=True
            )
        ],
    ),
    "DeleteElements": types.Prompt(
        name="DeleteElements",
        description="从Revit中删除元素。",
        arguments=[
            types.PromptArgument(
                name="elementId",
                description="要删除的元素ID。",
                required=True
            )
        ],
    ),
    "ShowElements": types.Prompt(
        name="ShowElements",
        description="在Revit中显示元素。",
        arguments=[
            types.PromptArgument(
                name="elementId",
                description="要显示的元素ID。",
                required=True
            )
        ],
    ),

    "CreateLevels": types.Prompt(
        name="CreateLevels",
        description="在Revit中创建标高。",
        arguments=[
            types.PromptArgument(
                name="name",
                description="标高名称（必填）。",
                required=True
            ),
            types.PromptArgument(
                name="elevation",
                description="标高高程（单位：mm，必填）。",
                required=True
            ),
        ],
    ),
    "CreateGrids": types.Prompt(
        name="CreateGrids",
        description="在Revit中创建轴网，支持直线和弧形轴网。",
        arguments=[
            types.PromptArgument(
                name="name",
                description="轴网名称（必填）。",
                required=True
            ),
            types.PromptArgument(
                name="startX",
                description="轴网起点X坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="startY",
                description="轴网起点Y坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="endX",
                description="轴网终点X坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="endY",
                description="轴网终点Y坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="centerX",
                description=(
                    "弧形轴网中心X坐标（单位：mm）。仅在创建弧形轴网时使用（可选）。"
                ),
            ),
            types.PromptArgument(
                name="centerY",
                description=(
                    "弧形轴网中心Y坐标（单位：mm）。仅在创建弧形轴网时使用（可选）。"
                ),
            ),
        ],
    ),

    "CreateWalls": types.Prompt(
        name="CreateWalls",
        description="在Revit中创建墙体。",
        arguments=[
            types.PromptArgument(
                name="startX",
                description="墙体起点X坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="startY",
                description="墙体起点Y坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="endX",
                description="墙体终点X坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="endY",
                description="墙体终点Y坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="height",
                description="墙体高度（单位：mm，必须为正数，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="width",
                description="墙体宽度（单位：mm，必须为正数，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="elevation",
                description="墙体所在层高（单位：mm，可选）。"
            ),
        ],
    ),

    "CreateFloors": types.Prompt(
        name="CreateFloors",
        description="在Revit中使用指定边界点和楼板类型创建楼板。",
        arguments=[
            types.PromptArgument(
                name="boundaryPoints",
                description=(
                    "表示楼板边界的坐标点列表，每个点为一个包含x, y, z的字典（必填）。"
                ),
                required=True
            ),
            types.PromptArgument(
                name="floorTypeName",
                description="用于创建楼板的楼板类型名称（可选）。",
                required=False
            ),
            types.PromptArgument(
                name="structural",
                description=(
                    "是否为结构性楼板。若为结构性则为True，否则为False。默认值为False。"
                ),
                required=False,
                default=False
            ),
        ]
    ),

    "CreateFamilyInstances": types.Prompt(
        name="CreateFamilyInstances",
        description="在Revit中创建族实例。",
        arguments=[
            types.PromptArgument(
                name="categoryName",
                description="族所属类别名称（例如：Windows、Doors等，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="startX",
                description="族实例放置起点X坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="startY",
                description="族实例放置起点Y坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="startZ",
                description="族实例放置起点Z坐标（单位：mm，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="name",
                description="族符号名称（例如：500x500、600x600等，必填）。",
                required=True
            ),
            types.PromptArgument(
                name="familyName",
                description="族名称（例如：钢结构、混凝土等，可选）。"
            ),
            types.PromptArgument(
                name="endX",
                description="族实例放置终点X坐标（单位：mm，可选）。",
            ),
            types.PromptArgument(
                name="endY",
                description="族实例放置终点Y坐标（单位：mm，可选）。",
            ),
            types.PromptArgument(
                name="endZ",
                description="族实例放置终点Z坐标（单位：mm，可选）。",
            ),
            types.PromptArgument(
                name="hostId",
                description="族实例所依赖宿主元素的ID（例如：墙、楼板等，可选）。"
            ),
            types.PromptArgument(
                name="viewName",
                description="放置族实例的视图名称（例如：3D视图、平面图视图，可选）。"
            ),
            types.PromptArgument(
                name="rotationAngle",
                description="族实例的旋转角度（单位：度，如适用，可选）。",
            ),
            types.PromptArgument(
                name="offset",
                description="族实例相对于宿主或基准层的偏移距离（单位：mm，如适用，可选）。"
            ),
        ]
    ),

}


async def list_prompts_response() -> list[types.Prompt]:
    """
    获取所有可用提示词的列表。
    返回：
    - list[types.Prompt]: 提示词定义列表。
    """
    return list(PROMPTS.values())


async def get_prompt_response(method: str, arguments: dict[str, str] | None = None) -> types.GetPromptResult:
    """
    根据提供的参数生成指定方法的响应信息。
    
    参数：
    - method (str): 要执行的提示词方法名称。
    - arguments (dict[str, str] | None): 可选，包含参数名称和值的字典。

    返回：
    - types.GetPromptResult: 格式化后的响应对象，包含执行详情。

    异常：
    - 如果提供的方法在PROMPTS中不存在，则抛出ValueError异常。
    """
    if method not in PROMPTS:
        available_prompts = ', '.join(PROMPTS.keys())
        raise ValueError(f"无效的方法：'{method}'。可用的提示词有：{available_prompts}")

    # 格式化参数信息以便显示
    params_str = "\n".join(f"- {key}: {value}" for key, value in (arguments or {}).items())

    return types.GetPromptResult(
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"响应消息的语言为中文。正在执行 '{method}'，详细信息如下：\n\n{params_str or '未提供参数。'}"
                )
            )
        ]
    )
