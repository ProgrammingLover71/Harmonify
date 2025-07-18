from typing import Callable, Any

# Function type defnitions: prefix, postfix and replace.
type PrefixFnType = Callable[..., tuple[Any, Any]]
type PostfixFnType = Callable[..., Any]
type ReplaceFnType = Callable[..., Any]