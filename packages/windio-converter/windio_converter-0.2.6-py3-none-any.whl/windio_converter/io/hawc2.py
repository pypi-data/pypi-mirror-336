import os
import sys
from io import StringIO

import jmespath
import numpy as np

from .aesopt import AESOpt_dict, AESOpt_list
from .utils import dict_type, is_list_of_dict, list_type


# %% Read and Write HTC-file to and from dict %% #
def read_htc_as_dict(filename, exe_path="./"):
    """Read a HTC-file into a dict.

    Data is being converted depending on 4 different data structures in the HTC-file, namely:

    - **Command**, unique keyword linked with a value that can be `int`, `float`, `str`, `list`.
    - **Repeated Command**, keyword that can be repeated many times. Data is stored as a `list` of `list`'s.
    - **Block**, A set of commands starting with a `begin *keyword*` and `end *keyword*`. Data becomes a `dict` of `dict`'s.
    - **Repeated Block**, similar to a *Block* but can be repeated multiple times. Data becomes a `list` of `dict`'s. Example:

    Used as the base reader for `HTC_file.read_htc`.

    Parameters
    ----------
    filename : str
        Path/filename
    exe_path : str, optional
        Execution path, used in case the file contains `continue_in_file`, by default "./"

    Returns
    -------
    (dict, dict)
        HTC-file data as a dict data structure and comments as dict
    """
    if isinstance(filename, list_type):
        htc_list_str = filename
    else:
        with open(filename, "r") as file:
            htc_list_str = file.read().split("\n")
    with recursionlimit_context_manager(
        recursionlimit
    ):  # Temporary increasing recursion limit
        htc_dict = _decode_htc_file(iter(htc_list_str), {}, {}, "", exe_path)
    return htc_dict


def _decode_htc_file(htcfile_iter, dict_out, dict_comment, cur_name, exe_path):
    try:
        line, comment = _clean_line(next(htcfile_iter))
    except StopIteration:
        return dict_out, dict_comment

    if "exit" in line:
        dict_comment["end"] = [comment]
        return _decode_htc_file(htcfile_iter, dict_out, dict_comment, "end", exe_path)

    if ("continue_in_file" in line) and (exe_path is not None):
        with open(os.path.join(exe_path, line.split()[1]), "r") as file:
            _decode_htc_file(
                iter(file.read().split("\n")),
                dict_out,
                dict_comment,
                cur_name,
                exe_path,
            )
        return _decode_htc_file(
            htcfile_iter, dict_out, dict_comment, cur_name, exe_path
        )

    if "begin" in line:
        cur_name = line.split()[1].lower()
        if cur_name in dict_out:  # Repeated block
            if not isinstance(dict_out[cur_name], (list, np.ndarray)):
                dict_out[cur_name] = [dict_out[cur_name]]
                dict_comment[cur_name] = [dict_comment[cur_name]]
            block, comments = _decode_htc_file(htcfile_iter, {}, {}, "", exe_path)
            dict_out[cur_name].append(block)
            comments.setdefault("begin", []).insert(0, comment)
            dict_comment[get_comment_name(cur_name)].append(comments)
        else:  # Single block
            block, comments = _decode_htc_file(htcfile_iter, {}, {}, "", exe_path)
            dict_out[cur_name] = block
            comments.setdefault("begin", []).insert(0, comment)
            dict_comment[get_comment_name(cur_name)] = comments
        return _decode_htc_file(
            htcfile_iter, dict_out, dict_comment, cur_name, exe_path
        )

    elif (len(line) > 0) and (line.split()[0] == "end"):
        dict_comment["end"] = [comment]
        return dict_out, dict_comment

    elif line:
        elements = line.strip().split()
        cur_name = elements[0].strip().lower()
        if cur_name.startswith("body"):
            cur_name = cur_name.replace("body", "mbdy")
        values = _convert_values(elements[1:])
        if cur_name in dict_out:  # Repeated command
            if not isinstance(dict_out[cur_name], list_type):
                dict_out[cur_name] = [[dict_out[cur_name]]]
                dict_comment[get_comment_name(cur_name)] = [
                    dict_comment[get_comment_name(cur_name)]
                ]
            elif isinstance(values, list_type) and not (
                isinstance(dict_out[cur_name][0], list_type)
            ):
                dict_out[cur_name] = [dict_out[cur_name]]
                dict_comment[get_comment_name(cur_name)] = [
                    dict_comment[get_comment_name(cur_name)]
                ]
            if isinstance(values, list_type):
                dict_out[cur_name].append(values)
            else:
                dict_out[cur_name].append([values])
            dict_comment[get_comment_name(cur_name)].append([])
        else:  # Single command
            dict_out[cur_name] = values

    if not "begin" in line:
        comment_name = get_comment_name(cur_name)
        if (comment_name in dict_comment) and isinstance(
            dict_comment[comment_name], dict_type
        ):
            dict_comment[comment_name]["end"].append(comment)
        elif (
            (comment_name in dict_comment)
            and isinstance(dict_comment[comment_name], list_type)
            and isinstance(dict_comment[comment_name][0], dict_type)
        ):
            dict_comment[comment_name][-1]["end"].append(comment)
        elif (comment_name in dict_comment) and isinstance(
            dict_comment[comment_name][0], list_type
        ):
            dict_comment[comment_name][-1].append(comment)
        else:
            dict_comment.setdefault(comment_name, []).append(comment)
    return _decode_htc_file(htcfile_iter, dict_out, dict_comment, cur_name, exe_path)


def _clean_line(line):
    out = line.strip().split(";")
    command = out[0]
    comment = ";".join(out[1:])
    if command.startswith("["):  # Check for leading tags
        out = command[1:].split("]")
        tag = out[0].strip()
        command = "]".join(out[1:])
        comment = f"$>tag:[{tag}]<$" + comment
    return command, comment


def _convert_values(elements):
    if not elements:
        return ""
    for i, el in enumerate(elements):
        elements[i] = _convert_value(el)
    if len(elements) == 1:
        return elements[0]
    return elements


def _convert_value(el):
    try:
        return int(el)
    except Exception:
        pass
    try:
        return float(el)
    except Exception:
        pass
    return el.strip()


def get_comment_name(cur_name):
    if not cur_name:
        return "begin"
    return cur_name


def write_htc_as_file(filename, htc_dict, comment_dict=None):
    """Write a HTC-file from a `htc_dict` and optionally with comments from the `comment_dict`.

    Parameters
    ----------
    filename : str
        Path/filename
    htc_dict : dict
        HTC-data as a dict
    comment_dict : dict, optional
        Comments as a dict like structure, by default None
    """
    if comment_dict is None:
        comment_dict = {}
    with recursionlimit_context_manager(
        recursionlimit
    ):  # Temporary increasing recursion limit
        htc_file = _encode_htc_file(htc_dict, comment_dict, [], "")
    htc_file += ["exit"]
    htc_file = add_comments(comment_dict, "end", htc_file, "")

    htc_str = "\n".join(htc_file)
    if isinstance(filename, StringIO):
        filename.write(htc_str)
    else:
        with open(filename, "w") as file:
            file.write(htc_str)


tab_size = "  "
recursionlimit = 5000


def _encode_htc_file(dict_htc, dict_comment, out, indent):
    # Add begin comments
    if len(out) == 0:
        out = add_comments(dict_comment, "begin", out, indent)

    for key, val in dict_htc.items():
        if isinstance(val, dict_type):
            # Any begin block is a dict
            comments = dict_comment.get(key, {})
            out += [indent + f"begin {key}"]
            out = add_comments(comments, "begin", out, indent + tab_size)
            out = _encode_htc_file(val, comments, out, indent + tab_size)
            out += [indent + f"end {key}"]
            out = add_comments(comments, "end", out, indent)
        elif isinstance(val, list_type):
            if isinstance(val[0], dict_type):
                # Blocks that are repeted more than once
                comments = dict_comment.get(key, {})
                for iel, el in enumerate(val):
                    _comments = (
                        comments[iel]
                        if isinstance(comments, list_type) and len(comments) >= iel + 1
                        else {}
                    )
                    out += [indent + f"begin {key}"]
                    out = add_comments(_comments, "begin", out, indent + tab_size)
                    out = _encode_htc_file(el, _comments, out, indent + tab_size)
                    out += [indent + f"end {key}"]
                    out = add_comments(_comments, "end", out, indent)
            elif isinstance(val[0], list_type):
                for iel, el in enumerate(val):
                    out += [indent + f"{key} " + " ".join([str(_el) for _el in el])]
                    out = add_comments(dict_comment, key, out, indent, iel)
            else:
                out += [indent + f"{key} " + " ".join([str(_el) for _el in val])]
                out = add_comments(dict_comment, key, out, indent)
        else:
            out += [indent + f"{key} " + str(val)]
            out = add_comments(dict_comment, key, out, indent)
    return out


def get_comments(comment_dict, key):
    return comment_dict.get(key, [])


def add_comments(comment_dict, key, out, indent, index=None):
    comments = get_comments(comment_dict, key)
    if comments and (not index is None):
        if len(comments) > index:
            comments = comments[index]
        else:
            comments = []
    if not comments:
        if len(out) == 0:
            return out
        out[-1] += ";"
        return out
    if "$>tag:" in comments[0]:
        tag, comments[0] = comments[0][6:].split("<$")
        out[-1] = tag + " " + out[-1]
    if len(out) == 0:
        out.append(";" + comments[0])
    else:
        out[-1] += ";" + comments[0]
    for comment in comments[1:]:
        out.append(indent + ";" + comment)
    return out


class recursionlimit_context_manager:
    """Context manager to handle increasing the recursion limit. From:
    https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-and-how-to-increase-it
    """

    def __init__(self, limit):
        self.limit = limit

    def __enter__(self):
        self.old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)


# %% HTC dict and list %% #
class HTC_dict(AESOpt_dict):
    """HAWC2 HTC dict type to interact with HTC dict-like data. Inherits from AESOpt_dict - see that for documentation of all methods."""

    list_merge_id = ["name", "mbdy", "mbdy2"]
    comments = None

    def read_htc(self, filename, exe_path=None, read_comments=True):
        """Read a HTC-file into self.

        Data is being converted depending on 4 different data structures in the HTC-file, namely:

        - **Command**, unique keyword linked with a value that can be `int`, `float`, `str`, `list`.
        - **Repeated Command**, keyword that can be repeated many times. Data is stored as a `list` of `list`'s.
        - **Block**, A set of commands starting with a `begin *keyword*` and `end *keyword*`. Data becomes a `dict` of `dict`'s.
        - **Repeated Block**, similar to a *Block* but can be repeated multiple times. Data becomes a `list` of `dict`'s. Example:

        Using the method `windio_converter.io.hawc2.read_htc_as_dict`

        Parameters
        ----------
        filename : str
            Path/filename
        exe_path : str, optional
            Execution path, used in case the file contains `continue_in_file`, by default "./"
        read_comments : bool, optional
            Flag, `True` means that it will read and add the comments to self, by default True

        Returns
        -------
        self
        """
        htc_dict, htc_comments = read_htc_as_dict(clean_filename(filename), exe_path)
        self.update(htc_dict)
        if read_comments:
            self.add_comment(htc_comments)
        return self

    def add_comment(self, key, comment=None, index=None):
        """Add/Overwrite a comment or comments for the for a specific command/block.

        Besides the commands and blocks keywords an HTC_dict instance can also have a
        `begin` and `end` keyword, which will add comments at the start and end of a block respectively.
        But it is also used to control the comments at the beginning and end of the HTC-file it self.

        Parameters
        ----------
        key : str, dict of list of str
            - str : Name of the command/block which the command needs to be added or overwritten.
            - dict : Dict following the structure of the HTC_dict but setting the command for each commands/block. Used for bulk update.
        comment : str, list of str, None, optional
            - str : Comment to be added/appended for the key. New comments will be added on a new line following the current indent level. If the current last comment is an empty string the comment will overwrite it.
            - list : Overwrite the current comment(s). Multiple comments can also be added.
            - None : Can only be none of key is a dict, (default None)
        index : int, optional
            Index to append the comment for. Only used for repeated comments, by default None

        Returns
        -------
        self

        Raises
        ------
        ValueError
            If `key` is a `str` and comment is `None`. `comment` should be `str` or `list`
        ValueError
            If `key` is a `str` and comment is `None`. `comment` should be `str` or `list`
        """
        if self.comments is None:
            self.comments = dict()
        if isinstance(key, dict_type):
            for name, comment in key.items():
                if isinstance(comment, dict_type):
                    self[name].add_comment(comment)
                elif is_list_of_dict(comment):
                    for i, _comment in enumerate(comment):
                        self[name][i].add_comment(_comment)
                else:
                    self.comments[name] = comment
            return
        if comment is None:
            raise ValueError(
                f"`comment` need to be set when `key` is not a dict/UserDict type (given: key={key}, comment={comment})"
            )
        elif isinstance(comment, list_type):
            if index is None:
                self.comments[key] = comment
            else:
                self.comments[key][index] = comment
        elif isinstance(comment, str):
            if index is None:
                if len(self.comments.get(key, [])) == 0:
                    self.comments[key] = [comment]
                else:
                    if len(self.comments[key][-1]) > 0:
                        self.comments[key].append(comment)
                    else:
                        self.comments[key][-1] = comment
            else:
                if len(self.comments[key][index]) == 0:
                    self.comments[key][index] = [comment]
                else:
                    if len(self.comments[key][index][-1]) > 0:
                        self.comments[key][index].append(comment)
                    else:
                        self.comments[key][index][-1] = comment
        else:
            raise ValueError(
                f"`comment` need to be a list/str type (given: comment={comment})"
            )
        return self

    def from_htc(self, htc_str, exe_path=None, read_comments=True):
        """Read a HTC-file from a string into self.

        Data is being converted depending on 4 different data structures in the HTC-file, namely:

        - **Command**, unique keyword linked with a value that can be `int`, `float`, `str`, `list`.
        - **Repeated Command**, keyword that can be repeated many times. Data is stored as a `list` of `list`'s.
        - **Block**, A set of commands starting with a `begin *keyword*` and `end *keyword*`. Data becomes a `dict` of `dict`'s.
        - **Repeated Block**, similar to a *Block* but can be repeated multiple times. Data becomes a `list` of `dict`'s. Example:

        Using the method `windio_converter.io.hawc2.read_htc_as_dict`

        Parameters
        ----------
        filename : str
            Path/filename
        exe_path : str, optional
            Execution path, used in case the file contains `continue_in_file`, by default "./"
        read_comments : bool, optional
            Flag, `True` means that it will read and add the comments to self, by default True

        Returns
        -------
        self
        """
        self.read_htc(htc_str.split("\n"), exe_path, read_comments)
        return self

    def write_htc(self, filename, with_comments=True):
        """Write the data in self as a HTC-file.

        Using the method `windio_converter.io.hawc2.write_htc_as_file`

        Parameters
        ----------
        filename : str
            Path/filename
        with_comments : bool, optional
            Flag, `True` means that comments will be added to the HTC_file, by default True
        """
        htc_comments = None
        if with_comments:
            htc_comments = self.get_comment()
        write_htc_as_file(filename, self, htc_comments)

    def get_comment(self, key=None):
        """Get a comment or comments for a specific command or block or the whole file.

        Parameters
        ----------
        key : str, None, optional
            - str : Name of the command or block
            - None : Gets all comments as a dict

        Returns
        -------
        list, dict
            - list : if `key` is a command name
            - dict : if `key` is a block name or None

        Raises
        ------
        ValueError
            If `key` is not in comments
        """
        if key is None:
            if self.comments is None:
                return dict()
            htc_comments = self.comments.copy()
            for name, val in self.items():
                if isinstance(val, HTC_dict):
                    htc_comments[name] = val.get_comment()
                elif is_list_of_dict(val):
                    htc_comments[name] = []
                    for el in val:
                        htc_comments[name].append(el.get_comment())
            return htc_comments
        elif self.comments is None:
            return []
        elif key in self.comments:
            return self.comments[key]
        elif isinstance(self.get(key, {}), HTC_dict):
            return self[key].get_comment()
        else:
            raise ValueError(f"{key} is an unknown key in comments")

    def as_htc(self, with_comments=True):
        """Get the data in self as string HTC-file.

        Using the method `windio_converter.io.hawc2.write_htc_as_file`

        Parameters
        ----------
        with_comments : bool, optional
            Flag, `True` means that comments will be added to the HTC_file, by default True

        Returns
        -------
        str
            HTC-file as a string
        """
        htc_str = StringIO()
        self.write_htc(htc_str, with_comments)
        return htc_str.getvalue()

    def __str__(self):
        return self.as_htc()

    def update(self, *args, list_merge_id=None, d_type=None, l_type=None, **kwargs):
        super().update(
            *args, list_merge_id=list_merge_id, d_type=d_type, l_type=l_type, **kwargs
        )
        """Update/merge `self` with `list_update` where items in `list_update` replaces the ones in `self`.

        Data containing `list` of `dict`'s can be merged according to `list_merge_id`.

        If elements in a specific list/array need to be updated it can be done with a `dict` of indices (e.g. `self=[1, 2]` and `list_update={1: 3}` -> `self=[1, 3]`).

        `list_update` can also contain callables (e.g. python object with a `.__call__` method defined or by `def`) where the data at the requested location is passed to the function and the function return is set at the data location (e.g. `self=[1, 2]` and `list_update={1: lambda val: val+5}` -> `self=[1, 7]`). List of numbers are converted to numpy array so math operations are done elementwise.

        When new `list`'s or `dict`'s are added from `list_update` to `list_main` they will be of `l_type` or `d_type` respectively.

        If a dict in `args` is of `HTC_dict` type the comments from it will be added inplace.

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
        for el in args:
            if isinstance(el, HTC_dict):
                self.add_comment(el.get_comment())
        return self


class HTC_list(AESOpt_list):
    """HAWC2 HTC list type to interact with HTC list-like data. Inherits from AESOpt_list - see that for documentation of all methods."""

    list_merge_id = HTC_dict.list_merge_id


def _get_header(file, match_f):
    """Find the location in the file that matches the header. `match_f` is a callable that returns True if header is found."""
    line = next(file)
    if not match_f(line):
        return _get_header(file, match_f)
    return line


# %% Data file lists %% #
class AE_list(AESOpt_list):
    """HAWC2 AE list type to interact with AE list-like data. Inherits from AESOpt_list - see that for documentation of all methods."""

    def __init__(self, list_in=None, list_merge_id=None, d_type=None, l_type=None):
        if isinstance(list_in, (dict, AESOpt_dict)):
            list_in = [list_in]
        if list_in is None:
            super().__init__()
        else:
            super().__init__(list_in, list_merge_id, d_type, l_type)

    # TODO: Add comment reader/writer
    def read_ae(self, filename):
        """Read an AE-file into self.

        Parameters
        ----------
        filename : str
            Path/filename

        Returns
        -------
        self
        """
        with open(clean_filename(filename), "r") as file:
            self.from_ae(file.read())
        return self

    def from_ae(self, ae_str):
        """Read an AE-file from string

        Parameters
        ----------
        ae_str : str
            AE-file string

        Returns
        -------
        self
        """
        file = iter(ae_str.split("\n"))
        nsets = int(next(file).strip().split()[0])
        for iset in range(nsets):
            nrows = int(_get_header(file, self._match_header).strip().split()[1])
            data = np.loadtxt(file, max_rows=nrows, comments=";")
            self.append(
                dict(
                    s=data[:, 0].tolist(),
                    chord=data[:, 1].tolist(),
                    tc=data[:, 2].tolist(),
                    pc_set=data[:, 3].tolist(),
                )
            )
        return self

    def _match_header(self, line):
        """Method to find AE-header"""
        return all(
            [isinstance(_convert_value(val), int) for val in line.strip().split()[:2]]
        )

    def write_ae(self, filename):
        """Write an AE-file from data en self.

        Parameters
        ----------
        filename : str
            Path/filename
        """
        with open(filename, "w") as file:
            file.write(self.as_ae())

    def as_ae(self):
        """Get data in self as AE-file string

        Returns
        -------
        str
            AE-file string
        """
        out = [f"{len(self.data)}"]
        for iset, set in enumerate(self):
            out += [f"{iset+1} {len(set['s'])}"]
            for s, c, tc, pc in zip(set["s"], set["chord"], set["tc"], set["pc_set"]):
                out += [f"  {s}  {c}  {tc} {int(pc)}"]
        return "\n".join(out)

    def __str__(self):
        return self.as_ae()


class PC_list(AESOpt_list):
    """HAWC2 PC list type to interact with PC list-like data. Inherits from AESOpt_list - see that for documentation of all methods."""

    def __init__(self, list_in=None, list_merge_id=None, d_type=None, l_type=None):
        if isinstance(list_in, dict_type):
            list_in = [list_in]
        AESOpt_list.__init__(self, list_in, list_merge_id, d_type, l_type)
        if (
            isinstance(self.data, list_type)
            and len(self.data) > 0
            and isinstance(self.data[0], dict_type)
        ):
            data = PC_list()
            data.append(self.data)
            self.data = data

    def read_pc(self, filename):
        """Read an PC-file into self.

        Parameters
        ----------
        filename : str
            Path/filename

        Returns
        -------
        self
        """
        with open(clean_filename(filename), "r") as file:
            self.from_pc(file.read())
        return self

    def from_pc(self, pc_str):
        """Read an PC-file from string

        Parameters
        ----------
        pc_str : str
            PC-file string

        Returns
        -------
        self
        """
        file = iter(pc_str.split("\n"))
        nsets = int(next(file).strip().split()[0])
        for iset in range(nsets):
            nprof = int(_get_header(file, self._match_profs_header).strip().split()[0])
            self.append([])
            for i in range(nprof):
                header = _get_header(file, self._match_prof_header).strip().split()
                nrows, tc = [int(header[1]), float(header[2])]
                data = np.loadtxt(file, max_rows=nrows)
                self[-1].append(
                    dict(
                        tc=tc,
                        aoa=data[:, 0].tolist(),
                        c_l=data[:, 1].tolist(),
                        c_d=data[:, 2].tolist(),
                        c_m=data[:, 3].tolist(),
                    )
                )
        return self

    def _match_profs_header(self, line):
        """Method for matching set header in airfoil profile header"""
        return isinstance(_convert_value(line.strip().split()[0]), int)

    def _match_prof_header(self, line):
        """Method for matching airfoil profil"""
        vals = [_convert_value(val) for val in line.strip().split()[:3]]
        return all(
            [
                isinstance(vals[0], int),
                isinstance(vals[1], int),
                isinstance(vals[2], (int, float)),
            ]
        )

    def as_pc(self):
        """Get data in self as PC-file string

        Returns
        -------
        str
            PC-file string
        """
        if not isinstance(self.data[0], list_type):
            data = [self.data]
        else:
            data = self.data
        out = [f"{len(data)}"]
        for iset, set in enumerate(data):
            out += [f"{len(set)}"]
            for iprof, prof in enumerate(set, 1):
                out += [f"{iprof} {len(prof['aoa'])} {prof['tc']}"]
                for aoa, cl, cd, cm in zip(
                    prof["aoa"], prof["c_l"], prof["c_d"], prof["c_m"]
                ):
                    out += [f"  {aoa}  {cl}  {cd} {cm}"]
        return "\n".join(out)

    def write_pc(self, filename):
        """Write an PC-file from data en self.

        Parameters
        ----------
        filename : str
            Path/filename
        """
        with open(filename, "w") as file:
            file.write(self.as_pc())

    def __str__(self):
        return self.as_pc()


class ST_list(AESOpt_list):
    """HAWC2 ST list type to interact with ST list-like data. Inherits from AESOpt_list - see that for documentation of all methods."""

    def __init__(self, list_in=None, list_merge_id=None, d_type=None, l_type=None):
        if isinstance(list_in, dict_type):
            list_in = [list_in]
        AESOpt_list.__init__(self, list_in, list_merge_id, d_type, l_type)
        if (
            isinstance(self.data, list_type)
            and len(self.data) > 0
            and isinstance(self.data[0], dict_type)
        ):
            data = ST_list()
            data.append(self.data)
            self.data = data

    def read_st(self, filename):
        """Read an ST-file into self.

        Parameters
        ----------
        filename : str
            Path/filename

        Returns
        -------
        self
        """
        with open(clean_filename(filename), "r") as file:
            self.from_st(file.read())
        return self

    def from_st(self, st_str):
        """Read an ST-file from string

        Parameters
        ----------
        st_str : str
            ST-file string

        Returns
        -------
        self
        """
        file = iter(st_str.split("\n"))
        iset = 0
        subset = 1
        self.append([])
        while subset > 0:
            try:
                header = _get_header(file, self._match_subset_header).strip().split()
                _subset = int(header[0][1:])
                if _subset < subset:
                    iset += 1
                    self.append([])
                subset = _subset
                nrows = int(header[1])
                data = np.loadtxt(file, max_rows=nrows)
                out = dict()
                header = (
                    self.header_FPM() if data.shape[1] == 30 else self.header_classic()
                )
                for name, vals in zip(header, data.T):
                    out[name] = vals.tolist()
                self[-1].append(out)
            except StopIteration:
                subset = 0
        return self

    @staticmethod
    def header_FPM():
        """Header for FPM ST-file"""
        return [
            "s",
            "m",
            "x_cg",
            "y_cg",
            "ri_x",
            "ri_y",
            "pitch",
            "xe",
            "ye",
            "K11",
            "K12",
            "K13",
            "K14",
            "K15",
            "K16",
            "K22",
            "K23",
            "K24",
            "K25",
            "K26",
            "K33",
            "K34",
            "K35",
            "K36",
            "K44",
            "K45",
            "K46",
            "K55",
            "K56",
            "K66",
        ]

    @staticmethod
    def header_classic():
        """Header for classic ST-file"""
        return [
            "s",
            "m",
            "x_cg",
            "y_cg",
            "ri_x",
            "ri_y",
            "x_sh",
            "y_sh",
            "E",
            "G",
            "Ix",
            "Iy",
            "K",
            "kx",
            "ky",
            "A",
            "pitch",
            "xe",
            "ye",
        ]

    def _match_subset_header(self, line):
        """Method for matching ST subset"""
        out = line.strip().split()[:2]
        return (
            (len(out) > 1)
            and (len(out[0]) > 1)
            and (out[0][0] == "$")
            and isinstance(_convert_value(out[0][1:]), int)
            and isinstance(_convert_value(out[1]), int)
        )

    def as_st(self):
        """Get data in self as ST-file string

        Returns
        -------
        str
            ST-file string
        """
        out = [f"{len(self)}"]
        for iset, set in enumerate(self):
            out += [f"#{iset+1}"]
            for isubset, subset in enumerate(set, 1):
                ns = len(subset["s"])
                out += [f"${isubset} {ns}"]
                names = self.header_FPM() if "K11" in subset else self.header_classic()
                for i in range(ns):
                    out += [
                        "  " + "  ".join([f"{subset[name][i]:1.15e}" for name in names])
                    ]
        return "\n".join(out)

    def write_st(self, filename):
        """Write an ST-file from data en self.

        Parameters
        ----------
        filename : str
            Path/filename
        """
        with open(filename, "w") as file:
            file.write(self.as_st())

    def __str__(self):
        return self.as_st()


class OPT_dict(AESOpt_dict):
    """HAWC2 OPT dict type to interact with OPT dict-like data. Inherits from AESOpt_dict - see that for documentation of all methods."""

    def read_opt(self, filename):
        """Read an OPT-file into self.

        Parameters
        ----------
        filename : str
            Path/filename

        Returns
        -------
        self
        """
        with open(filename, "r") as file:
            data = np.loadtxt(file, skiprows=1)

        self["V0"] = data[:, 0].tolist()
        self["pitch"] = data[:, 1].tolist()
        self["rotor_speed"] = data[:, 2].tolist()
        if data.shape[1] > 3:
            self["P"] = data[:, 3].tolist()
            self["T"] = data[:, 4].tolist()
        return self

    def write_opt(self, filename):
        """Write an OPT-file from data en self.

        Parameters
        ----------
        filename : str
            Path/filename
        """
        out = [f"{len(self['V0'])} wind speed [m/s]    pitch [deg]    rot. speed [rpm]"]
        if "P" in self:
            out[0] += "    aero power [kw]    aero thrust [kn]"
        for iV0, (V0, p, rs) in enumerate(
            zip(self["V0"], self["pitch"], self["rotor_speed"])
        ):
            out += [f"{V0}    {p}    {rs}"]
            if "P" in self:
                out[-1] += f"    {self['P'][iV0]}    {self['T'][iV0]}"

        with open(filename, "w") as file:
            file.write("\n".join(out))
        return self


# %% Read full HAWC2 model %% #
class HAWC2_dict(AESOpt_dict):
    """HAWC2 dict type to interact with a full HAWC2 dict-like data (HTC-, AE-, PC-. ST-, OPT-files) Inherits from AESOpt_dict - see that for documentation of all methods."""

    list_merge_id = ["name", "mbdy", "mbdy2"]

    def read_hawc2(self, path, htc_path):
        """Reads a full HAWC2 model (HTC-, AE-, PC-. ST-, OPT-files).

        All files are read using the their respective reader. After reading the model the HAWC2_dict will contain:

        - `htc` : HTC-data (using `HTC_dict`)
        - `htc_filename` : The HTC-filename. Same as when reading the file, if not changed.
        - `ae` : AE-data (using `AE_list`). Filename from HTC-data.
        - `pc` : PC-data (using `PC_list`). Filename from HTC-data.
        - `st` : ST-data for each of the `main_body`'s where the ST-data for each of the bodies is stored by its `main_body.name` (using `ST_list`).
        - `opt` : OPT-data if `hawcstab2` block and OPT-filename is present (using `OPT_dict`).

        Parameters
        ----------
        path : str
            Execution path for the HAWC2 model.
        htc_path : str
            Relative path/filename for the HTC-file

        Returns
        -------
        self
        """
        self["htc"] = HTC_dict().read_htc(os.path.join(path, htc_path), path)
        self["htc_filename"] = htc_path
        fname_ae = self["htc"]["aero"]["ae_filename"]
        fname_pc = self["htc"]["aero"]["pc_filename"]
        fname_sts = jmespath.search(
            "new_htc_structure.main_body[*][name, timoschenko_input.filename]",
            self["htc"].as_dict(),
        )
        self["ae"] = AE_list().read_ae(os.path.join(path, fname_ae))
        self["pc"] = PC_list().read_pc(os.path.join(path, fname_pc))
        self["st"] = HAWC2_dict()
        for [mbdy_name, fname_st] in fname_sts:
            if fname_st is not None:
                self["st"][mbdy_name] = ST_list().read_st(os.path.join(path, fname_st))
        if (
            "hawcstab2" in self["htc"]
            and "operational_data_filename" in self["htc"]["hawcstab2"]
        ):
            fname_opt = self["htc"]["hawcstab2"]["operational_data_filename"]
            self["opt"] = OPT_dict().read_opt(os.path.join(path, fname_opt))
        return self

    def write_hawc2(self, path):
        """Write the HAWC2 model to file.

        Filenames for each of the files can be modified in the `htc_filename` or in related HTC-data (e.g. `aero.ae_filename`, `aero.pc_filename`)

        Parameters
        ----------
        path : str
            Execution path for the HAWC2 model
        """
        if not isinstance(self["htc"], HTC_dict):
            self["htc"] = HTC_dict(**self["htc"])
        self["htc"].write_htc(
            self._create_path(os.path.join(path, self["htc_filename"]))
        )
        if "ae" in self.data:
            if not isinstance(self["ae"], AE_list):
                self["ae"] = AE_list(self["ae"])
            self["ae"].write_ae(
                self._create_path(
                    os.path.join(path, self["htc"]["aero"]["ae_filename"])
                )
            )
        if "pc" in self.data:
            if not isinstance(self["pc"], PC_list):
                self["pc"] = PC_list(self["pc"])
            self["pc"].write_pc(
                self._create_path(
                    os.path.join(path, self["htc"]["aero"]["pc_filename"])
                )
            )
        if "st" in self.data:
            fname_sts = jmespath.search(
                "new_htc_structure.main_body[*][name, timoschenko_input.filename]",
                self["htc"].as_dict(),
            )
            for [mbdy_name, fname_st] in fname_sts:
                if fname_st is not None:
                    st = self["st"][mbdy_name]
                    if not isinstance(st, ST_list):
                        st = ST_list(st)
                    st.write_st(self._create_path(os.path.join(path, fname_st)))
        if "opt" in self.data:
            fname_opt = self["htc"]["hawcstab2"]["operational_data_filename"]
            if not isinstance(self["opt"], OPT_dict):
                self["opt"] = OPT_dict(self["opt"])
            self["opt"].write_opt(self._create_path(os.path.join(path, fname_opt)))

    def _create_path(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    def get_hawc2_cases(self, hawc2_update_list_of_dict):
        """Creates a list of cases from the current self instance where each case is updated based on the `dict_update` from `hawc2_update_list_of_dict`.

        Each dict in the `hawc2_update_list_of_dict` is applied with the `.update` method.

        Parameters
        ----------
        hawc2_update_list_of_dict : list of hawc2 dict's
            List of update dict's to be applied for each of the cases.

        Returns
        -------
        list of HAWC2_dict's
        """
        cases = []
        for case in hawc2_update_list_of_dict:
            cases.append(self.copy().update(case))
        return cases

    def write_hawc2_cases(
        self, hawc2_update_list_of_dict, case_path="case%d", base_path="./"
    ):
        """Creates a list of cases from the current self instance where each case is updated based on the `dict_update` from `hawc2_update_list_of_dict`.

        Each dict in the `hawc2_update_list_of_dict` is applied with the `.update` method.

        The case_path can be overwritten by adding `case_path` for each of the `dict_update`

        Parameters
        ----------
        hawc2_update_list_of_dict : list of hawc2 dict's
            List of update dict's to be applied for each of the cases.
        case_path : str, optional
            The base case path, used a the path for each case where %d is replaced with the case index, by default "case%d"
        base_path : str, optional
            Path for writing the cases, by default "./"
        """
        cases = self.get_hawc2_cases(hawc2_update_list_of_dict)
        for icase, case in enumerate(cases, 1):
            full_case_path = os.path.join(
                base_path, case.get("case_path", case_path % (icase))
            )
            case.write_hawc2(full_case_path)

    def update(self, *args, list_merge_id=None, d_type=None, l_type=None, **kwargs):
        """Update/merge `self` with `list_update` where items in `list_update` replaces the ones in `self`.

        Data containing `list` of `dict`'s can be merged according to `list_merge_id`.

        If elements in a specific list/array need to be updated it can be done with a `dict` of indices (e.g. `self=[1, 2]` and `list_update={1: 3}` -> `self=[1, 3]`).

        `list_update` can also contain callables (e.g. python object with a `.__call__` method defined or by `def`) where the data at the requested location is passed to the function and the function return is set at the data location (e.g. `self=[1, 2]` and `list_update={1: lambda val: val+5}` -> `self=[1, 7]`). List of numbers are converted to numpy array so math operations are done elementwise.

        When new `list`'s or `dict`'s are added from `list_update` to `list_main` they will be of `l_type` or `d_type` respectively.

        If `args` or `kwargs` contains a `HTC_dict` the comments from it will be added inplace.

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
        for el in args + (kwargs,):
            for name, val in el.items():
                if name == "htc":
                    self["htc"] = self.setdefault("htc", HTC_dict()).update(
                        val,
                        list_merge_id=list_merge_id,
                        d_type=HTC_dict,
                        l_type=HTC_list,
                    )
                elif name == "ae":
                    self["ae"] = self.setdefault("ae", AE_list()).update(
                        val, list_merge_id=list_merge_id, d_type=d_type, l_type=AE_list
                    )
                elif name == "pc":
                    self["pc"] = self.setdefault("pc", PC_list()).update(
                        val, list_merge_id=list_merge_id, d_type=d_type, l_type=PC_list
                    )
                elif name == "opt":
                    self["opt"] = self.setdefault("opt", OPT_dict()).update(
                        val, list_merge_id=list_merge_id, d_type=OPT_dict, l_type=l_type
                    )
                else:
                    super().update(
                        list_merge_id=None, d_type=None, l_type=None, **{name: val}
                    )

        if "st" in self:
            for name in self["st"].keys():
                if not isinstance(self["st"][name], ST_list):
                    self["st"][name] = ST_list(self["st"][name])
        return self


def clean_filename(filename):
    """Replace path seperators on posix systems (linux, mac) with front slash (\\->/)"""
    if not isinstance(filename, str):
        return filename
    if os.name == "posix":
        return filename.replace("\\", "/")
    return filename  # pragma: no cover
