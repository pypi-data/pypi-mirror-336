from ..common import windio_to_hawc2_child


class st_base(windio_to_hawc2_child):

    def header_FPM(self):
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

    def header_classic(self):
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
