import os

import numpy as np
from pytest import raises

from windio_converter.io.windio import WindIO_dict
from windio_converter.test import test_path


def test_read_yaml():
    wio = WindIO_dict().read_yaml(
        os.path.join(test_path, "data", "IEA_15MW", "windIO", "IEA-15-240-RWT.yaml")
    )

    # Test key access
    np.testing.assert_almost_equal(
        wio["components"]["blade"]["outer_shape_bem"]["chord"]["values"][0], 5.2, 9
    )
    np.testing.assert_almost_equal(
        wio.jp("components.blade.outer_shape_bem.chord.values")[0], 5.2, 9
    )

    np.testing.assert_almost_equal(wio["airfoils"][0]["aerodynamic_center"], 0.5, 9)
    np.testing.assert_almost_equal(wio.jp("airfoils[0].aerodynamic_center"), 0.5, 9)

    # Test interp
    # list input
    chord_val = wio.jp("components.blade.outer_shape_bem.chord")
    np.testing.assert_almost_equal(
        wio.jp("components.blade.outer_shape_bem.chord").interp(chord_val["grid"]),
        chord_val["values"],
        9,
    )

    # Int input
    wio_twist = wio["components.blade.outer_shape_bem.twist"]
    twist = wio_twist.copy()
    twist.interp(5, inplace=True)
    np.testing.assert_almost_equal(
        twist["grid"], np.linspace(wio_twist["grid"][0], wio_twist["grid"][-1], 5)
    )

    # With no input
    twist = wio["components.blade.outer_shape_bem.twist"].interp()
    np.testing.assert_almost_equal(
        np.array(twist), wio["components.blade.outer_shape_bem.twist.values"]
    )

    # With extrapolate
    thickness = wio["components"]["blade"]["internal_structure_2d_fem"]["layers"][12][
        "thickness"
    ].interp(chord_val["grid"], extrapolate=False)
    np.testing.assert_equal(thickness.shape[0], 43)

    # With inplace
    wio["components"]["blade"]["internal_structure_2d_fem"]["layers"][12][
        "thickness"
    ].interp(chord_val["grid"], extrapolate=False, inplace=True)
    np.testing.assert_equal(
        np.array(
            wio["components"]["blade"]["internal_structure_2d_fem"]["layers"][12][
                "thickness"
            ]["values"]
        ).shape[0],
        43,
    )

    # Raises
    with raises(AttributeError):
        wio.interp(5)
