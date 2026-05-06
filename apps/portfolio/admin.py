from django.contrib import admin
from .models import Category, Project, ProjectImage, ProjectScopeItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectScopeItemInline(admin.TabularInline):
    model = ProjectScopeItem
    extra = 2
    ordering = ('order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'is_featured', 'order', 'created_at')
    list_filter = ('is_featured', 'categories')
    list_editable = ('is_featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    inlines = [ProjectScopeItemInline, ProjectImageInline]
    fieldsets = (
        (
            'Project basics',
            {
                'fields': (
                    'title',
                    'slug',
                    'categories',
                    'client',
                    'description',
                    'thumbnail',
                ),
            },
        ),
        (
            'Project links',
            {
                'fields': (
                    'behance_url',
                    'youtube_url',
                ),
                'description': 'Add a YouTube URL when this project should play as video in the portfolio lightbox.',
            },
        ),
        (
            'Visibility',
            {
                'fields': (
                    'is_featured',
                    'order',
                ),
            },
        ),
    )
