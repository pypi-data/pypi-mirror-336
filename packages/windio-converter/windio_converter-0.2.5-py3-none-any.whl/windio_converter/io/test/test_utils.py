import copy
import unittest

import numpy as np
import pytest

from windio_converter.io import utils
from windio_converter.io.aesopt import AESOpt_dict, AESOpt_list

dummytestcase = unittest.TestCase()


def as_dict(dict_in):
    if hasattr(dict_in, "as_dict"):
        return dict_in.as_dict()
    return dict_in


def contain_same_dict(d1, d2):
    for key, val in d1.items():
        if isinstance(val, utils.dict_type):
            val2 = as_dict(d2[key])
            dummytestcase.assertDictEqual(val, val2)
        elif isinstance(val, utils.list_type) and isinstance(val[0], utils.dict_type):
            for el1, el2 in zip(val, d2[key]):
                contain_same_dict(el1, el2)
        else:
            np.testing.assert_array_equal(val, d2[key])


def contain_same_list(l1, l2):
    for val1, val2 in zip(l1, l2):
        if isinstance(val1, utils.dict_type):
            dummytestcase.assertDictEqual(as_dict(val1), as_dict(val2))
        elif isinstance(val1, utils.list_type) and isinstance(val1[0], utils.dict_type):
            for el1, el2 in zip(val1, val2):
                contain_same_dict(el1, el2)
        else:
            np.testing.assert_equal(val1, val2)


def test_update_list():
    # Testing for both build-in list/dict and UserList/UserDict
    for l_obj, d_obj in [
        (lambda obj: obj, dict),
        (AESOpt_list, AESOpt_dict),
    ]:
        ## Update single level list
        # Simple overwrite
        d1 = l_obj([1, 2, 3])
        d2 = l_obj([4, 5, 6])
        dout = utils.update_list(d1, d2)
        assert dout == d2
        # Single element update
        d1 = l_obj([1, 2, 3])
        d2 = d_obj({1: -2, -1: None})
        dout = utils.update_list(d1, d2)
        assert dout == [1, -2]
        # Callable (array)
        d1 = l_obj([1, 2, 3])
        d2 = lambda arr: arr * 5
        dout = utils.update_list(d1, d2).tolist()
        assert dout == [1 * 5, 2 * 5, 3 * 5]
        # Callable (element)
        d1 = l_obj([1, 2, 3])
        d2 = d_obj({1: lambda arr: arr * 5})
        dout = utils.update_list(d1, d2)
        assert dout == [1, 2 * 5, 3]

        # Callable (non numeric)
        def mod_list(list_in):
            assert not isinstance(list_in, np.ndarray)
            list_in[1] = "updated"
            return list_in

        d1 = l_obj([1, "test", 3])
        d2 = mod_list
        dout = utils.update_list(d1, d2)
        assert dout == [1, "updated", 3]
        ## Update nested lists
        # Simple update (same size)
        d1 = l_obj([[1, 2, 3], [4, 5, 6]])
        d2 = l_obj([[7, 8, 9], [10, 11, 12]])
        dout = utils.update_list(d1, d2)
        assert dout == d2
        # Simple update (different size)
        d1 = l_obj([[1, 2, 3], [4, 5, 6]])
        d2 = l_obj([[7, 8, 9], [10, 11, 12], [13, 14, 15, 16]])
        dout = utils.update_list(d1, d2)
        assert dout == d2
        d1 = l_obj([[1, 2, 3], [4, 5, 6]])
        d2 = l_obj([[7, 8, 9], [10, 11, 12], [13, 14, 15, 16]])
        dout = utils.update_list(d2, d1)
        assert dout == d1
        # With dict selection
        d1 = l_obj([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        d2 = {1: {-1: 10}, -1: {1: -8}, 0: None}
        dout = utils.update_list(d1, d2)
        assert dout == [[4, 5, 10], [7, -8, 9]]

        # With callable (list)
        def mod_arr(arr):
            arr[1] *= 5
            return arr

        d1 = l_obj([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        d2 = d_obj({0: mod_arr, 1: lambda arr: arr * 6, 2: None})
        dout = np.asarray(utils.update_list(d1, d2)).tolist()
        assert dout == [[1, 2 * 5, 3], [4 * 6, 5 * 6, 6 * 6]]
        # With callable (dict)
        d1 = l_obj([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        d2 = {1: mod_arr, -1: lambda arr: 5 * arr}
        dout = np.asarray(utils.update_list(d1, d2)).tolist()
        assert dout == [[1, 2, 3], [4, 5 * 5, 6], [7 * 5, 8 * 5, 9 * 5]]

        ## Update list of dicts
        # Merge by "name" (default)
        d1 = l_obj(
            [
                d_obj(
                    name="x", dummy1=5, dummy2="test2", dummy3=[[1, 2, 3], [4, 5, 6]]
                ),
                d_obj(
                    name="y", dummy1=6, dummy2="test2", dummy3=[[1, 2, 3], [4, 5, 6]]
                ),
            ]
        )
        d2 = l_obj([d_obj(name="y", dummy1=10), d_obj(name="x", dummy2="updated")])
        dout = utils.update_list(d1, d2)
        contain_same_list(
            dout,
            [
                d_obj(
                    name="x", dummy1=5, dummy2="updated", dummy3=[[1, 2, 3], [4, 5, 6]]
                ),
                d_obj(
                    name="y", dummy1=10, dummy2="test2", dummy3=[[1, 2, 3], [4, 5, 6]]
                ),
            ],
        )
        # Merge by another name
        d1 = l_obj(
            [
                d_obj(
                    not_name="x",
                    dummy1=5,
                    dummy2="test2",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
                d_obj(
                    not_name="y",
                    dummy1=6,
                    dummy2="test2",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
            ]
        )
        d2 = l_obj(
            [d_obj(not_name="y", dummy1=10), d_obj(not_name="x", dummy2="updated")]
        )
        dout = utils.update_list(d1, d2, ["not_name"])
        contain_same_list(
            dout,
            [
                dict(
                    not_name="x",
                    dummy1=5,
                    dummy2="updated",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
                dict(
                    not_name="y",
                    dummy1=10,
                    dummy2="test2",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
            ],
        )
        # Merge by multiple names
        d1 = l_obj(
            [
                d_obj(
                    name="x", dummy1=5, dummy2="test2", dummy3=[[1, 2, 3], [4, 5, 6]]
                ),
                d_obj(
                    not_name="y",
                    dummy1=6,
                    dummy2="test2",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
                d_obj(
                    mbdy="z", dummy1=6, dummy2="test3", dummy3=[[1, 2, 3], [4, 5, 6]]
                ),
            ]
        )
        d2 = l_obj(
            [
                d_obj(not_name="y", dummy1=10),
                d_obj(mbdy="z", dummy1=-10),
                d_obj(name="x", dummy2="updated"),
            ]
        )
        dout = utils.update_list(d1, d2, ["name", "not_name", "mbdy"])
        contain_same_list(
            dout,
            [
                dict(
                    name="x", dummy1=5, dummy2="updated", dummy3=[[1, 2, 3], [4, 5, 6]]
                ),
                dict(
                    not_name="y",
                    dummy1=10,
                    dummy2="test2",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
                dict(
                    mbdy="z", dummy1=-10, dummy2="test3", dummy3=[[1, 2, 3], [4, 5, 6]]
                ),
            ],
        )
        # Merge by multiple names with non-string values
        d1 = l_obj(
            [
                d_obj(
                    name=("x", 1),
                    dummy1=5,
                    dummy2="test2",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
                d_obj(
                    not_name=("y", 2),
                    dummy1=6,
                    dummy2="test2",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
                d_obj(
                    mbdy=("z", 3),
                    dummy1=6,
                    dummy2="test3",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
            ]
        )
        d2 = l_obj(
            [
                d_obj(not_name=("y", 2), dummy1=10),
                d_obj(mbdy=("z", 3), dummy1=-10),
                d_obj(name=("x", 1), dummy2="updated"),
            ]
        )
        dout = utils.update_list(d1, d2, ["name", "not_name", "mbdy"])
        contain_same_list(
            dout,
            [
                dict(
                    name=("x", 1),
                    dummy1=5,
                    dummy2="updated",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
                dict(
                    not_name=("y", 2),
                    dummy1=10,
                    dummy2="test2",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
                dict(
                    mbdy=("z", 3),
                    dummy1=-10,
                    dummy2="test3",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
            ],
        )
        # Cast dict with list_merge_id to list of dict
        d1 = d_obj(name="y", dummy1=6, dummy2="test2", dummy3=[[1, 2, 3], [4, 5, 6]])
        d2 = l_obj([d_obj(name="y", dummy1=10)])
        dout = utils.update_list(d1, d2)
        contain_same_list(
            dout,
            [d_obj(name="y", dummy1=10, dummy2="test2", dummy3=[[1, 2, 3], [4, 5, 6]])],
        )
        # Overwrite list of dict (no merge id)
        d1 = l_obj(
            [
                d_obj(
                    name="x", dummy1=5, dummy2="test2", dummy3=[[1, 2, 3], [4, 5, 6]]
                ),
                d_obj(
                    not_name="y",
                    dummy1=6,
                    dummy2="test2",
                    dummy3=[[1, 2, 3], [4, 5, 6]],
                ),
                d_obj(
                    mbdy="z", dummy1=6, dummy2="test3", dummy3=[[1, 2, 3], [4, 5, 6]]
                ),
            ]
        )
        d2 = l_obj(
            [
                d_obj(not_name="y", dummy1=10),
                d_obj(mbdy="z", dummy1=-10),
                d_obj(name="x", dummy2="updated"),
            ]
        )
        dout = utils.update_list(d1, d2, "not an ID")
        contain_same_list(dout, d2)
        # Overwrite list of dict (with merge id but not in data)
    # Raises
    # Incorrect merge ID
    with pytest.raises(ValueError) as exc_info:
        utils.update_list(d1, d2, 5)
    assert "list_merge_id" in exc_info.value.args[0]
    with pytest.raises(ValueError) as exc_info:
        utils.update_list(d1, d2, [["name"]])
    assert "list_merge_id" in exc_info.value.args[0]
    # Wrong input type
    with pytest.raises(ValueError) as exc_info:
        utils.update_list(object(), d2)
    assert "type(list_main)" in exc_info.value.args[0]
    with pytest.raises(ValueError) as exc_info:
        utils.update_list(d1, object())
    assert "type(list_update)" in exc_info.value.args[0]
    # Non-homogenous list of list
    with pytest.raises(ValueError) as exc_info:
        utils.update_list([[5, 2], 4, "test"], d2)
    assert "list are lists" in exc_info.value.args[0]
    # Non-homogenous list of dict
    with pytest.raises(ValueError) as exc_info:
        utils.update_list([{1: 2, 3: 4}, 5, "test"], d2)
    assert "list are dicts" in exc_info.value.args[0]


def test_update_dict():
    def mod_list(list_in):
        assert not isinstance(list_in, np.ndarray)
        list_in[1] = "updated"
        return list_in

    def mod_array(arr):
        return (arr * 5).tolist()

    for l_obj, d_obj in [
        (lambda obj: obj, dict),
        (AESOpt_list, AESOpt_dict),
    ]:
        base = d_obj(
            x1=1,  # Value
            x2=l_obj([1, 2, 3]),  # Numeric list
            x3=l_obj([1, "test", 5]),  # Non-numeric list
            x4=np.array([1, 2.5, 5.0]),  # numpy array
            x5=l_obj(  # List of dicts
                [
                    d_obj(
                        name_="1",
                        y1=2,
                        y2=l_obj([1, 2, 3]),
                        y3=l_obj([1, "test", 5.0]),
                        y4=np.array([1, 2.5, 5.0]),
                    ),
                    d_obj(
                        name_="2",
                        y1=2,
                        y2=l_obj([1, 2, 3]),
                        y3=l_obj([1, "test", 5.0]),
                        y4=[1, 2.5, 5.0],
                    ),
                ]
            ),
            x6=l_obj(  # List of lists
                [l_obj([1, 2, 3]), l_obj([4, "test", 5]), [1, 2.5, 5.0]]
            ),
            x7=d_obj(z1=5, z2=[1, 2, 3], z3=d_obj(a1=6, a2=[4, 5, 6])),  # Nested dict
        )
        d1 = copy.deepcopy(base)
        d2 = d_obj(
            x1=2,
            x2=mod_array,
            x3=mod_list,
            x4=None,
            x5=[d_obj(name_="2", y1=4, y5="new")],
            x6={0: mod_array, 1: mod_list, 2: None},
            x7=d_obj(z1=6, z2=mod_array, z3=d_obj(a1=0, a3=3), z4=2),
        )
        dout = utils._update_dict(d1, d2, "name_")
        dnew = copy.deepcopy(base)
        dnew["x1"] = 2
        dnew["x2"] = [1 * 5, 2 * 5, 3 * 5]
        dnew["x3"] = [1, "updated", 5]
        dnew.pop("x4")
        dnew["x5"][1]["y1"] = 4
        dnew["x5"][1]["y5"] = "new"
        dnew["x6"] = [[1 * 5, 2 * 5, 3 * 5], [4, "updated", 5]]
        dnew["x7"]["z1"] = 6
        dnew["x7"]["z2"] = [1 * 5, 2 * 5, 3 * 5]
        dnew["x7"]["z3"]["a1"] = 0
        dnew["x7"]["z3"]["a3"] = 3
        dnew["x7"]["z4"] = 2
        if d_obj == dict:
            contain_same_dict(dout, dnew)
        else:
            contain_same_dict(dout.as_dict(), dnew.as_dict())
        # Overwrite list of dicts
        d1 = copy.deepcopy(base)
        dout = utils._update_dict(d1, d2)
        dnew["x5"] = d2["x5"]
        if d_obj == dict:
            contain_same_dict(dout, dnew)
        else:
            contain_same_dict(dout.as_dict(), dnew.as_dict())
        # Update with list of list's with [[key1, val],[key2, val], ..]
        dout = utils.update_dict(
            d1, l_obj([l_obj(["x1", 2]), l_obj(["x2", l_obj([4, 5, 6])])])
        )
        assert dout["x1"] == 2
        assert dout["x2"] == [4, 5, 6]
    ## Raises
    with pytest.raises(ValueError) as exc_info:
        utils._update_dict(object(), d2)
    assert "type(dict_main)" in exc_info.value.args[0]
    with pytest.raises(ValueError) as exc_info:
        utils._update_dict(d1, object())
    assert "type(dict_update)" in exc_info.value.args[0]
    # Incorrect merge ID
    with pytest.raises(ValueError) as exc_info:
        utils._update_dict(d1, d2, 5)
    assert "list_merge_id" in exc_info.value.args[0]
    with pytest.raises(ValueError) as exc_info:
        utils._update_dict(d1, d2, [["name"]])
    assert "list_merge_id" in exc_info.value.args[0]


def test_path_to_X():
    path = "name1.name2.name3[0].name4[-1][+10]"
    # Path to Path-list
    path_list = utils.path_to_path_list(path)
    assert path_list == ["name1", "name2", "name3", 0, "name4", -1, 10]
    path_list = utils.path_to_path_list("name[0]")
    assert path_list == ["name", 0]
    path_list = utils.path_to_path_list("name")
    assert path_list == ["name"]
    path_list = utils.path_to_path_list("[0]")
    assert path_list == [0]

    # Path-list to dict
    path_list = utils.path_to_path_list(path)
    dict_out = utils.path_list_to_dict(path_list)
    contain_same_dict(
        dict_out, {"name1": {"name2": {"name3": {0: {"name4": {-1: {10: None}}}}}}}
    )
    dict_out = utils.path_list_to_dict(path_list, 5)
    contain_same_dict(
        dict_out, {"name1": {"name2": {"name3": {0: {"name4": {-1: {10: 5}}}}}}}
    )
    # Path to dict
    dict_out = utils.path_to_dict(path)
    contain_same_dict(
        dict_out, {"name1": {"name2": {"name3": {0: {"name4": {-1: {10: None}}}}}}}
    )
    dict_out = utils.path_to_dict(path, 5)
    contain_same_dict(
        dict_out, {"name1": {"name2": {"name3": {0: {"name4": {-1: {10: 5}}}}}}}
    )
    # Path to value
    value = utils.path_to_value(dict_out, "name1.name2.name3[0].name4[-1][10]")
    assert value == 5
    # Raises
    with pytest.raises(ValueError) as exc_info:
        utils.path_to_path_list("name1.name2[name3]")
    assert "Indices need to integers: index=name3" in exc_info.value.args[0]


def test_update_path_in_dict():
    # With nothing else
    dict_in = {
        "name1.name2.name3[0].name4[0][10]": 5,
    }
    dict_out = utils.update_path_in_dict(dict_in)
    contain_same_dict(
        dict_out, {"name1": {"name2": {"name3": {0: {"name4": {0: {10: 5}}}}}}}
    )
    # With values
    dict_in = {
        "name1.name2.name3[0].name4[0][10]": 5,
        "name1": {
            "name2": {
                "name3": {
                    0: {"name4": {0: {0: 2, 10: 7}, 1: 5}, "another_name4": 4},
                    1: 4,
                }
            },
            "another_name3": 3,
        },
    }
    dict_out = utils.update_path_in_dict(dict_in)
    contain_same_dict(
        dict_out,
        {
            "name1": {
                "name2": {
                    "name3": {
                        0: {"name4": {0: {0: 2, 10: 5}, 1: 5}, "another_name4": 4},
                        1: 4,
                    }
                },
                "another_name3": 3,
            }
        },
    )
    # Composit data
    dict_in = {
        "name0": {"name1.name2.name3[0].name4[0][10]": 5},
        "list_dict": [
            {"name1": 1},
            {"name1.name2.name3[0].name4[0][10]": 5},
            {"name1": 2},
        ],
    }
    dict_out = utils.update_path_in_dict(dict_in)
    contain_same_dict(
        dict_out,
        {
            "name0": {"name1": {"name2": {"name3": {0: {"name4": {0: {10: 5}}}}}}},
            "list_dict": [
                {"name1": 1},
                {"name1": {"name2": {"name3": {0: {"name4": {0: {10: 5}}}}}}},
                {"name1": 2},
            ],
        },
    )
