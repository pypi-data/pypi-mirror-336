import os
from copy import deepcopy
from io import StringIO

import numpy as np
import pytest

from windio_converter.io import aesopt
from windio_converter.io.test.test_utils import contain_same_dict, contain_same_list
from windio_converter.test import test_path

dict_in = dict(
    a=5,
    b="test",
    c=[3, "test", 4.0],
    d=dict(a=5, b="test", c=[3, "test", 4.0]),
    e=[[1, "test1", 4.0], [2, "test2", 5.0]],
    f=[dict(a=1, b="test1", c=4.0), dict(a=2, b="test2", c=5.0)],
)


def get_dict():
    return deepcopy(dict_in)


def contain_same_dict_instance(d1, d2, test_dict=True):
    if test_dict:
        np.testing.assert_equal(type(d1), type(d2))
    for key, val in d1.items():
        if isinstance(val, dict):
            if test_dict:
                contain_same_dict_instance(val, d2[key], test_dict)
            else:
                continue
        elif isinstance(val, list):
            contain_same_list_instance(val, d2[key], test_dict)
        np.testing.assert_equal(type(val), type(d2[key]))


def contain_same_list_instance(l1, l2, test_dict=True):
    np.testing.assert_equal(type(l1), type(l2))
    for val1, val2 in zip(l1, l2):
        if isinstance(val1, dict):
            if test_dict:
                contain_same_dict_instance(val1, val2)
            else:
                continue
        elif isinstance(val1, list):
            contain_same_list_instance(val1, val2)
        np.testing.assert_equal(type(val1), type(val2))


def test_dl_type_conversion():
    # Default
    aopt_dict = aesopt.AESOpt_dict(**get_dict())
    assert isinstance(aopt_dict["c"], aesopt.AESOpt_list)
    assert isinstance(aopt_dict["d"], aesopt.AESOpt_dict)
    assert isinstance(aopt_dict["d"]["c"], aesopt.AESOpt_list)
    assert isinstance(aopt_dict["e"], aesopt.AESOpt_list)
    assert isinstance(aopt_dict["f"], aesopt.AESOpt_list)
    for el in aopt_dict["f"]:
        assert isinstance(el, aesopt.AESOpt_dict)

    # Build in dict
    aopt_dict = aesopt.AESOpt_dict(**get_dict(), d_type=dict)
    assert isinstance(aopt_dict["c"], aesopt.AESOpt_list)
    assert isinstance(aopt_dict["d"], dict)
    assert isinstance(aopt_dict["d"]["c"], aesopt.AESOpt_list)
    assert isinstance(aopt_dict["e"], aesopt.AESOpt_list)
    assert isinstance(aopt_dict["f"], aesopt.AESOpt_list)
    for el in aopt_dict["f"]:
        assert isinstance(el, dict)

    # Build in list
    aopt_dict = aesopt.AESOpt_dict(**get_dict(), l_type=list)
    assert isinstance(aopt_dict["c"], list)
    assert isinstance(aopt_dict["d"], aesopt.AESOpt_dict)
    assert isinstance(aopt_dict["d"]["c"], list)
    assert isinstance(aopt_dict["e"], list)
    assert isinstance(aopt_dict["f"], list)
    for el in aopt_dict["f"]:
        assert isinstance(el, aesopt.AESOpt_dict)

    # Both dict and list
    aopt_dict = aesopt.AESOpt_dict(**get_dict(), d_type=dict, l_type=list)
    assert isinstance(aopt_dict["c"], list)
    assert isinstance(aopt_dict["d"], dict)
    assert isinstance(aopt_dict["d"]["c"], list)
    assert isinstance(aopt_dict["e"], list)
    assert isinstance(aopt_dict["f"], list)
    for el in aopt_dict["f"]:
        assert isinstance(el, dict)


def test_equal_to_dict():
    # Different initialization methods
    for i in range(3):
        if i == 0:
            aopt_dict = aesopt.AESOpt_dict(**get_dict())
        elif i == 1:
            aopt_dict = aesopt.AESOpt_dict(get_dict())
        elif i == 2:
            aopt_dict = aesopt.AESOpt_dict().from_dict(get_dict())
        # Iter methods
        contain_same_list(get_dict().keys(), aopt_dict.keys())
        contain_same_list(get_dict().values(), aopt_dict.values())
        np.testing.assert_equal(len(get_dict().items()), len(aopt_dict.items()))
        for key1, key2 in zip(get_dict(), aopt_dict):
            assert key1 == key2

        # As Item
        assert aopt_dict["c"] == dict_in["c"]

        # If in works
        assert "c" in aopt_dict

        # Should fail
        with pytest.raises(AssertionError):
            assert "x" in aopt_dict

        # Dynamically add values that are not set yet
        val = 5
        aopt_dict.add("g")["a"] = val
        aopt_dict["g"].add("b")["a"] = val
        assert aopt_dict["g"]["a"] == val
        assert aopt_dict["g"]["b"]["a"] == val


def test_file_io(tmp_path):
    aopt_dict = aesopt.AESOpt_dict(**get_dict())

    aopt_dict.write_yaml(os.path.join(tmp_path, "test.yaml"))
    aopt_dict.write_json(os.path.join(tmp_path, "test.json"))

    # Reading file
    a1 = aesopt.AESOpt_dict().read_yaml(os.path.join(tmp_path, "test.yaml"))
    contain_same_dict(dict_in, a1)
    a3 = aesopt.AESOpt_dict().read_json(os.path.join(tmp_path, "test.json"))
    contain_same_dict(dict_in, a3)

    # Write yaml with numpy data types
    a1 = aesopt.AESOpt_dict()
    a1["a"] = np.array([0.1, 0.2])
    a1["b"] = np.int16(40)
    a1["c"] = np.float16(30.0)
    a1["d"] = np.str_("test")
    a1.write_yaml(os.path.join(tmp_path, "test2.yaml"))
    b1 = aesopt.AESOpt_dict().read_yaml(os.path.join(tmp_path, "test2.yaml")).as_dict()
    assert isinstance(b1["a"], list) and np.all(b1["a"] == [0.1, 0.2])
    assert isinstance(b1["b"], int) and np.all(b1["b"] == 40)
    assert isinstance(b1["c"], float) and np.all(b1["c"] == 30.0)
    assert isinstance(b1["d"], str) and np.all(b1["d"] == "test")

    # Reading string
    a1 = aesopt.AESOpt_dict().from_yaml(aopt_dict.as_yaml())
    contain_same_dict(dict_in, a1)
    a3 = aesopt.AESOpt_dict().from_json(aopt_dict.as_json())
    contain_same_dict(dict_in, a3)

    # Overwrite the yaml object
    aopt_dict.yaml_object = aesopt.YAML(typ="rt")
    aopt_dict.write_yaml(os.path.join(tmp_path, "test.yaml"))
    aopt_dict.write_json(os.path.join(tmp_path, "test.json"))

    a1 = aesopt.AESOpt_dict().read_yaml(os.path.join(tmp_path, "test.yaml"))
    contain_same_dict(dict_in, a1)
    a3 = aesopt.AESOpt_dict().read_json(os.path.join(tmp_path, "test.json"))
    contain_same_dict(dict_in, a3)
    # Testing yaml object is the same
    assert aopt_dict.get_yaml_object() == aopt_dict._yaml_obj

    # Testing that the yaml parser can convert numpy arrays and AESOpt_list
    out = StringIO()
    aopt_dict.get_yaml_object().dump(np.array([0.1, 0.2]), out)
    assert out.getvalue().strip() == "[0.1, 0.2]"
    out = StringIO()
    aopt_dict.get_yaml_object().dump(aesopt.AESOpt_list([0.1, 0.2]), out)
    assert out.getvalue().strip() == "[0.1, 0.2]"


def test_to_from_numpy():
    aopt_dict = aesopt.AESOpt_dict().read_yaml(
        os.path.join(test_path, "data", "IEA_22MW", "windIO", "IEA-22-280-RWT.yaml")
    )
    # Not inplace
    aopt_new = aopt_dict.to_numpy(False)
    assert not isinstance(
        aopt_dict["components"]["blade"]["outer_shape_bem"]["chord"]["values"],
        np.ndarray,
    )
    assert isinstance(
        aopt_new["components"]["blade"]["outer_shape_bem"]["chord"]["values"],
        np.ndarray,
    )
    assert not isinstance(
        aopt_dict["components"]["blade"]["elastic_properties_mb"]["six_x_six"][
            "stiff_matrix"
        ]["values"],
        np.ndarray,
    )
    assert isinstance(
        aopt_new["components"]["blade"]["elastic_properties_mb"]["six_x_six"][
            "stiff_matrix"
        ]["values"],
        np.ndarray,
    )
    assert not isinstance(
        aopt_dict["airfoils"][1]["polars"][1]["c_l"]["values"],
        np.ndarray,
    )
    assert isinstance(
        aopt_new["airfoils"][1]["polars"][1]["c_l"]["values"],
        np.ndarray,
    )

    # Inplace
    aopt_dict.to_numpy()
    assert isinstance(
        aopt_dict["components"]["blade"]["outer_shape_bem"]["chord"]["values"],
        np.ndarray,
    )
    assert isinstance(
        aopt_dict["components"]["blade"]["elastic_properties_mb"]["six_x_six"][
            "stiff_matrix"
        ]["values"],
        np.ndarray,
    )
    assert isinstance(
        aopt_dict["airfoils"][1]["polars"][1]["c_l"]["values"],
        np.ndarray,
    )

    aopt_dict["components"]["blade"]["outer_shape_bem"]["chord"]["values"] = np.asarray(
        aopt_dict["components"]["blade"]["outer_shape_bem"]["chord"]["values"]
    )
    aopt_dict.as_yaml()


def test_jmespath():
    aopt_dict = aesopt.AESOpt_dict(**get_dict())

    out1 = aopt_dict.jp("f[*]")
    assert len(out1) == len(aopt_dict["f"])
    contain_same_list(out1, aopt_dict["f"])

    out2 = aopt_dict.jp("f[?b=='test2'] | [0]")
    assert len(out2) == len(aopt_dict["f"][1])
    contain_same_list(out2, aopt_dict["f"][1])

    out3 = aopt_dict.jp("e[?[1]=='test2'] | [0]")
    assert len(out3) == len(aopt_dict["e"][1])
    contain_same_list(out3, aopt_dict["e"][1])


def test_as_dict():
    aopt_dict = aesopt.AESOpt_dict(**get_dict())
    assert isinstance(aopt_dict["c"], aesopt.AESOpt_list)
    assert isinstance(aopt_dict["d"], aesopt.AESOpt_dict)
    aopt_as_dict = aopt_dict.as_dict()
    assert isinstance(aopt_dict, aesopt.AESOpt_dict)
    assert isinstance(aopt_dict["c"], aesopt.AESOpt_list)
    assert isinstance(aopt_dict["d"], aesopt.AESOpt_dict)
    assert isinstance(aopt_as_dict, dict)
    assert isinstance(aopt_as_dict["c"], list)
    assert isinstance(aopt_as_dict["d"], dict)
    contain_same_dict_instance(aopt_as_dict, dict_in)

    aopt_dict = aesopt.AESOpt_dict(**get_dict())
    assert isinstance(aopt_dict["c"], aesopt.AESOpt_list)
    assert isinstance(aopt_dict["d"], aesopt.AESOpt_dict)
    aopt_dict.as_dict(inplace=True)
    assert isinstance(aopt_dict, aesopt.AESOpt_dict)
    assert isinstance(aopt_dict["c"], list)
    assert isinstance(aopt_dict["d"], dict)
    contain_same_dict_instance(aopt_dict.data, dict_in)

    assert str(aopt_dict) == aopt_dict.as_yaml()


def test_to_list():
    aopt_dict = aesopt.AESOpt_dict(**get_dict())
    with pytest.raises(AssertionError):
        contain_same_dict_instance(dict_in, aopt_dict.to_list())
    contain_same_dict_instance(dict_in, aopt_dict.to_list(), False)
    aopt_dict["k"] = np.arange(3)
    aopt_dict.to_list(inplace=True)
    assert isinstance(aopt_dict["k"], list)


def test_get_set_item():
    aopt_dict = aesopt.AESOpt_dict(**get_dict())
    # Get
    # By key
    assert aopt_dict["d"]["c"][1] == "test"
    # By path
    assert aopt_dict["d.c[1]"] == "test"

    # Set
    aopt_dict["a"] = 3
    assert aopt_dict["a"] == 3
    aopt_dict["d"]["a"] = 3
    assert aopt_dict["d"]["a"] == 3
    aopt_dict["d.a"] = 4
    assert aopt_dict["d"]["a"] == 4
    aopt_dict["d.c[1]"] = "new test"
    assert aopt_dict["d"]["c"][1] == "new test"


def test_aesopt_list():
    aopt_list = aesopt.AESOpt_list([[0.0, 0.0], [1.0, 1.0]])
    assert isinstance(aopt_list.data, list)
    assert isinstance(aopt_list.data[0], list)
    assert isinstance(aopt_list.data[1], list)
    aopt_new = aopt_list.to_numpy(inplace=False)
    assert isinstance(aopt_list.data, list)
    assert isinstance(aopt_list.data[0], list)
    assert isinstance(aopt_list.data[1], list)
    assert isinstance(aopt_new, np.ndarray)
    assert isinstance(aopt_new[0], np.ndarray)
    assert isinstance(aopt_new[1], np.ndarray)
    aopt_list.to_numpy()
    assert isinstance(aopt_list.data, np.ndarray)
    assert isinstance(aopt_list.data[0], np.ndarray)
    assert isinstance(aopt_list.data[1], np.ndarray)
    aopt_new = aopt_list.to_list()
    assert isinstance(aopt_new, list)
    assert isinstance(aopt_new[0], list)
    assert isinstance(aopt_new[1], list)
    assert isinstance(aopt_list.data, np.ndarray)
    assert isinstance(aopt_list.data[0], np.ndarray)
    assert isinstance(aopt_list.data[1], np.ndarray)
    aopt_new = aopt_list.to_list(inplace=True)
    assert isinstance(aopt_list.data, list)
    assert isinstance(aopt_list.data[0], list)
    assert isinstance(aopt_list.data[1], list)

    aopt_list = aesopt.AESOpt_list([[0.0, 0.0], [1.0, 1.0, 1.0]])
    assert isinstance(aopt_list.data, list)
    assert isinstance(aopt_list.data[0], list)
    assert isinstance(aopt_list.data[1], list)
    aopt_list.to_numpy()
    assert isinstance(aopt_list.data, list)
    assert isinstance(aopt_list.data[0], np.ndarray)
    assert isinstance(aopt_list.data[1], np.ndarray)
    aopt_list.to_list(inplace=True)
    assert isinstance(aopt_list.data, list)
    assert isinstance(aopt_list.data[0], list)
    assert isinstance(aopt_list.data[1], list)

    aopt_list = aesopt.AESOpt_list(
        [
            [0.0, 0.0],
            dict(x=[1.0, 2.0], y=2, z=3),
            dict(name=1, x=[1.0, 2.0], y=2, z=3),
            dict(name=2, x=[1.0, 2.0], y=2, z=3),
        ]
    )
    assert isinstance(aopt_list.data, list)
    assert isinstance(aopt_list.data[0], list)
    assert isinstance(aopt_list.data[1], aesopt.AESOpt_dict)
    assert isinstance(aopt_list.data[2], aesopt.AESOpt_dict)
    assert isinstance(aopt_list.data[3], aesopt.AESOpt_dict)
    aopt_list.to_numpy()
    assert isinstance(aopt_list.data, list)
    assert isinstance(aopt_list.data[0], np.ndarray)
    assert isinstance(aopt_list.data[1], aesopt.AESOpt_dict)
    assert isinstance(aopt_list.data[1]["x"], np.ndarray)
    assert isinstance(aopt_list.data[2], aesopt.AESOpt_dict)
    assert isinstance(aopt_list.data[2]["x"], np.ndarray)
    assert isinstance(aopt_list.data[3], aesopt.AESOpt_dict)
    assert isinstance(aopt_list.data[3]["x"], np.ndarray)
    aopt_list.to_list(inplace=True)
    assert isinstance(aopt_list.data, list)
    assert isinstance(aopt_list.data[0], list)
    assert isinstance(aopt_list.data[1], dict)
    assert isinstance(aopt_list.data[1]["x"], list)
    assert isinstance(aopt_list.data[2], dict)
    assert isinstance(aopt_list.data[2]["x"], list)
    assert isinstance(aopt_list.data[3], dict)
    assert isinstance(aopt_list.data[3]["x"], list)

    aopt_list = aesopt.AESOpt_list(
        [
            dict(x=[1.0, 2.0], y=2, z=3),
            dict(name=1, x=[1.0, 2.0], y=2, z=3),
            dict(name=2, x=[1.0, 2.0], y=2, z=3),
            dict(name=3, x=[1.0, 2.0], y=2, z=3),
        ]
    )
    aopt_list.update([dict(name=1, x=lambda arr: arr + 1.0, y=3, z1=1)])
    assert isinstance(aopt_list.data, list)
    assert isinstance(aopt_list.data[0], aesopt.AESOpt_dict)
    assert isinstance(aopt_list.data[0]["x"], aesopt.AESOpt_list)
    assert isinstance(aopt_list.data[1], aesopt.AESOpt_dict)
    assert isinstance(aopt_list.data[1]["x"], np.ndarray)
    assert all(aopt_list.data[1]["x"] == [2.0, 3.0])
    assert aopt_list.data[1]["y"] == 3
    assert aopt_list.data[1]["z"] == 3
    assert aopt_list.data[1]["z1"] == 1
    assert isinstance(aopt_list.data[2], aesopt.AESOpt_dict)
    assert isinstance(aopt_list.data[2]["x"], aesopt.AESOpt_list)
    assert isinstance(aopt_list.data[3], aesopt.AESOpt_dict)
    assert isinstance(aopt_list.data[3]["x"], aesopt.AESOpt_list)
