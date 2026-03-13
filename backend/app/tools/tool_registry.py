from app.tools.write_file import write_file
from app.tools.run_code import run_code
from app.tools.install_package import install_package
from app.tools.read_file import read_file


TOOL_REGISTRY = {
    "write_file": write_file,
    "run_code": run_code,
    "install_package": install_package,
    "read_file": read_file
}