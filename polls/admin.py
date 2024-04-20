# from django.contrib import admin

# from .models import Question, Choice

# # admin.site.register(Question)
# admin.site.register(Choice)


# class QuestionAdmin(admin.ModelAdmin):
#     # fields = ["pub_date", "question_text"]

#     fieldsets = [
#         (None, {"fields": ["question_text"]}),
#         ("Date information", {"fields": ["pub_date"]}),
#     ]


# admin.site.register(Question, QuestionAdmin)

# --------------------------CUSTOMIZE ADMIN PAGE (tutorial 07)---------------
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)