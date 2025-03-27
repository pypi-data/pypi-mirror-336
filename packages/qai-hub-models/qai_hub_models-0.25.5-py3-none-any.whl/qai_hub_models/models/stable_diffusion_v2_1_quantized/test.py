# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import pytest

from qai_hub_models.models._shared.stable_diffusion.test_utils import (
    export_for_component,
)
from qai_hub_models.models.stable_diffusion_v2_1_quantized.demo import main as demo_main
from qai_hub_models.models.stable_diffusion_v2_1_quantized.export import export_model
from qai_hub_models.models.stable_diffusion_v2_1_quantized.model import (
    StableDiffusionQuantized,
)


def test_from_precompiled():
    StableDiffusionQuantized.from_precompiled()


# @pytest.mark.skip("#105 move slow_cloud and slow tests to nightly.")
@pytest.mark.slow_cloud
def test_export():
    export_for_component(export_model, "TextEncoder_Quantized")


# @pytest.mark.skip("#105 move slow_cloud and slow tests to nightly.")
@pytest.mark.slow_cloud
def test_demo():
    demo_main(is_test=True)
