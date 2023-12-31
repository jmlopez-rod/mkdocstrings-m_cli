from contextlib import suppress
from importlib import import_module
from inspect import cleandoc
from typing import Any, Mapping, cast

from griffe.dataclasses import Alias, Class, Docstring, Object
from griffe.exceptions import AliasResolutionError
from pydantic import BaseModel


def import_attr(attr_path: str) -> Any:
    """Get an attribute from a module.

    The `attr_path` should be a fully qualified path to the attribute. For
    example `import_attr('m.core.one_of')` will attempt to retrieve a handle
    on `one_of`.

    Args:
        attr_path: The path to the attribute.

    Returns:
        A `Good` containing the attribute or an issue.
    """
    module_parts = attr_path.split('.')
    module_name = '.'.join(module_parts[:-1])
    item_name = module_parts[-1]
    module = import_module(module_name)
    module_dict = module.__dict__
    return module_dict[item_name]


def get_class_identifier(
    mod_identifier: str,
    member: Object | Alias,
    member_name: str,
) -> str:
    """Obtain the class identifier of a Griffe object.

    Args:
        mod_identifier: The identifier of the module.
        member: The member object or alias.
        member_name: The name of the member.

    Returns:
        The class identifier if the member is a class or an alias of a class,
             otherwise returns an empty string.
    """
    if isinstance(member, Class):
        return f'{mod_identifier}.{member_name}'
    is_class = False
    with suppress(AliasResolutionError):
        is_class = member.is_class
    if isinstance(member, Alias) and is_class:
        return member.target_path
    return ''


def _fmt_attr(name: str, desc: str) -> str:
    desc_lines = cleandoc(desc).split('\n')
    new_desc = '\n        '.join(desc_lines)
    return f'{name}: {new_desc}'


def attach_attributes(
    griffe_class: Class,
    identifier: str,
    config: Mapping[str, Any],
) -> BaseModel:
    """Attach attributes to the docstring of a class.

    It will only work for classes that that derive from  pydantic's `BaseModel`.

    Args:
        griffe_class: The class to attach attributes to.
        identifier: The identifier of the class.
        config: The configuration for the mkdocstring handler.

    Returns:
        A `BaseModel` instance of the class.
    """
    docstr = griffe_class.docstring
    arg_model = cast(BaseModel, import_attr(identifier))
    is_command = config.get('is_command', False)
    has_fields = hasattr(arg_model, 'model_fields')  # noqa: WPS421
    if docstr and '\n\nAttributes:\n' in docstr.value:
        return arg_model
    if not is_command and has_fields and docstr and arg_model.model_fields:
        att_str = '\n    '.join([
            _fmt_attr(field, field_info.description or '...')
            for field, field_info in arg_model.model_fields.items()
        ])
        to_add = f'\n\nAttributes:\n    {att_str}'
        griffe_class.docstring = Docstring(
            value=f'{docstr.value}{to_add}',
            lineno=docstr.lineno,
            endlineno=docstr.endlineno,
            parent=docstr.parent,
            parser=docstr.parser,
            parser_options=docstr.parser_options,
        )
    return arg_model
