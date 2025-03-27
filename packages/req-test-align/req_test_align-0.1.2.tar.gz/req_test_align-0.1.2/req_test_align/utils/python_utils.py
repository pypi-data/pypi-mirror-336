import parso
from .utils import has_intersection_between_code_lines


def extract_code_structure_python(
    python_code, start_line, end_line, function_only=False
):
    """
    Extract code structure from Python code using Parso.

    Args:
        python_code: Python code snippet
        start_line: Start line of the code change
        end_line: End line of the code change
        function_only: Whether to extract only function definitions

    Returns:
        dict: Extracted code structure
    """
    try:
        # Parse the Python code using Parso
        tree = parso.parse(python_code)
        lines = python_code.splitlines(keepends=True)

        # Map node types to structure types
        structure_types = {
            "funcdef": "function",
            "async_funcdef": "function",  # Async functions are also functions
            "classdef": "class",
        }

        # Try to extract each type of structure
        for node_type, structure_type in structure_types.items():
            if (
                function_only
                and node_type != "funcdef"
                and node_type != "async_funcdef"
            ):
                continue

            result = _extract_structure_python(
                tree, lines, start_line, end_line, node_type, structure_type
            )
            if len(result.values()) > 0:
                return result

        # Fallback to single line extraction if not function_only
        return (
            _extract_single_line(lines, start_line, end_line)
            if not function_only
            else {}
        )

    except Exception as e:
        print(f"Error parsing Python code: {e}")
        return {}


def _extract_structure_python(
    node, lines, start_line, end_line, node_type, structure_type, class_path=None
):
    """
    Generic structure extractor for Python functions and classes.

    Args:
        node: Parso node
        lines: List of code lines
        start_line: Start line of the code change
        end_line: End line of the code change
        node_type: Parso node type
        structure_type: Structure type
        class_path: Current class path for nested definitions

    Returns:
        dict: Extracted structure
    """
    result = {}

    if node.type == node_type:
        # Determine the start and end lines of the structure
        struct_start = node.start_pos[0]
        struct_end = node.end_pos[0]

        # Check for decorators
        if hasattr(node, "get_decorators"):
            decorators = node.get_decorators()
            if decorators and len(decorators) > 0:
                struct_start = decorators[0].start_pos[0]

        if has_intersection_between_code_lines(
            [struct_start, struct_end], [start_line, end_line]
        ):
            # Build full name with class path if available
            if hasattr(node, "name") and hasattr(node.name, "value"):
                name = node.name.value
                full_name = name if not class_path else f"{class_path}.{name}"

                return {
                    f"{struct_start}-{struct_end}": {
                        "type": structure_type,
                        "full_name": full_name,
                        "name": name,
                        "code": "".join(lines[struct_start - 1 : struct_end]),
                        "start_line": struct_start,
                        "end_line": struct_end,
                    }
                }

    # Recursively check child nodes
    if hasattr(node, "children"):
        # Update class path if this is a class definition
        new_class_path = class_path
        if node.type == "classdef" and hasattr(node.children, "__getitem__"):
            class_name_leaf = node.children[1]  # 'class' [whitespace] 'ClassName' ...
            if hasattr(class_name_leaf, "type") and class_name_leaf.type == "name":
                new_class_path = (
                    class_name_leaf.value
                    if not class_path
                    else f"{class_path}.{class_name_leaf.value}"
                )

        for child in node.children:
            child_result = _extract_structure_python(
                child,
                lines,
                start_line,
                end_line,
                node_type,
                structure_type,
                class_path=new_class_path,
            )
            if len(child_result.values()) > 0:
                result.update(child_result)

    return result


def _extract_single_line(lines, start_line, end_line):
    """
    Extract single line changes when no structural elements are found.

    Args:
        lines: List of code lines
        start_line: Start line of the code change
        end_line: End line of the code change

    Returns:
        dict: Extracted structure
    """
    if has_intersection_between_code_lines([1, len(lines)], [start_line, end_line]):
        return {
            f"{start_line}_{end_line}": {
                "type": "single_line",
                "code": "".join(lines[start_line - 1 : end_line]),
                "start_line": start_line,
                "end_line": end_line,
                "name": f"line_{start_line}_{end_line}",
            }
        }
    return {}
