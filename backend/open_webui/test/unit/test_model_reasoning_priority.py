import pathlib
import sys


_BACKEND_DIR = pathlib.Path(__file__).resolve().parents[3]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from open_webui.utils.payload import (
    apply_model_params_to_body_ollama,
    apply_model_params_to_body_openai,
)


def test_apply_model_params_to_body_openai_preserves_explicit_reasoning_effort():
    payload = {"reasoning_effort": "low", "temperature": 0.3}

    result = apply_model_params_to_body_openai(
        {"reasoning_effort": "high", "temperature": 0.8},
        payload,
    )

    assert result["reasoning_effort"] == "low"
    assert result["temperature"] == 0.3


def test_apply_model_params_to_body_openai_preserves_explicit_sampling_params():
    payload = {
        "temperature": 0.3,
        "top_p": 0.4,
        "max_tokens": 512,
    }

    result = apply_model_params_to_body_openai(
        {
            "temperature": 0.8,
            "top_p": 0.9,
            "max_tokens": 2048,
            "frequency_penalty": 0.2,
        },
        payload,
    )

    assert result["temperature"] == 0.3
    assert result["top_p"] == 0.4
    assert result["max_tokens"] == 512
    assert result["frequency_penalty"] == 0.2


def test_apply_model_params_to_body_ollama_preserves_explicit_options():
    payload = {
        "temperature": 0.3,
        "top_p": 0.4,
        "max_tokens": 512,
    }

    result = apply_model_params_to_body_ollama(
        {
            "temperature": 0.8,
            "top_p": 0.9,
            "max_tokens": 2048,
            "repeat_penalty": 1.1,
        },
        payload,
    )

    assert result["temperature"] == 0.3
    assert result["top_p"] == 0.4
    assert result["num_predict"] == 512
    assert "max_tokens" not in result
    assert result["repeat_penalty"] == 1.1


def test_apply_model_params_to_body_openai_uses_model_reasoning_effort_when_missing():
    result = apply_model_params_to_body_openai({"reasoning_effort": "high"}, {})

    assert result["reasoning_effort"] == "high"


def test_apply_model_params_to_body_openai_preserves_explicit_reasoning_off():
    result = apply_model_params_to_body_openai(
        {"reasoning_effort": "high"},
        {"reasoning_effort": "none"},
    )

    assert result["reasoning_effort"] == "none"
