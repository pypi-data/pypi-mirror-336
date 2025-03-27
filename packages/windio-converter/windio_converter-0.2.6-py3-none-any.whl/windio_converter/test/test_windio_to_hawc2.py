import os
import warnings

import numpy as np

from windio_converter import windio_to_hawc2
from windio_converter.io.hawc2 import HAWC2_dict
from windio_converter.io.windio import WindIO_dict
from windio_converter.test import test_path

number_dtype = (float, int)


def is_type(dtype):
    def assert_is_dtype(el, name_or_element):
        assert isinstance(
            el, dtype
        ), f"{name_or_element} is not of data-type: {dtype} (given: {type(el)})"

    return assert_is_dtype


def is_len(n):
    def assert_is_len(el, name_or_element):
        assert (
            len(el) == n
        ), f"{name_or_element} is not of length {n} (given: {len(el)})"

    return assert_is_len


def is_equal_to(val):
    def assert_is_equal_to(el, name_or_element):
        assert np.all(
            np.asarray(el) == val
        ), f"{name_or_element} is not equal to {val} (given: {el})"

    return assert_is_equal_to


def is_approx_equal_to(val, tol):
    def assert_is_approx_equal_to(el, name_or_element):
        assert np.all(
            np.abs(1 - np.asarray(el) / val) < tol
        ), f"{name_or_element} is not approximate equal to {val} (given: abs(1-el/val)={np.abs(1-np.asarray(el)/val)})"

    return assert_is_approx_equal_to


def assert_dict_entries(dict_in, entry_validations):
    assert len(dict_in) == len(
        entry_validations
    ), f"The number of elements in the dict_in is different than the expected (given: len(dict_in)={len(dict_in)}, len(entry_validations)={len(entry_validations)})"
    for name, validations in entry_validations.items():
        assert name in dict_in, f"{name} is not in dict_in"
        for val in validations if isinstance(validations, list) else [validations]:
            val(dict_in[name], name)


def assert_list_entries(list_in, element_validations):
    assert len(list_in) == len(
        element_validations
    ), f"The number of elements in the list_in is different than the expected (given: len(list_in)={len(list_in)}, len(element_validations)={len(element_validations)})"
    for iel, validations in enumerate(element_validations):
        for val in validations if isinstance(validations, list) else [validations]:
            val(list_in[iel], iel)


def assert_is_num_list(num_list, name_or_element):
    assert np.issubdtype(
        np.asarray(num_list).dtype, np.number
    ), f"For {name_or_element} the elements are not numbers num_list.dtype={np.asarray(num_list).dtype}"


def assert_positive_values(num_list, name_or_element):
    _num_list = np.asarray(num_list)
    assert_is_num_list(_num_list, name_or_element)
    assert np.all(
        _num_list >= 0
    ), f"For {name_or_element} not all points are positive for a grid (given: grid={_num_list})"


def assert_grid(grid, name_or_element):
    _grid = np.asarray(grid)
    assert_positive_values(_grid, name_or_element)
    assert np.all(
        np.diff(_grid) > 0
    ), f"For {name_or_element} points are not monotonically increasing for the grid (given: np.diff(grid)={np.diff(_grid)})"


def assert_tabular_data(tabular_data, element_validation, nel1, nel2=None):
    assert isinstance(
        tabular_data, list
    ), f"tabular_data is not of type list (given: {type(tabular_data)})"
    assert (
        len(tabular_data) == nel1
    ), f"len(tabular_data) do not match {nel1} (given: {len(tabular_data)})"

    def assert_tabular_element(el, element_validation):
        assert len(el) == len(
            element_validation
        ), f"The number of keys in the element do not match the validation (given: len(el)={len(el)}, len(element_validation)={len(element_validation)})"
        for name, val_fun in element_validation.items():
            assert (
                name in el
            ), f"{name} is not in element (given: el.keys()={el.keys()})"
            if val_fun is None:
                assert_is_num_list(el)
            elif isinstance(val_fun, list):
                for val in val_fun:
                    val(el[name], name)
            else:
                val_fun(el[name], name)

    for el1 in tabular_data:
        if not nel2 is None:
            assert isinstance(
                el1, list
            ), f"tabular_data is not of type list (given: {type(el1)})"
            assert (
                len(el1) == nel2
            ), f"len(tabular_data) do not match {nel2} (given: {len(el1)})"
            for el2 in el1:
                assert_tabular_element(el2, element_validation)
        else:
            assert_tabular_element(el1, element_validation)


def test_iea15mw_floater(tmp_path):
    yamlPath = os.path.join(
        test_path, "data", "IEA_15MW", "windIO", "IEA-15-240-RWT_VolturnUS-S.yaml"
    )

    iea15MW_wio = WindIO_dict().read_yaml(yamlPath)

    # Creates a generic dictionary
    iea15MW_wio2h2_dict = windio_to_hawc2(
        iea15MW_wio.as_dict(), init_rotor_speed=0.7, filenames=dict(base_name="IEA15MW")
    ).convert()

    # Convert to HAWC2_dict object
    iea15MW_wio2h2 = HAWC2_dict(**iea15MW_wio2h2_dict)

    # Read a template file
    iea15MW_H2 = HAWC2_dict().read_hawc2(
        os.path.join(
            test_path, "data", "IEA_15MW", "HAWC2", "IEA-15-240-RWT-UMaineSemi"
        ),
        os.path.join("htc", "IEA_15MW_RWT_UMaineSemi.htc"),
    )

    # Copying the H2 model as the "master" H2-file
    iea15MW_main = iea15MW_H2.copy()

    # Updating the master with the converted data
    # iea15MW_main.update(iea15MW_wio2h2)
    iea15MW_main["htc"]["new_htc_structure"] = iea15MW_wio2h2["htc"][
        "new_htc_structure"
    ]
    iea15MW_main["htc"]["simulation"]["time_stop"] = 30.0
    iea15MW_main["st"] = iea15MW_wio2h2["st"]
    iea15MW_main["htc"]["hydro"] = iea15MW_wio2h2["htc"]["hydro"]
    iea15MW_main["htc"]["simulation"]["visualization"] = "viz/viz.hdf5"
    iea15MW_main["htc"]["simulation"]["animation"] = "ani/ani.dat"
    iea15MW_main["htc"]["new_htc_structure"]["constraint"]["bearing1"][0][
        "name"
    ] = "shaft_rot"

    # Saving the master files
    iea15MW_main.write_hawc2(os.path.join(tmp_path, "IEA15MW_Floating"))


def test_iea15mw_monopile(tmp_path):
    yamlPath = os.path.join(
        test_path, "data", "IEA_15MW", "windIO", "IEA-15-240-RWT.yaml"
    )

    iea15MW_wio = WindIO_dict().read_yaml(yamlPath)

    converter = windio_to_hawc2(
        iea15MW_wio.as_dict(), init_rotor_speed=0.7, filenames=dict(base_name="IEA15MW")
    )

    converter._repr_html_()

    iea15MW_wio2h2_dict = converter.convert()

    # Converting dict to HAWC2_dict
    iea15MW_wio2h2 = HAWC2_dict(**iea15MW_wio2h2_dict)

    # Read a template file
    iea15MW_H2 = HAWC2_dict().read_hawc2(
        os.path.join(test_path, "data", "IEA_15MW", "HAWC2", "IEA-15-240-RWT-Monopile"),
        os.path.join("htc", "IEA_15MW_RWT_Monopile.htc"),
    )

    # Copying the H2 model as the "master" H2-file
    iea15MW_main = iea15MW_H2.copy()

    # Updating the master with the converted data
    # iea15MW_main.update(iea15MW_wio2h2)
    iea15MW_main["htc"]["new_htc_structure"] = iea15MW_wio2h2["htc"][
        "new_htc_structure"
    ]
    iea15MW_main["htc"]["simulation"]["time_stop"] = 30.0
    iea15MW_main["st"] = iea15MW_wio2h2["st"]
    iea15MW_main["htc"]["hydro"] = iea15MW_wio2h2["htc"]["hydro"]
    iea15MW_main["htc"]["simulation"]["visualization"] = "viz/viz.hdf5"
    iea15MW_main["htc"]["simulation"]["animation"] = "ani/ani.dat"
    iea15MW_main["htc"]["new_htc_structure"]["constraint"]["bearing1"][0][
        "name"
    ] = "shaft_rot"

    # Writing the HAWC2 model to folder
    iea15MW_main["htc_filename"] = "IEA_15MW_RWT_Monopile.htc"
    iea15MW_main.write_hawc2(os.path.join(tmp_path, "IEA15MW"))


def test_onshore_hawc2_output():
    """Test of HAWC2 output data structure and content for onshore turbine. Tests correct key-value pairs, data-types and names"""

    # Read windIO file
    fname_iea15mw_wio = os.path.join(
        test_path, "data", "IEA_15MW", "windIO", "IEA-15-240-RWT.yaml"
    )

    iea15MW_wio = WindIO_dict().read_yaml(fname_iea15mw_wio)
    iea15MW_wio["components"].pop(
        "monopile"
    )  # Remove monopile to make it an onshore turbine
    iea15MW_wio["components"]["nacelle"]["drivetrain"][
        "gearbox_efficiency"
    ] = 0.9655  # Value from HAWC2 model

    # Convert the windIO file to HAWC2
    converter = windio_to_hawc2(
        iea15MW_wio.as_dict(),
        init_rotor_speed=0.7,
        filenames=dict(base_name="IEA15MW"),
        dtu_we_controller=dict(CP_design=0.45496603434036204),
    )

    iea15MW_onshore_wio2h2_dict = converter.convert()

    # Overall #
    assert_dict_entries(
        iea15MW_onshore_wio2h2_dict,
        {
            "htc": is_type(dict),
            "ae": is_type(list),
            "pc": is_type(list),
            "st": is_type(dict),
            "htc_filename": is_type(str),
        },
    )

    # %% AE %% #
    def assert_tc(num_list, name):
        assert_positive_values(num_list, name)
        assert (
            np.abs(num_list[0] - 100) < 1e-7
        ), f"For {name} the first point should be 100 (given: num_list[0]={num_list[0]})"

    ae_validation = {
        "s": assert_grid,
        "chord": assert_positive_values,
        "tc": assert_tc,
        "pc_set": [assert_positive_values, is_equal_to(1)],
    }
    assert_tabular_data(iea15MW_onshore_wio2h2_dict["ae"], ae_validation, 1)

    # %% PC %% #
    warnings.warn("The PC-list is not tested yet")

    # %% ST %% #
    warnings.warn("The ST-dict is not tested yet")

    # %% HTC %% #
    htc = iea15MW_onshore_wio2h2_dict["htc"]
    warnings.warn("The base HTC is not tested yet")

    warnings.warn("The HTC.new_htc_structure is not tested yet")

    warnings.warn("The HTC.aero is not tested yet")

    warnings.warn("The HTC.aerodrag is not tested yet")

    # dll-block
    dll_entries = {"type2_dll": [is_type(list), is_len(1)]}
    assert_dict_entries(htc["dll"], dll_entries)

    # dtu-we-controller
    dtu_we_entries = {
        "name": [is_type(str), is_equal_to("dtu_we_controller")],
        "init": [is_type(dict), is_len(1)],
    }
    assert_dict_entries(htc["dll"]["type2_dll"][0], dtu_we_entries)
    # init
    init_entries = {"constant": [is_type(list), is_len(1)]}
    assert_dict_entries(htc["dll"]["type2_dll"][0]["init"], init_entries)
    # constant
    constant_entries = [
        [is_type(int), is_equal_to(11)],
        [is_type(number_dtype), is_approx_equal_to(0.302217e08, 1e-5)],
    ]
    assert_list_entries(
        htc["dll"]["type2_dll"][0]["init"]["constant"][0], constant_entries
    )


if __name__ == "__main__":
    file_dir = os.path.dirname(__file__)

    test_iea15mw_floater(os.path.join(file_dir, "temp"))
    test_iea15mw_monopile(os.path.join(file_dir, "temp"))
