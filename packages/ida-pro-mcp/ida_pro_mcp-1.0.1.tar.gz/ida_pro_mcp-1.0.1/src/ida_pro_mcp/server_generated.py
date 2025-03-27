# NOTE: This file has been automatically generated, do not modify!
from typing import Annotated, Optional, TypedDict
from pydantic import Field

class Function(TypedDict):
    start_address: int
    end_address: int
    name: str
    prototype: str

class DecompilationResult(TypedDict):
    address: int
    pseudocode: str
    error: str

class Metadata(TypedDict):
    path: str
    module: str
    base: str
    size: str
    md5: str
    sha256: str
    crc32: str
    filesize: str

@mcp.tool()
def get_function_by_name(name: Annotated[str, Field(description='Name of the function to get')]) -> Optional[Function]:
    """Get a function by its name"""
    return make_jsonrpc_request('get_function_by_name', name)

@mcp.tool()
def get_function_by_address(address: Annotated[int, Field(description='Address of the function to get')]) -> Optional[Function]:
    """Get a function by its address"""
    return make_jsonrpc_request('get_function_by_address', address)

@mcp.tool()
def get_current_address() -> int:
    """Get the address currently selected by the user"""
    return make_jsonrpc_request('get_current_address')

@mcp.tool()
def get_current_function() -> Optional[Function]:
    """Get the function currently selected by the user"""
    return make_jsonrpc_request('get_current_function')

@mcp.tool()
def list_functions() -> list[Function]:
    """List all functions in the database"""
    return make_jsonrpc_request('list_functions')

@mcp.tool()
def decompile_function(address: Annotated[int, Field(description='Address of the function to decompile')]) -> DecompilationResult:
    """Decompile a function at the given address"""
    return make_jsonrpc_request('decompile_function', address)

@mcp.tool()
def show_decompilation(address: Annotated[int, Field(description='Address of the function to show in the decompiler')]) -> None:
    """Show a function in the decompiler"""
    return make_jsonrpc_request('show_decompilation', address)

@mcp.tool()
def show_disassembly(address: Annotated[int, Field(description='Address to show in the disassembly view')]) -> None:
    """Show an address in the disassembly view"""
    return make_jsonrpc_request('show_disassembly', address)

@mcp.tool()
def rename_local_variable(function_address: Annotated[int, Field(description='Address of the function containing the variable')], old_name: Annotated[str, Field(description='Current name of the variable')], new_name: Annotated[str, Field(description='New name for the variable')]) -> bool:
    """Rename a local variable in a function"""
    return make_jsonrpc_request('rename_local_variable', function_address, old_name, new_name)

@mcp.tool()
def rename_function(function_address: Annotated[int, Field(description='Address of the function to rename')], new_name: Annotated[str, Field(description='New name for the function')]) -> bool:
    """Rename a function"""
    return make_jsonrpc_request('rename_function', function_address, new_name)

@mcp.tool()
def set_function_prototype(function_address: Annotated[int, Field(description='Address of the function')], prototype: Annotated[str, Field(description='New function prototype')]) -> str:
    """Set a function's prototype"""
    return make_jsonrpc_request('set_function_prototype', function_address, prototype)

@mcp.tool()
def set_local_variable_type(function_address: Annotated[int, Field(description='Address of the function containing the variable')], variable_name: Annotated[str, Field(description='Name of the variable')], new_type: Annotated[str, Field(description='New type for the variable')]) -> str:
    """Set a local variable's type"""
    return make_jsonrpc_request('set_local_variable_type', function_address, variable_name, new_type)

@mcp.tool()
def get_metadata() -> Metadata:
    """Get metadata about the current IDB"""
    return make_jsonrpc_request('get_metadata')

