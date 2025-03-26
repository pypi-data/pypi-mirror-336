"""
This shows how to define your extension client
"""

from diracx.client.patches.utils import DiracClientMixin

from lhcbdiracx.client.generated._client import Dirac as LHCbDiracxGenerated


class LHCbDiracxClient(DiracClientMixin, LHCbDiracxGenerated): ...
