from django import template
from django.utils.safestring import mark_safe, SafeString
import json

register = template.Library()


def _snake_case_to_camel_case(data: str) -> str:
    words = data.split("_")
    return f"{words[0]}{''.join([word.capitalize() for word in words[1:]])}"


def _dict_to_camel_case(data: dict) -> dict:
    if isinstance(data, dict):
        return {
            _snake_case_to_camel_case(key): _dict_to_camel_case(value)
            for key, value in data.items()
        }
    else:
        return data


def _construct_hyperscript(data, name=None, accepted_kwargs=None, **kwargs) -> SafeString:
    """
    Constructs Hyperscript code to dump Django data.

    This function is used to generate Hyperscript code for setting variables based on the provided data.
    It vlaidates and processes additional keyword arguments for customization. This function
    is shared between different tags like `hs_dump` and `hs_expand`.

    Args:
        data (Any): The data to be dumped into a Hyperscript variable.
        name (str, optional): The name of the Hyperscript variable for the dumped data. (Only valid for the `hs_dump` tag.)
        accepted_kwargs (dict, optional): A dictionary of additional keyword arguments to validate sbeyond the default arguments.

    Kwargs:
        show (bool): If `True`, keeps the Hyperscript element in the DOM after initialization. Defaults to `False`.
        translate (bool): If `True`, converts dictionary keys from snake_case to camelCase to fit JavaScript conventions. Defaults to `True`.
        scope (str): The scope of the Hyperscript variable (e.g., 'global', 'local'). Defaults to `'global'`.
        wrap (bool): If `True`, wraps the Hyperscript code in a `<div>` element. Defaults to `True`.

    Returns:
        SafeString: A Django-safe string containing the generated Hyperscript code. If `wrap=True`, the Hyperscript is enclosed in a `<div>`.

    Raises:
        TypeError: If an unexpected or invalid keyword argument/type is provided.
        ValueError: If required arguments (like `name`) are missing or invalid.
    """
    DEFAULT_KWARGS = {
        "show": bool,
        "translate": bool,
        "scope": str,
        "wrap": bool,
        "debug": bool,
        "event": str,
    }

    accepted_kwargs = {**DEFAULT_KWARGS, **(accepted_kwargs or {})}
    for key, value in kwargs.items():
        if key not in accepted_kwargs:
            raise TypeError(
                f"Unexpected keyword argument: {key}. Accepted arguments: {', '.join([f'{kwarg}: {type.__name__}' for kwarg, type in accepted_kwargs.items()])}."
            )
        expected_type = accepted_kwargs[key]
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Invalid type for keyword argument {key}: expected {expected_type}, got {type(value).__name__}"
            )

    event = kwargs.get("event", None)
    event = f"on {event}" if event not in ["init", None] else "init"
    debug = kwargs.get("debug", False)
    scope = kwargs.get("scope", "global")
    wrap = kwargs.get("wrap", True)

    if kwargs.get("translate", True):
        data = _dict_to_camel_case(data)

    if kwargs.get("expand", False):
        if not isinstance(data, dict):
            raise TypeError(
                f"Invalid type for mapping: expected dict, got {type(data).__name__}"
            )
        
        assignments = []
        for key, value in data.items():
            assignment = f"set {scope} {key} to {json.dumps(value)}"
            if debug:
                logging_statement = f"call console.log(`{key}:\\n`, {key})"
                assignment = f"{assignment} then {logging_statement}"
            assignments.append(assignment)
        assignment = "\n    ".join(assignments)
        
    else:
        assignment = f"set {scope} {name} to {json.dumps(data)}"
        if debug:
            logging_statement = f"call console.log(`{name}:\\n`, {name})"
            assignment = f"{assignment} then {logging_statement}"

    hyperscript = f"{event}\n    {assignment}"

    if not kwargs.get("show", False):
        if not wrap:
            hyperscript = f"{hyperscript} then remove @_ from me"
        else:
            hyperscript = f"{hyperscript} then remove me"  

    hyperscript = f"{hyperscript}\n   end"

    if wrap:
        hyperscript = f"<div _='{hyperscript}'></div>"

    return mark_safe(hyperscript)


@register.simple_tag()
def hs_dump(data, name: str, **kwargs):
    """
    Dumps data into a single Hyperscript variable.

    This tag generates Hyperscript code to set a single variable (`name`)
    to the given `data` value. It delegates most of its behavior to
    `_construct_hyperscript`.

    Args:
        data (Any): The data to be dumped into a Hyperscript variable.
        name (str): The name of the Hyperscript variable.

    Kwargs:
        Any additional keyword arguments are passed to `_construct_hyperscript`
        for customization, including `show`, `translate`, `scope`, and `wrap`.

    Returns:
        SafeString: A Django-safe string containing the generated Hyperscript code.
    """
    return _construct_hyperscript(data, name, **kwargs)


@register.simple_tag()
def hs_expand(data, **kwargs):
    """
    Expands a dictionary into multiple Hyperscript variables.

    This tag generates Hyperscript code to expand the given `data` (a dictionary)
    into multiple variables, with each key in `data` becoming a separate variable.
    It automatically sets `expand=True` and delegates most of its behavior to
    `_construct_hyperscript`.

    Args:
        data (dict): A dictionary where each key-value pair will be dumped as separate Hyperscript variables.

    Kwargs:
        Any additional keyword arguments are passed to `_construct_hyperscript`
        for customization, including `show`, `translate`, `scope`, and `wrap`.

    Returns:
        SafeString: A Django-safe string containing the generated Hyperscript code.

    Raises:
        TypeError: If `data` is not a dictionary.
    """
    kwargs["expand"] = True
    accepted_kwargs = {"expand": bool}
    return _construct_hyperscript(data, accepted_kwargs=accepted_kwargs, **kwargs)
