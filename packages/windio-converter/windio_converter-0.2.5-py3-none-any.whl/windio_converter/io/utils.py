import re
from collections import UserDict, UserList

import numpy as np

dict_type = (dict, UserDict)
list_type = (list, UserList, np.ndarray)


# %% Update dict and list's %% #
def update_dict(
    dict_main,
    dict_update,
    list_merge_id=None,
    d_type=dict,
    l_type=list,
    replace_path=True,
):
    """Update/merge `dict_main` with `dict_update` where items in `dict_update` replaces the ones in `dict_main`.

    Nested dicts are recursively being updated, so not replaced. Data containing `list` of `dict`'s can be merged according to `list_merge_id`.

    If elements in a specific list/array need to be updated it can be done with a `dict` of indices (e.g. `dict_main={"key": [1, 2]}` and `dict_update={"key": {1: 3}}` -> `dict_main={"key": [1, 3]}`).

    `dict_update` can also contain callables (e.g. python object with a `.__call__` method defined or by `def`) where the data at the requested location is passed to the function and the function return is set at the data location (e.g. `dict_main={"key": 5}` and `dict_update={"key": lambda val: val+5}` -> `dict_main={"key":10}`). List of numbers are converted to numpy array so math operations are done elementwise.

    When new `list`'s or `dict`'s are added from `dict_update` to `dict_main` they will be of `l_type` or `d_type` respectively.

    The flag `replace_path` sets weather `dict_update` should be updated to replace paths (e.g. `{"key1.key2": 5}` -> `{"key1":{"key2":5}}`).

    Parameters
    ----------
    dict_main : dict,UserDict
        Dict-like data structure to be updated. Will be don in place, so copy `dict_main` if this is not the target behavior.
    dict_update : dict,UserDict
        Dict-like data structure used to update the `dict_main`
    list_merge_id : list, str, optional
        List of keys (string is converted to a list) to merge `list` of `dict`'s by, by default None which results in `["name"]`
    d_type : dict,UserDict, optional
        Dict-type used when creating new dicts in `dict_main`, by default dict
    l_type : list,UserList, optional
        List-type used when creating new list in `dict_main`, by default list
    replace_path : bool, optional
        Flag to enable/disable updating/replacing path-syntax for `dict_update`, by default True

    Returns
    -------
    dict,UserDict
        `dict_main` with updates from `dict_update` applied.
    """
    if isinstance(dict_update, list_type):
        dict_update = dict(dict_update)
    if replace_path:
        dict_update = update_path_in_dict(dict_update, list_merge_id, d_type, l_type)
    return _update_dict(dict_main, dict_update, list_merge_id, d_type, l_type)


def _update_dict(dict_main, dict_update, list_merge_id=None, d_type=dict, l_type=list):
    if not isinstance(dict_main, dict_type):
        raise ValueError(
            f"Dict to be updated need to be of type dict/UserDict (given: type(dict_main)={type(dict_main)})"
        )
    if not isinstance(dict_update, dict_type):
        raise ValueError(
            f"Dict to update the main dict need to be of type dict/UserDict (given: type(dict_update)={type(dict_update)})"
        )
    for key, val in dict_update.items():
        if isinstance(val, dict_type):
            if isinstance(dict_main.get(key, {}), list_type):
                dict_main[key] = update_list(
                    dict_main.get(key, l_type()), val, list_merge_id, d_type, l_type
                )
            else:
                dict_main[key] = _update_dict(
                    dict_main.get(key, d_type()), val, list_merge_id, d_type, l_type
                )
        elif isinstance(val, list_type):
            dict_main[key] = update_list(
                dict_main.get(key, l_type()), val, list_merge_id, d_type, l_type
            )
        elif is_callable(val):
            if key in dict_main:
                dict_main[key] = update_from_callable(dict_main[key], val)
            else:
                dict_main[key] = val
        elif val is None:
            if key in dict_main:
                dict_main.pop(key)
            else:
                dict_main[key] = val
        else:
            dict_main[key] = val
    return dict_main


def update_list(list_main, list_update, list_merge_id=None, d_type=dict, l_type=list):
    """Update/merge `list_main` with `list_update` where items in `list_update` replaces the ones in `list_main`.

    Nested dicts are recursively being updated, so not replaced. Data containing `list` of `dict`'s can be merged according to `list_merge_id`.

    If elements in a specific list/array need to be updated it can be done with a `dict` of indices (e.g. `list_main=[1, 2]` and `list_update={1: 3}` -> `list_main=[1, 3]`).

    `list_update` can also contain callables (e.g. python object with a `.__call__` method defined or by `def`) where the data at the requested location is passed to the function and the function return is set at the data location (e.g. `list_main=[1, 2]` and `list_update={1: lambda val: val+5}` -> `list_main=[1, 7]`). List of numbers are converted to numpy array so math operations are done elementwise.

    When new `list`'s or `dict`'s are added from `list_update` to `list_main` they will be of `l_type` or `d_type` respectively.

    Parameters
    ----------
    list_main : list,UserList
        List-like data structure to be updated. Will be done in place, so copy `list_main` if this is not the target behavior.
    list_update : list,UserList
        List-like data structure used to update the `list_main`
    list_merge_id : list, str, optional
        List of keys (string is converted to a list) to merge `list` of `dict`'s by, by default None which results in `["name"]`
    d_type : dict,UserDict, optional
        Dict-type used when creating new dicts in `dict_main`, by default dict
    l_type : list,UserList, optional
        List-type used when creating new list in `dict_main`, by default list

    Returns
    -------
    list, UserList
        `list_main` updated with the data in `list_update`

    Raises
    ------
    ValueError
        If `list_main` is not a list-type
    ValueError
        If `list_update` is not list- or dict-type or a callable
    ValueError
        If list_merge_id is not a string (`str`) or `list` of `str`
    """
    if list_merge_id is None:
        list_merge_id = ["name"]
    if isinstance(list_merge_id, str):
        list_merge_id = [list_merge_id]
    if not (
        isinstance(list_merge_id, list_type)
        and all([isinstance(el, str) for el in list_merge_id])
    ):
        raise ValueError(
            f"`list_merge_id` needs to be a string or a list of strings (given: {list_merge_id})"
        )
    if isinstance(list_main, dict_type) and any(
        [name in list_main for name in list_merge_id]
    ):
        # If list_main is not a list of dict but contains list_merge_id it will cast it as a dict
        list_main = [list_main]
    if not isinstance(list_main, list_type):
        raise ValueError(
            f"List to be updated need to be of type list/UserList/ndarray (given: type(list_main)={type(list_main)})"
        )
    if not (
        isinstance(list_update, list_type)
        or isinstance(list_update, dict_type)
        or is_callable(list_update)
    ):
        raise ValueError(
            f"List to updated the main list need to be of type list/UserList/ndarray or dict/UserDict or callable (given: type(list_update)={type(list_update)})"
        )

    if is_list_of_list(list_main):
        if isinstance(list_update, dict_type):
            for i, el in list_update.items():
                if el is None:
                    list_main.pop(i)
                else:
                    list_main[i] = update_list(
                        list_main[i], el, list_merge_id, d_type, l_type
                    )
            return list_main
    if is_list_of_dict(list_main):
        has_id = False
        for el1 in list_update if isinstance(list_update, list_type) else [list_update]:
            for iel2, el2 in enumerate(list_main):
                for id in list_merge_id:
                    if el1.get(id, "__el1__") == el2.get(id, "__el2__"):
                        list_main[iel2] = _update_dict(
                            el2, el1, list_merge_id, d_type, l_type
                        )
                        has_id = True
        if has_id:
            return list_main

    if isinstance(list_update, list_type):
        if is_list_of_dict(list_update):
            if hasattr(l_type, "dict_type"):
                out = l_type()
                out.update(list_update, list_merge_id, d_type, l_type)
                return out
            return l_type([d_type(d) for d in list_update])
        return l_type(list_update)
    elif isinstance(list_update, dict_type):
        for i, el in list_update.items():
            if el is None:
                list_main.pop(i)
            elif is_callable(el):
                list_main[i] = update_from_callable(list_main[i], el)
            elif isinstance(list_main[i], dict_type):
                list_main[i] = _update_dict(list_main[i], el)
            else:
                list_main[i] = el
    elif is_callable(list_update):
        list_main = update_from_callable(list_main, list_update)
    return list_main


def update_from_callable(data, callable):
    """Update `data` from a callable.

    If `data` is a list of numbers (checked with the `is_list_numbers` method) it is converted to an numpy array.

    Parameters
    ----------
    data : int, float, list, dict, ndarray
        Data to apply the callable for
    callable : `callable`
        Any object with a `.__call__` method taking a single argument (`data`)

    Returns
    -------
    int, float, list, dict, ndarray
        Value from any operation or transformation of the `data` input.
    """
    if isinstance(data, list_type):
        if is_list_numbers(data):
            return callable(np.array(data))
    return callable(data)


def is_list_of_dict(list_in):
    """Method for testing if data is a `list` of `dict`'s

    Parameters
    ----------
    list_in : Any
        Data structure to test

    Returns
    -------
    bool
        Flag, `True` if data is a `list` of `dict`'s

    Raises
    ------
    ValueError
        If data is not homogeneous (if `list_in[0]` is a dict but not all elements of `list_in[:]` is `dict`'s)
    """
    if (
        isinstance(list_in, list_type)
        and (len(list_in) > 0)
        and isinstance(list_in[0], dict_type)
    ):
        if not all([isinstance(el, dict_type) for el in list_in]):
            raise ValueError(
                f"Not all elements in list are dicts, data should be homogeneous (given: {list_in})"
            )
        return True
    else:
        return False


def is_list_of_list(list_in):
    """Method for testing if data is a `list` of `list`'s

    Parameters
    ----------
    list_in : Any
        Data structure to test

    Returns
    -------
    bool
        Flag, `True` if data is a `list` of `list`'s

    Raises
    ------
    ValueError
        If data is not homogeneous (if `list_in[0]` is a `list` but not all elements of `list_in[:]` is `list`'s)
    """
    if (
        isinstance(list_in, list_type)
        and (len(list_in) > 0)
        and isinstance(list_in[0], list_type)
    ):
        if not all([isinstance(el, list_type) for el in list_in]):
            raise ValueError(
                f"Not all elements in list are lists, data should be homogeneous (given: {list_in})"
            )
        return True
    else:
        return False


def is_callable(obj):
    """Method to test if an object is a callable (Tests if the object has a `.__call__` method)

    Parameters
    ----------
    obj : Any
        Object to test if it is a callable

    Returns
    -------
    bool
        Flag, `True` means that the object is callable
    """
    return hasattr(obj, "__call__")


def is_list_numbers(list_in):
    """Method to test if a `list` or nested `list`'s only contains `float`'s or `int`'s. Testing by casting to an array and check the resulting `.dtype`.

    Parameters
    ----------
    list_in : Any
        Data to test

    Returns
    -------
    bool
        Flag, `True` means the list is a `list` or nested `list`'s of numbers.
    """
    try:
        if np.issubdtype(np.asarray(list_in).dtype, np.number):
            return True
        return False
    except:
        return False


def dict_to_numpy(dict_in):
    """Convert all list of numbers to numpy array (Tested with the `is_list_numbers`). Data is changed inplace.

    Parameters
    ----------
    dict_in : dict_type
        Any dict-like data structure (`dict`, `UserDict`)

    Returns
    -------
    dict_type
        Returns `dict_in` but with all list of numbers replaced by the equivalent numpy array
    """
    for name, val in dict_in.items():
        if isinstance(val, dict_type):
            dict_in[name] = dict_to_numpy(val)
        elif isinstance(val, list_type) and is_list_numbers(val):
            dict_in[name] = np.asarray(val)
        elif is_list_of_dict(val):
            for i in range(len(val)):
                dict_in[name][i] = dict_to_numpy(val[i])
        elif hasattr(val, "to_numpy"):
            dict_in[name].to_numpy(True)
    return dict_in


def list_to_numpy(list_in):
    """Convert a list to numpy array. If the list contains inhomogeneous data (lists are not the same length) it will not convert the main array to numpy, but only each of the sub arrays.

    Parameters
    ----------
    list_in : list,UserList
        Data to convert to numpy array

    Returns
    -------
    list of ndarray, ndarray
        Data where as much as possible is converted to numpy arrays
    """
    if is_list_numbers(list_in):
        return np.asarray(list_in)
    for i in range(len(list_in)):
        if isinstance(list_in[i], list_type):
            list_in[i] = list_to_numpy(list_in[i])
        elif isinstance(list_in[i], dict_type):
            list_in[i] = dict_to_numpy(list_in[i])
    return list_in


# %% Object-Path to X %% #
def path_to_path_list(path):
    """Converts an object path string to a `path_list`.

    Parameters
    ----------
    path : str
        Object path (e.g. `"key1.key2.key3[0].key4"`)

    Returns
    -------
    list
        List of keys and indices (e.g. `["key1","key2","key3",0,"key4"]`)

    Raises
    ------
    ValueError
        If indices are not integers (e.g. `key1[key3]` will fail)
    """
    path_list = []
    for name in path.split(".") if path.split(".") else [path]:
        if "[" in name:
            names = re.findall(r"([^\[\]]+)", name)
            if len(names) > 1:
                path_list.append(names[0])
                names = names[1:]
            for index in names:
                if not index.replace("-", "").replace("+", "").isdigit():
                    raise ValueError(
                        f"Indices need to integers: index={index} (name={name}, path={path})"
                    )
                path_list.append(int(index))
        else:
            path_list.append(name)
    return path_list


def path_list_to_dict(path_list, val=None):
    """Convert a `path_list` (output from `path_to_path_list`) to a `dict` with `val` at the inner most level of the dict.

    Parameters
    ----------
    path_list : list of str
        List of keys used to create the dict
    val : Any, optional
        Value to be assigned at the inner level of the dict, by default None

    Returns
    -------
    dict
        Dict or nested dict with the keys from `path_list` with `val` at the inner level
    """
    if len(path_list) == 1:
        return {path_list[0]: val}
    return {path_list[0]: path_list_to_dict(path_list[1:], val)}


def path_to_dict(path, val=None):
    """Converts an object path string to a `dict` with `val` at the inner most level of the dict.

    Combines `path_to_path_list` and `path_list_to_dict`.

    Parameters
    ----------
    path : str
        Object path (e.g. `"key1.key2.key3[0].key4"`)
    val : Any, optional
        Value to be assigned at the inner level of the dict, by default None

    Returns
    -------
    dict
        Dict or nested dict with the keys from `path` with `val` at the inner level
    """
    return path_list_to_dict(path_to_path_list(path), val)


def update_path_in_dict(dict_in, list_merge_id=None, d_type=dict, l_type=list):
    """Update object-path's in `dict_in` to be nested `dict`'s instead.

    Recursively going thought all `dict`'s in `dict_in` and converting any object-path using `path_to_dict`. The resulting dict is merged into `dict_in` using the `update_dict` method.

    Parameters
    ----------
    dict_in : dict,UserDict
        Dict containing keys as object-path's
    list_merge_id : list, str, optional
        List of keys (string is converted to a list) to merge `list` of `dict`'s by, by default None which results in `["name"]`
    d_type : dict,UserDict, optional
        Dict-type used when creating new dicts in `dict_main`, by default dict
    l_type : list,UserList, optional
        List-type used when creating new list in `dict_main`, by default list

    Returns
    -------
    dict
        `dict_in` but with object-path's replaced with the equvilant nested dict
    """
    names = list(dict_in.keys())
    for name in names:
        if isinstance(name, str) and (("." in name) or ("[" in name)):
            dict_in = _update_dict(
                dict_in,
                path_to_dict(name, dict_in[name]),
                list_merge_id,
                d_type,
                l_type,
            )
            dict_in.pop(name)
        elif isinstance(dict_in[name], dict_type):
            dict_in[name] = update_path_in_dict(
                dict_in[name], list_merge_id, d_type, l_type
            )
        elif is_list_of_dict(dict_in[name]):
            for i in range(len(dict_in[name])):
                dict_in[name][i] = update_path_in_dict(
                    dict_in[name][i], list_merge_id, d_type, l_type
                )
    return dict_in


def path_to_value(dict_in, path):
    """Extract a value from `dict_in` according to an object-path (`path`)

    Parameters
    ----------
    dict_in : dict
        Dict structure to extract a value from
    path : str
        Object-path

    Returns
    -------
    Any
        Value at the end of the object-path in `dict_in`
    """
    path_list = path_to_path_list(path)
    return path_list_to_value(dict_in, path_list)


def path_list_to_value(dict_in, path_list):
    """Extract a value from `dict_in` according to an object-path-list (`path_list`)

    Parameters
    ----------
    dict_in : dict
        Dict structure to extract a value from
    path_list : list of str
        Object-path

    Returns
    -------
    Any
        Value at the end of the object-path in `dict_in`
    """
    if len(path_list) == 1:
        return dict_in[path_list[0]]
    return path_list_to_value(dict_in[path_list[0]], path_list[1:])
