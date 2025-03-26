"""
This shows how to define your extension aio client
"""

from __future__ import annotations

from diracx.client.patches.aio.utils import DiracClientMixin

from lhcbdiracx.client.generated.aio._client import Dirac as LHCbDiracxGenerated


class LHCbDiracxClient(DiracClientMixin, LHCbDiracxGenerated): ...
