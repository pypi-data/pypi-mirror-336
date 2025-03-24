# -------------------------------------------------------------------------------
# (c) Copyright 2022 Sony Semiconductor Israel, Ltd. All rights reserved.
#
#      This software, in source or object form (the "Software"), is the
#      property of Sony Semiconductor Israel Ltd. (the "Company") and/or its
#      licensors, which have all right, title and interest therein, You
#      may use the Software only in accordance with the terms of written
#      license agreement between you and the Company (the "License").
#      Except as expressly stated in the License, the Company grants no
#      licenses by implication, estoppel, or otherwise. If you are not
#      aware of or do not agree to the License terms, you may not use,
#      copy or modify the Software. You may use the source code of the
#      Software only for your internal purposes and may not distribute the
#      source code of the Software, any part thereof, or any derivative work
#      thereof, to any third party, except pursuant to the Company's prior
#      written consent.
#      The Software is the confidential information of the Company.
# -------------------------------------------------------------------------------
from abc import ABC
from typing import Optional, List

import numpy as np

from . import NnirNode, Variable


class BinaryOp(NnirNode, ABC):
    NUM_INPUTS = 2
    NUM_OUTPUTS = 1

    def _check_input_const(self, index: Optional[int], val) -> bool:
        """ Returns True if the input is Variable and all its values are val.
            If index is None, checks whether exactly one of the inputs is such const """
        input_nodes: List[NnirNode] = self.graph_ctx.get_in_nodes()
        consts = [(i, n) for i, n in enumerate(input_nodes) if isinstance(n, Variable)]
        if len(consts) != 1 or index is not None and consts[0][0] != index:
            return False
        return bool(np.all(consts[0][1].data == val))
