from typing import Any, Optional, Protocol, List, Dict
from requests import Response


class RequestFunction(Protocol):
    def __call__(self, __endpoint: str, *args: Any, **kwargs: Any) -> Response: ...


def get_paged_data(
    request_function: RequestFunction, 
    endpoint: str, 
    data_key: str,
    next_key: str = 'links',
    max_pages: int = -1, 
    *request_args: Any, 
    **request_kwargs: Any
) -> List[Dict]:
    """
    Schoology requests which deal with large amounts of data are paged.
    This function automatically sends the several paged requests and combines the data
    """
    data = []
    page = 0
    next_url: Optional[str] = ''
    while next_url is not None and (page < max_pages or max_pages == -1):
        res = request_function(next_url if next_url else endpoint, *request_args, **request_kwargs)
        json = res.json()

        next_url = json[next_key].get('next')
        data += json[data_key]
        page += 1

    return data
