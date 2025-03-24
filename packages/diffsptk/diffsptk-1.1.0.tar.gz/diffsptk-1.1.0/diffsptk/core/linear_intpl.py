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

import torch.nn as nn
import torch.nn.functional as F


class LinearInterpolation(nn.Module):
    """Perform linear interpolation.

    Note that this is not for linear_intpl in C/C++ version of SPTK, but for
    filter coefficients interpolation in digital filtering.

    Parameters
    ----------
    upsampling_factor : int >= 1 [scalar]
        Upsampling factor, :math:`P`.

    """

    def __init__(self, upsampling_factor):
        super(LinearInterpolation, self).__init__()

        self.upsampling_factor = upsampling_factor

        assert 1 <= self.upsampling_factor

        self.pad = nn.ReplicationPad1d((0, 1))

    def forward(self, x):
        """Interpolate filter coefficients.

        Parameters
        ----------
        x : Tensor [shape=(B, N, D) or (N, D) or (N,)]
            Filter coefficients.

        Returns
        -------
        y : Tensor [shape=(B, NxP, D) or (NxP, D) or (NxP,)]
            Upsampled filter coefficients.

        Examples
        --------
        >>> x = diffsptk.ramp(2)
        >>> x
        tensor([0., 1., 2.])
        >>> linear_intpl = diffsptk.LinearInterpolation(2)
        >>> y = linear_intpl(x)
        >>> y
        tensor([0.0000, 0.5000, 1.0000, 1.5000, 2.0000, 2.0000])

        """
        # Pass through if upsampling factor is one.
        if self.upsampling_factor == 1:
            return x

        d = x.dim()
        if d == 1:
            x = x.view(1, -1, 1)
        elif d == 2:
            x = x.unsqueeze(0)
        assert x.dim() == 3, "Input must be 3D tensor"
        B, T, D = x.shape

        x = x.mT
        x = self.pad(x)
        x = F.interpolate(
            x,
            size=T * self.upsampling_factor + 1,
            mode="linear",
            align_corners=True,
        )[
            ..., :-1
        ]  # Remove the padded value.
        y = x.mT.reshape(B, -1, D)

        if d == 1:
            y = y.view(-1)
        elif d == 2:
            y = y.squeeze(0)
        return y
