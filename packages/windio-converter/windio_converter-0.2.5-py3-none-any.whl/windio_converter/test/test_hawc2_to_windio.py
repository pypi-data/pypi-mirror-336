import os

from windio_converter import hawc2_to_windio
from windio_converter.io.hawc2 import HAWC2_dict, PC_list
from windio_converter.io.windio import WindIO_dict
from windio_converter.test import test_path


def get_hawc2_dict():
    hawc2_dict = HAWC2_dict().read_hawc2(
        os.path.join(test_path, "data", "IEA_15MW", "HAWC2", "IEA-15-240-RWT-Monopile"),
        os.path.join("htc", "IEA_15MW_RWT_Monopile.htc"),
    )
    # Not using the highly resolved "*_OpenFASTpolars_*"
    hawc2_dict["pc"] = PC_list().read_pc(
        os.path.join(
            test_path,
            "data",
            "IEA_15MW",
            "HAWC2",
            "IEA-15-240-RWT",
            "IEA_15MW_RWT_pc.dat",
        )
    )
    return hawc2_dict


wio_fname = os.path.join(test_path, "data", "IEA_15MW", "windIO", "IEA-15-240-RWT.yaml")


def test_hawc2_to_windio(tmp_path):
    wio_dict_test = WindIO_dict().read_yaml(wio_fname)

    hawc2_dict = get_hawc2_dict()
    wio_dict = hawc2_to_windio(
        hawc2_dict.as_dict(),
        airfoil_names=[
            "FFA-W3-211",
            "FFA-W3-241",
            "FFA-W3-270blend",
            "FFA-W3-301",
            "FFA-W3-330blend",
            "FFA-W3-360",
            "SNL-FFA-W3-500",
            "Cylinder",
        ],
        pitch_axis=wio_dict_test["components"]["blade"]["outer_shape_bem"][
            "pitch_axis"
        ],
        tilt_location=dict(mbdy2="connector", eulerang_index=1),
        shaft_bodies=["shaft"],
        concentrated_mass=dict(
            hub=dict(name="shaft", index=1),
            nacelle=dict(name="towertop", index=0),
            yaw=dict(name="towertop", index=1),
        ),
        materials=dict(tower=dict(rho=8500)),
    )()
    wio_dict = WindIO_dict(wio_dict)
    wio_dict.write_yaml(os.path.join(tmp_path, "IEA_10MW_h2_to_windio.yaml"))

    # _validate_dicts(wio_dict.as_dict(), wio_dict_test.as_dict())
    test_hawc2_to_windio.wio_dict = wio_dict
    test_hawc2_to_windio.wio_dict_test = wio_dict_test
    test_hawc2_to_windio.hawc2_dict = hawc2_dict
