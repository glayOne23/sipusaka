"""Journal View"""
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render

from apps.sinta.models.journal import Journal


def index(request):
    """list of journal"""

    context = {}

    # ===[GET Search]===
    search_text = request.GET.get('search', '')
    context['search_text'] = search_text

    # ===[Fetch Data]===
    journals_data = (
        Journal.objects
        .filter(article__title__icontains=search_text)
        .annotate(total_article=Count('article'))
        .all()
        # .order_by('-impact')
        .order_by('id')
    )

    # ===[Fetch Paginator]===
    per_page = 10
    page_number = request.GET.get('page', 1)
    paginator = Paginator(journals_data, per_page)
    journals = paginator.get_page(page_number)
    context['journals'] = journals
    dari = journals.number if journals.number == 1 else ((journals.number-1) * per_page) + 1
    context['tampilkan'] = {
    'from': dari,
    'to': journals.object_list.count() if journals.number == 1 else dari + journals.object_list.count() - 1,
    'total': journals_data.count()
    }

    # ===[Render Template]===
    context['page'] = 'journal'
    return render(request, 'landingpage/journal/index.html', context)
