# server.py
from mcp.server.fastmcp import FastMCP
import requests
import json

# Create an MCP server
mcp = FastMCP("SlicerMCP")

SLICER_WEB_SERVER_URL = "http://localhost:2016/slicer"

# Add list_nodes tool
@mcp.tool()
def list_nodes(filter_type: str = "names", class_name: str = None, 
              name: str = None, id: str = None) -> dict:
    """
    List MRML nodes via the Slicer Web Server API.

    The filter_type parameter specifies the type of node information to retrieve.
    Possible values include "names" (node names), "ids" (node IDs), and "properties" (node properties).
    The default value is "names".

    The class_name, name, and id parameters are optional and can be used to further filter nodes.
    The class_name parameter allows filtering nodes by class name.
    The name parameter allows filtering nodes by name.
    The id parameter allows filtering nodes by ID.

    Examples:
    - List the names of all nodes: {"tool": "list_nodes", "arguments": {"filter_type": "names"}}
    - List the IDs of nodes of a specific class: {"tool": "list_nodes", "arguments": {"filter_type": "ids", "class_name": "vtkMRMLModelNode"}}
    - List the properties of nodes with a specific name: {"tool": "list_nodes", "arguments": {"filter_type": "properties", "name": "MyModel"}}
    - List nodes with a specific ID: {"tool": "list_nodes", "arguments": {"filter_type": "ids", "id": "vtkMRMLModelNode123"}}

    Returns a dictionary containing node information.
    If filter_type is "names" or "ids", the returned dictionary contains a "nodes" key, whose value is a list containing node names or IDs.
    Example: {"nodes": ["node1", "node2", ...]} or {"nodes": ["id1", "id2", ...]}
    If filter_type is "properties", the returned dictionary contains a "nodes" key, whose value is a dictionary containing node properties.
    Example: {"nodes": {"node1": {"property1": "value1", "property2": "value2"}, ...}}
    If an error occurs, a dictionary containing an "error" key is returned, whose value is a string describing the error.
    """
    try:
        # Build API endpoint based on filter type
        endpoint_map = {
            "names": "/mrml/names",
            "ids": "/mrml/ids",
            "properties": "/mrml/properties"
        }
        
        if filter_type not in endpoint_map:
            return {"error": "Invalid filter_type specified"}
            
        api_url = f"{SLICER_WEB_SERVER_URL}{endpoint_map[filter_type]}"
        
        # Build query parameters
        params = {}
        if class_name:
            params["class"] = class_name
        if name:
            params["name"] = name
        if id:
            params["id"] = id

        # Send GET request to Slicer Web Server
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        
        # Process response based on filter type
        if filter_type == "properties":
            return {"nodes": response.json()}
            
        return {"nodes": response.json()}

    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP Error {e.response.status_code}: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON response: {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}
    except Exception as e:
        return {"error": f"Node listing failed: {str(e)}"}


# Add execute_python_code tool
@mcp.tool()
def execute_python_code(code: str) -> dict:
    """
    Execute Python code in 3D Slicer.

    Parameters:
    code (str): The Python code to execute.

    The code parameter is a string containing the Python code to be executed in 3D Slicer's Python environment.
    The code should be executable by Python's `exec()` function. To get return values, the code should assign the result to a variable named `__execResult`.

    Examples:
    - Create a sphere model: {"tool": "execute_python_code", "arguments": {"code": "sphere = slicer.vtkMRMLModelNode(); slicer.mrmlScene.AddNode(sphere); sphere.SetName('MySphere'); __execResult = sphere.GetID()"}}
    - Get the number of nodes in the current scene: {"tool": "execute_python_code", "arguments": {"code": "__execResult = len(slicer.mrmlScene.GetNodes())"}}
    - Calculate 1+1: {"tool": "execute_python_code", "arguments": {"code": "__execResult = 1 + 1"}}

    Returns:
        dict: A dictionary containing the execution result.

        If the code execution is successful, the dictionary will contain the following key-value pairs:
        - "success": True
        - "message": The result of the code execution. If the code assigns the result to `__execResult`, the value of `__execResult` is returned, otherwise it returns empty.

        If the code execution fails, the dictionary will contain the following key-value pairs:
        - "success": False
        - "message": A string containing an error message indicating the cause of the failure. The error message may come from the Slicer Web Server or the Python interpreter.

    Examples:
    - Successful execution: {"success": True, "message": 2}  # Assuming the result of 1+1 is 2
    - Successful execution: {"success": True, "message": "vtkMRMLScene1"} # Assuming the created sphere id is vtkMRMLScene1
    - Python execution error: {"success": False, "message": "Server error: name 'slicer' is not defined"}
    - Connection error: {"success": False, "message": "Connection error: ..."}
    - HTTP error: {"success": False, "message": "HTTP Error 404: Not Found"}
    """
    api_url = f"{SLICER_WEB_SERVER_URL}/exec"
    headers = {'Content-Type': 'text/plain'}
    try:
        response = requests.post(api_url, data=code.encode('utf-8'), headers=headers)
        result_data = response.json()
        
        if isinstance(result_data, dict) and not result_data.get("success", True):
            return {
                "success": False,
                "message": result_data.get("message", "Unknown Python execution error")
                }
            
        return {
            "success": True,
            "message": result_data.get("__execResult") if isinstance(result_data, dict) and "__execResult" in result_data else result_data
            }
    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "message": f"HTTP Error {e.response.status_code}: {str(e)}"
            }
    except json.JSONDecodeError:
        return {
            "success": False,
            "message": f"Invalid JSON response: {response.text}"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Connection error: {str(e)}"
            }
