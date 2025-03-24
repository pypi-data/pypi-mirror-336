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

import numpy as np
import torch
import torch.nn as nn

from ..misc.utils import numpy_to_torch


class NegativeDerivativeOfPhaseSpectrumToCepstrum(nn.Module):
    """See `this page <https://sp-nitech.github.io/sptk/latest/main/ndps2c.html>`_
    for details.

    Parameters
    ----------
    cep_order : int >= 0 [scalar]
        Order of cepstrum, :math:`M`.

    fft_length : int >= 2 [scalar]
        Number of FFT bins, :math:`L`.

    """

    def __init__(self, cep_order, fft_length):
        super(NegativeDerivativeOfPhaseSpectrumToCepstrum, self).__init__()

        self.cep_order = cep_order
        half_fft_length = fft_length // 2

        assert 0 <= self.cep_order
        assert 2 <= fft_length
        assert self.cep_order <= half_fft_length

        ramp = np.arange(self.cep_order + 1, dtype=np.float64) * half_fft_length
        if self.cep_order == half_fft_length:
            ramp[-1] *= 2
        ramp[1:] = 1 / ramp[1:]
        self.register_buffer("ramp", numpy_to_torch(ramp))

    def forward(self, n):
        """Convert NPDS to cepstrum.

        Parameters
        ----------
        n : Tensor [shape=(..., L/2+1)]
            NDPS.

        Returns
        -------
        c : Tensor [shape=(..., M+1)]
            Cepstrum.

        Examples
        --------
        >>> n = diffsptk.ramp(4)
        >>> ndps2c = diffsptk.NegativeDerivativeOfPhaseSpectrumToCepstrum(4, 8)
        >>> c = ndps2c(n)
        >>> c
        tensor([ 0.0000, -1.7071,  0.0000, -0.0976,  0.0000])

        """
        c = torch.fft.hfft(n)[..., : self.cep_order + 1]
        c = c * self.ramp
        return c
