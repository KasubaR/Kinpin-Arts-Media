from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from apps.core.views import SOCIAL_LINKS, _nav_links

from .models import Category, Project, ProjectScopeItem

BEHANCE_URL = 'https://www.behance.net/KinpinArts'


def _portfolio_page_context():
    return {
        'nav_links': _nav_links(),
        'social_links': SOCIAL_LINKS,
        'nav_active_label': 'Our Work',
        'behance_url': BEHANCE_URL,
    }


def _project_queryset():
    return Project.objects.prefetch_related(
        'categories',
        'images',
        Prefetch(
            'scope_items',
            queryset=ProjectScopeItem.objects.order_by('order', 'pk'),
        ),
    ).order_by('order', '-created_at')


def portfolio_list(request):
    projects = _project_queryset()
    categories = (
        Category.objects.annotate(project_count=Count('projects', distinct=True))
        .filter(project_count__gt=0)
        .order_by('name')
    )

    payload = []
    for p in projects:
        behance = (p.behance_url or '').strip()
        payload.append({
            'slug': p.slug,
            'title': p.title,
            'year': p.created_at.year,
            'categories': [c.name for c in p.categories.all()],
            'featured': p.is_featured,
            'image': p.thumbnail.url,
            'description': p.description,
            'detail_url': reverse('portfolio_detail', kwargs={'slug': p.slug}),
            'behance_url': behance,
            'scope': [s.text for s in p.scope_items.all()],
        })

    ctx = _portfolio_page_context()
    ctx.update({
        'projects': projects,
        'categories': categories,
        'projects_payload': payload,
        'project_total': projects.count(),
    })
    return render(request, 'portfolio/list.html', ctx)


def portfolio_detail(request, slug):
    project = get_object_or_404(_project_queryset(), slug=slug)
    related = (
        Project.objects.filter(categories__in=project.categories.all())
        .exclude(pk=project.pk)
        .distinct()
        .prefetch_related('categories')
        .order_by('order', '-created_at')[:6]
    )

    ctx = _portfolio_page_context()
    ctx.update({
        'project': project,
        'related': related,
    })
    return render(request, 'portfolio/detail.html', ctx)
