from typing import Any

from django.core.paginator import Paginator

from app.core.constants import PAGE, PER_PAGE


def paginate_queryset(
    queryset,
    page: int = PAGE,
    per_page: int = PER_PAGE,
) -> dict[str, Any]:
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    return {
        "items": page_obj.object_list,
        "currentPage": page,
        "lastPage": paginator.num_pages,
    }
