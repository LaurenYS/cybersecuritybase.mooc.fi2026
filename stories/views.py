from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from django.db import models

import sqlite3

from stories.models import Story, Review
# from stories.models import Mail

# Create your views here.
def homePageView(request):
    if not request.user.is_authenticated:
        return render(request, "index.html")

    stories = []
    sstories = []

    for story in Story.objects.all():
        avg_rate = story.review_set.aggregate(models.Avg("rate"))["rate__avg"]
        my_rate = Review.objects.filter(user=request.user, story=story).first()
        rate = my_rate.rate if my_rate is not None else None
        s = {
            "id": story.id,
            "title": story.title,
            "content": story.content,
            "avg_rate": f"{avg_rate:.2f}" if avg_rate is not None else "0.00",
            "my_rate": rate,
        }

        if story.author == request.user:
            stories.append(s)
        else:
            s["author"] = story.author.username
            sstories.append(s)

    return render(request, "index.html", {
        "stories": stories,
        "sstories": sstories,
    })

@login_required
def addStoryView(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if title and content:

            try:
                with transaction.atomic():
                    Story.objects.create(title=title, content=content, author=request.user)
            except Exception as e:
                return HttpResponse(f"Error creating story: {str(e)}", status=500)
        else:
            return HttpResponse("Title and content are required.", status=400)
    return redirect("/")

@login_required
def reviewsView(request, username):
    query = "SELECT stories_review.id, user_id, story_id, rate FROM stories_review INNER JOIN auth_user ON stories_review.user_id = auth_user.id WHERE auth_user.username = '%s'" % username

    # Connect to the database and execute the raw SQL query
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        reviews = cursor.fetchall()

    # FLAW 1: How to fix it? Uncomment the following code block (lines XXX-XXX)
    # (the reviews variable is overwritten in the patch, there is no need to
    # comment the previous code):
    # try:
    #     user = User.objects.get(username=username)
    #     reviews = Review.objects.filter(user=user)
    # except User.DoesNotExist:
    #     reviews = []

    # FLAW 2: How to fix it? Uncomment the following code block (lines XXX-XXX)
    if username != request.user.username:
        reviews = []

    return render(request, "reviews.html", {
        "username": username,
        "reviews": reviews
    })

@login_required
def addReviewView(request):
    username = request.user.username
    story_id = request.POST.get("story_id")
    rate = request.POST.get("rate")

    try:
        story = Story.objects.get(id=story_id)
        if story.author == request.user:
            return HttpResponse("You cannot review your own story.", status=400)
    except Story.DoesNotExist:
        return HttpResponse("Story not found.", status=404)

    try:
        rate = int(rate)
        if rate < 0 or rate > 5:
            raise ValueError("Rate must be between 0 and 5.")
    except ValueError as e:
        return HttpResponse(f"Invalid rate: {str(e)}", status=400)

    try:
        with transaction.atomic():
            if Review.objects.filter(user=request.user, story=story).exists():
                review = Review.objects.get(user=request.user, story=story)
                review.rate = rate
                review.save()
            else:
                Review.objects.create(user=request.user, story=story, rate=rate)
    except Exception as e:
        return HttpResponse(f"Error creating review: {str(e)}", status=500)

    return redirect("/")

@login_required
def deleteReviewView(request):
    story_id = request.POST.get("story_id")

    try:
        story = Story.objects.get(id=story_id)
        review = Review.objects.get(user=request.user, story=story)
        review.delete()
    except Story.DoesNotExist:
        return HttpResponse("Story not found.", status=404)
    except Review.DoesNotExist:
        return HttpResponse("Review not found.", status=404)

    return redirect("/")

# @csrf_exempt
# def mailView(request):

#     if request.method == "POST":
#         Mail.objects.create(content=request.body.decode('utf-8'))
#         print(request.body.decode('utf-8'))

#     return render(request, "mail.html", context={
#         "mails": Mail.objects.all()
#     })
