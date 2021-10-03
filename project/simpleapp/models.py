from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    author = models.CharField(max_length=200)
    rating_auth = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author

    def update_rating(self):
        auth = Author.objects.get(author=self.author)
        sum_rat_new = 0
        news = auth.new_set.all()
        for new in news:
            sum_rat_new += new.rating_new * 3

        usr = auth.user
        sum_rat_comm = 0
        comments = usr.comment_set.all()
        for comm in comments:
            sum_rat_comm += comm.rating_comm

        sum_rat_auth = 0
        for new in news:
            comm_news = new.comment_set.all()
            for comm_new in comm_news:
                sum_rat_auth += comm_new.rating_comm

        self.rating_auth = sum_rat_new + sum_rat_comm + sum_rat_auth
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category


class New(models.Model):
    state = 'ST'
    new = 'NE'
    POSITIONS = [
        (state, 'Статья'),
        (new, 'Новость')
    ]
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=state)
    created = models.DateTimeField(auto_now_add=True)
    post_name = models.CharField(max_length=250)
    content = models.TextField()
    rating_new = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='NewCategory')

    def __str__(self):
        return self.post_name

    def like(self):
        self.rating_new += 1
        self.save()

    def dislike(self):
        self.rating_new -= 1
        if self.rating_comm < 0:
            self.rating_comm = 0
        self.save()

    def preview(self):
        prev = self.content[:124] + '...'
        return prev


class NewCategory(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.post_name} - {self.category.category}'


class Comment(models.Model):
    comment = models.TextField()
    created_comm = models.DateTimeField(auto_now_add=True)
    rating_comm = models.IntegerField(default=0)

    new = models.ForeignKey(New, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_comm += 1
        self.save()

    def dislike(self):
        self.rating_comm -= 1
        if self.rating_comm < 0:
            self.rating_comm = 0
        self.save()
