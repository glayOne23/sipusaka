"""Article View"""
import operator
from functools import reduce

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.sinta.models.article import Article
from apps.sinta.models.journal import Journal


def index(request, journal_id):
    """list of article"""

    context = {}

    # ===[GET Search]===
    search_text = request.GET.get('search', '')
    context['search_text'] = search_text

    # ===[Fetch Data]===
    journal_obj = get_object_or_404(Journal, pk=journal_id)
    context['journal_obj'] = journal_obj

    articles_data = (
        Article.objects
        .filter(journal=journal_obj)
        .order_by('-id')
    )

    if search_text:
        search_list = search_text.split(',')
        query = reduce(operator.or_, (Q(title__icontains = item) for item in search_list))
        articles_data = articles_data.filter(query)

    # ===[Fetch Paginator]===
    per_page = 10
    page_number = request.GET.get('page', 1)
    paginator = Paginator(articles_data, per_page)
    articles = paginator.get_page(page_number)
    context['articles'] = articles
    context['tampilkan'] = {
        'from': articles.start_index(),
        'to': articles.end_index(),
        'total': articles.paginator.count
    }

    # ===[Render Template]===
    context['page'] = 'article'
    return render(request, 'landingpage/article/index.html', context)
