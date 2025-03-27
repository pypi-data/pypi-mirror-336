import os

import numpy as np

from windio_converter.io.windio import WindIO_dict
from windio_converter.test import test_path
from windio_converter.windio.coordinate_system import convert_coordinate_system


def test_convert_coordinate_system():
    wio_dict = (
        WindIO_dict()
        .read_yaml(
            os.path.join(test_path, "data", "IEA_22MW", "windIO", "IEA-22-280-RWT.yaml")
        )
        .as_dict()
    )
    # Adding dummy data to test coordinate transformation
    for name in ["monopile", "tower"]:
        for field in ["outer_shape_bem", "internal_structure_2d_fem"]:
            wio_dict["components"][name][field]["reference_axis"]["x"]["values"][
                -1
            ] = 10

    wio_new = convert_coordinate_system(
        wio_dict, cs_transform_name="windio_to_hawc2"
    ).convert()

    # Blade outer_shape_bem
    blade_osb = wio_new["components"]["blade"]["outer_shape_bem"]
    np.testing.assert_almost_equal(blade_osb["pitch_axis"]["values"], 0.5)
    assert (
        not wio_dict["components"]["blade"]["outer_shape_bem"]["pitch_axis"]["values"][
            -1
        ]
        == 0.5
    )
    # Test that z axis change from change in pitch axis
    assert any(
        abs(
            np.asarray(blade_osb["reference_axis"]["z"]["values"])
            - np.asarray(
                wio_dict["components"]["blade"]["outer_shape_bem"]["reference_axis"][
                    "z"
                ]["values"]
            )
        )
        > 1e-3
    )
    assert blade_osb["reference_axis"]["coordinate_system"] == "hawc2 blade"

    for comp in ["tower", "monopile"]:
        for field in ["outer_shape_bem", "internal_structure_2d_fem"]:
            comp_old = wio_dict["components"][comp][field]
            comp_new = wio_new["components"][comp][field]
            np.testing.assert_equal(
                comp_old["reference_axis"]["y"]["values"],
                comp_new["reference_axis"]["x"]["values"],
            )
            np.testing.assert_equal(
                comp_old["reference_axis"]["x"]["values"],
                comp_new["reference_axis"]["y"]["values"],
            )
            np.testing.assert_equal(
                -np.array(comp_old["reference_axis"]["z"]["values"]),
                comp_new["reference_axis"]["z"]["values"],
            )
            assert not ("coordinate_system" in comp_old["reference_axis"])
            assert comp_new["reference_axis"]["coordinate_system"] == "hawc2 base"

    # Convert back
    wio_new2 = convert_coordinate_system(
        wio_new,
        cs_transform_name="hawc2_to_windio",
        components=dict(
            blade=dict(
                outer_shape_bem=dict(
                    pitch_axis_out=wio_dict["components"]["blade"]["outer_shape_bem"][
                        "pitch_axis"
                    ]
                )
            )
        ),
    ).convert()
    comp = "blade"
    for field in ["outer_shape_bem", "internal_structure_2d_fem"]:
        comp_old = wio_dict["components"][comp][field]
        comp_new = wio_new2["components"][comp][field]
        np.testing.assert_array_almost_equal(
            comp_old["reference_axis"]["x"]["values"],
            comp_new["reference_axis"]["x"]["values"],
            4,
        )
        np.testing.assert_array_almost_equal(
            comp_old["reference_axis"]["y"]["values"],
            comp_new["reference_axis"]["y"]["values"],
            3,
        )
        np.testing.assert_array_almost_equal(
            # Using relative error (absolute error is >1e-2)
            (
                np.asarray(comp_old["reference_axis"]["z"]["values"])
                / np.asarray(comp_new["reference_axis"]["z"]["values"])
                - 1
            ),
            0.0,
            2,
        )
        assert not ("coordinate_system" in comp_new["reference_axis"])

    for comp in ["tower", "monopile"]:
        for field in ["outer_shape_bem", "internal_structure_2d_fem"]:
            comp_old = wio_dict["components"][comp][field]
            comp_new = wio_new2["components"][comp][field]
            np.testing.assert_array_almost_equal(
                comp_old["reference_axis"]["x"]["values"],
                comp_new["reference_axis"]["x"]["values"],
            )
            np.testing.assert_array_almost_equal(
                comp_old["reference_axis"]["y"]["values"],
                comp_new["reference_axis"]["y"]["values"],
            )
            np.testing.assert_array_almost_equal(
                comp_old["reference_axis"]["z"]["values"],
                comp_new["reference_axis"]["z"]["values"],
            )
            assert not "coordinate_system" in comp_old["reference_axis"]
            assert not "coordinate_system" in comp_new["reference_axis"]
