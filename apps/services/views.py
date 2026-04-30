from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.models import ContactInquiry
from apps.core.views import PROCESS_STEPS, SOCIAL_LINKS, _nav_links

from .models import Service, ServiceFeature

SERVICES_CONTACT_META = [
    {'icon': '📍', 'label': 'Location', 'value': 'Lusaka, Zambia'},
    {'icon': '✉️', 'label': 'Email', 'value': 'hello@kinpinarts.com'},
    {'icon': '📞', 'label': 'Phone', 'value': '+260 977 000 000'},
]


def _services_page_context():
    footer_qs = Service.objects.order_by('order', 'title')
    return {
        'nav_links': _nav_links(),
        'social_links': SOCIAL_LINKS,
        'nav_active_label': 'Services',
        'process_steps': PROCESS_STEPS,
        'contact_meta': SERVICES_CONTACT_META,
        'services_for_footer': footer_qs,
    }


def services_list(request):
    if request.method == 'POST' and request.POST.get('form_type') == 'services_contact':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        service = request.POST.get('service', '').strip()
        message = request.POST.get('message', '').strip()
        subject = service if service else 'Services page inquiry'
        if name and email and message:
            ContactInquiry.objects.create(
                name=name,
                email=email,
                phone='',
                subject=subject,
                message=message,
            )
            messages.success(request, "Thanks! We'll get back to you within 24 hours.")
            return redirect('services')
        messages.error(request, 'Please fill in all required fields.')
        return redirect('services')

    services = Service.objects.prefetch_related(
        Prefetch('features', queryset=ServiceFeature.objects.order_by('order'))
    ).order_by('order', 'title')

    ctx = _services_page_context()
    ctx['services'] = services
    return render(request, 'services/list.html', ctx)


def service_detail(request, slug):
    service = get_object_or_404(
        Service.objects.prefetch_related(
            Prefetch('features', queryset=ServiceFeature.objects.order_by('order'))
        ),
        slug=slug,
    )
    other_services = (
        Service.objects.exclude(pk=service.pk).order_by('order', 'title')[:8]
    )

    ctx = _services_page_context()
    ctx['service'] = service
    ctx['other_services'] = other_services
    return render(request, 'services/detail.html', ctx)
