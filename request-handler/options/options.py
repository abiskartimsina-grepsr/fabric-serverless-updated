from typing import TypedDict


class RequestHandlerOptions(TypedDict):
    """Dict for Request Handler options."""

    auto_retry: bool
    crawl_delay_seconds: int
    use_proxy: bool
    max_retries: int
