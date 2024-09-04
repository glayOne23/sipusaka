"""Journal View"""
import operator
import time
from functools import reduce

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render

from apps.sinta.models.journal import Journal


def index(request):
    """list of journal"""
    context = {}

    # Start Time
    start_time = time.time()

    # ===[GET Search]===
    search_text = request.GET.get('search', '')
    context['search_text'] = search_text

    # ===[Fetch Data]===
    journals_data = (
        Journal.objects
        .prefetch_related('article_set')
    )
    if search_text:
        search_list = search_text.split(',')
        # query = reduce(operator.or_, (Q(article__title__icontains = item) for item in search_list))
        query = reduce(operator.or_, (Q(article__title__icontains=item.strip()) for item in search_list))
        journals_data = journals_data.filter(query)

    journals_data = (
        journals_data
        .annotate(total_article=Count('article'))
        .order_by('-impact')
        # .order_by('-id')
    )

    # ===[Fetch Paginator]===
    per_page = 10
    page_number = request.GET.get('page', 1)
    paginator = Paginator(journals_data, per_page)
    journals = paginator.get_page(page_number)
    context['journals'] = journals
    context['tampilkan'] = {
        'from': journals.start_index(),
        'to': journals.end_index(),
        'total': journals.paginator.count
    }

    # End Time
    end_time = time.time()
    query_time = end_time - start_time
    # Print the time taken for the query to execute
    print(f"Query Execution Time: {query_time:.4f} seconds")

    # ===[Render Template]===
    context['page'] = 'journal'
    return render(request, 'landingpage/journal/index.html', context)
