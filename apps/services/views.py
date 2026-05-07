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
_ICON_WHATSAPP = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="currentColor" class="w-5 h-5"><path d="M19.11 17.27c-.29-.14-1.7-.84-1.96-.94-.26-.1-.45-.14-.64.14-.19.29-.73.94-.9 1.13-.17.19-.33.22-.62.07-.29-.14-1.2-.44-2.28-1.41-.84-.75-1.4-1.68-1.56-1.96-.16-.29-.02-.44.12-.58.12-.12.29-.33.43-.5.14-.17.19-.29.29-.48.1-.19.05-.36-.02-.5-.07-.14-.64-1.55-.88-2.12-.23-.55-.47-.47-.64-.48h-.55c-.19 0-.5.07-.76.36-.26.29-1 1-.97 2.45.02 1.45 1.04 2.85 1.19 3.05.14.19 2.03 3.1 4.92 4.34.69.3 1.23.48 1.65.61.69.22 1.32.19 1.81.12.55-.08 1.7-.69 1.94-1.36.24-.67.24-1.24.17-1.36-.07-.12-.26-.19-.55-.33z"/><path d="M27.52 4.48A15.86 15.86 0 0 0 16 0C7.16 0 0 7.16 0 16c0 2.82.74 5.57 2.14 8l-2.27 8.29 8.49-2.23A15.92 15.92 0 0 0 16 32c8.84 0 16-7.16 16-16 0-4.28-1.67-8.3-4.48-11.52zM16 29.27c-2.45 0-4.86-.65-6.97-1.88l-.5-.29-5.04 1.32 1.35-4.91-.33-.51A13.2 13.2 0 0 1 2.73 16C2.73 8.67 8.67 2.73 16 2.73c3.53 0 6.85 1.37 9.35 3.87 2.5 2.5 3.87 5.82 3.87 9.4-.01 7.33-5.95 13.27-13.22 13.27z"/></svg>'


def _services_contact_meta():
    meta = [
        {'icon': _ICON_MAP_PIN, 'label': loc['label'], 'lines': loc['lines']}
        for loc in OFFICE_LOCATIONS
    ]
    meta.extend(
        [
            {'icon': _ICON_ENVELOPE, 'label': 'Email', 'value': 'Info@kinpinarts.com'},
            {'icon': _ICON_PHONE, 'label': 'Phone', 'value': '+260 965 023 606'},
            {'icon': _ICON_WHATSAPP, 'label': 'WhatsApp', 'value': '+260 965 023 606', 'href': 'https://wa.me/260965023606'},
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
