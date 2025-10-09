from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_queryset(request, queryset, items_per_page=9):
    """
    Takes a request, a QuerySet, and returns a paginated Page object.
    
    Args:
        request: The HttpRequest object.
        queryset: The Django QuerySet to be paginated.
        items_per_page: The number of items to show on each page.
        
    Returns:
        A django.core.paginator.Page object.
    """
    
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)
        
    return page_obj