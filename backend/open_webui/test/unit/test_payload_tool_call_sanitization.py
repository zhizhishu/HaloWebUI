from open_webui.utils.payload import sanitize_incomplete_tool_call_messages


def test_sanitize_keeps_complete_tool_call_group():
    payload = {
        "messages": [
            {"role": "user", "content": "run a tool"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {"name": "run_command", "arguments": "{}"},
                    }
                ],
            },
            {"role": "tool", "tool_call_id": "call_1", "content": "ok"},
            {"role": "assistant", "content": "done"},
        ]
    }

    assert sanitize_incomplete_tool_call_messages(payload) == payload


def test_sanitize_drops_incomplete_stopped_tool_call_group():
    payload = {
        "model": "test-model",
        "messages": [
            {"role": "user", "content": "run a tool"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {"name": "run_command", "arguments": "{}"},
                    }
                ],
            },
            {"role": "user", "content": "try again"},
        ],
    }

    assert sanitize_incomplete_tool_call_messages(payload) == {
        "model": "test-model",
        "messages": [
            {"role": "user", "content": "run a tool"},
            {"role": "user", "content": "try again"},
        ],
    }


def test_sanitize_preserves_visible_assistant_text_when_tool_result_is_missing():
    payload = {
        "messages": [
            {"role": "user", "content": "check this"},
            {
                "role": "assistant",
                "content": "I will check that.",
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {"name": "search_web", "arguments": '{"query":"x"}'},
                    }
                ],
            },
            {"role": "assistant", "content": "new response"},
        ]
    }

    assert sanitize_incomplete_tool_call_messages(payload)["messages"] == [
        {"role": "user", "content": "check this"},
        {"role": "assistant", "content": "I will check that."},
        {"role": "assistant", "content": "new response"},
    ]


def test_sanitize_drops_orphan_tool_results():
    payload = {
        "messages": [
            {"role": "user", "content": "hello"},
            {"role": "tool", "tool_call_id": "call_missing", "content": "orphan"},
            {"role": "assistant", "content": "answer"},
        ]
    }

    assert sanitize_incomplete_tool_call_messages(payload)["messages"] == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "answer"},
    ]


def test_sanitize_drops_extra_tool_result_after_complete_group():
    payload = {
        "messages": [
            {"role": "user", "content": "hello"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {"name": "a", "arguments": "{}"},
                    }
                ],
            },
            {"role": "tool", "tool_call_id": "call_1", "content": "ok"},
            {"role": "tool", "tool_call_id": "call_2", "content": "extra"},
        ]
    }

    assert sanitize_incomplete_tool_call_messages(payload)["messages"] == [
        {"role": "user", "content": "hello"},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {"name": "a", "arguments": "{}"},
                }
            ],
        },
        {"role": "tool", "tool_call_id": "call_1", "content": "ok"},
    ]
