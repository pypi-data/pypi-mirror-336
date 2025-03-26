import logging
import socket
import json
import time
import struct
import uuid
from typing import Dict, Any, List, Union, Optional, Tuple
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)
from enum import Enum
from pydantic import BaseModel

# 修改请求模型
class GetFunctionAssembly(BaseModel):
    function_name: str

class GetFunctionDecompiled(BaseModel):
    function_name: str

class GetGlobalVariable(BaseModel):
    variable_name: str

class GetCurrentFunctionAssembly(BaseModel):
    pass

class GetCurrentFunctionDecompiled(BaseModel):
    pass

class RenameLocalVariable(BaseModel):
    function_name: str
    old_name: str
    new_name: str

class RenameGlobalVariable(BaseModel):
    old_name: str
    new_name: str

class RenameFunction(BaseModel):
    old_name: str
    new_name: str

class AddAssemblyComment(BaseModel):
    address: str  # 可以是十六进制地址字符串
    comment: str
    is_repeatable: bool = False  # 是否为可重复注释

class AddFunctionComment(BaseModel):
    function_name: str
    comment: str
    is_repeatable: bool = False  # 是否为可重复注释

class AddPseudocodeComment(BaseModel):
    function_name: str
    address: str  # Address in the pseudocode
    comment: str
    is_repeatable: bool = False  # Whether comment should be repeated at all occurrences

class IDATools(str, Enum):
    GET_FUNCTION_ASSEMBLY = "ida_get_function_assembly"
    GET_FUNCTION_DECOMPILED = "ida_get_function_decompiled"
    GET_GLOBAL_VARIABLE = "ida_get_global_variable"
    GET_CURRENT_FUNCTION_ASSEMBLY = "ida_get_current_function_assembly"
    GET_CURRENT_FUNCTION_DECOMPILED = "ida_get_current_function_decompiled"
    RENAME_LOCAL_VARIABLE = "ida_rename_local_variable"
    RENAME_GLOBAL_VARIABLE = "ida_rename_global_variable"
    RENAME_FUNCTION = "ida_rename_function"
    ADD_ASSEMBLY_COMMENT = "ida_add_assembly_comment"
    ADD_FUNCTION_COMMENT = "ida_add_function_comment"
    ADD_PSEUDOCODE_COMMENT = "ida_add_pseudocode_comment"

# IDA Pro通信处理器
class IDAProCommunicator:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.sock = None
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.last_reconnect_time = 0
        self.reconnect_cooldown = 5  # 秒
        self.request_count = 0
    
    def connect(self):
        """连接到IDA插件"""
        # 检查是否需要冷却
        current_time = time.time()
        if current_time - self.last_reconnect_time < self.reconnect_cooldown and self.reconnect_attempts > 0:
            self.logger.debug("重连冷却中，跳过")
            return False
            
        # 如果已连接，先断开
        if self.connected:
            self.disconnect()
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)  # 设置超时
            self.sock.connect((self.host, self.port))
            self.connected = True
            self.reconnect_attempts = 0
            self.logger.info(f"已连接到IDA Pro ({self.host}:{self.port})")
            return True
        except Exception as e:
            self.last_reconnect_time = current_time
            self.reconnect_attempts += 1
            if self.reconnect_attempts <= self.max_reconnect_attempts:
                self.logger.warning(f"无法连接到IDA Pro: {str(e)}。尝试 {self.reconnect_attempts}/{self.max_reconnect_attempts}")
            else:
                self.logger.error(f"经过 {self.max_reconnect_attempts} 次尝试后无法连接到IDA Pro: {str(e)}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None
        self.connected = False
    
    def ensure_connection(self):
        """确保连接已建立"""
        if not self.connected:
            return self.connect()
        return True
    
    def send_message(self, data: bytes) -> None:
        """发送带长度前缀的消息"""
        length = len(data)
        length_bytes = struct.pack('!I', length)  # 4字节的长度前缀
        self.sock.sendall(length_bytes + data)
    
    def receive_message(self) -> Optional[bytes]:
        """接收带长度前缀的消息"""
        try:
            # 接收4字节的长度前缀
            length_bytes = self.receive_exactly(4)
            if not length_bytes:
                return None
                
            length = struct.unpack('!I', length_bytes)[0]
            
            # 接收消息主体
            data = self.receive_exactly(length)
            return data
        except Exception as e:
            self.logger.error(f"接收消息时出错: {str(e)}")
            return None
    
    def receive_exactly(self, n: int) -> Optional[bytes]:
        """接收确切的n字节数据"""
        data = b''
        while len(data) < n:
            chunk = self.sock.recv(min(n - len(data), 4096))
            if not chunk:  # 连接已关闭
                return None
            data += chunk
        return data
    
    def send_request(self, request_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送请求到IDA插件"""
        # 确保已连接
        if not self.ensure_connection():
            return {"error": "无法连接到IDA Pro"}
        
        # 添加请求ID
        request_id = str(uuid.uuid4())
        self.request_count += 1
        request_count = self.request_count
        
        request = {
            "id": request_id,
            "count": request_count,
            "type": request_type,
            "data": data
        }
        
        self.logger.debug(f"发送请求: {request_id}, 类型: {request_type}, 计数: {request_count}")
        
        try:
            # 发送请求
            request_json = json.dumps(request).encode('utf-8')
            self.send_message(request_json)
            
            # 接收响应
            response_data = self.receive_message()
            
            # 如果没有接收到数据，认为连接已断开
            if not response_data:
                self.logger.warning("未收到数据，连接可能已关闭")
                self.disconnect()
                return {"error": "未收到IDA Pro的响应"}
            
            # 解析响应
            try:
                self.logger.debug(f"收到原始数据长度: {len(response_data)}")
                response = json.loads(response_data.decode('utf-8'))
                
                # 验证响应ID是否匹配
                response_id = response.get("id")
                if response_id != request_id:
                    self.logger.warning(f"响应ID不匹配! 请求ID: {request_id}, 响应ID: {response_id}")
                
                self.logger.debug(f"接收到响应: ID={response.get('id')}, 计数={response.get('count')}")
                
                # 额外的类型验证
                if not isinstance(response, dict):
                    self.logger.error(f"收到的响应不是字典类型: {type(response)}")
                    return {"error": f"响应格式错误: 预期是字典，实际是 {type(response).__name__}"}
                
                return response
            except json.JSONDecodeError as e:
                self.logger.error(f"无法解析JSON响应: {str(e)}")
                return {"error": f"无效的JSON响应: {str(e)}"}
                
        except Exception as e:
            self.logger.error(f"与IDA Pro通信时出错: {str(e)}")
            self.disconnect()  # 出错后断开连接
            return {"error": str(e)}
    
    def ping(self):
        """检查连接是否有效"""
        response = self.send_request("ping", {})
        return response.get("status") == "pong"

# 实际的IDA Pro功能实现
class IDAProFunctions:
    def __init__(self, communicator):
        self.communicator = communicator
        self.logger = logging.getLogger(__name__)
        
    def get_function_assembly(self, function_name: str) -> str:
        """获取函数的汇编代码"""
        try:
            response = self.communicator.send_request(
                "get_function_assembly", 
                {"function_name": function_name}
            )
            
            if "error" in response:
                return f"Error retrieving assembly for function '{function_name}': {response['error']}"
            
            assembly = response.get("assembly")
            # 验证assembly是字符串类型
            if assembly is None:
                return f"Error: No assembly data returned for function '{function_name}'"
            if not isinstance(assembly, str):
                self.logger.warning(f"Assembly数据类型不是字符串而是 {type(assembly).__name__}，尝试转换")
                assembly = str(assembly)
            
            return f"Assembly code for function '{function_name}':\n{assembly}"
        except Exception as e:
            self.logger.error(f"获取函数汇编时出错: {str(e)}", exc_info=True)
            return f"Error retrieving assembly for function '{function_name}': {str(e)}"
    
    def get_function_decompiled(self, function_name: str) -> str:
        """获取函数的反编译伪代码"""
        try:
            response = self.communicator.send_request(
                "get_function_decompiled", 
                {"function_name": function_name}
            )
            
            # 记录完整的响应用于调试
            self.logger.debug(f"反编译响应: {response}")
            
            if "error" in response:
                return f"Error retrieving decompiled code for function '{function_name}': {response['error']}"
            
            decompiled_code = response.get("decompiled_code")
            
            # 详细的类型检查和转换
            if decompiled_code is None:
                return f"Error: No decompiled code returned for function '{function_name}'"
                
            # 记录实际类型
            actual_type = type(decompiled_code).__name__
            self.logger.debug(f"反编译代码类型为: {actual_type}")
            
            # 确保结果是字符串
            if not isinstance(decompiled_code, str):
                self.logger.warning(f"反编译代码类型不是字符串而是 {actual_type}，尝试转换")
                try:
                    decompiled_code = str(decompiled_code)
                except Exception as e:
                    return f"Error: Failed to convert decompiled code from {actual_type} to string: {str(e)}"
            
            return f"Decompiled code for function '{function_name}':\n{decompiled_code}"
        except Exception as e:
            self.logger.error(f"获取函数反编译代码时出错: {str(e)}", exc_info=True)
            return f"Error retrieving decompiled code for function '{function_name}': {str(e)}"
    
    def get_global_variable(self, variable_name: str) -> str:
        """获取全局变量信息"""
        try:
            response = self.communicator.send_request(
                "get_global_variable", 
                {"variable_name": variable_name}
            )
            
            if "error" in response:
                return f"Error retrieving global variable '{variable_name}': {response['error']}"
            
            variable_info = response.get("variable_info")
            
            # 验证variable_info是字符串类型
            if variable_info is None:
                return f"Error: No variable info returned for '{variable_name}'"
            if not isinstance(variable_info, str):
                self.logger.warning(f"变量信息类型不是字符串而是 {type(variable_info).__name__}，尝试转换")
                try:
                    # 如果是字典，先转为JSON字符串
                    if isinstance(variable_info, dict):
                        variable_info = json.dumps(variable_info, indent=2)
                    else:
                        variable_info = str(variable_info)
                except Exception as e:
                    return f"Error: Failed to convert variable info to string: {str(e)}"
            
            return f"Global variable '{variable_name}':\n{variable_info}"
        except Exception as e:
            self.logger.error(f"获取全局变量时出错: {str(e)}", exc_info=True)
            return f"Error retrieving global variable '{variable_name}': {str(e)}"
    
    def get_current_function_assembly(self) -> str:
        """获取当前光标所在函数的汇编代码"""
        try:
            response = self.communicator.send_request(
                "get_current_function_assembly", 
                {}
            )
            
            if "error" in response:
                return f"Error retrieving assembly for current function: {response['error']}"
            
            assembly = response.get("assembly")
            function_name = response.get("function_name", "Current function")
            
            # 验证assembly是字符串类型
            if assembly is None:
                return f"Error: No assembly data returned for current function"
            if not isinstance(assembly, str):
                self.logger.warning(f"Assembly数据类型不是字符串而是 {type(assembly).__name__}，尝试转换")
                assembly = str(assembly)
            
            return f"Assembly code for function '{function_name}':\n{assembly}"
        except Exception as e:
            self.logger.error(f"获取当前函数汇编时出错: {str(e)}", exc_info=True)
            return f"Error retrieving assembly for current function: {str(e)}"
    
    def get_current_function_decompiled(self) -> str:
        """获取当前光标所在函数的反编译代码"""
        try:
            response = self.communicator.send_request(
                "get_current_function_decompiled", 
                {}
            )
            
            if "error" in response:
                return f"Error retrieving decompiled code for current function: {response['error']}"
            
            decompiled_code = response.get("decompiled_code")
            function_name = response.get("function_name", "Current function")
            
            # 详细的类型检查和转换
            if decompiled_code is None:
                return f"Error: No decompiled code returned for current function"
                
            # 确保结果是字符串
            if not isinstance(decompiled_code, str):
                self.logger.warning(f"反编译代码类型不是字符串而是 {type(decompiled_code).__name__}，尝试转换")
                try:
                    decompiled_code = str(decompiled_code)
                except Exception as e:
                    return f"Error: Failed to convert decompiled code: {str(e)}"
            
            return f"Decompiled code for function '{function_name}':\n{decompiled_code}"
        except Exception as e:
            self.logger.error(f"获取当前函数反编译代码时出错: {str(e)}", exc_info=True)
            return f"Error retrieving decompiled code for current function: {str(e)}"

    def rename_local_variable(self, function_name: str, old_name: str, new_name: str) -> str:
        """重命名函数内的局部变量"""
        try:
            response = self.communicator.send_request(
                "rename_local_variable", 
                {"function_name": function_name, "old_name": old_name, "new_name": new_name}
            )
            
            if "error" in response:
                return f"Error renaming local variable from '{old_name}' to '{new_name}' in function '{function_name}': {response['error']}"
            
            success = response.get("success", False)
            message = response.get("message", "")
            
            if success:
                return f"Successfully renamed local variable from '{old_name}' to '{new_name}' in function '{function_name}': {message}"
            else:
                return f"Failed to rename local variable from '{old_name}' to '{new_name}' in function '{function_name}': {message}"
        except Exception as e:
            self.logger.error(f"重命名局部变量时出错: {str(e)}", exc_info=True)
            return f"Error renaming local variable from '{old_name}' to '{new_name}' in function '{function_name}': {str(e)}"

    def rename_global_variable(self, old_name: str, new_name: str) -> str:
        """重命名全局变量"""
        try:
            response = self.communicator.send_request(
                "rename_global_variable", 
                {"old_name": old_name, "new_name": new_name}
            )
            
            if "error" in response:
                return f"Error renaming global variable from '{old_name}' to '{new_name}': {response['error']}"
            
            success = response.get("success", False)
            message = response.get("message", "")
            
            if success:
                return f"Successfully renamed global variable from '{old_name}' to '{new_name}': {message}"
            else:
                return f"Failed to rename global variable from '{old_name}' to '{new_name}': {message}"
        except Exception as e:
            self.logger.error(f"重命名全局变量时出错: {str(e)}", exc_info=True)
            return f"Error renaming global variable from '{old_name}' to '{new_name}': {str(e)}"

    def rename_function(self, old_name: str, new_name: str) -> str:
        """重命名函数"""
        try:
            response = self.communicator.send_request(
                "rename_function", 
                {"old_name": old_name, "new_name": new_name}
            )
            
            if "error" in response:
                return f"Error renaming function from '{old_name}' to '{new_name}': {response['error']}"
            
            success = response.get("success", False)
            message = response.get("message", "")
            
            
            if success:
                return f"Successfully renamed function from '{old_name}' to '{new_name}': {message}"
            else:
                return f"Failed to rename function from '{old_name}' to '{new_name}': {message}"
        except Exception as e:
            self.logger.error(f"重命名函数时出错: {str(e)}", exc_info=True)
            return f"Error renaming function from '{old_name}' to '{new_name}': {str(e)}"

    def add_assembly_comment(self, address: str, comment: str, is_repeatable: bool = False) -> str:
        """添加汇编注释"""
        try:
            response = self.communicator.send_request(
                "add_assembly_comment", 
                {"address": address, "comment": comment, "is_repeatable": is_repeatable}
            )
            
            if "error" in response:
                return f"Error adding assembly comment at address '{address}': {response['error']}"
            
            success = response.get("success", False)
            message = response.get("message", "")
            
            if success:
                comment_type = "repeatable" if is_repeatable else "regular"
                return f"Successfully added {comment_type} assembly comment at address '{address}': {message}"
            else:
                return f"Failed to add assembly comment at address '{address}': {message}"
        except Exception as e:
            self.logger.error(f"添加汇编注释时出错: {str(e)}", exc_info=True)
            return f"Error adding assembly comment at address '{address}': {str(e)}"

    def add_function_comment(self, function_name: str, comment: str, is_repeatable: bool = False) -> str:
        """添加函数注释"""
        try:
            response = self.communicator.send_request(
                "add_function_comment", 
                {"function_name": function_name, "comment": comment, "is_repeatable": is_repeatable}
            )
            
            if "error" in response:
                return f"Error adding comment to function '{function_name}': {response['error']}"
            
            success = response.get("success", False)
            message = response.get("message", "")
            
            if success:
                comment_type = "repeatable" if is_repeatable else "regular"
                return f"Successfully added {comment_type} comment to function '{function_name}': {message}"
            else:
                return f"Failed to add comment to function '{function_name}': {message}"
        except Exception as e:
            self.logger.error(f"添加函数注释时出错: {str(e)}", exc_info=True)
            return f"Error adding comment to function '{function_name}': {str(e)}"

    def add_pseudocode_comment(self, function_name: str, address: str, comment: str, is_repeatable: bool = False) -> str:
        """Add a comment to a specific address in the function's decompiled pseudocode"""
        try:
            response = self.communicator.send_request(
                "add_pseudocode_comment",
                {
                    "function_name": function_name,
                    "address": address,
                    "comment": comment,
                    "is_repeatable": is_repeatable
                }
            )
            
            if "error" in response:
                return f"Error adding comment at address {address} in function '{function_name}': {response['error']}"
            
            success = response.get("success", False)
            message = response.get("message", "")
            
            if success:
                comment_type = "repeatable" if is_repeatable else "regular"
                return f"Successfully added {comment_type} comment at address {address} in function '{function_name}': {message}"
            else:
                return f"Failed to add comment at address {address} in function '{function_name}': {message}"
        except Exception as e:
            self.logger.error(f"添加伪代码注释时出错: {str(e)}", exc_info=True)
            return f"Error adding comment at address {address} in function '{function_name}': {str(e)}"


async def serve() -> None:
    """MCP服务器主入口"""
    logger = logging.getLogger(__name__)
    # 设置日志级别为DEBUG以获取详细信息
    logger.setLevel(logging.DEBUG)
    server = Server("mcp-ida")
    
    # 创建communicator并尝试连接
    ida_communicator = IDAProCommunicator()
    logger.info("尝试连接到IDA Pro插件...")
    
    if ida_communicator.connect():
        logger.info("成功连接到IDA Pro插件")
    else:
        logger.warning("初始连接到IDA Pro插件失败，将在请求时重试")
    
    # 使用持久连接创建IDA功能类
    ida_functions = IDAProFunctions(ida_communicator)

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """列出支持的工具"""
        return [
            Tool(
                name=IDATools.GET_FUNCTION_ASSEMBLY,
                description="Get assembly code for a function by name",
                inputSchema=GetFunctionAssembly.schema(),
            ),
            Tool(
                name=IDATools.GET_FUNCTION_DECOMPILED,
                description="Get decompiled pseudocode for a function by name",
                inputSchema=GetFunctionDecompiled.schema(),
            ),
            Tool(
                name=IDATools.GET_GLOBAL_VARIABLE,
                description="Get information about a global variable by name",
                inputSchema=GetGlobalVariable.schema(),
            ),
            Tool(
                name=IDATools.GET_CURRENT_FUNCTION_ASSEMBLY,
                description="Get assembly code for the function at the current cursor position",
                inputSchema=GetCurrentFunctionAssembly.schema(),
            ),
            Tool(
                name=IDATools.GET_CURRENT_FUNCTION_DECOMPILED,
                description="Get decompiled pseudocode for the function at the current cursor position",
                inputSchema=GetCurrentFunctionDecompiled.schema(),
            ),
            Tool(
                name=IDATools.RENAME_LOCAL_VARIABLE,
                description="Rename a local variable within a function in the IDA database",
                inputSchema=RenameLocalVariable.schema(),
            ),
            Tool(
                name=IDATools.RENAME_GLOBAL_VARIABLE,
                description="Rename a global variable in the IDA database",
                inputSchema=RenameGlobalVariable.schema(),
            ),
            Tool(
                name=IDATools.RENAME_FUNCTION,
                description="Rename a function in the IDA database",
                inputSchema=RenameFunction.schema(),
            ),
            Tool(
                name=IDATools.ADD_ASSEMBLY_COMMENT,
                description="Add a comment at a specific address in the assembly view of the IDA database",
                inputSchema=AddAssemblyComment.schema(),
            ),
            Tool(
                name=IDATools.ADD_FUNCTION_COMMENT,
                description="Add a comment to a function in the IDA database",
                inputSchema=AddFunctionComment.schema(),
            ),
            Tool(
                name=IDATools.ADD_PSEUDOCODE_COMMENT,
                description="Add a comment to a specific address in the function's decompiled pseudocode",
                inputSchema=AddPseudocodeComment.schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> List[TextContent]:
        """调用工具并处理结果"""
        # 确保有连接
        if not ida_communicator.connected and not ida_communicator.ensure_connection():
            return [TextContent(
                type="text",
                text=f"Error: Cannot connect to IDA Pro plugin. Please ensure the plugin is running."
            )]
            
        try:
            match name:
                case IDATools.GET_FUNCTION_ASSEMBLY:
                    assembly = ida_functions.get_function_assembly(arguments["function_name"])
                    return [TextContent(
                        type="text",
                        text=assembly
                    )]

                case IDATools.GET_FUNCTION_DECOMPILED:
                    decompiled = ida_functions.get_function_decompiled(arguments["function_name"])
                    return [TextContent(
                        type="text",
                        text=decompiled
                    )]

                case IDATools.GET_GLOBAL_VARIABLE:
                    variable_info = ida_functions.get_global_variable(arguments["variable_name"])
                    return [TextContent(
                        type="text",
                        text=variable_info
                    )]
                    
                case IDATools.GET_CURRENT_FUNCTION_ASSEMBLY:
                    assembly = ida_functions.get_current_function_assembly()
                    return [TextContent(
                        type="text",
                        text=assembly
                    )]
                
                case IDATools.GET_CURRENT_FUNCTION_DECOMPILED:
                    decompiled = ida_functions.get_current_function_decompiled()
                    return [TextContent(
                        type="text",
                        text=decompiled
                    )]

                case IDATools.RENAME_LOCAL_VARIABLE:
                    result = ida_functions.rename_local_variable(
                        arguments["function_name"],
                        arguments["old_name"], 
                        arguments["new_name"]
                    )
                    return [TextContent(
                        type="text",
                        text=result
                    )]

                case IDATools.RENAME_GLOBAL_VARIABLE:
                    result = ida_functions.rename_global_variable(
                        arguments["old_name"], 
                        arguments["new_name"]
                    )
                    return [TextContent(
                        type="text",
                        text=result
                    )]

                case IDATools.RENAME_FUNCTION:
                    result = ida_functions.rename_function(
                        arguments["old_name"], 
                        arguments["new_name"]
                    )
                    return [TextContent(
                        type="text",
                        text=result
                    )]

                case IDATools.ADD_ASSEMBLY_COMMENT:
                    result = ida_functions.add_assembly_comment(
                        arguments["address"], 
                        arguments["comment"], 
                        arguments.get("is_repeatable", False)
                    )
                    return [TextContent(
                        type="text",
                        text=result
                    )]

                case IDATools.ADD_FUNCTION_COMMENT:
                    result = ida_functions.add_function_comment(
                        arguments["function_name"], 
                        arguments["comment"], 
                        arguments.get("is_repeatable", False)
                    )
                    return [TextContent(
                        type="text",
                        text=result
                    )]

                case IDATools.ADD_PSEUDOCODE_COMMENT:
                    result = ida_functions.add_pseudocode_comment(
                        arguments["function_name"],
                        arguments["address"],
                        arguments["comment"],
                        arguments.get("is_repeatable", False)
                    )
                    return [TextContent(
                        type="text",
                        text=result
                    )]

                case _:
                    raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            logger.error(f"调用工具时发生错误: {str(e)}", exc_info=True)
            return [TextContent(
                type="text",
                text=f"Error executing {name}: {str(e)}"
            )]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
