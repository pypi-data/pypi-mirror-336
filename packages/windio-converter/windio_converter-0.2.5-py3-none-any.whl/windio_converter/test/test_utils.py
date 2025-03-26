import os
from copy import deepcopy

import numpy as np
import pytest

from windio_converter.io import HTC_dict, WindIO_dict
from windio_converter.test import test_path
from windio_converter.utils import (
    airfoils2polars,
    change_pitch_axis,
    compute_curve_length,
    get_s_airfoils,
    interp,
)

IEA_22MW_wio_path = os.path.join(
    test_path, "data", "IEA_22MW", "windIO", "IEA-22-280-RWT.yaml"
)

IEA_15MW_wio_path = os.path.join(
    test_path, "data", "IEA_15MW", "windIO", "IEA-15-240-RWT.yaml"
)


def is_valid_airfoils_polar(airs):
    assert isinstance(airs, list)
    for air in airs:
        assert isinstance(air, dict)
        assert isinstance(air["name"], str)
        assert isinstance(air["relative_thickness"], (float, int))
        assert isinstance(air["aerodynamic_center"], (float, int))
        assert isinstance(air["polar"], dict)
        assert isinstance(air["polar"]["re"], float)
        assert isinstance(air["polar"]["configuration"], (str, dict))
        if isinstance(air["polar"]["configuration"], dict):
            assert all(
                [isinstance(name, str) for name in air["polar"]["configuration"]]
            )
            assert all(
                [
                    isinstance(name, (int, float))
                    for name in air["polar"]["configuration"].values()
                ]
            )
        assert isinstance(air["polar"]["configuration_value"], (int, float, str))
        for key in ["aoa_rad", "aoa_deg", "c_l", "c_d", "c_m"]:
            assert isinstance(air["polar"][key], (list, np.ndarray))
            assert isinstance(air["polar"][key][0], (int, float))


def test_airfoils2polars():
    # Load data
    airfoils_wio = WindIO_dict().read_yaml(IEA_15MW_wio_path).as_dict()["airfoils"]

    # Adding more polars
    for air in airfoils_wio:
        Re = air["polars"][0]["re"] = 3e6
        air["polars"].append(deepcopy(air["polars"][0]))
        air["polars"].append(deepcopy(air["polars"][0]))
        Re_new = 3e7
        # Default with higher Re
        air["polars"][1]["re"] = Re_new
        air["polars"][1]["c_d"]["values"] = [
            val * Re / Re_new for val in air["polars"][1]["c_d"]["values"]
        ]
        # Triped with same Re
        air["polars"][2]["configuration"] = "Triped"
        air["polars"][2]["c_l"]["values"] = [
            val * 0.8 for val in air["polars"][2]["c_l"]["values"]
        ]
        air["polars"][2]["c_d"]["values"] = [
            val * 1.2 for val in air["polars"][2]["c_d"]["values"]
        ]
        # Triped with higher Re
        air["polars"].append(deepcopy(air["polars"][2]))
        air["polars"][3]["re"] = Re_new
        air["polars"][3]["c_d"]["values"] = [
            val * Re / Re_new for val in air["polars"][3]["c_d"]["values"]
        ]

    # Ensure that copies of the polar are made
    assert id(air["polars"][0]["c_d"]["values"]) != id(
        air["polars"][1]["c_d"]["values"]
    )
    assert id(air["polars"][0]["c_d"]["values"]) != id(
        air["polars"][2]["c_d"]["values"]
    )
    assert id(air["polars"][0]["c_d"]["values"]) != id(
        air["polars"][3]["c_d"]["values"]
    )

    # Run without additional arguments
    airfoils = airfoils2polars(airfoils_wio)
    is_valid_airfoils_polar(airfoils)
    np.testing.assert_equal(
        [air["name"] for air in airfoils], [air["name"] for air in airfoils_wio]
    )
    np.testing.assert_equal(
        [air["relative_thickness"] for air in airfoils],
        [air["relative_thickness"] for air in airfoils_wio],
    )
    polars_wio = [air["polars"][0] for air in airfoils_wio]
    for air, pol_wio in zip(airfoils, polars_wio):
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], pol_wio["c_l"]["grid"])
        np.testing.assert_almost_equal(
            air["polar"]["aoa_deg"], np.rad2deg(pol_wio["c_l"]["grid"])
        )
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(air["polar"][coef], pol_wio[coef]["values"])

    # --- Polar Index variations --- #
    # Selecting another polar index
    ipol = 2
    airfoils = airfoils2polars(airfoils_wio, polar_index=ipol)
    is_valid_airfoils_polar(airfoils)
    polars_wio = [air["polars"][ipol] for air in airfoils_wio]
    for air, pol_wio in zip(airfoils, polars_wio):
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], pol_wio["c_l"]["grid"])
        np.testing.assert_almost_equal(
            air["polar"]["aoa_deg"], np.rad2deg(pol_wio["c_l"]["grid"])
        )
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(air["polar"][coef], pol_wio[coef]["values"])

    # Selecting first Triped polar
    ipol = 2
    polars_wio = [air["polars"][ipol] for air in airfoils_wio]
    airfoils = airfoils2polars(airfoils_wio, polar_index="Triped")
    is_valid_airfoils_polar(airfoils)
    for air, pol_wio in zip(airfoils, polars_wio):
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], pol_wio["c_l"]["grid"])
        np.testing.assert_almost_equal(
            air["polar"]["aoa_deg"], np.rad2deg(pol_wio["c_l"]["grid"])
        )
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(air["polar"][coef], pol_wio[coef]["values"])

    # - Interpolation in Re and triped - #
    # Getting polar[0]
    ipol = 0
    polar_index = dict(
        default=dict(
            configuration=dict(Default=0.0, Triped=1.0), configuration_value=0.0, re=3e6
        )
    )
    airfoils = airfoils2polars(airfoils_wio, polar_index=polar_index)
    is_valid_airfoils_polar(airfoils)
    polars_wio = [air["polars"][ipol] for air in airfoils_wio]
    for air, pol_wio in zip(airfoils, polars_wio):
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], pol_wio["c_l"]["grid"])
        np.testing.assert_almost_equal(
            air["polar"]["aoa_deg"], np.rad2deg(pol_wio["c_l"]["grid"])
        )
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(air["polar"][coef], pol_wio[coef]["values"])

    # Getting polar[1]
    ipol = 1
    polar_index = dict(
        default=dict(
            configuration=dict(Default=0.0, Triped=1.0), configuration_value=0.0, re=3e7
        )
    )
    airfoils = airfoils2polars(airfoils_wio, polar_index=polar_index)
    is_valid_airfoils_polar(airfoils)
    polars_wio = [air["polars"][ipol] for air in airfoils_wio]
    for air, pol_wio in zip(airfoils, polars_wio):
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], pol_wio["c_l"]["grid"])
        np.testing.assert_almost_equal(
            air["polar"]["aoa_deg"], np.rad2deg(pol_wio["c_l"]["grid"])
        )
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(air["polar"][coef], pol_wio[coef]["values"])

    # Getting polar[2]
    ipol = 2
    polar_index = dict(
        default=dict(
            configuration=dict(Default=0.0, Triped=1.0), configuration_value=1.0, re=3e6
        )
    )
    airfoils = airfoils2polars(airfoils_wio, polar_index=polar_index)
    is_valid_airfoils_polar(airfoils)
    polars_wio = [air["polars"][ipol] for air in airfoils_wio]
    for air, pol_wio in zip(airfoils, polars_wio):
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], pol_wio["c_l"]["grid"])
        np.testing.assert_almost_equal(
            air["polar"]["aoa_deg"], np.rad2deg(pol_wio["c_l"]["grid"])
        )
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(air["polar"][coef], pol_wio[coef]["values"])

    # Getting polar[3]
    ipol = 3
    polar_index = dict(
        default=dict(
            configuration=dict(Default=0.0, Triped=1.0), configuration_value=1.0, re=3e7
        )
    )
    airfoils = airfoils2polars(airfoils_wio, polar_index=polar_index)
    is_valid_airfoils_polar(airfoils)
    polars_wio = [air["polars"][ipol] for air in airfoils_wio]
    for air, pol_wio in zip(airfoils, polars_wio):
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], pol_wio["c_l"]["grid"])
        np.testing.assert_almost_equal(
            air["polar"]["aoa_deg"], np.rad2deg(pol_wio["c_l"]["grid"])
        )
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(air["polar"][coef], pol_wio[coef]["values"])

    # Flipping Triped or not range for airfoils[0] (with index) and airfoil[3] (with name)
    ipol = 0
    polar_index = {
        0: dict(
            configuration=dict(Default=1.0, Triped=0.0), configuration_value=0.0, re=3e7
        ),
        "FFA-W3-301": dict(
            configuration=dict(Default=1.0, Triped=0.0), configuration_value=0.0, re=3e7
        ),
    }
    airfoils = airfoils2polars(airfoils_wio, polar_index=polar_index)
    is_valid_airfoils_polar(airfoils)
    polars_wio = deepcopy([air["polars"][ipol] for air in airfoils_wio])
    polars_wio[0] = airfoils_wio[0]["polars"][3]
    polars_wio[5] = airfoils_wio[5]["polars"][3]
    for iair, (air, pol_wio) in enumerate(zip(airfoils, polars_wio)):
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], pol_wio["c_l"]["grid"])
        np.testing.assert_almost_equal(
            air["polar"]["aoa_deg"], np.rad2deg(pol_wio["c_l"]["grid"])
        )
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(air["polar"][coef], pol_wio[coef]["values"])

    # --- AoA varations --- #
    # Same grid for all
    aoa_rad = np.linspace(-np.pi, np.pi, 30)
    airfoils = airfoils2polars(airfoils_wio, aoa_rad)
    is_valid_airfoils_polar(airfoils)
    polars_wio = [air["polars"][0] for air in airfoils_wio]
    for air, pol_wio in zip(airfoils, polars_wio):
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], aoa_rad)
        np.testing.assert_almost_equal(air["polar"]["aoa_deg"], np.rad2deg(aoa_rad))
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(
                air["polar"][coef],
                interp(aoa_rad, pol_wio[coef]["grid"], pol_wio[coef]["values"]),
            )

    # Specific grid for airfoils[1] (with index) and airfoil[3] (with name) otherwise use default
    aoa1 = np.linspace(-np.pi, np.pi, 10)
    aoa3 = np.linspace(-np.pi, np.pi, 15)
    aoa_default = np.linspace(-np.pi, np.pi, 30)
    aoa_rad = {1: aoa1, "FFA-W3-301": aoa3, "default": aoa_default}
    airfoils = airfoils2polars(airfoils_wio, aoa_rad)
    is_valid_airfoils_polar(airfoils)
    polars_wio = [air["polars"][0] for air in airfoils_wio]
    for iair, (air, pol_wio) in enumerate(zip(airfoils, polars_wio)):
        if iair == 1:
            aoa = aoa1
        elif iair == 5:
            aoa = aoa3
        else:
            aoa = aoa_default
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], aoa)
        np.testing.assert_almost_equal(air["polar"]["aoa_deg"], np.rad2deg(aoa))
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(
                air["polar"][coef],
                interp(aoa, pol_wio[coef]["grid"], pol_wio[coef]["values"]),
            )

    # With empty dicts for both aoa_rad and polar_index
    airfoils = airfoils2polars(airfoils_wio, dict(), dict())
    is_valid_airfoils_polar(airfoils)
    polars_wio = [air["polars"][0] for air in airfoils_wio]
    for air, pol_wio in zip(airfoils, polars_wio):
        np.testing.assert_almost_equal(air["polar"]["aoa_rad"], pol_wio["c_l"]["grid"])
        np.testing.assert_almost_equal(
            air["polar"]["aoa_deg"], np.rad2deg(pol_wio["c_l"]["grid"])
        )
        for coef in ["c_l", "c_d", "c_m"]:
            np.testing.assert_almost_equal(air["polar"][coef], pol_wio[coef]["values"])


def test_get_s_airfoils():
    # Load data
    wio_dict = (
        WindIO_dict()
        .read_yaml(
            os.path.join(test_path, "data", "IEA_15MW", "windIO", "IEA-15-240-RWT.yaml")
        )
        .as_dict()
    )

    # Default (with only airfoil_position)
    name_rthick_wio = {
        air["name"]: air["relative_thickness"] for air in wio_dict["airfoils"]
    }
    air_pos = wio_dict["components"]["blade"]["outer_shape_bem"]["airfoil_position"]
    rthick_wio = [name_rthick_wio[name] for name in air_pos["labels"]]
    grid, rthick = get_s_airfoils(wio_dict)
    np.testing.assert_almost_equal(grid, air_pos["grid"])
    np.testing.assert_almost_equal(rthick, rthick_wio)

    # Default (with rthick)
    grid_rthick = np.linspace(0, 1, 40).tolist()
    rthick_new = np.interp(grid_rthick, air_pos["grid"], rthick_wio).tolist()
    wio_dict_temp = deepcopy(wio_dict)
    wio_dict_temp["components"]["blade"]["outer_shape_bem"]["rthick"] = dict(
        grid=grid_rthick, values=rthick_new
    )
    grid, rthick = get_s_airfoils(wio_dict_temp)
    np.testing.assert_almost_equal(grid, grid_rthick)
    np.testing.assert_almost_equal(rthick, rthick_new)

    # Adding a dummy cylinder
    wio_dict_temp = deepcopy(wio_dict)
    wio_dict_temp["components"]["blade"]["outer_shape_bem"]["airfoil_position"][
        "labels"
    ][0] = "cylinder2"
    wio_dict_temp["airfoils"].append(deepcopy(wio_dict["airfoils"][-1]))
    wio_dict_temp["airfoils"][-1]["name"] = "cylinder2"
    air_pos = wio_dict_temp["components"]["blade"]["outer_shape_bem"][
        "airfoil_position"
    ]
    with pytest.raises(Exception):
        get_s_airfoils(wio_dict_temp)
    airfoil_values = {
        air["name"]: air["relative_thickness"] for air in wio_dict_temp["airfoils"]
    }
    airfoil_values["cylinder2"] = 1.01
    s_airfoils_wio = [airfoil_values[name] for name in air_pos["labels"]]
    grid, s_airfoils = get_s_airfoils(wio_dict_temp, airfoil_values)
    np.testing.assert_almost_equal(grid, air_pos["grid"])
    np.testing.assert_almost_equal(s_airfoils, s_airfoils_wio)


def test_change_pitch_axis():
    wiodict = WindIO_dict().read_yaml(
        os.path.join(test_path, "data", "IEA_22MW", "windIO", "IEA-22-280-RWT.yaml")
    )
    htcdict = HTC_dict().read_htc(
        os.path.join(
            test_path,
            "data",
            "IEA_22MW",
            "HAWC2",
            "IEA-22-280-RWT-Monopile",
            "htc",
            "iea_22mw_rwt_steps.htc",
        )
    )
    x_h2 = np.array(
        htcdict.jp("new_htc_structure.main_body[?name=='blade1'].c2_def.sec[*][1]")[0]
    )
    y_h2 = np.array(
        htcdict.jp("new_htc_structure.main_body[?name=='blade1'].c2_def.sec[*][2]")[0]
    )
    z_h2 = np.array(
        htcdict.jp("new_htc_structure.main_body[?name=='blade1'].c2_def.sec[*][3]")[0]
    )
    x_h2wio, y_h2wio, z_h2wio = (y_h2, -x_h2, z_h2)
    grid_h2 = np.array(compute_curve_length(x_h2wio, y_h2wio, z_h2wio))
    grid_h2 /= grid_h2[-1]
    grid = (
        grid_h2  # wiodict.jp("components.blade.outer_shape_bem.reference_axis.x.grid")
    )
    inp_data = dict(
        x=wiodict.jp("components.blade.outer_shape_bem.reference_axis.x").interp(grid),
        y=wiodict.jp("components.blade.outer_shape_bem.reference_axis.y").interp(grid),
        z=wiodict.jp("components.blade.outer_shape_bem.reference_axis.z").interp(grid),
        chord=wiodict.jp("components.blade.outer_shape_bem.chord").interp(grid),
        twist_rad=np.array(
            wiodict.jp("components.blade.outer_shape_bem.twist").interp(grid)
        ),
        pitch_axis_in=wiodict.jp("components.blade.outer_shape_bem.pitch_axis").interp(
            grid
        ),
        pitch_axis_out=np.full_like(grid, 0.5),
    )
    x, y, z = change_pitch_axis(**inp_data)

    np.testing.assert_array_almost_equal(x[2:] / x_h2wio[2:] - 1, 0.0, 1)
    np.testing.assert_array_almost_equal(y[2:] / y_h2wio[2:] - 1, 0.0, 1)
    np.testing.assert_array_almost_equal(z[2:] / z_h2wio[2:] - 1, 0.0, 2)
