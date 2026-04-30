from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.portfolio.models import Project
from apps.services.models import Service, ServiceFeature

from .models import ClientLogo, ContactInquiry, NewsletterSubscriber, Testimonial

PROCESS_STEPS = [
    {'title': 'Discovery', 'desc': 'Deep-dive into your brand, goals, and audience through research and consultation.'},
    {'title': 'Design', 'desc': 'Translating insights into compelling visual concepts aligned with your identity.'},
    {'title': 'Development', 'desc': 'Bringing designs to life — responsive, functional, and meticulously crafted.'},
    {'title': 'Launch & Support', 'desc': 'Flawless delivery and post-launch guidance to maximise your new presence.'},
]

STATS = [
    {'value': '7+', 'label': 'Years of Experience', 'sub': 'In the creative industry'},
    {'value': '100+', 'label': 'Projects Delivered', 'sub': 'Across all service areas'},
    {'value': '98%', 'label': 'Client Satisfaction', 'sub': 'Long-term partnerships'},
    {'value': '13+', 'label': 'Active Clients', 'sub': 'Zambia & beyond'},
]

SOCIAL_LINKS = [
    {'name': 'Behance', 'icon': 'Be', 'href': 'https://www.behance.net/KinpinArts'},
    {'name': 'Instagram', 'icon': 'IG', 'href': '#'},
    {'name': 'LinkedIn', 'icon': 'in', 'href': '#'},
    {'name': 'X', 'icon': 'X', 'href': '#'},
]

ABOUT_MILESTONES = [
    {
        'year': '2017',
        'title': 'Studio Founded',
        'desc': 'Kinpin Arts opened its doors as a freelance design studio in Lusaka, taking on local branding and print projects.',
    },
    {
        'year': '2018',
        'title': 'First Major Client',
        'desc': 'Landed our first institutional client — a national brand campaign that put us on the map and shaped our agency model.',
    },
    {
        'year': '2020',
        'title': 'Full Agency Structure',
        'desc': 'Expanded into a full-service agency with dedicated teams for design, development, and social media management.',
    },
    {
        'year': '2022',
        'title': 'Digital Expansion',
        'desc': 'Launched our web development and motion graphics divisions, completing our end-to-end creative offering.',
    },
    {
        'year': '2024',
        'title': 'Growing Portfolio & Reach',
        'desc': 'Now serving 13+ active clients across Zambia with a portfolio spanning finance, sport, wellness, media, and government.',
    },
]

ABOUT_VALUES = [
    {
        'icon': '◈',
        'title': 'Craft First',
        'desc': 'We refuse mediocrity. Every pixel, word, and line of code is deliberate — because the quality of the work is the quality of your brand.',
    },
    {
        'icon': '✦',
        'title': 'Strategy-Led Design',
        'desc': 'Beautiful is not enough. Everything we create is grounded in research, positioning, and a clear understanding of your audience and goals.',
    },
    {
        'icon': '◉',
        'title': 'Partnership Over Projects',
        'desc': 'We invest in long-term relationships. Your success is our benchmark — not just the delivery of a file.',
    },
    {
        'icon': '⬡',
        'title': 'African Excellence',
        'desc': 'We are proud of where we come from. We bring a distinctly African creative lens to every brief — bold, contextual, and globally competitive.',
    },
    {
        'icon': '▣',
        'title': 'Transparent Process',
        'desc': 'No surprises. Clear timelines, honest communication, and structured project governance from brief to delivery.',
    },
    {
        'icon': '❖',
        'title': 'Continuous Innovation',
        'desc': 'We stay ahead of design, technology, and marketing trends — so the work we deliver is always current, competitive, and built to last.',
    },
]

ABOUT_CREDENTIALS = [
    {
        'icon': '🏛️',
        'title': 'Registered Business — Republic of Zambia',
        'detail': 'Kinpin Arts Media is a formally registered business entity operating in full compliance with Zambian commercial law.',
    },
    {
        'icon': '📋',
        'title': 'Structured Client Agreements',
        'detail': 'All engagements are governed by signed service agreements with defined scope, timelines, and deliverables.',
    },
    {
        'icon': '🔒',
        'title': 'Confidentiality & IP Protection',
        'detail': 'Client work remains entirely the property of the client upon final payment. NDAs available on request.',
    },
    {
        'icon': '🏆',
        'title': '7+ Years of Proven Delivery',
        'detail': 'A track record of 100+ completed projects across branding, digital, events, and media production.',
    },
]

ABOUT_TEAM = [
    {
        'name': 'Creative Director',
        'role': 'Founder & Creative Director',
        'bio': 'Leading the creative vision of Kinpin Arts since 2017. Replace with actual team member details.',
        'photo': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&auto=format&fit=crop&q=80',
    },
    {
        'name': 'Lead Designer',
        'role': 'Senior Brand Designer',
        'bio': 'Specialising in brand identity and print. Replace with actual team member details.',
        'photo': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=600&auto=format&fit=crop&q=80',
    },
    {
        'name': 'Web Developer',
        'role': 'Lead Developer',
        'bio': 'Building fast, responsive digital experiences. Replace with actual team member details.',
        'photo': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&auto=format&fit=crop&q=80',
    },
    {
        'name': 'Social Media Manager',
        'role': 'Digital Marketing Lead',
        'bio': 'Driving social strategy and content production. Replace with actual team member details.',
        'photo': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=600&auto=format&fit=crop&q=80',
    },
]

ABOUT_CLIENT_FALLBACK = [
    'FC Bwacha', 'Skin Sensation', 'Zenith', 'Access Bank',
    'Africast', 'ZDA', 'Amiran', 'Ecobank',
    'Mannock', 'Lukanda', 'Ntumai', 'Freedom',
]


def _nav_links():
    return [
        {'label': 'Home', 'href': reverse('home')},
        {'label': 'About', 'href': reverse('about')},
        {'label': 'Services', 'href': reverse('services')},
        {'label': 'Our Work', 'href': reverse('portfolio')},
        {'label': 'Contact', 'href': reverse('home') + '#contact'},
    ]


def _initials(name):
    parts = (name or '').strip().split()
    if not parts:
        return '?'
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def _testimonial_cards():
    rows = []
    for t in Testimonial.objects.filter(is_featured=True)[:4]:
        title_parts = [p for p in (t.client_title, t.client_company) if p]
        rows.append({
            'quote': t.content,
            'name': t.client_name,
            'title': ', '.join(title_parts),
            'initials': _initials(t.client_name),
        })
    return rows


def home(request):
    if request.method == 'POST' and request.POST.get('form_type') == 'contact':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        service = request.POST.get('service', '').strip()
        message = request.POST.get('message', '').strip()
        subject = service if service else 'Project inquiry'
        if name and email and message:
            ContactInquiry.objects.create(
                name=name,
                email=email,
                phone='',
                subject=subject,
                message=message,
            )
            messages.success(request, "Thanks! We'll be in touch soon.")
            return redirect('home')
        messages.error(request, 'Please fill in all required fields.')
        return redirect('home')

    services = Service.objects.prefetch_related(
        Prefetch('features', queryset=ServiceFeature.objects.order_by('order'))
    ).order_by('order', 'title')

    projects = list(
        Project.objects.prefetch_related('categories').order_by('order', '-created_at')[:12]
    )

    category_names = set()
    for p in projects:
        for c in p.categories.all():
            category_names.add(c.name)
    portfolio_tabs = ['All'] + sorted(category_names, key=str.lower)

    context = {
        'nav_links': _nav_links(),
        'social_links': SOCIAL_LINKS,
        'nav_active_label': '',
        'services': services,
        'projects': projects,
        'portfolio_tabs': portfolio_tabs,
        'process_steps': PROCESS_STEPS,
        'stats': STATS,
        'clients': ClientLogo.objects.all(),
        'testimonial_cards': _testimonial_cards(),
    }
    return render(request, 'core/home.html', context)


def about(request):
    client_names = list(
        ClientLogo.objects.order_by('order', 'name').values_list('name', flat=True)
    )
    if not client_names:
        client_names = ABOUT_CLIENT_FALLBACK

    services = Service.objects.order_by('order', 'title')

    return render(request, 'core/about.html', {
        'nav_links': _nav_links(),
        'social_links': SOCIAL_LINKS,
        'nav_active_label': 'About',
        'services': services,
        'stats': STATS,
        'milestones': ABOUT_MILESTONES,
        'values': ABOUT_VALUES,
        'credentials': ABOUT_CREDENTIALS,
        'team_members': ABOUT_TEAM,
        'client_pills': client_names,
    })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and subject and message:
            ContactInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
            )
            messages.success(request, "Thanks! We'll be in touch soon.")
            return redirect('contact')
        messages.error(request, 'Please fill in all required fields.')
    return render(request, 'core/contact.html')


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            _, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'You are now subscribed!')
            else:
                messages.info(request, 'You are already subscribed.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')
