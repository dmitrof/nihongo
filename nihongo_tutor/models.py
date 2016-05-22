from django.db import models
from django_cbtools.models import CouchbaseModel
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

#для пробы
class CBArticle(CouchbaseModel):
    class Meta:
        abstract = True
    doc_type = 'article'
    uid_prefix = 'atl'
    title = models.CharField(max_length=45, null=True, blank=True)
    year_published = models.IntegerField(default=2014)
    is_draft = models.BooleanField(default=True)
    author_uid = models.TextField()

class KanjiCard(CouchbaseModel):
    class Meta:
        abstract = True
    doc_type = 'kanji_card'
    uid_prefix = 'kanji'
    author_uid = models.TextField()
    contents = JSONField()


class CBAuthor(CouchbaseModel):
    class Meta:
        abstract = True
    doc_type = 'author'
    uid_prefix = 'aur'
    name = models.CharField(max_length=45, null=True, blank=True)
# Create your models here.
@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

class Assignment(CouchbaseModel):
    class Meta:
        abstract = True
    doc_type = 'stat_doc'
    uid_prefix = 'stat'
    user_id = models.CharField(max_length=200)
    card_id = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

