"""Project generator for the C language."""

import re

from .base import BaseLanguageInterface

STDBOOL_HEADER = "#include <stdbool.h>\n"
HEADER_FILE_TEMPLATE = "{returnType} {name}({params});"

TEST_FILE_TEMPLATE = """\
#include <stdio.h>
#include "solution.h"

int main() {{
    {params_setup};
    {result_var_declaration}{name}({params_call});
    printf("{OUTPUT_RESULT_PREFIX} %d\\n", {result_var});
    return 0;
}}
"""

FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^(?P<returnType>(?:struct\s)?\w+(?:\[\]|\s?\*+)?) (?P<name>\w+)\((?P<params>[^)]+)\)\s?{$",
    flags=re.MULTILINE,
)

SOLUTION_REPLACEMENT_PATTERN = re.compile(r"\n}")
SOLUTION_REPLACEMENT_TEMPLATE = "return 0;\n}"


class CLanguageInterface(BaseLanguageInterface):
    """Implementation of the C language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN
    compile_command = ["gcc", "solution.c", "test.c", "-o", "test"]
    test_command = ["./test"]
    default_output = "0"

    def prepare_project_files(self, template: str):

        params = self.groups["params"].split(", ")
        self.groups["params_setup"] = self.groups["params"].replace(", ", ";\n    ")
        self.groups["params_call"] = ", ".join(param.split()[-1] for param in params)

        headers = ""
        if "bool" in template:
            headers += STDBOOL_HEADER
        # ... additional header checks can be added here
        if headers != "":
            headers += "\n"

        formatted_template = self.get_formatted_nonvoid_template(
            template,
            lambda: re.sub(
                SOLUTION_REPLACEMENT_PATTERN, SOLUTION_REPLACEMENT_TEMPLATE, template
            ),
        )

        return {
            "solution.c": f"{headers}{formatted_template}\n",
            "solution.h": f"{headers}{HEADER_FILE_TEMPLATE.format(**self.groups)}",
            "test.c": TEST_FILE_TEMPLATE.format(**self.groups),
        }
