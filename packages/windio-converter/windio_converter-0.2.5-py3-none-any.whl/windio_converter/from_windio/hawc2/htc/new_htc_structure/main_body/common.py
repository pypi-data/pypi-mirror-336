import aesoptparam as apm

from ....common import windio_to_hawc2_child


class main_body_base(windio_to_hawc2_child):

    def get_mbdy_base(self, imbdy=None):
        name = self.get_full_mbdy_name(self.mbdy_name, imbdy)
        return dict(
            name=name,
            type="timoschenko",
            nbodies=self.nbodies,
            node_distribution="c2_def",
            timoschenko_input=dict(filename=self.filename, set=[1, 1]),
            c2_def=dict(),
        )
