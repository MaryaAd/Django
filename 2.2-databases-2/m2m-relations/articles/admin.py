from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Section, ArticleSection


class ArticleSectionInlineFormset(BaseInlineFormSet):
    def clean(self):
        flag = 0
        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                continue
            if form.cleaned_data.get('main_section'):
                flag += 1
            if flag > 1:
                raise ValidationError('Выберите 1 основной раздел.')
        if flag == 0:
            raise ValidationError('Выберите 1 основной раздел.')
        return super().clean()


class ArticleSectionInline(admin.TabularInline):
    model = ArticleSection
    extra = 7
    formset = ArticleSectionInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'published_at', 'image', ]
    list_filter = ['published_at', ]
    inlines = [ArticleSectionInline, ]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
