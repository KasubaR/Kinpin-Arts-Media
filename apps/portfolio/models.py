from urllib.parse import parse_qs, urlparse

from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField(Category, related_name='projects')
    client = models.CharField(max_length=150, blank=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='portfolio/thumbnails/')
    behance_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Optional link to this project on Behance. Falls back to the agency Behance profile when empty.',
    )
    youtube_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Optional YouTube URL for video projects (youtube.com or youtu.be).',
    )
    is_featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def youtube_video_id(self):
        raw_url = (self.youtube_url or '').strip()
        if not raw_url:
            return ''
        try:
            parsed = urlparse(raw_url)
        except ValueError:
            return ''

        host = parsed.netloc.lower()
        if host.startswith('www.'):
            host = host[4:]
        if host.startswith('m.'):
            host = host[2:]

        if host == 'youtu.be':
            return parsed.path.strip('/').split('/')[0]
        if host in {'youtube.com', 'music.youtube.com'}:
            if parsed.path == '/watch':
                return parse_qs(parsed.query).get('v', [''])[0]
            if parsed.path.startswith('/embed/'):
                return parsed.path.split('/embed/', 1)[1].split('/')[0]
            if parsed.path.startswith('/shorts/'):
                return parsed.path.split('/shorts/', 1)[1].split('/')[0]
        return ''

    @property
    def youtube_embed_url(self):
        video_id = self.youtube_video_id
        if not video_id:
            return ''
        return f'https://www.youtube.com/embed/{video_id}?rel=0'

    def clean(self):
        super().clean()
        raw_url = (self.youtube_url or '').strip()
        if not raw_url:
            return

        video_id = self.youtube_video_id
        if not video_id:
            raise ValidationError({
                'youtube_url': 'Enter a valid YouTube video URL (youtube.com/watch, youtube.com/embed, youtube.com/shorts, or youtu.be).',
            })


class ProjectScopeItem(models.Model):
    """Deliverables / scope lines shown in the portfolio lightbox and detail page."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='scope_items')
    text = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'pk']

    def __str__(self):
        return f'{self.project.title} — {self.text}'


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio/images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} — image {self.order}"
