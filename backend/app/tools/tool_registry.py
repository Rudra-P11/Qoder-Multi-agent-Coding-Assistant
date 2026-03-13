from app.tools.write_file import write_file
from app.tools.run_code import run_code
from app.tools.install_package import install_package


TOOL_REGISTRY = {
    "write_file": write_file,
    "run_code": run_code,
    "install_package": install_package
}