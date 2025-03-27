import ast
import io
import sys

class CodeToEnglish:
    def __init__(self, code_snippet):
        self.code_snippet = code_snippet

    def parse_code(self):
        try:
            tree = ast.parse(self.code_snippet)
            return tree
        except SyntaxError as e:
            return f"Syntax Error: {e}"

    def convert_to_english(self):
        tree = self.parse_code()
        if isinstance(tree, str):
            return tree

        english_explanation = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                targets = ", ".join(t.id for t in node.targets if isinstance(t, ast.Name))
                value = self._get_node_value(node.value)
                english_explanation.append(f"Assign the value {value} to the variable {targets}.")
            elif isinstance(node, ast.Expr):
                value = self._get_node_value(node.value)
                english_explanation.append(f"Evaluate the expression: {value}.")
            elif isinstance(node, ast.FunctionDef):
                english_explanation.append(f"Define a function named {node.name}.")
            elif isinstance(node, ast.Call):
                func_name = self._get_node_value(node.func)
                args = ", ".join(self._get_node_value(arg) for arg in node.args)
                english_explanation.append(f"Call the function {func_name} with arguments {args}.")

        return "\n".join(english_explanation)

    def _get_node_value(self, node):
        if isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.BinOp):
            left = self._get_node_value(node.left)
            right = self._get_node_value(node.right)
            op = self._get_operator(node.op)
            return f"{left} {op} {right}"
        elif isinstance(node, ast.Call):
            return self._get_node_value(node.func)
        return "unknown"

    def _get_operator(self, op_node):
        return {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
        }.get(type(op_node), "unknown_operator")

    def execute_code(self):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        global_vars = {}

        try:
            exec(self.code_snippet, global_vars)
            output = new_stdout.getvalue()
        except Exception as e:
            output = f"Error during execution: {e}"
        finally:
            sys.stdout = old_stdout

        return output