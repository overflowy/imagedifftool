# type: ignore

import ast
import inspect
import os
import re
from pprint import pformat

global count
count = 0


class d:
    """
    Prints the name, type and the value of the argument(s) passed to it.

    Example:
        >>> a = 1
        >>> b = "hello"
        >>> c = [1, 2, 3]
        >>> d(a, b, c)
        d [0] > a: int = 1 | b: str = 'hello' | c: list = [1, 2, 3]
        >>> d()
        d [1] > "path/to/script.py", line 10
        >>> d("some comment", a, b, c)
        d [2] > (some comment) | a: int = 1 | b: str = 'hello' | c: list = [1, 2, 3]
    """

    NO_COLOR = os.getenv("NO_COLOR")
    BLUE = "" if NO_COLOR else "\033[0;34m"
    BOLD = "" if NO_COLOR else "\033[1m"
    CYAN = "" if NO_COLOR else "\033[0;36m"
    GREEN = "" if NO_COLOR else "\033[0;32m"
    ITALIC = "" if NO_COLOR else "\033[3m"
    RED = "" if NO_COLOR else "\033[0;31m"
    YELLOW = "" if NO_COLOR else "\033[0;33m"
    R = "" if NO_COLOR else "\033[0m"  # Reset.
    SEP = f"{RED}|{R}"
    CTX = re.compile(r"^d\s*\((.+?)\)$")

    def __init__(self, *args, **kwargs):  # sourcery skip: use-named-expression
        if kwargs:
            raise TypeError("d() only accepts positional arguments.")
        if not args:
            self.print_line_no()
            return
        self.args = args

        try:
            frame = inspect.currentframe()
            context = inspect.getframeinfo(frame.f_back).code_context[0]
            found = re.search(d.CTX, context.strip())
            if found:
                arg_names = self.get_arg_names(found[0])
                self.print_args(arg_names)
            else:
                raise ValueError("d() arg list must not end with a comma.")
        finally:
            del frame

    def get_arg_names(self, src):
        module = ast.parse(src)
        body = module.body[0].value
        names = []
        for node in ast.walk(body):
            if isinstance(node, ast.Call):
                names.extend(ast.unparse(name) for name in node.args)
        return names

    def prettify(self, arg):
        pretty = pformat(arg, compact=True, underscore_numbers=True)
        if isinstance(arg, (list, tuple, dict, set)):
            pretty = "\ \n" + pretty + "\n"
        return pretty

    def print_header(self):
        global count
        header = f"\n{d.BLUE}d{d.R} [{d.GREEN}{count}{d.R}] >"
        count += 1
        print(header, end=" ")

    def print_args(self, names):
        self.print_header()
        to_print = []
        for name, arg in zip(names, self.args):
            t = type(arg).__name__
            if isinstance(arg, type):
                t = arg.__name__
            pretty = self.prettify(arg)
            if name.lstrip("'").rstrip("'") == arg:
                to_print.append(f"({d.ITALIC}{arg}{d.R}) {d.SEP} ")
            else:
                to_print.append(f"{d.BOLD}{name}{d.R}: {d.YELLOW}{t}{d.R} = {d.CYAN}{pretty}{d.R} {d.SEP} ")
        print("".join(to_print)[: -len(d.SEP) - 1])

    def print_line_no(self):
        script_path = inspect.currentframe().f_back.f_back.f_code.co_filename
        line_no = inspect.currentframe().f_back.f_back.f_lineno
        self.print_header()
        print(f"'{script_path}', line {d.YELLOW}{line_no}{d.R}")


a = {
    "expand": "attributes",
    "link": {"rel": "self", "href": "http://localhost:8095/crowd/rest/usermanagement/1/user?username=my_username"},
    "name": "my_username",
    "first-name": "My",
    "last-name": "Username",
    "display-name": "My Username",
    "email": "user@example.test",
    "password": {
        "link": {
            "rel": "edit",
            "href": "http://localhost:8095/crowd/rest/usermanagement/1/user/password?username=my_username",
        }
    },
    "active": True,
    "attributes": {
        "link": {
            "rel": "self",
            "href": "http://localhost:8095/crowd/rest/usermanagement/1/user/attribute?username=my_username",
        },
        "attributes": [],
    },
}
