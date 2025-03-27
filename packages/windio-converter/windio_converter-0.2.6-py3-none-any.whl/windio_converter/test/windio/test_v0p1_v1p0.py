import os

import numpy as np
import pytest

from windio_converter.io.windio import WindIO_dict
from windio_converter.test import test_path
from windio_converter.windio.v0p1_v1p0 import nac_epm_names, v0p1_to_v1p0, v1p0_to_v0p1


def test_convert_wio_v0p1_to_v1p0():
    wio_v0p1_dict = WindIO_dict().read_yaml(
        os.path.join(
            test_path, "data", "IEA_15MW", "windIO", "IEA-15-240-RWT_v0p1.yaml"
        )
    )

    wio_v1p0_dict = v0p1_to_v1p0(wio_v0p1_dict).convert()

    assert wio_v1p0_dict["windio_version"] == 1.0

    # Hub
    assert not "outer_shape_bem" in wio_v1p0_dict["components"]["hub"]
    for name in ["diameter", "cone_angle", "drag_coefficient"]:
        assert name in wio_v1p0_dict["components"]["hub"]

    # Nacelle
    assert not "outer_shape_bem" in wio_v1p0_dict["components"]["nacelle"]
    for name in ["uptilt", "distance_tt_hub", "overhang", "drag_coefficient"]:
        assert name in wio_v1p0_dict["components"]["nacelle"]["drivetrain"]
    assert not "uptilt_angle" in wio_v1p0_dict["components"]["nacelle"]
    nac_epm = wio_v1p0_dict["components"]["nacelle"]["drivetrain"][
        "elastic_properties_mb"
    ]
    for o_name, n_name in nac_epm_names.items():
        assert n_name in nac_epm
        assert not o_name in nac_epm

    # Raise
    # Additional hub.outer_shape_bem
    with pytest.raises(RuntimeError) as exc_info:
        wio_v0p1_dict["components"]["hub"]["outer_shape_bem"][
            "not_an_osb_element"
        ] = None
        wio_v1p0_dict = v0p1_to_v1p0(wio_v0p1_dict).convert()
    assert "hub.outer_shape_bem" in exc_info.value.args[0]
    wio_v0p1_dict["components"]["hub"]["outer_shape_bem"].pop("not_an_osb_element")
    # Additional nacelle.outer_shape_bem
    with pytest.raises(RuntimeError) as exc_info:
        wio_v0p1_dict["components"]["nacelle"]["outer_shape_bem"][
            "not_an_osb_element"
        ] = None
        wio_v1p0_dict = v0p1_to_v1p0(wio_v0p1_dict).convert()
    assert "nacelle.outer_shape_bem" in exc_info.value.args[0]
    wio_v0p1_dict["components"]["nacelle"]["outer_shape_bem"].pop("not_an_osb_element")


def test_convert_wio_v1p0_to_v0p1():
    wio_v1p0_dict = WindIO_dict().read_yaml(
        os.path.join(test_path, "data", "IEA_22MW", "windIO", "IEA-22-280-RWT.yaml")
    )

    wio_v0p1_dict = v1p0_to_v0p1(wio_v1p0_dict).convert()

    assert wio_v0p1_dict["windio_version"] == 0.1

    # Hub
    assert "outer_shape_bem" in wio_v0p1_dict["components"]["hub"]
    for name in ["diameter", "cone_angle", "drag_coefficient"]:
        assert name in wio_v0p1_dict["components"]["hub"]["outer_shape_bem"]
        assert not name in wio_v0p1_dict["components"]["hub"]

    # Nacelle
    assert "outer_shape_bem" in wio_v0p1_dict["components"]["nacelle"]
    new_name = dict(uptilt_angle="uptilt")
    for name in ["uptilt_angle", "distance_tt_hub", "overhang", "drag_coefficient"]:
        assert name in wio_v0p1_dict["components"]["nacelle"]["outer_shape_bem"]
        assert (
            not new_name.get(name, name)
            in wio_v0p1_dict["components"]["nacelle"]["drivetrain"]
        )
    # Elastic properties
    assert (
        not "elastic_properties_mb"
        in wio_v0p1_dict["components"]["nacelle"]["drivetrain"]
    )
    assert "elastic_properties_mb" in wio_v0p1_dict["components"]["nacelle"]
    nac_epm = wio_v0p1_dict["components"]["nacelle"]["elastic_properties_mb"]
    for n_name, o_name in nac_epm_names.items():
        assert n_name in nac_epm
        assert not o_name in nac_epm


def test_round_trip():
    # v0.1 -> v1.0 -> v0.1
    wio_v0p1_dict = (
        WindIO_dict()
        .read_yaml(
            os.path.join(
                test_path, "data", "IEA_15MW", "windIO", "IEA-15-240-RWT_v0p1.yaml"
            )
        )
        .as_dict()
    )
    wio_v1p0_dict = v0p1_to_v1p0(wio_v0p1_dict).convert()
    wio_v0p1_dict_rt = v1p0_to_v0p1(wio_v1p0_dict).convert()
    assert_dicts(wio_v0p1_dict, wio_v0p1_dict_rt)

    # v1.0 -> v0.1 -> v1.0
    wio_v1p0_dict = (
        WindIO_dict()
        .read_yaml(
            os.path.join(test_path, "data", "IEA_22MW", "windIO", "IEA-22-280-RWT.yaml")
        )
        .as_dict()
    )
    wio_v0p1_dict = v1p0_to_v0p1(wio_v1p0_dict).convert()
    wio_v1p0_dict_rt = v0p1_to_v1p0(wio_v0p1_dict).convert()
    assert_dicts(wio_v1p0_dict, wio_v1p0_dict_rt)


def assert_dicts(d1, d2):
    for name, val in d1.items():
        if isinstance(val, dict):
            assert_dicts(val, d2[name])
        elif isinstance(val, str):
            assert val == d2[name]
        elif isinstance(val, list):
            if isinstance(val[0], str):
                assert val == d2[name]
            elif isinstance(val[0], dict):
                assert len(val) == len(d2[name])
                for _d1, _d2 in zip(val, d2[name]):
                    assert_dicts(_d1, _d2)
            else:
                np.testing.assert_almost_equal(val, d2[name], 12)
        else:
            np.testing.assert_almost_equal(val, d2[name], 12)
