from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.models import ContactInquiry
from apps.core.site_content import OFFICE_LOCATIONS
from apps.core.views import PROCESS_STEPS, SOCIAL_LINKS, _nav_links

from .models import Service, ServiceFeature


_ICON_MAP_PIN = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z"/></svg>'
_ICON_ENVELOPE = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75"/></svg>'
_ICON_PHONE = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z"/></svg>'


def _services_contact_meta():
    meta = [
        {'icon': _ICON_MAP_PIN, 'label': loc['label'], 'lines': loc['lines']}
        for loc in OFFICE_LOCATIONS
    ]
    meta.extend(
        [
            {'icon': _ICON_ENVELOPE, 'label': 'Email', 'value': 'Info@kinpinarts.com'},
            {'icon': _ICON_PHONE, 'label': 'Phone', 'value': '+260 975 587 617'},
        ]
    )
    return meta


def _services_page_context():
    footer_qs = Service.objects.order_by('order', 'title')
    return {
        'nav_links': _nav_links(),
        'social_links': SOCIAL_LINKS,
        'nav_active_label': 'Services',
        'process_steps': PROCESS_STEPS,
        'contact_meta': _services_contact_meta(),
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
