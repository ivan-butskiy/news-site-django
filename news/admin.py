from django.contrib import admin
from .models import News, Category
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ['id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    list_filter = ['is_published', 'category']
    fields = ['title', 'category', 'content', 'photo', 'get_photo', 'created_at',
              'updated_at', 'is_published', 'views']    # указывает список полей при отображении новости
    # Указать, какие поля доступны только для просмотра, но не редактирования
    readonly_fields = ['created_at', 'updated_at', 'get_photo', 'views']
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return 'Нет изображения'

    get_photo.short_description = 'миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['title']


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'