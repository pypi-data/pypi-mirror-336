# tools.py
# Copyright (c) 2025 zedmoster

import logging
from typing import List
from mcp.server.fastmcp import Context

logger = logging.getLogger("RevitTools")


def call_func(ctx: Context, method: str = "CallFunc", params: List[str] = None) -> List[int]:
    """
    Calls a specified function asynchronously based on the given method and parameters.
    The language for the response message. Default is 中文 ("zh").

    This function handles the execution of various Revit API functions, such as "ClearDuplicates",
    based on the method provided. It sends a command to Revit, which is then executed
    asynchronously, and returns the list of element IDs affected by the function.

    Supported Functions:
    - "ClearDuplicates": Removes duplicate elements located at the same position, preventing
      double counting in schedules. This is useful when unintended duplicate instances
      of the same family are placed on top of each other.

    Parameters:
    - ctx (Context): The current FastMCP context for managing Revit operations.
    - method (str): The name of the function to call. Default is "CallFunc".
    - params (List[str]): A list of parameters required for the function. For "ClearDuplicates",
      no additional parameters are required.

    Returns:
    - List[int]: A list of element IDs affected by the function call. When using "ClearDuplicates",
      it returns the IDs of the elements that were removed.

    Exceptions:
    - Raises ValueError if `params` is not a list of strings.
    - Logs and returns an empty list in case of errors during function execution.
    """
    try:
        # 参数验证，确保params为一个包含字符串的列表
        if params is not None and (not isinstance(params, list) or not all(isinstance(param, str) for param in params)):
            raise ValueError(
                "Invalid input: 'params' should be a list of strings or None.")

        # 获取Revit连接实例
        from .server import get_Revit_connection
        revit = get_Revit_connection()

        # 发送命令并等待结果
        result = revit.send_command(method, params or [])
        # 返回执行结果
        return result

    except Exception as e:
        # 记录异常信息并返回空列表
        logging.error(f"Error in call_func: {str(e)}", exc_info=True)
        return []


def find_elements(ctx: Context, method: str = "FindElements", params: List[dict[str, object]] = None) -> List[int]:
    """
    Finds elements in the Revit scene using categoryId or categoryName.
    The language for the response message. Default is 中文 ("zh").

    Parameters:
    - ctx (Context): The current FastMCP context for managing Revit operations.
    - method (str): The Revit API method to call. Default is "FindElements".
    - params (List[dict[str, object]]): A list of dictionaries specifying search parameters.
      - categoryId (int, optional): The ID of the category to search.
      - categoryName (str, optional): The name of the category to search.
      - isInstance (bool, optional): Whether to search for instances or types.

    Returns:
    - List[int]: A list of matching element IDs.
    """
    try:
        if not isinstance(params, list) or not all(isinstance(param, dict) for param in params):
            raise ValueError(
                "Invalid input: 'params' should be a list of dictionaries.")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"Error finding elements. {str(e)}", exc_info=True)
        return []


def update_elements(ctx: Context, method: str = "UpdateElements", params: list[dict[str, str]] = None) -> str:
    """
    Updates the parameters of elements in the Revit model.
    The language for the response message. Default is 中文 ("zh").

    Parameters:
    - ctx (Context): The FastMCP context.
    - method (str): The Revit API method to call. Default is "UpdateElements".
    - params (List[dict[str, str]]): List of dictionaries with update data:
      - elementId (int or str): The ID of the element to be updated.
      - parameterName (str): The parameter name to update.
      - parameterValue (str): The new parameter value.

    Returns:
    - str: Result message indicating success or failure.
    """
    try:
        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"Error updating elements. {str(e)}", exc_info=True)
        return f"Error: {str(e)}"


def delete_elements(ctx: Context, method: str = "DeleteElements", params: List[dict[str, str]] = None) -> str:
    """
    Deletes elements from the Revit model using their IDs.
    The language for the response message. Default is 中文 ("zh").

    Parameters:
    - ctx (Context): The FastMCP context.
    - method (str): The Revit API method to call. Default is "DeleteElements".
    - params (List[int]): List of element IDs to delete.

    Returns:
    - str: Result message indicating success or failure.
    """
    try:
        if not params or not all(isinstance(el_id, int) for el_id in params):
            raise ValueError(
                "Invalid input: 'params' should be a list of element IDs (int).")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"Error deleting elements. {str(e)}", exc_info=True)
        return f"Error: {str(e)}"


def show_elements(ctx: Context, method: str = "ShowElements", params: List[dict[str, str]] = None) -> str:
    """
    Makes elements visible in the Revit view using their IDs.
    The language for the response message. Default is 中文 ("zh").

    Parameters:
    - ctx (Context): The FastMCP context.
    - method (str): The Revit API method to call. Default is "ShowElements".
    - params (List[dict[str, str]]): List of dictionaries specifying element IDs:
      - elementId (int or str): The ID of the element to be shown.

    Returns:
    - str: Result message indicating success or failure.
    """
    try:
        if not params or not all(isinstance(param.get("elementId"), (int, str)) for param in params):
            raise ValueError(
                "Invalid input: 'params' should be a list of dictionaries with 'elementId' (int or str).")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"Error showing elements. {str(e)}", exc_info=True)
        return f"Error: {str(e)}"


def parameter_elements(ctx: Context, method: str = "ParameterElements", params: List[dict[str, str]] = None) -> str:
    """
    Retrieve parameter names and values for specified Revit elements.
    The language for the response message. Default is 中文 ("zh").

    Parameters:
    - ctx (Context): The FastMCP context.
    - method (str): The Revit API method to call. Default is `"ParameterElements"`.
    - params (List[dict[str, str]]):
    A list of dictionaries specifying the element IDs and optional parameter names.
    - `elementId` (int or str): The ID of the Revit element to query.
    - `parameterName` (str, Optional): The specific parameter name to retrieve.
        If not provided, all parameters for the element will be returned.
    **Example Usage:**
    - Retrieve all parameters for an element:
        `[{ "elementId": 123456 }]`
    - Retrieve a specific parameter:
        `[{ "elementId": 123456, "parameterName": "Comments" }]`

    Returns:
    - str:
    A result message containing the parameter data in a formatted string,
    or an error message if the operation fails.
    """
    try:
        if not params or not all(isinstance(param.get("elementId"), (int, str)) for param in params):
            raise ValueError(
                "Invalid input: 'params' should be a list of dictionaries with 'elementId' (int or str).")

        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(
            f"Error retrieving element parameters: {str(e)}", exc_info=True)
        return f"Error: {str(e)}"


def create_elements(ctx: Context, method: str, params: List[dict[str, object]] = None) -> str:
    """
    Create various types of elements in the Revit scene.
    The language for the response message. Default is 中文 ("zh").

    Parameters:
    - ctx (Context): The FastMCP context.
    - method (str): The Revit API method for creating elements.
        Supported methods:
        - "CreateLevels": Create Levels
        - "CreateGrids": Create Grids
        - "CreateWalls": Create Walls
        - "CreateFamilyInstances": Create Family Instances
        - "CreateFloors": Create Floors
    - params (List[dict[str, object]]): A list of dictionaries specifying the creation parameters. The required and optional parameters depend on the method used:

    **CreateLevels** (Create Levels)
    - `name` (str): Name of the level.
    - `elevation` (float): Elevation height of the level.
    *No optional parameters.*

    **CreateGrids** (Create Grids)
    - `name` (str): Name of the grid.
    - `startX`, `startY`, `endX`, `endY` (float): Coordinates for the grid's start and end points.
    - `centerX`, `centerY` (float, Optional): Center coordinates for creating arc grids.
    *Use `centerX` and `centerY` when creating arc-shaped grids. For straight-line grids, these can be omitted.*

    **CreateWalls** (Create Walls)
    - `startX`, `startY`, `endX`, `endY` (float): Start and end coordinates for the wall.
    - `height` (float): Wall height.
    - `width` (float): Wall thickness.
    - `elevation` (float, Optional): Base elevation of the wall, default is 0.
    *Specify `elevation` to place the wall at a specific height.*

    **CreateFloors** (Create Floors)
    - `boundaryPoints` (List[dict[str, float]]): List of points representing the floor boundary (x, y coordinates).
    - `floorTypeName` (str, Optional): Name of the floor type. If not specified, the default floor type will be used.
    - `structural` (bool, Optional): Indicates whether the floor is structural. Default is `False`.
    *Use `floorTypeName` for specific floor types or `structural` if it is a structural floor.*

    **CreateFamilyInstances** (Create Family Instances)
    - `categoryName` (str): Category of the family instance (e.g., "Doors", "Windows", "Furniture").
    - `startX`, `startY`, `startZ` (float): Insertion point coordinates of the family instance.
    - `name` (str): Name of the family instance. If the user does not provide it, the system will retrieve available family types from the project for the user to select.
    - Optional parameters:
    - `familyName` (str, Optional): Specifies the family type. Defaults to the project's default family type if not provided.
    - `endX`, `endY`, `endZ` (float, Optional): Required for linear families where a start and end point are needed.
    - `hostId` (int, Optional): **Mandatory for host-based families like doors and windows**. Specifies the host element (e.g., a wall).
    - `viewName` (str, Optional): Name of the view to insert the family instance into. Defaults to the current view.
    - `rotationAngle` (float, Optional): Rotation angle in radians.
    - `offset` (float, Optional): Offset value to adjust the insertion point.
    *Use `hostId` when creating families like doors or windows that require a host. Specify `rotationAngle` or `offset` to adjust the instance position.*

    Returns:
    - str: A result message indicating success or failure.
    """

    try:
        # Validate parameters
        if not isinstance(params, list) or not all(isinstance(param, dict) for param in params):
            raise ValueError(
                "Invalid input: 'params' should be a list of dictionaries.")

        valid_methods = ["CreateWalls", "CreateFamilyInstances",
                         "CreateFloors", "CreateGrids", "CreateLevels"]
        if method not in valid_methods:
            raise ValueError(
                f"Invalid method: '{method}'. Supported methods: {', '.join(valid_methods)}")

        # Validate required parameters for each method
        required_params = {
            # For levels, name and elevation are required
            "CreateLevels": ["name", "elevation"],
            # For grid lines, start and end coordinates are required
            "CreateGrids": ["name", "startX", "startY", "endX", "endY"],
            "CreateWalls": ["startX", "startY", "endX", "endY", "height", "width"],
            # boundaryPoints is required for CreateFloors
            "CreateFloors": ["boundaryPoints"],
            "CreateFamilyInstances": ["categoryName", "startX", "startY", "startZ", "name"],
        }

        missing_keys = []
        for param in params:
            if method in required_params:
                missing_keys += [key for key in required_params[method]
                                 if key not in param]

        if missing_keys:
            raise ValueError(
                f"Missing required parameters for {method}: {', '.join(set(missing_keys))}")

        # Specifically handle "CreateGrids" to ensure the correct structure
        if method == "CreateGrids":
            for param in params:
                if "centerX" in param and "centerY" in param:
                    # It's an arc grid, so we need centerX, centerY
                    if "startX" not in param or "startY" not in param or "endX" not in param or "endY" not in param:
                        raise ValueError(
                            f"Missing required parameters for arc grid: startX, startY, endX, endY must be provided.")
                else:
                    # It's a line grid, so just startX, startY, endX, endY
                    if "startX" not in param or "startY" not in param or "endX" not in param or "endY" not in param:
                        raise ValueError(
                            f"Missing required parameters for line grid: startX, startY, endX, endY must be provided.")

        # Handle levels (CreateLevels)
        if method == "CreateLevels":
            for param in params:
                if "name" not in param or "elevation" not in param:
                    raise ValueError(
                        f"Missing required parameters for level: name and elevation must be provided.")

        # Proceed with sending the command to Revit
        from .server import get_Revit_connection
        revit = get_Revit_connection()
        result = revit.send_command(method, params)
        return result

    except Exception as e:
        logger.error(f"Error creating elements: {str(e)}", exc_info=True)
        return f"Error: {str(e)}"
