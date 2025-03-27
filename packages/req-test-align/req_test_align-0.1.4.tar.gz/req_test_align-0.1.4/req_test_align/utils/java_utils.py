import javalang
from .utils import has_intersection_between_code_lines


def extract_code_structure_java(java_code, start_line, end_line):
    """
    Extract code structure from Java code.

    Args:
        java_code: Java code snippet
        start_line: Start line of the code change
        end_line: End line of the code change

    Returns:
        dict: Extracted code structure
    """
    try:
        tree = javalang.parse.parse(java_code)
        lines = java_code.splitlines(keepends=True)

        # Map of node types to their structure types
        structure_types = {
            javalang.tree.MethodDeclaration: "method",
            javalang.tree.ConstructorDeclaration: "constructor",
        }

        # Try to extract each type of structure
        for node_type, structure_type in structure_types.items():
            result = _extract_structure(
                tree, lines, start_line, end_line, node_type, structure_type
            )
            if len(result.values()) > 0:
                return result

        # Special handling for class declarations
        if _is_class_change(start_line, end_line, tree, lines):
            return _extract_class_fields(tree, lines, start_line, end_line)

        # Fallback to single line extraction
        return _extract_single_line(lines, start_line, end_line)

    except Exception as e:
        print(f"Error parsing Java code: {e}")
        return {}


def _extract_class_fields(tree, lines, start_line, end_line):
    """
    Extract only field declarations from class.

    Args:
        tree: Java AST
        lines: List of code lines
        start_line: Start line of the code change
        end_line: End line of the code change

    Returns:
        dict: Extracted class fields
    """
    for _, node in tree.filter(javalang.tree.ClassDeclaration):
        if hasattr(node, "position") and node.position:
            class_start = node.position.line

            # Find first method/constructor position
            first_method_line = float("inf")
            for member in node.body:
                if isinstance(
                    member,
                    (
                        javalang.tree.MethodDeclaration,
                        javalang.tree.ConstructorDeclaration,
                    ),
                ):
                    if hasattr(member, "position") and member.position:
                        first_method_line = min(first_method_line, member.position.line)

            if first_method_line == float("inf"):
                first_method_line = _find_structure_end(lines, class_start)

            if has_intersection_between_code_lines(
                [class_start, first_method_line], [start_line, end_line]
            ):
                return {
                    f"{class_start}-{first_method_line}": {
                        "type": "class",
                        "code": "".join(lines[class_start - 1 : first_method_line - 1]),
                        "start_line": class_start,
                        "end_line": first_method_line - 1,
                        "name": node.name,
                    }
                }
    return {}


def _is_class_change(start_line, end_line, tree, lines):
    """
    Check if the change is within a class declaration.

    Args:
        start_line: Start line of the code change
        end_line: End line of the code change
        tree: Java AST
        lines: List of code lines

    Returns:
        bool: True if the change is within a class declaration
    """
    for _, node in tree.filter(javalang.tree.ClassDeclaration):
        if hasattr(node, "position") and node.position:
            class_start = node.position.line
            class_end = _find_structure_end(lines, class_start)
            if has_intersection_between_code_lines(
                [class_start, class_end], [start_line, end_line]
            ):
                return True
    return False


def _extract_structure(tree, lines, start_line, end_line, node_type, structure_type):
    """
    Generic structure extractor for methods, constructors and classes.

    Args:
        tree: Java AST
        lines: List of code lines
        start_line: Start line of the code change
        end_line: End line of the code change
        node_type: AST node type
        structure_type: Structure type

    Returns:
        dict: Extracted structure
    """
    for _, node in tree.filter(node_type):
        if hasattr(node, "position") and node.position:
            struct_start = node.position.line
            struct_end = _find_structure_end(lines, struct_start)

            if has_intersection_between_code_lines(
                [struct_start, struct_end], [start_line, end_line]
            ):
                return {
                    f"{struct_start}-{struct_end}": {
                        "type": structure_type,
                        "code": "".join(lines[struct_start - 1 : struct_end]),
                        "name": node.name,
                        "start_line": struct_start,
                        "end_line": struct_end,
                    }
                }
    return {}


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


def _find_structure_end(lines, start_line):
    """
    Find the end of the structure based on braces counting.

    Args:
        lines: List of code lines
        start_line: Start line of the structure

    Returns:
        int: End line of the structure
    """
    brace_count = 0
    found_first_brace = False

    for i, line in enumerate(lines[start_line - 1 :], start=start_line):
        if "{" in line:
            found_first_brace = True
            brace_count += line.count("{")
        if "}" in line:
            brace_count -= line.count("}")
        if found_first_brace and brace_count == 0:
            return i
    return len(lines)
