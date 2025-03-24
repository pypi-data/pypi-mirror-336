###############################################################################
# Copyright (c) 2024 MyTorch Systems Inc. All rights reserved.
###############################################################################
from .PreTrainedTokenizerBase import PreTrainedTokenizerBase

class PreTrainedTokenizerFast(PreTrainedTokenizerBase):

    def __init__(self, uuid=None, special_tokens: dict = None):
        super().__init__(uuid, special_tokens)

