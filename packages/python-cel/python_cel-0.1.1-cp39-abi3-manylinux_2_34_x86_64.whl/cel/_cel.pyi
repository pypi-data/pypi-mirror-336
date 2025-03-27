from typing import Any, Callable

class Context:
    """
    An execution context for CEL programs.

    :param variables: The initial set of variables to be used in the context.
    :type variables: dict[str, Any] | None
    """
    def __init__(
        self,
        variables: dict[str, Any] | None = None,
        functions: dict[str, Callable] | None = None,
    ) -> None: ...
    def add_variables(self, variables: dict[str, Any]) -> None: ...
    def get_variable(self, name: str) -> Any: ...
    def add_functions(self, functions: dict[str, Callable]) -> None: ...


class Program:
    """
    A CEL program that can be executed against a context.

    :param expression: The CEL expression to be executed.
    :type expression: str
    """
    def __init__(self, expression: str) -> None: ...
    def execute(self, context: Context) -> Any: ...


def evaluate_expression(
    expression: str,
    variables: dict[str, Any] | None = None,
    functions: dict[str, Callable] | None = None,
) -> Any:
    """
    Evaluates a CEL expression with the given variables.

    :param expression: The CEL expression to be executed.
    :type expression: str
    :param variables: The variables to be used in the evaluation.
    :type variables: dict[str, Any] | None
    :return: The result of the evaluation.
    :rtype: Any
    """
    ...
