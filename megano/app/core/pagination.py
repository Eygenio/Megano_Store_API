from math import ceil
from django.core.paginator import Paginator

def paginate_queryset(queryset, request, per_page=8):
    page = int(request.GET.get("currentPage", 1))
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)

    return {
        "items": page_obj.object_list,
        "current_page": page,
        "lastPage": paginator.num_pages
    }
