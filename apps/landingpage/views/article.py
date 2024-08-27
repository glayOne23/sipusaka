"""Article View"""
from django.core.paginator import Paginator
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
        .filter(title__icontains=search_text)
        .order_by('-id')
    )

    # ===[Fetch Paginator]===
    per_page = 10
    page_number = request.GET.get('page', 1)
    paginator = Paginator(articles_data, per_page)
    articles = paginator.get_page(page_number)
    context['articles'] = articles
    dari = articles.number if articles.number == 1 else ((articles.number-1) * per_page) + 1
    context['tampilkan'] = {
    'from': dari,
    'to': articles.object_list.count() if articles.number == 1 else dari + articles.object_list.count() - 1,
    'total': articles_data.count()
    }

    # ===[Render Template]===
    context['page'] = 'article'
    return render(request, 'landingpage/article/index.html', context)
