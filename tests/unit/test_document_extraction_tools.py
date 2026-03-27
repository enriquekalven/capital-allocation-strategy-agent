# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for the Market Intelligence Agent tools (document extraction)."""

import pytest
from unittest.mock import MagicMock
from capital_allocation_strategy_agent.sub_agents.document_extraction.tools import inject_document_into_request


class TestInjectDocumentIntoRequest:
    def test_no_document_leaves_request_untouched(self):
        mock_context = MagicMock()
        mock_context.state = {}
        
        mock_request = MagicMock()
        mock_request.contents = []

        inject_document_into_request(mock_context, mock_request)

        # The list should remain empty (and no crashes!)
        assert len(mock_request.contents) == 0

    def test_document_is_injected_successfully(self):
        mock_context = MagicMock()
        mock_context.state = {
            "inline_document": {
                "mime_type": "application/pdf",
                "data": "Q29udGVudHM="  # "Contents" encoded in base64
            }
        }
        
        mock_request = MagicMock()
        mock_request.contents = []

        inject_document_into_request(mock_context, mock_request)

        assert len(mock_request.contents) == 1
        assert "application/pdf" in str(mock_request.contents[0])
