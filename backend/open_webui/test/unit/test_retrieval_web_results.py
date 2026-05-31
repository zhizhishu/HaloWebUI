import asyncio
import pathlib
import sys
from types import SimpleNamespace

_BACKEND_DIR = pathlib.Path(__file__).resolve().parents[3]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from open_webui.retrieval.web.main import SearchResult  # noqa: E402
from open_webui.routers import retrieval as retrieval_module  # noqa: E402
from open_webui.routers.retrieval import (  # noqa: E402
    SearchForm,
    _build_direct_docs_from_web_results,
    process_web_search,
)


def test_build_direct_docs_from_web_results_preserves_content_without_urls():
    payload = _build_direct_docs_from_web_results(
        "今天热点",
        [
            SearchResult(
                link="",
                title="Grok Search Result",
                snippet="这是直接传递给主模型的全文内容。",
            )
        ],
        "grok",
    )

    assert payload is not None
    assert payload["loaded_count"] == 1
    assert payload["direct_content_only"] is True
    assert payload["docs"][0]["content"] == "这是直接传递给主模型的全文内容。"
    metadata = payload["docs"][0]["metadata"]
    assert metadata["engine"] == "grok"
    assert metadata["source_type"] == "search_summary"
    assert metadata["internal_source"] is True
    assert metadata["display_source"] == "grok 搜索摘要"
    assert metadata["content"] == "这是直接传递给主模型的全文内容。"
    assert metadata["snippet"] == "这是直接传递给主模型的全文内容。"
    assert "url" not in metadata
    assert payload["filenames"][0].startswith("grok://search/")


def test_process_web_search_uses_search_snippets_when_loader_returns_no_docs(
    monkeypatch,
):
    request = SimpleNamespace(
        app=SimpleNamespace(
            state=SimpleNamespace(
                config=SimpleNamespace(
                    WEB_SEARCH_ENGINE="searxng",
                    WEB_LOADER_ENGINE="safe_web",
                    BYPASS_WEB_SEARCH_EMBEDDING_AND_RETRIEVAL=False,
                )
            )
        )
    )

    monkeypatch.setattr(
        retrieval_module,
        "search_web",
        lambda request, engine, query: [
            SearchResult(
                link="https://example.com/result",
                title="Example Result",
                snippet="Search result summary that should still be injected.",
            )
        ],
    )

    async def load_no_documents(*args, **kwargs):
        return []

    monkeypatch.setattr(
        retrieval_module,
        "_load_web_documents_with_loader",
        load_no_documents,
    )

    payload = asyncio.run(
        process_web_search(
            request,
            SearchForm(query="python docs"),
            user=SimpleNamespace(),
        )
    )

    assert payload["direct_content_only"] is True
    assert payload["docs"][0]["content"] == (
        "Search result summary that should still be injected."
    )
    assert payload["docs"][0]["metadata"]["source"] == "https://example.com/result"
