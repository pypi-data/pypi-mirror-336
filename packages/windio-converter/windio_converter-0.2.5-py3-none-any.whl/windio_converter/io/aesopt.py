import json
from collections import UserDict, UserList
from copy import deepcopy
from io import StringIO

import jmespath
import numpy as np
from aesoptparam.utils.html_repr import json_data_render
from aesoptparam.utils.json_utils import is_valid_json
from ruamel.yaml import YAML

from .utils import (
    dict_to_numpy,
    dict_type,
    is_list_numbers,
    list_to_numpy,
    list_type,
    path_to_value,
    update_dict,
    update_list,
)


class AESOpt_dict(UserDict):
    """AESOpt dict type. Mimics all methods in the build-in `dict` type but adds methods relevant for data manipulation within AESOpt.

    The class is based on `collections.UserDict` an `AESOpt_dict` is used as the base class for other dict-like data structure.
    """

    list_merge_id = ["name"]

    def __init__(self, *args, **kwargs):
        self._yaml_obj = None
        self._comment = dict()
        UserDict.__init__(self)
        self.update(*args, **kwargs)

    def copy(self):
        """Creates a deepcopy of the object"""
        return deepcopy(self)

    def update(
        self,
        *args,
        list_merge_id=None,
        d_type=None,
        l_type=None,
        replace_path=True,
        **kwargs,
    ):
        """Update/merge `self` with `*args` (`list` of `dict`'s) and `**kwargs` (key-value pairs), referred to a `dict_update`.

        Nested dicts are recursively being updated, so not replacing the whole `dict`. Data containing `list` of `dict`'s can be merged according to `list_merge_id`.

        If elements in a specific list/array need to be updated it can be done with a `dict` of indices (e.g. `self={"key": [1, 2]}` and `dict_update={"key": {1: 3}}` -> `self={"key": [1, 3]}`).

        `dict_update` can also contain callables (e.g. python object with a `.__call__` method defined or by `def`) where the data at the requested location is passed to the function and the function return is set at the data location (e.g. `self={"key": 5}` and `dict_update={"key": lambda val: val+5}` -> `self={"key":10}`). List of numbers are converted to numpy array so math operations are done elementwise.

        When new `list`'s or `dict`'s are added from `dict_update` to `self` they will be of `l_type` or `d_type` respectively.

        The flag `replace_path` sets weather `dict_update` should be updated to replace paths (e.g. `{"key1.key2": 5}` -> `{"key1":{"key2":5}}`).

        Parameters
        ----------
        args : dict,UserDict
            Dict-like data structure used to update the `self`.
        kwargs : key-value paris
            Dict-like data structure used to update the `self`.
        list_merge_id : list, str, optional
            List of keys (string is converted to a list) to merge `list` of `dict`'s by, by default None which results in `["name"]`
        d_type : dict,UserDict, optional
            Dict-type used when creating new dicts in `self`, by default to type(self)
        l_type : list,UserList, optional
            List-type used when creating new list in `self`, by default type(self).__name__.replace("dict", "list")
        replace_path : bool, optional
            Flag to enable/disable updating/replacing path-syntax for `dict_update`, by default True

        Returns
        -------
        self
        """
        if d_type is None:
            d_type = type(self)
        if l_type is None:
            l_type = self.list_type
        if list_merge_id is None:
            list_merge_id = self.list_merge_id
        for _dict in args:
            self = update_dict(self, _dict, list_merge_id, d_type, l_type, replace_path)
        self = update_dict(self, kwargs, list_merge_id, d_type, l_type, replace_path)
        return self

    # Dict dunder methoders
    def __repr__(self) -> str:
        return (
            str(type(self))[:-2].split(".")[-1] + "{" + ",".join(self.data.keys()) + "}"
        )

    def add(self, key):
        """Adds a new key with the value of the same type as self if the key is not present in the dict

        Parameters
        ----------
        key : str
            Name of the new key
        """
        if not key in self.data:
            self.data[key] = type(self)()
        return self[key]

    def __str__(self) -> str:
        return self.as_yaml()

    # dict
    def as_dict(self, inplace=False):
        """Convert the dict-like data into the build-in `dict` type. The conversion is done recursively and it also converts any list-like data to build-in list or numpy arrays.

        Parameters
        ----------
        inplace : bool, optional
            Flag, `True` means that all data will be set in place, by default False

        Returns
        -------
        dict
            self, converted to a build-in dict and list
        """
        if inplace:
            out = self.data
        else:
            out = deepcopy(self.data)
        for key, item in out.items():
            if hasattr(item, "as_dict"):
                out[key] = item.as_dict(inplace)
            elif hasattr(item, "to_list"):
                out[key] = item.to_list(True, inplace)
            elif isinstance(item, np.ndarray):
                out[key] = item.tolist()
        if inplace:
            self.data = out
        return out

    def from_dict(self, dict_in):
        """Set/update self from a dict. (thin wrapper around `self.update`)

        See `.update` for more.

        Returns
        -------
        self
        """
        self.update(dict_in)
        return self

    def to_list(self, as_dict=False, inplace=False):
        """Convert all list-like data to build-in `list` type (Converting any `UserList` or `ndarray`).

        Parameters
        ----------
        as_dict : bool, optional
            Flag for also converting to dict, by default False
        inplace : bool, optional
            Flag for doing it inplace, by default False

        Returns
        -------
        dict-like, self
        """
        # Convert to lists
        if inplace:
            out = self
        else:
            out = deepcopy(self)
        for key, item in out.items():
            if hasattr(item, "to_list"):
                out[key] = item.to_list(as_dict, inplace)
            elif isinstance(item, np.ndarray):
                out[key] = item.tolist()
        return out

    def to_numpy(self, inplace=True):
        """Convert all list and nested lists of number to numpy arrays

        Parameters
        ----------
        inplace : bool, optional
            Flag for doing it inplace, by default True

        Returns
        -------
        dict-like, self
        """
        if inplace:
            return dict_to_numpy(self)
        return dict_to_numpy(self.copy())

    # YAML in
    @property
    def yaml_object(self):
        """`ruamel.YAML` object used for reading and writing yaml files. Can be overwritten.

        Uses `.get_yaml_object` if not set by user.

        Returns
        -------
        ruamel.YAML
        """
        if self._yaml_obj is None:
            return self.get_yaml_object()
        return self._yaml_obj

    def get_yaml_object(self, typ="rt"):
        """Method for getting the yaml object.

        Parameters
        ----------
        typ : str, optional
            Type parsed to the initilization of the ruemel.YAML object (`YAML(typ=typ)`), by default "rt"

        Returns
        -------
        ruamel.YAML
        """
        if self._yaml_obj is None:
            yaml_obj = YAML(typ=typ)
            # From: https://github.com/WISDEM/WISDEM/blob/master/wisdem/inputs/validation.py#L32C5-L35C31
            yaml_obj.default_flow_style = False
            yaml_obj.width = 1e6
            yaml_obj.indent(mapping=4, sequence=6, offset=3)
            yaml_obj.allow_unicode = False
            # Convert numpy types to build in data types
            yaml_obj.Representer.add_multi_representer(
                np.str_, lambda dumper, data: dumper.represent_str(str(data))
            )
            yaml_obj.Representer.add_multi_representer(
                np.number,
                lambda dumper, data: dumper.represent_float(float(data)),
            )
            yaml_obj.Representer.add_multi_representer(
                np.integer, lambda dumper, data: dumper.represent_int(int(data))
            )

            # Write non-nested list with flow-style
            def list_rep(dumper, data):
                if len(data) > 0 and isinstance(data[0], (list, dict)):
                    return dumper.represent_sequence(
                        "tag:yaml.org,2002:seq", data, flow_style=False
                    )
                return dumper.represent_sequence(
                    "tag:yaml.org,2002:seq", data, flow_style=True
                )

            def ndarray_rep(dumper, data):
                return list_rep(dumper, data.tolist())

            def aesopt_dict_rep(dumper, data):
                return dumper.represent_dict(data.as_dict())

            def aesopt_list_rep(dumper, data):
                return list_rep(dumper, data.to_list())

            yaml_obj.Representer.add_representer(list, list_rep)
            yaml_obj.Representer.add_representer(np.ndarray, ndarray_rep)
            yaml_obj.Representer.add_representer(type(self), aesopt_dict_rep)
            yaml_obj.Representer.add_representer(self.list_type, aesopt_list_rep)

            return yaml_obj
        return self._yaml_obj

    @yaml_object.setter
    def yaml_object(self, yaml_obj):
        self._yaml_obj = yaml_obj

    def from_yaml(self, yaml_str):
        """Set/update data from a YAML file as a string

        Parameters
        ----------
        yaml_str : str

        Returns
        -------
        self
        """
        self.update(self.get_yaml_object("safe").load(yaml_str))
        return self

    def read_yaml(self, filename):
        """Set/update data from a YAML file

        Parameters
        ----------
        filename : str
            Path/filename

        Returns
        -------
        self
        """
        with open(filename, "r") as file:
            self.from_yaml(file.read())
        return self

    # YAML out
    def as_yaml(self):
        """Serialize data to a YAML string

        Returns
        -------
        str
            Data as a YAML string
        """
        out = StringIO()
        self.yaml_object.dump(self, out)
        return out.getvalue()

    def write_yaml(self, filename):
        """Serialize data in a YAML file

        Parameters
        ----------
        filename : str
            Path/Filename for the yaml file

        Returns
        -------
        self
        """
        with open(filename, "w") as file:
            file.write(self.as_yaml())
        return self

    # JSON in
    def from_json(self, json_str):
        """Set/update data from a JSON file as a string

        Parameters
        ----------
        json_str : str

        Returns
        -------
        self
        """
        self.update(json.loads(json_str))
        return self

    def read_json(self, filename):
        """Set/update data from a JSON file

        Parameters
        ----------
        filename : str
            Path/filename

        Returns
        -------
        self
        """
        with open(filename, "r") as file:
            self.from_json(file.read())
        return self

    # JSON out
    def as_json(self):
        """Serialize data to a JSON string

        Returns
        -------
        str
            Data as a JSON string
        """
        out = StringIO()
        json.dump(self.as_dict(), out)
        return out.getvalue()

    def write_json(self, filename):
        """Serialize data in a YAML file

        Parameters
        ----------
        filename : str
            Path/Filename for the yaml file

        Returns
        -------
        self
        """
        with open(filename, "w") as file:
            file.write(self.as_json())

    def jp(self, expression):
        """Extract data from dict-like data structure using the [JMESPath query language](https://jmespath.org/)

        Parameters
        ----------
        expression : str
            JMESPath query sting

        Returns
        -------
        Any
            Output from the JMESPath query. Notices that if nothing was found it will return `None` - not fail.
        """
        return jmespath.search(
            expression, self.to_list(), jmespath.Options(dict_cls=type(self))
        )

    @property
    def list_type(self):
        name = type(self).__name__.replace("dict", "list")
        if name in globals():
            return globals()[name]
        else:
            return AESOpt_list

    def __getitem__(self, key):
        if isinstance(key, str) and (("." in key) or ("[" in key)):
            return path_to_value(self, key)
        return super().__getitem__(key)

    def __setitem__(self, key, item):
        if isinstance(key, str) and (("." in key) or ("[" in key)):
            self.update({key: item})
        else:
            super().__setitem__(key, item)

    def _repr_html_(self):
        data = self.as_dict()
        if is_valid_json(data):
            return json_data_render(data)._repr_html_()
        return self.__repr__()

    def display(self, open_default=False, fields=None):
        """Display the dict as an interactive HTML table in the notebook. Optionally allows to and close some fields

        Parameters
        ----------
        open_default : bool, optional
            Flag for default opening or closing collapsible entries, by default False
        fields : list, optional
            list or list of list of names to open or close (opposed to open_default), by default None
        """
        from IPython.display import display

        display(json_data_render(self.as_dict(), open_default, fields))


class AESOpt_list(UserList):
    """AESOpt list type to which adds methods for interacting with list like data in AESOpt. Used as base class for other dedicate list-like data structures."""

    list_merge_id = AESOpt_dict.list_merge_id

    def __init__(self, list_in=None, list_merge_id=None, d_type=None, l_type=None):
        UserList.__init__(self)
        if not list_in is None:
            self.update(list_in, list_merge_id, d_type, l_type)

    def to_list(self, as_dict=True, inplace=False):
        """Convert all list-like data to build-in `list` type (Converting any `UserList` or `ndarray`).

        Parameters
        ----------
        as_dict : bool, optional
            Flag for also converting to dict, by default False
        inplace : bool, optional
            Flag for doing it inplace, by default False

        Returns
        -------
        dict-like, self
        """
        if inplace:
            out = self
        else:
            out = deepcopy(self)

        if isinstance(out.data, np.ndarray):
            if inplace:
                self.data = out.data.tolist()
                return self.data
            return out.data.tolist()

        for i in range(len(out)):
            if as_dict and isinstance(out[i], AESOpt_dict):
                out[i] = out[i].as_dict(True)
            elif isinstance(out[i], (AESOpt_list, AESOpt_dict)):
                out[i] = out[i].to_list(as_dict, inplace)
            elif isinstance(out[i], np.ndarray):
                out[i] = out[i].tolist()
        return list(out.data)

    def to_numpy(self, inplace=True):
        """Convert all list and nested lists of number to numpy arrays

        Parameters
        ----------
        inplace : bool, optional
            Flag for doing it inplace, by default True

        Returns
        -------
        list-like, ndarray, self
        """
        if inplace:
            self.data = list_to_numpy(self.data)
            return self
        return list_to_numpy(self.copy())

    def copy(self):
        """Creates a deepcopy of the object"""
        return deepcopy(self)

    def update(self, list_update, list_merge_id=None, d_type=None, l_type=None):
        """Update/merge `self` with `list_update` where items in `list_update` replaces the ones in `self`.

        Data containing `list` of `dict`'s can be merged according to `list_merge_id`.

        If elements in a specific list/array need to be updated it can be done with a `dict` of indices (e.g. `self=[1, 2]` and `list_update={1: 3}` -> `self=[1, 3]`).

        `list_update` can also contain callables (e.g. python object with a `.__call__` method defined or by `def`) where the data at the requested location is passed to the function and the function return is set at the data location (e.g. `self=[1, 2]` and `list_update={1: lambda val: val+5}` -> `self=[1, 7]`). List of numbers are converted to numpy array so math operations are done elementwise.

        When new `list`'s or `dict`'s are added from `list_update` to `list_main` they will be of `l_type` or `d_type` respectively.

        Parameters
        ----------
        list_update : list,UserList
            List-like data structure used to update the `list_main`
        list_merge_id : list, str, optional
            List of keys (string is converted to a list) to merge `list` of `dict`'s by, by default None which results in `["name"]`
        d_type : dict,UserDict, optional
            Dict-type used when creating new dicts in `dict_main`, by default type(self).__name__.replace("list", "dict")
        l_type : list,UserList, optional
            List-type used when creating new list in `dict_main`, by default type(self)

        Returns
        -------
        self
        """
        if d_type is None:
            d_type = self.dict_type
        if l_type is None:
            l_type = type(self)
        if list_merge_id is None:
            list_merge_id = self.list_merge_id
        if not self.data:
            self.data = list_update
            for i in range(len(self.data)):
                if is_list_numbers(self.data[i]):
                    continue
                elif isinstance(self.data[i], list_type):
                    self.data[i] = update_list(
                        l_type(), self.data[i], list_merge_id, d_type, l_type
                    )
                elif isinstance(self.data[i], dict_type):
                    self.data[i] = update_dict(
                        d_type(), self.data[i], list_merge_id, d_type, l_type
                    )
        else:
            self = update_list(self, list_update, list_merge_id, d_type, l_type)
        return self

    @property
    def dict_type(self):
        name = type(self).__name__.replace("list", "dict")
        if name in globals():
            return globals()[name]
        else:
            return AESOpt_dict

    def _repr_html_(self):
        data = self.to_list()
        if is_valid_json(data):
            return json_data_render(data)._repr_html_()
        return self.__repr__()

    def display(self, open_default=False, fields=None):
        """Display the list as an interactive HTML table in the notebook. Optionally allows to and close some fields

        Parameters
        ----------
        open_default : bool, optional
            Flag for default opening or closing collapsible entries, by default False
        fields : list, optional
            list or list of list of names to open or close (opposed to open_default), by default None
        """
        from IPython.display import display

        display(json_data_render(self.to_list(), open_default, fields))
