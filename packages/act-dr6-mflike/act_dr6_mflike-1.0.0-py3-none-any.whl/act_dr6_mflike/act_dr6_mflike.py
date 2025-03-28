""".. module:: ACTDR6MFLike

:Synopsis: Definition of python-native CMB likelihood for ACT DR6 data release.

:Author: ACT Collaboration

"""

from mflike.mflike import _MFLike


class ACTDR6MFLike(_MFLike):
    """
    Likelihood for ACT DR6 data release (2022)
    """

    file_base_name = "act_dr6"

    install_options = {
        "download_url": "https://lambda.gsfc.nasa.gov/data/act/pspipe/sacc_files/dr6_data.tar.gz"
    }
