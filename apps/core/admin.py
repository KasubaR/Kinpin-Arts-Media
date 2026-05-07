from django.contrib import admin
from .models import ContactInquiry, NewsletterSubscriber, Testimonial, ClientLogo


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active', 'sync_status', 'sync_last_attempt_at')
    list_filter = ('is_active', 'sync_status')
    search_fields = ('email',)
    readonly_fields = ('sync_last_attempt_at',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'rating', 'is_featured')
    list_filter = ('is_featured', 'rating')
    list_editable = ('is_featured',)


@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
