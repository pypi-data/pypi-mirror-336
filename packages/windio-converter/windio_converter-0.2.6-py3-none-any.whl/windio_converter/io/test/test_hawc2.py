import os
from io import StringIO

import numpy as np
import pytest

import windio_converter.io.hawc2 as hawc2_io
from windio_converter.io.hawc2 import (
    AE_list,
    HAWC2_dict,
    HTC_dict,
    OPT_dict,
    PC_list,
    ST_list,
    read_htc_as_dict,
    write_htc_as_file,
)
from windio_converter.io.test import test_path_io
from windio_converter.io.utils import dict_type, list_type
from windio_converter.test import test_path


def test_load_htc():
    htc_dict, htc_comments = read_htc_as_dict(
        os.path.join(test_path_io, "data", "dummy_test_htc.dat")
    )

    # %% Test reading data %% #
    # new_htc_structure
    assert "new_htc_structure" in htc_dict
    assert "main_body" in htc_dict["new_htc_structure"]
    # main_body 0
    assert htc_dict["new_htc_structure"]["main_body"][0]["name"] == "tower"
    assert "c2_def" in htc_dict["new_htc_structure"]["main_body"][0]
    assert htc_dict["new_htc_structure"]["main_body"][0]["c2_def"]["nsec"] == 3
    assert len(htc_dict["new_htc_structure"]["main_body"][0]["c2_def"]["sec"]) == 3
    assert htc_dict["new_htc_structure"]["main_body"][0]["c2_def"]["sec"][0] == [
        1,
        0.0,
        0.0,
        0.0,
        0.0,
    ]
    assert htc_dict["new_htc_structure"]["main_body"][0]["c2_def"]["sec"][1] == [
        2,
        0.0,
        0.0,
        1.0,
        -10.0,
    ]
    assert htc_dict["new_htc_structure"]["main_body"][0]["c2_def"]["sec"][2] == [
        3,
        0.0,
        0.0,
        100.0,
        5.0,
    ]
    # main_body 1
    assert htc_dict["new_htc_structure"]["main_body"][1]["name"] == "top"
    assert "c2_def" in htc_dict["new_htc_structure"]["main_body"][1]
    assert htc_dict["new_htc_structure"]["main_body"][1]["c2_def"]["nsec"] == 4
    assert len(htc_dict["new_htc_structure"]["main_body"][1]["c2_def"]["sec"]) == 4
    assert htc_dict["new_htc_structure"]["main_body"][1]["c2_def"]["sec"][0] == [
        1,
        0.0,
        0.0,
        0.0,
        0.0,
    ]
    assert htc_dict["new_htc_structure"]["main_body"][1]["c2_def"]["sec"][1] == [
        2,
        0.0,
        0.0,
        1.0,
        -10.0,
    ]
    assert htc_dict["new_htc_structure"]["main_body"][1]["c2_def"]["sec"][2] == [
        3,
        0.0,
        0.0,
        100.0,
        5.0,
    ]
    assert htc_dict["new_htc_structure"]["main_body"][1]["c2_def"]["sec"][3] == [
        4,
        0.0,
        0.0,
        150.0,
        5.0,
    ]

    # hawcstab2
    assert "hawcstab2" in htc_dict
    assert htc_dict["hawcstab2"]["save_power"] == ""

    # aero
    assert "aero" in htc_dict
    assert len(htc_dict["aero"]) == 1
    assert htc_dict["aero"]["ae_filename"] == "[test_inline_tag].dat"
    # hydro
    assert "hydro" in htc_dict
    assert len(htc_dict["hydro"]) == 1
    assert len(htc_dict["hydro"]["hydro_element"]) == 1
    assert htc_dict["hydro"]["hydro_element"]["mbdy_name"] == "test"

    # %% Test comments %% #
    # Initial
    assert_comments(htc_comments, "begin", [" Start comment 0", " Start comment 1"])

    # new_htc_structure
    assert "new_htc_structure" in htc_comments
    nhs = htc_comments["new_htc_structure"]
    assert_comments(nhs, "begin", [" new_htc_structure 1", " new_htc_structure 2"])
    # main_body 0
    assert "main_body" in nhs
    assert isinstance(nhs["main_body"], list) and (len(nhs["main_body"]) == 2)
    mb = nhs["main_body"][0]
    assert_comments(mb, "begin", [" main_body 00", " main_body 01"])
    assert_no_comment(mb, "name")
    assert "c2_def" in mb
    c2 = mb["c2_def"]
    assert_no_comment(c2, "begin")
    assert_no_comment(c2, "nsec")
    assert len(c2["sec"]) == 3
    assert_no_comment(c2, "sec", 0)
    assert_comments(c2, "sec", [" c2_def 02"], 1)
    assert_no_comment(c2, "sec", 2)
    assert_comments(c2, "end", [" c2_def end 0", " c2_def end 1"])
    assert_comments(mb, "end", [" main_body end 00", " main_body end 10"])
    # main_body 1
    mb = nhs["main_body"][1]
    assert_comments(mb, "begin", [" main_body 10"])
    assert_comments(mb, "name", [" top"])
    assert "c2_def" in mb
    c2 = mb["c2_def"]
    assert_comments(c2, "begin", [" c2_def 1"])
    assert_no_comment(c2, "nsec")
    assert len(c2["sec"]) == 4
    assert_no_comment(c2, "sec", 0)
    assert_comments(c2, "sec", [" sec 20", " sec 21"], 1)
    assert_no_comment(c2, "sec", 2)
    assert_comments(c2, "sec", [" sec 40", " sec 41"], 3)
    assert_no_comment(c2, "end")
    assert_no_comment(mb, "end")
    assert_comments(
        nhs, "end", [" new_htc_structure end 0", " new_htc_structure end 1"]
    )

    # hawcstab2
    assert "hawcstab2" in htc_comments
    hs2 = htc_comments["hawcstab2"]
    assert_no_comment(hs2, "begin")
    assert_no_comment(hs2, "save_power")
    assert_no_comment(hs2, "end")

    # aero
    assert "aero" in htc_comments
    aero = htc_comments["aero"]
    assert_comments(aero, "begin", ["$>tag:[test 1 tag]<$"])
    assert_comments(aero, "ae_filename", ["$>tag:[test 1 tag]<$"])
    assert_comments(aero, "end", ["$>tag:[test 1 tag]<$ end of aero block with tag"])

    # hydro
    assert "hydro" in htc_comments
    hydro = htc_comments["hydro"]
    assert_no_comment(hydro, "begin")
    assert_comments(hydro["hydro_element"], "begin", ["$>tag:[test 2 tag]<$"])
    assert_comments(hydro["hydro_element"], "mbdy_name", ["$>tag:[test 2 tag]<$"])
    assert_comments(
        hydro["hydro_element"],
        "end",
        [
            "$>tag:[test 2 tag]<$ end of hydro_element with tag",
            " test tag 2 with new line comment",
        ],
    )
    assert_no_comment(hydro, "end")

    # End of file
    assert_comments(htc_comments, "end", [" end 0", " end 1"])

    # Test recursion limit
    r_limit_old = hawc2_io.recursionlimit
    hawc2_io.recursionlimit = 5
    with pytest.raises(RecursionError):
        htc_dict, htc_comments = read_htc_as_dict(
            os.path.join(test_path_io, "data", "dummy_test_htc.dat")
        )
    hawc2_io.recursionlimit = r_limit_old


def test_htc_continue_in_file(tmp_path):
    # Reading HTC file
    htc_dict = HTC_dict().read_htc(
        os.path.join(test_path_io, "data", "dummy_test_htc.dat")
    )
    htc_str = htc_dict.as_htc(False)
    # Writing output as file
    htc_dict["output"].write_htc(os.path.join(tmp_path, "output.htc"), tmp_path)
    # Remove output block
    htc_dict["output"] = dict(continue_in_file="./output.htc")
    # Write htc file
    htc_fname = os.path.join(tmp_path, "dummy.htc")
    htc_dict.write_htc(htc_fname, tmp_path)

    # Read file with continue in file
    htc_dict = HTC_dict().read_htc(htc_fname, tmp_path)
    assert htc_dict.as_htc(False) == htc_str


def test_save_htc():
    # %% Round trip conversion %% #
    # Load HTC file
    htc_filename = os.path.join(test_path_io, "data", "dummy_test_htc.dat")
    invalid_line, invalid_line_on_com = check_round_trip_htc(htc_filename)

    if invalid_line:
        raise Exception(
            "Round Trip Conversion failed with comments for the following line:\n"
            + "\n".join(
                [f"line {line[0]}: {line[1]} <-> {line[2]}" for line in invalid_line]
            )
        )

    if invalid_line_on_com:
        raise Exception(
            "Round Trip Conversion failed withOUT comments for the following line:\n"
            + "\n".join(
                [
                    f"line {line[0]}: {line[1]} <-> {line[2]}"
                    for line in invalid_line_on_com
                ]
            )
        )


def check_round_trip_htc(htc_filename, remove_whitespace=False, use_HTC_dict=False):
    # %% Round trip conversion %% #
    # Load HTC file
    if use_HTC_dict:
        htc_dict = HTC_dict().read_htc(htc_filename)
        htc_str = htc_dict.as_htc()
    else:
        htc_dict, htc_comments = read_htc_as_dict(htc_filename)

        # Save file (round trip)
        htc_file = StringIO()
        write_htc_as_file(htc_file, htc_dict, htc_comments)
        htc_str = htc_file.getvalue()
    htc_list_str = htc_str.split("\n")

    # Load raw file
    with open(htc_filename, "r") as file:
        htc_list_str_base = file.read().split("\n")

    # Compare files
    assert len(htc_list_str) == len(htc_list_str_base)
    invalid_lines = []
    for iline, (line1, line2) in enumerate(zip(htc_list_str, htc_list_str_base), 1):
        if remove_whitespace:
            if not line1.replace(" ", "").replace("\t", "") == line2.replace(
                " ", ""
            ).replace("\t", ""):
                invalid_lines.append(
                    [
                        iline,
                        line1.replace(" ", "").replace("\t", ""),
                        line2.replace(" ", "").replace("\t", ""),
                    ]
                )
        else:
            if not line1 == line2:
                invalid_lines.append([iline, line1, line2])

    # %% Without comments %% #
    if use_HTC_dict:
        htc_str = htc_dict.as_htc(False)
    else:
        htc_file = StringIO()
        write_htc_as_file(htc_file, htc_dict)
        htc_str = htc_file.getvalue()
    htc_list_str = htc_str.split("\n")
    htc_list_str_base_no_com = [
        line.split(";")[0] + ";"
        for line in htc_list_str_base
        if line.split(";")[0].strip()
    ]
    for iline, line in enumerate(htc_list_str_base_no_com):
        if line.startswith("["):
            htc_list_str_base_no_com[iline] = line.split("] ")[1]
    assert len(htc_list_str) == len(htc_list_str_base_no_com)
    invalid_lines_no_com = []
    for iline, (line1, line2) in enumerate(
        zip(htc_list_str, htc_list_str_base_no_com), 1
    ):
        if remove_whitespace:
            if not line1.replace(" ", "").replace("\t", "") == line2.replace(
                " ", ""
            ).replace("\t", ""):
                invalid_lines_no_com.append(
                    [
                        iline,
                        line1.replace(" ", "").replace("\t", ""),
                        line2.replace(" ", "").replace("\t", ""),
                    ]
                )
        else:
            if not line1 == line2:
                invalid_lines_no_com.append([iline, line1, line2])
    return invalid_lines, invalid_lines_no_com


def assert_no_comment(htc_comments, name, index=None):
    assert name in htc_comments
    if index is None:
        comment = htc_comments[name]
    else:
        assert isinstance(htc_comments[name], list)
        comment = htc_comments[name][index]
    assert isinstance(comment, list) and (len(comment) == 1) and (comment[0] == "")


def assert_comments(htc_comments, name, comments, index=None):
    assert name in htc_comments
    if index is None:
        comment = htc_comments[name]
    else:
        assert isinstance(htc_comments[name], list)
        comment = htc_comments[name][index]
    assert len(comment) == len(comments)
    assert comment == comments


def test_HTC_dict():
    # Round trip conversion
    htc_filename = os.path.join(test_path_io, "data", "dummy_test_htc.dat")
    invalid_line, invalid_line_on_com = check_round_trip_htc(
        htc_filename, use_HTC_dict=True
    )

    if invalid_line:
        raise Exception(
            "Round Trip Conversion failed with comments for the following line:\n"
            + "\n".join(
                [f"line {line[0]}: {line[1]} <-> {line[2]}" for line in invalid_line]
            )
        )

    if invalid_line_on_com:
        raise Exception(
            "Round Trip Conversion failed withOUT comments for the following line:\n"
            + "\n".join(
                [
                    f"line {line[0]}: {line[1]} <-> {line[2]}"
                    for line in invalid_line_on_com
                ]
            )
        )
    # %% Add comments %% #
    with open(htc_filename, "r") as file:
        htc_dict = HTC_dict().from_htc(file.read())

    # Simple header line change (currently has a comment)
    comment = "First line"
    htc_dict.add_comment("begin", comment)  # As a string to append
    assert len(htc_dict.get_comment("begin")) == 3
    assert htc_dict.comments["begin"][-1] == comment
    htc_dict.add_comment("begin", [comment])  # As a list to overwrite
    assert len(htc_dict.comments["begin"]) == 1
    assert htc_dict.comments["begin"][0] == comment
    htc_dict.comments.pop("begin")
    htc_dict.add_comment("begin", comment)  # As a list to overwrite
    assert len(htc_dict.comments["begin"]) == 1
    assert htc_dict.comments["begin"][0] == comment

    # Simple header line change (with no current comment)
    comment = "name tower comment"
    htc_dict["new_htc_structure"]["main_body"][0].add_comment(
        "name", comment
    )  # As a string to append empty should replace
    assert len(htc_dict["new_htc_structure"]["main_body"][0].comments["name"]) == 1
    assert htc_dict["new_htc_structure"]["main_body"][0].comments["name"][0] == comment

    # For repeated blocks
    comment = "1. main-body comment"
    htc_dict["new_htc_structure"]["main_body"][0].add_comment("begin", comment)
    comments = htc_dict["new_htc_structure"].get_comment()
    assert len(comments["main_body"][0]["begin"]) == 3
    assert comments["main_body"][0]["begin"][-1] == comment
    htc_dict["new_htc_structure"]["main_body"][0].add_comment("begin", [comment])
    comments = htc_dict.get_comment("new_htc_structure")
    assert len(comments["main_body"][0]["begin"]) == 1
    assert comments["main_body"][0]["begin"][0] == comment

    # For repeated commands
    comment = "2. aero thrust command"
    # With comment
    htc_dict["output"].add_comment("aero", comment, 1)
    assert len(htc_dict["output"].comments["aero"][1]) == 2
    assert htc_dict["output"].comments["aero"][1][-1] == comment
    # Replace comment
    htc_dict["output"].add_comment("aero", [comment], 1)
    assert len(htc_dict["output"].comments["aero"][1]) == 1
    assert htc_dict["output"].comments["aero"][1][0] == comment
    # No comment
    htc_dict["output"].comments["aero"][1] = []
    htc_dict["output"].add_comment("aero", comment, 1)
    assert len(htc_dict["output"].comments["aero"][1]) == 1
    assert htc_dict["output"].comments["aero"][1][-1] == comment
    # Empty comment
    comment = "1. aero power command"
    htc_dict["output"].add_comment("aero", comment, 0)
    assert len(htc_dict["output"].comments["aero"][0]) == 1
    assert htc_dict["output"].comments["aero"][0][-1] == comment
    # Add a line to main_body.c2_def.sec to not have comments (! Not a read value !)
    htc_dict["new_htc_structure"]["main_body"][0]["c2_def"]["sec"].append(
        [-1, 0.0, 0.0, 0.0, 0.0]
    )
    # Should not fail
    htc_dict.as_htc()

    # %% Functionality %% #
    assert str(htc_dict) == htc_dict.as_htc()
    # Update main body
    htc_dict.update(
        dict(new_htc_structure=dict(main_body=[dict(name="top", new_command=5)]))
    )
    assert htc_dict["new_htc_structure"]["main_body"][1]["new_command"] == 5
    # Return empty dict if no comments
    htc_empty = HTC_dict()
    comments = htc_empty.get_comment()
    assert isinstance(comments, dict) and len(comments) == 0
    # Return empty list if comments=None
    comments = htc_empty.get_comment("key")
    assert isinstance(comments, list) and len(comments) == 0
    # Update top comment
    htc_empty.add_comment("begin", ["New header"])
    htc_dict.update(htc_empty)
    assert htc_dict.get_comment("begin")[0] == "New header"

    # %% Raises %% #
    with pytest.raises(ValueError) as exc_info:
        htc_dict["output"].add_comment("no comment")
    assert exc_info.value.args[0].startswith("`comment` need to be set when `key`")
    with pytest.raises(ValueError) as exc_info:
        htc_dict["output"].add_comment("not a str or list", object())
    assert exc_info.value.args[0].startswith("`comment` need to be a list/str")
    with pytest.raises(ValueError) as exc_info:
        htc_dict["output"].get_comment("## unknown key ##")
    assert exc_info.value.args[0].startswith("## unknown key ## is an unknown")


def test_ae_list():
    test_ae_list.ae_list = ae_list = AE_list().read_ae(
        os.path.join(
            test_path,
            "data",
            "IEA_15MW",
            "HAWC2",
            "IEA-15-240-RWT",
            "IEA_15MW_RWT_ae.dat",
        )
    )
    assert isinstance(ae_list.data[0], dict_type)
    assert AE_list(ae_list.data[0]) == ae_list

    assert str(ae_list) == ae_list.as_ae()


def test_pc_list():
    test_pc_list.pc_list = pc_list = PC_list().read_pc(
        os.path.join(
            test_path,
            "data",
            "IEA_15MW",
            "HAWC2",
            "IEA-15-240-RWT",
            "IEA_15MW_RWT_pc.dat",
        )
    )
    assert isinstance(pc_list.data[0], list_type)
    assert PC_list(pc_list.data[0]) == pc_list

    assert isinstance(pc_list.data[0][0], dict_type)
    assert PC_list(pc_list.data[0][0]) == [[pc_list[0][0]]]

    pc_list2 = PC_list([[pc_list[0][0]]])
    assert isinstance(pc_list2, PC_list)
    assert isinstance(pc_list2[0], PC_list)
    assert isinstance(pc_list2[0][0], dict_type)

    assert str(pc_list) == pc_list.as_pc()
    pc_list.data = pc_list.data[0]
    assert str(pc_list) == pc_list.as_pc()


def test_st_list():
    test_st_list.st_list = st_list = ST_list().read_st(
        os.path.join(
            test_path,
            "data",
            "IEA_15MW",
            "HAWC2",
            "IEA-15-240-RWT",
            "IEA_15MW_RWT_Blade_st_noFPM.st",
        )
    )
    assert len(st_list) == 2
    assert len(st_list[0]) == 2
    assert len(st_list[1]) == 1
    assert isinstance(st_list.data[0], list_type)
    assert ST_list(st_list.data[0]) == [st_list[0]]

    assert isinstance(st_list.data[0][0], dict_type)
    assert ST_list(st_list.data[0][0]) == [[st_list[0][0]]]

    assert str(st_list) == st_list.as_st()


def test_opt_dict(tmp_path):
    opt_dict = OPT_dict().read_opt(
        os.path.join(
            test_path,
            "data",
            "IEA_15MW",
            "HAWC2",
            "IEA-15-240-RWT-Onshore",
            "data",
            "IEA_15MW_RWT_Onshore.opt",
        )
    )
    opt_dict.pop("P")
    opt_dict.pop("T")
    assert ("V0" in opt_dict) and ("pitch" in opt_dict) and ("rotor_speed" in opt_dict)
    assert not ("P" in opt_dict) and not ("T" in opt_dict)
    assert len(opt_dict["V0"]) == 17
    opt_dict.write_opt(os.path.join(tmp_path, "iea15_woPT.opt"))
    opt_rt = OPT_dict().read_opt(os.path.join(tmp_path, "iea15_woPT.opt"))
    assert opt_dict == opt_rt

    opt_dict = OPT_dict().read_opt(
        os.path.join(
            test_path,
            "data",
            "IEA_15MW",
            "HAWC2",
            "IEA-15-240-RWT-Onshore",
            "data",
            "IEA_15MW_RWT_Onshore.opt",
        )
    )
    assert (
        ("V0" in opt_dict)
        and ("pitch" in opt_dict)
        and ("rotor_speed" in opt_dict)
        and ("P" in opt_dict)
        and ("T" in opt_dict)
    )
    assert len(opt_dict["V0"]) == 17
    opt_dict.write_opt(os.path.join(tmp_path, "iea15.opt"))
    opt_rt = OPT_dict().read_opt(os.path.join(tmp_path, "iea15.opt"))
    assert opt_dict == opt_rt


def test_HAWC2_io(tmp_path):
    tmp_path = os.path.join(tmp_path, "IEA_15MW")
    os.makedirs(tmp_path, exist_ok=True)
    hawc2_dict = HAWC2_dict().read_hawc2(
        os.path.join(test_path, "data", "IEA_15MW", "HAWC2", "IEA-15-240-RWT-Onshore"),
        os.path.join("htc", "IEA_15MW_RWT_Onshore.htc"),
    )
    hawc2_dict.write_yaml(os.path.join(tmp_path, "iea_15MW_h2_data.yaml"))
    hawc2_dict.write_hawc2(tmp_path)
    # Convert to python dict and write out
    hawc2_dict.as_dict(True)
    hawc2_dict.write_hawc2(tmp_path)
    # Ensuring that data from dict is converted to relevant object (htc->HTC_dict, ae->AE_list, ..)
    hawc2_dict = HAWC2_dict().read_hawc2(
        os.path.join(test_path, "data", "IEA_15MW", "HAWC2", "IEA-15-240-RWT-Onshore"),
        os.path.join("htc", "IEA_15MW_RWT_Onshore.htc"),
    )
    h2_dict_raw = hawc2_dict.as_dict()
    assert isinstance(h2_dict_raw["htc"], dict)
    assert isinstance(h2_dict_raw["ae"], list)
    assert isinstance(h2_dict_raw["pc"], list)
    assert isinstance(h2_dict_raw["opt"], dict)
    for name, st in h2_dict_raw["st"].items():
        assert isinstance(st, list)
        for s in st:
            for ss in s:
                for name, val in ss.items():
                    assert isinstance(val, list)
    h2_dict = HAWC2_dict(hawc2_dict.as_dict())
    assert isinstance(h2_dict["htc"], HTC_dict)
    assert isinstance(h2_dict["ae"], AE_list)
    assert isinstance(h2_dict["pc"], PC_list)
    assert isinstance(h2_dict["opt"], OPT_dict)
    for name, st in h2_dict["st"].items():
        assert isinstance(st, ST_list)
        # Assert is not empty
        assert len(st) > 0
    # Test that instance is not empty
    assert len(h2_dict["htc"]) > 0
    assert len(h2_dict["ae"]) > 0
    assert len(h2_dict["pc"]) > 0
    assert len(h2_dict["htc"]) > 0
    # Update top comment
    htc_comment = HTC_dict().add_comment("begin", ["New header"])
    hawc2_dict.update(htc=htc_comment)
    assert hawc2_dict["htc"].get_comment("begin")[0] == "New header"
    # Init from dict
    hawc2_dict2 = HAWC2_dict(hawc2_dict.as_dict()).as_dict()
    assert isinstance(hawc2_dict2["htc"], dict)
    assert isinstance(hawc2_dict2["ae"], list)
    assert isinstance(hawc2_dict2["pc"], list)
    assert isinstance(hawc2_dict2["opt"], dict)
    for name, st in hawc2_dict2["st"].items():
        assert isinstance(st, list)
        for s in st:
            for ss in s:
                for name, val in ss.items():
                    assert isinstance(val, list)
    test_HAWC2_io.hawc2_dict = hawc2_dict


def test_hawc2_parametric(tmp_path):
    hawc2_dict = HAWC2_dict().read_hawc2(
        os.path.join(test_path, "data", "IEA_15MW", "HAWC2", "IEA-15-240-RWT-Onshore"),
        os.path.join("htc", "IEA_15MW_RWT_Onshore.htc"),
    )
    h2_update = [
        dict(  # case 1: changing ST-subset and multiplying ST E and G with 1e7
            htc=dict(
                new_htc_structure=dict(
                    main_body=[
                        dict(name="towertop", timoschenko_input=dict(set=[1, 1]))
                    ]
                )
            ),
            st=dict(
                towertop={
                    0: {0: dict(E=lambda arr: arr * 1e7, G=lambda arr: arr * 1e7)}
                }
            ),
        ),
        dict(  # case 2: Update title angle
            htc=dict(
                new_htc_structure=dict(
                    orientation=dict(
                        relative=[
                            dict(mbdy2=["connector", 1], mbdy2_eulerang={1: {0: 10}})
                        ]
                    )
                )
            )
        ),
        dict(  # case 3: remove blade3 main body
            case_path="removed_blade3_mbdy",
            htc=dict(new_htc_structure=dict(main_body={-1: None})),
        ),
    ]
    htc_update = HTC_dict()
    htc_update.add_comment("begin", [" Case 4"])
    h2_update.append(dict(htc=htc_update))
    cases = hawc2_dict.get_hawc2_cases(h2_update)

    # %% Validating cases update %% #
    # Ensuring that the base case is not changed
    # case 1
    case = cases[0]
    assert hawc2_dict["htc"]["new_htc_structure"]["main_body"][1]["timoschenko_input"][
        "set"
    ] == [1, 1]
    assert case["htc"]["new_htc_structure"]["main_body"][1]["timoschenko_input"][
        "set"
    ] == [1, 1]
    np.testing.assert_almost_equal(hawc2_dict["st"]["towertop"][0][0]["E"], 2.1e17, 10)
    np.testing.assert_almost_equal(case["st"]["towertop"][0][0]["E"], 2.1e24, 10)
    np.testing.assert_almost_equal(hawc2_dict["st"]["towertop"][0][0]["G"], 8.08e17, 10)
    np.testing.assert_almost_equal(case["st"]["towertop"][0][0]["G"], 8.08e24, 10)

    # case 2
    case = cases[1]
    assert (
        hawc2_dict["htc"]["new_htc_structure"]["orientation"]["relative"][1][
            "mbdy2_eulerang"
        ][1][0]
        == 6
    )
    assert (
        case["htc"]["new_htc_structure"]["orientation"]["relative"][1][
            "mbdy2_eulerang"
        ][1][0]
        == 10
    )

    # case 3
    case = cases[2]
    assert (
        len(hawc2_dict["htc"]["new_htc_structure"]["main_body"])
        == len(case["htc"]["new_htc_structure"]["main_body"]) + 1
    )
    assert hawc2_dict["htc"]["new_htc_structure"]["main_body"][-1]["name"] == "blade3"
    assert case["htc"]["new_htc_structure"]["main_body"][-1]["name"] == "blade2"

    # case 4
    case = cases[3]
    comment = case["htc"].get_comment("begin")
    assert len(comment) == 1
    assert comment[0] == " Case 4"

    # %% Writing out the cases %% #
    cases_base_path = os.path.join(tmp_path, "cases")
    hawc2_dict.write_hawc2_cases(h2_update, base_path=cases_base_path)

    # case 1
    case = HAWC2_dict().read_hawc2(
        os.path.join(cases_base_path, "case1"),
        os.path.join("htc", "IEA_15MW_RWT_Onshore.htc"),
    )
    assert case["htc"]["new_htc_structure"]["main_body"][1]["timoschenko_input"][
        "set"
    ] == [1, 1]
    np.testing.assert_almost_equal(case["st"]["towertop"][0][0]["E"], 2.1e17, 10)
    np.testing.assert_almost_equal(case["st"]["towertop"][0][0]["G"], 8.08e17, 10)

    # case 2
    case = HAWC2_dict().read_hawc2(
        os.path.join(cases_base_path, "case2"),
        os.path.join("htc", "IEA_15MW_RWT_Onshore.htc"),
    )
    assert (
        case["htc"]["new_htc_structure"]["orientation"]["relative"][1][
            "mbdy2_eulerang"
        ][1][0]
        == 10
    )

    # case 3
    case = HAWC2_dict().read_hawc2(
        os.path.join(cases_base_path, "removed_blade3_mbdy"),
        os.path.join("htc", "IEA_15MW_RWT_Onshore.htc"),
    )
    assert (
        len(hawc2_dict["htc"]["new_htc_structure"]["main_body"])
        == len(case["htc"]["new_htc_structure"]["main_body"]) + 1
    )
    assert hawc2_dict["htc"]["new_htc_structure"]["main_body"][-1]["name"] == "blade3"
    assert case["htc"]["new_htc_structure"]["main_body"][-1]["name"] == "blade2"

    case = HAWC2_dict().read_hawc2(
        os.path.join(cases_base_path, "case4"),
        os.path.join("htc", "IEA_15MW_RWT_Onshore.htc"),
    )
    comment = case["htc"].get_comment("begin")
    assert len(comment) == 1
    assert comment[0] == " Case 4"
