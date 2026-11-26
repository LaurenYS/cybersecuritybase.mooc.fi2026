from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Story(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_title_per_author"
            ),
        ]
        ordering = ["-created_at"]

    def story_preview(self):
        return self.content[:100] + "..." if len(self.content) > 100 else self.content

    story_preview.short_description = "Story Preview"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    rate = models.IntegerField(
        validators=[
            MinValueValidator(0, message="Rate must be >= 0"),
            MaxValueValidator(5, message="Rate must be <= 5"),
        ],
        default=0,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "story"], name="one_review_per_user_per_story"
            ),
        ]
        ordering = ["story__title", "rate", "user__username"]

# This is only needed for "save" all the stolen information. In real world, this would be sent to an external server or database.
# class Mail(models.Model):
# 	content = models.TextField()
