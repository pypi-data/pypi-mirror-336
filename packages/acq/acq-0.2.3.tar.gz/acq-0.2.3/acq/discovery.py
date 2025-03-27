import logging
import collections
import importlib
import inspect
import types
import typing

MODULE_NAME_SEPARATOR = '.'

T = typing.TypeVar("T", bound=typing.Type[object])


def import_module_safe(
    module: str | types.ModuleType,
) -> None | types.ModuleType:
    """ Wrapper for importlib.import_module that ignores ModuleNotFoundError

    """

    if inspect.ismodule(module):
        return module

    try:
        return importlib.import_module(module)
    except ModuleNotFoundError as e:
        pass

    return None


def get_module_name(*parts: str) -> str:
    return MODULE_NAME_SEPARATOR.join(parts)


def get_modules(
    *modules: str | types.ModuleType,
    package_names: typing.Sequence[str] = [],
) -> typing.List[types.ModuleType]:
    if not package_names:
        return list(filter(None, map(import_module_safe, modules)))

    if not modules:
        return get_modules(*package_names)

    all_modules: typing.List[str | types.ModuleType] = []

    for package_name in package_names:
        for module in modules:
            # NOTE: If a module ends up here, should we search it for package
            # names? It feels like it'd be weird to do, but maybe?
            if inspect.ismodule(module):
                all_modules.append(module)
                continue

            all_modules.append(get_module_name(package_name, module))

    return get_modules(*all_modules)


def get_module_objects(
    modules: typing.List[types.ModuleType],
    types: typing.Tuple[T],
) -> typing.Mapping[T, typing.Sequence[T]]:
    results = collections.defaultdict(list)

    for module in modules:
        for attribute_name in dir(module):
            for object_type in types:
                module_object = getattr(module, attribute_name)
                is_class = inspect.isclass(module_object)

                if attribute_name == 'FancySubClass':
                    print(
                        module_object,
                        issubclass(module_object, object_type),
                    )

                if module_object is object_type:
                    results[object_type].append(module_object)
                elif is_class and issubclass(module_object, object_type):
                    results[object_type].append(module_object)
                elif isinstance(module_object, object_type):
                    results[object_type].append(module_object)

    return results


@typing.overload
def discover(
    *modules: str | types.ModuleType,
    package_names: typing.Sequence[str] = [],
    types: typing.Literal[None] = None,
) -> typing.List[types.ModuleType]:
    """ called with no types provided """


@typing.overload
def discover(
    *modules: str | types.ModuleType,
    package_names: typing.Sequence[str] = [],
    types: typing.Tuple[T],
) -> typing.Mapping[T, typing.Sequence[T]]:
    """ called with types provided """


def discover(
    *modules: str | types.ModuleType,
    package_names: typing.Sequence[str] = [],
    types: None | typing.Tuple[T] = None,
) -> typing.List[types.ModuleType] | typing.Mapping[T, typing.Sequence[T]]:
    """ Allows discovery of modules, packages, or objects within them """

    resolved_modules = get_modules(*modules, package_names=package_names)

    if types is None:
        return resolved_modules

    return get_module_objects(resolved_modules, types)
