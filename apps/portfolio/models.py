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
    is_featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


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
