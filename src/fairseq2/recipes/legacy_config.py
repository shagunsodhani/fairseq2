# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from fairseq2.dependency import DependencyResolver
from fairseq2.recipes.checkpoint import ScoreConfig
from fairseq2.recipes.config_manager import StandardConfigManager
from fairseq2.recipes.gang import GangConfig
from fairseq2.typing import DataClass


def _set_legacy_config(resolver: DependencyResolver, config: DataClass) -> None:
    config_dict: dict[str, object] = {}

    def set_gang_config() -> None:
        monitored_gang = getattr(config, "monitored_gang", False)

        tensor_parallel_size = getattr(config, "tensor_parallel_size", 1)

        config_dict["gang"] = GangConfig(
            monitored=monitored_gang,
            tensor_parallel_size=tensor_parallel_size,
        )

    def set_checkpoint_search_dir() -> None:
        search_dir = getattr(config, "resume_checkpoint_dir", None)
        if search_dir is None:
            search_dir = getattr(config, "checkpoint_dir", None)

        config_dict["checkpoint_search_dir"] = search_dir

    def set_score_config() -> None:
        score_metric = getattr(config, "score_metric", None)
        if score_metric is not None:
            lower_score_better = getattr(config, "lower_score_better", False)

            config_dict["score"] = ScoreConfig(
                metric=score_metric,
                lower_better=lower_score_better,
            )

    set_gang_config()
    set_checkpoint_search_dir()
    set_score_config()

    config_manager = resolver.resolve(StandardConfigManager)

    config_manager.update_config_dict(config_dict)
