from django.urls import path
from stories.views import homePageView, addStoryView, reviewsView, addReviewView, deleteReviewView
# from stories.views import mailView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add-story/', addStoryView, name='add-story'),
    # path('mail/', mailView, name='mail'),
    path('reviews/<str:username>/', reviewsView, name='reviews'),
    path('add-review/', addReviewView, name='add-review'),
    path('delete-review/', deleteReviewView, name='delete-review'),
]
