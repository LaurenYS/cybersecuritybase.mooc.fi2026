from django.contrib import admin

from stories.models import Story, Review

# Register your models here.
@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author__username', 'story_preview', 'created_at')
    list_filter = ('author__username', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'story__title', 'rate')
    list_filter = ('user__username', 'story__title', 'rate')
