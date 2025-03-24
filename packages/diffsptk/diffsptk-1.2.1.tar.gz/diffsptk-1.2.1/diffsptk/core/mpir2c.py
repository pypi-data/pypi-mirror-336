# ------------------------------------------------------------------------ #
# Copyright 2022 SPTK Working Group                                        #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
# ------------------------------------------------------------------------ #

import torch
import torch.nn as nn

from ..misc.utils import check_size
from ..misc.utils import clog


class MinimumPhaseImpulseResponseToCepstrum(nn.Module):
    """See `this page <https://sp-nitech.github.io/sptk/latest/main/mpir2c.html>`_
    for details. The conversion uses FFT instead of recursive formula.

    Parameters
    ----------
    cep_order : int >= 0 [scalar]
        Order of cepstrum, :math:`M`.

    ir_length : int >= 1 [scalar]
        Length of impulse response, :math:`N`.

    n_fft : int >> :math:`N` [scalar]
        Number of FFT bins. Accurate conversion requires the large value.

    """

    def __init__(self, cep_order, ir_length, n_fft=512):
        super(MinimumPhaseImpulseResponseToCepstrum, self).__init__()

        self.cep_order = cep_order
        self.ir_length = ir_length
        self.n_fft = n_fft

        assert 0 <= self.cep_order
        assert 1 <= self.ir_length
        assert max(self.cep_order + 1, self.ir_length) < self.n_fft

    def forward(self, h):
        """Convert minimum phase impulse response to cepstrum.

        Parameters
        ----------
        h : Tensor [shape=(..., N)]
            Truncated minimum phase impulse response.

        Returns
        -------
        c : Tensor [shape=(..., M+1)]
            Cepstral coefficients.

        Examples
        --------
        >>> h = diffsptk.ramp(4, 0, -1)
        >>> mpir2c = diffsptk.MinimumPhaseImpulseResponseToCepstrum(3, 5)
        >>> c = mpir2c(h)
        >>> c
        tensor([1.3863, 0.7500, 0.2188, 0.0156])

        """
        check_size(h.size(-1), self.ir_length, "impulse response length")

        H = torch.fft.fft(h, n=self.n_fft)
        c = torch.fft.ifft(clog(H))[..., : self.cep_order + 1].real
        c[..., 1:] *= 2
        return c
