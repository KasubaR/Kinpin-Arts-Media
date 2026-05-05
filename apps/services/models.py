from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    text = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.title} — {self.text}"
