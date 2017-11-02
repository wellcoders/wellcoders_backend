from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from users import emails
from django.core.mail import send_mail
import re


class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    styles = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    DRAFT = 'DRF'
    PUBLISHED = 'PUB'
    DELETED = 'DEL'

    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (DELETED, 'Deleted')
    )

    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField()
    title = models.CharField(max_length=155)
    title_slug = models.CharField(max_length=155, null=True, blank=True)
    content = models.TextField()
    summary = models.CharField(max_length=155)
    category = models.ForeignKey(Category)
    media = models.TextField(null=True, blank=True)  # Use with an url until media model is included
    status = models.CharField(max_length=3, choices=STATUS, default=DRAFT)

    class Meta:
        unique_together = ('title', 'owner',)

    @staticmethod
    def generate_title_slug(source):
        source = source.lower()

        for string, replacement in settings.TITLE_SLUG_REPLACEMENTS:
            source = source.replace(string, replacement)
            
        return "-".join(re.findall("[a-zA-Z0-9]+", source))

        mention_regex = re.compile('(@[a-zA-ZñÑ0-9]+)')

    def get_users_mentioned_on_post(self):
        mentions = re.compile(settings.MENTION_REGEX).findall(self.content)

        users = []
        for mention in mentions:
            mention = mention.replace('@', '')

            users_found = User.objects.filter(username=mention)

            if len(users_found) >= 1:

                if not PostUserMention.objects.filter(user=users_found[0], post=self).exists():
                    PostUserMention.objects.create(user=users_found[0], post=self)
                    users.append(users_found[0])

        return users

    def get_url(self):
        return settings.WELLCODERS_PUBLIC_URL + '/articles/' + self.owner.username + '/' + self.title_slug

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        super(Post, self).save(force_insert=force_insert, force_update=force_update,
                               using=using, update_fields=update_fields)

        for mentioned_user in self.get_users_mentioned_on_post():
            if mentioned_user.email:
                send_mail(
                    emails.USER_MENTIONED_IN_POST_SUBJECT,
                    emails.USER_MENTIONED_IN_POST_BODY % {'user': mentioned_user.username,
                                                          'other_user': self.owner.username,
                                                          'url': self.get_url()},
                    settings.WELLCODERS_USER_REGISTERED_EMAIL,
                    [mentioned_user.email],
                    fail_silently=False,
                )


class Comment(models.Model):
    owner = models.ForeignKey(User)
    content = models.TextField()
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(auto_now_add=True)  # automáticamente añada la fecha de creación
    modified_at = models.DateTimeField(auto_now=True)  # automáticamente actualiza la fecha al guardar

    def __str__(self):
        return "%s - %s" % (self.owner.username, self.post.title)

    def get_users_mentioned_on_comment(self):
        mentions = re.compile(settings.MENTION_REGEX).findall(self.content)

        users = []
        for mention in mentions:
            mention = mention.replace('@', '')

            users_found = User.objects.filter(username=mention)

            if len(users_found) >= 1:

                if not CommentUserMention.objects.filter(user=users_found[0], comment=self).exists():
                    CommentUserMention.objects.create(user=users_found[0], comment=self)
                    users.append(users_found[0])

        return users

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        super(Comment, self).save(force_insert=force_insert, force_update=force_update,
                               using=using, update_fields=update_fields)      

        for mentioned_user in self.get_users_mentioned_on_comment():
            if mentioned_user.email:
                send_mail(
                    emails.USER_MENTIONED_IN_COMMENT_SUBJECT,
                    emails.USER_MENTIONED_IN_COMMENT_BODY % {'user': mentioned_user.username,
                                                          'other_user': self.owner.username,
                                                          'url': self.post.get_url()},
                    settings.WELLCODERS_USER_REGISTERED_EMAIL,
                    [mentioned_user.email],
                    fail_silently=False,
                )                               


class FavoritePost(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)

    class Meta:
        unique_together = ('user', 'post')

class PostUserMention(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)

    class Meta:
        unique_together = ('user', 'post')

class CommentUserMention(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)

    class Meta:
        unique_together = ('user', 'comment')
