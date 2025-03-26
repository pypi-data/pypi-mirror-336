import logging
import os
import subprocess
import time
from typing import Type, Any

from langchain_core.tools import BaseTool
from langchain_core.tools.base import ToolException
from pydantic import BaseModel, Field

from llm_workers.api import ExtendedBaseTool
from llm_workers.api import WorkerException, ConfirmationRequest, ConfirmationRequestParam
from llm_workers.utils import LazyFormatter, open_file_in_default_app, is_safe_to_open

logger = logging.getLogger(__name__)


def _not_in_working_directory(file_path) -> bool:
    return file_path.startswith("/") or ".." in file_path.split("/")


class ReadFileToolSchema(BaseModel):
    filename: str = Field(..., description="Path to the file to read")
    lines: int = Field(0, description="Number of lines to read. If 0 (default), read the entire file. If negative, read from the end of file (tail).")

class ReadFileTool(BaseTool, ExtendedBaseTool):
    name: str = "read_file"
    description: str = "Reads a file and returns its content"
    args_schema: Type[ReadFileToolSchema] = ReadFileToolSchema

    def needs_confirmation(self, input: dict[str, Any]) -> bool:
        return _not_in_working_directory(input['filename'])

    def make_confirmation_request(self, input: dict[str, Any]) -> ConfirmationRequest:
        filename = input['filename']
        return ConfirmationRequest(
            action = f"read file \"{filename}\" outside working directory" if _not_in_working_directory(filename)
            else f"read file \"{filename}\"",
            params = [ ]
        )

    def _run(self, filename: str, lines: int) -> str:
        try:
            with open(filename, 'r') as file:
                if lines == 0:
                    return file.read()
                else:
                    file_lines: list[str] = file.readlines()
                    if lines > 0:
                        return '\n'.join(file_lines[:lines])
                    else:
                        return '\n'.join(file_lines[lines:])
        except Exception as e:
            raise WorkerException(f"Error reading file {filename}: {e}")


class WriteFileToolSchema(BaseModel):
    filename: str = Field(..., description="Path to the file to write")
    content: str = Field(..., description="Content to write")
    append: bool = Field(False, description="If true, append to the file instead of overwriting it")


class WriteFileTool(BaseTool, ExtendedBaseTool):
    name: str = "write_file"
    description: str = "Writes content to a file"
    args_schema: Type[WriteFileToolSchema] = WriteFileToolSchema

    def needs_confirmation(self, input: dict[str, Any]) -> bool:
        return _not_in_working_directory(input['filename'])

    def make_confirmation_request(self, input: dict[str, Any]) -> ConfirmationRequest:
        filename = input['filename']
        return ConfirmationRequest(
            action = f"write to the file \"{filename}\" outside working directory" if _not_in_working_directory(filename)
                else f"write to the file \"{filename}\"",
            params = []
        )

    def _run(self, filename: str, content: str, append: bool):
        try:
            if append:
                with open(filename, 'a') as file:
                    file.write(content)
            else:
                with open(filename, 'w') as file:
                    file.write(content)
        except Exception as e:
            raise WorkerException(f"Error writing file {filename}: {e}")



class RunPythonScriptToolSchema(BaseModel):
    """
    Schema for the RunPythonScriptTool.
    """

    script: str = Field(
        ...,
        description="Python script to run. Must be a valid Python code."
    )

class RunPythonScriptTool(BaseTool, ExtendedBaseTool):
    """
    Tool to run Python scripts. This tool is not safe to use with untrusted code.
    """

    name: str = "run_python_script"
    description: str = "Run a Python script and return its output."
    args_schema: Type[RunPythonScriptToolSchema] = RunPythonScriptToolSchema
    require_confirmation: bool = True

    def needs_confirmation(self, input: dict[str, Any]) -> bool:
        return True

    def make_confirmation_request(self, input: dict[str, Any]) -> ConfirmationRequest:
        return ConfirmationRequest(
            action = "run Python script",
            params = [ ConfirmationRequestParam(name = "script", value = input["script"], format = "python" ) ]
        )

    def _run(self, script: str) -> str:
        file_path = f"script_{time.strftime('%Y%m%d_%H%M%S')}.py"
        with open(file_path, 'w') as file:
            file.write(script)
        try:
            cmd = ["python3", file_path]
            cmd_str = LazyFormatter(cmd, custom_formatter = lambda x: " ".join(x))
            logger.debug("Running %s", cmd_str)
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            (result, stderr) = process.communicate()
            exit_code = process.wait()

            if exit_code != 0:
                raise WorkerException(f"Running Python script returned code {exit_code}:\n{stderr}")
            return result
        except WorkerException as e:
            raise e
        except Exception as e:
            raise WorkerException(f"Error running Python script: {e}")
        finally:
            if file_path:
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.warning(f"Failed to delete script file {file_path}: {e}")


class ShowFileToolSchema(BaseModel):
    filename: str = Field(..., description="Path to the file")

class ShowFileTool(BaseTool, ExtendedBaseTool):
    name: str = "show_file"
    description: str = "Show file to the user using OS-default application"
    args_schema: Type[ShowFileToolSchema] = ShowFileToolSchema

    def needs_confirmation(self, input: dict[str, Any]) -> bool:
        return _not_in_working_directory(input['filename'])

    def make_confirmation_request(self, input: dict[str, Any]) -> ConfirmationRequest:
        filename = input['filename']
        return ConfirmationRequest(
            action=f"open the file \"{filename}\" outside working directory in OS-default application" if _not_in_working_directory(
                filename)
            else f"open the file \"{filename}\" in OS-default application",
            params=[]
        )

    def _run(self, filename: str):
        if not is_safe_to_open(filename):
            raise ToolException(f"File {filename} is not safe to open")
        open_file_in_default_app(filename)
