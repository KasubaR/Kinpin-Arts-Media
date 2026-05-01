from apps.core.site_content import OFFICE_LOCATIONS
from apps.services.models import Service


def global_context(request):
    nav_links = [
        {'label': 'Home',      'href': '/'},
        {'label': 'Services',  'href': '/services/'},
        {'label': 'Our Work',  'href': '/portfolio/'},
        {'label': 'About Us',  'href': '/about/'},
    ]

    social_links = [
        {'icon': 'Be', 'href': 'https://www.behance.net/KinpinArts'},
        {'icon': 'in', 'href': 'https://www.linkedin.com/company/kinpin-arts-media'},
        {'icon': 'IG', 'href': 'https://www.instagram.com/kinpinarts'},
        {'icon': 'FB', 'href': 'https://www.facebook.com/kinpinarts'},
    ]

    services = Service.objects.all().order_by('order')[:8]

    behance_url = 'https://www.behance.net/KinpinArts'

    # Determine active nav label
    path = request.path
    nav_active_label = 'Home'
    for link in nav_links:
        if link['href'] != '/' and path.startswith(link['href']):
            nav_active_label = link['label']
            break

    return {
        'nav_links': nav_links,
        'social_links': social_links,
        'services': services,
        'behance_url': behance_url,
        'nav_active_label': nav_active_label,
        'office_locations': OFFICE_LOCATIONS,
    }
