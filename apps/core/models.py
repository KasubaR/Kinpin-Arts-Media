from django.db import models


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Contact Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.subject}"


class NewsletterSubscriber(models.Model):
    SYNC_PENDING = 'pending'
    SYNC_SYNCED = 'synced'
    SYNC_ALREADY_SYNCED = 'already_synced'
    SYNC_CONTACT_LIMIT = 'contact_limit'
    SYNC_FAILED = 'failed'
    SYNC_STATUS_CHOICES = [
        (SYNC_PENDING, 'Pending'),
        (SYNC_SYNCED, 'Synced'),
        (SYNC_ALREADY_SYNCED, 'Already Synced'),
        (SYNC_CONTACT_LIMIT, 'Contact Limit'),
        (SYNC_FAILED, 'Failed'),
    ]

    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    sync_status = models.CharField(max_length=20, choices=SYNC_STATUS_CHOICES, default=SYNC_PENDING)
    sync_last_attempt_at = models.DateTimeField(blank=True, null=True)
    sync_error_message = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.email


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_title = models.CharField(max_length=150, blank=True)
    client_company = models.CharField(max_length=150, blank=True)
    client_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.client_name} ({self.client_company})"


class ClientLogo(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clients/')
    website = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
