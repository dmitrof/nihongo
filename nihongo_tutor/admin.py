from django.contrib import admin
from nihongo_tutor.models import Question, CBArticle
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    pass

class CBArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question, QuestionAdmin)
#admin.site.register(CBArticle, CBArticleAdmin)