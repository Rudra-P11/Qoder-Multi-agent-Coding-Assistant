from app.tools.write_file import write_file
from app.tools.read_file import read_file
from app.tools.append_file import append_file
from app.tools.delete_file import delete_file
from app.tools.list_files import list_files
from app.tools.search_code import search_code
from app.tools.run_command import run_command
from app.tools.run_code import run_code
from app.tools.install_package import install_package
from app.tools.read_todo import read_todo
from app.tools.update_todo import update_todo


TOOL_REGISTRY = {

    "write_file": write_file,
    "read_file": read_file,
    "append_file": append_file,
    "delete_file": delete_file,
    "list_files": list_files,
    "search_code": search_code,
    "run_command": run_command,
    "run_code": run_code,
    "install_package": install_package,
    "read_todo": read_todo,
    "update_todo": update_todo
}