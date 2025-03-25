# Copyright 2024 Advanced Micro Devices, Inc.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Callable, Union

from ..messages import LlmInferenceExecRequest

import shortfin.array as sfnp


class TokenSelectionStrategy(Enum):
    """Supported token selection strategies."""

    GREEDY = auto()


@dataclass
class TokenSelectionStrategyConfig:
    """Configuration for token selection strategies."""

    token_selection_strategy: TokenSelectionStrategy
    prefill_callback: Callable[[LlmInferenceExecRequest], None]
    decode_callback: Callable[[LlmInferenceExecRequest], None]
    results_callback: Callable[[Union[int, List[int]]], None]
    eos_token_id: int
    max_completion_tokens: int


class BaseTokenSelectionStrategy(ABC):
    """Abstract class for implementing token selection strategies."""

    @property
    @abstractmethod
    def token_selection_strategy_config(self) -> TokenSelectionStrategyConfig:
        """Configuration object for defining the parameters of the decode loop.

        Returns:
            TokenSelectionStrategyConfig: Configuration object.
        """
        pass

    async def prefill(self, exec_req: LlmInferenceExecRequest) -> int:
        """Perform standard `prefill` on an LlmInferenceExecRequest.

        This takes an inference exec request and submits it to the batcher
        for prefill. We use greedy token selection to pick our 0th generated
        token.

        Args:
            exec_req (LlmInferenceExecRequest): Execution Request.

        Returns:
            int: Token generated from prefill.
        """
        token_selection_strategy_config = self.token_selection_strategy_config

        token_selection_strategy_config.prefill_callback(exec_req)
        await exec_req.done

        token = sfnp.argmax(exec_req.result_logits)
        token_int = token.items[0]
        token_selection_strategy_config.results_callback(token_int)

        exec_req.input_token_ids.append(token_int)
        exec_req.start_position = len(exec_req.input_token_ids) - 1

    @abstractmethod
    async def decode(self, exec_req: LlmInferenceExecRequest) -> List[int]:
        """Abstract method for generating completion tokens in a decode loop.

        This takes an LlmInferenceExecRequest, that has had prefill invoked
        on it. It then handles the logic of submitting decode requests to
        the batcher, in a loop, in order to generate a list of tokens.

        Args:
            exec_req (LlmInferenceExecRequest): Execution Request that has had prefill invoked on it.

        Returns:
            List[int]: A list of tokens generated from decode loop.
        """
        pass
