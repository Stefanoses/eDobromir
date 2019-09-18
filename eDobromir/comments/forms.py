from django.forms import ModelForm, Textarea, CharField, TextInput
from django.forms.widgets import Textarea
from .models import Comment
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextFormField
import itertools
from django.utils.text import slugify

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content':CKEditorWidget(config_name='description_ckeditor')
        }

    def save(self):
        instance = super(CommentCreateForm, self).save(commit=False)
        max_length = Comment._meta.get_field('slug').max_length
        instance.slug = orig = slugify(instance.created_by)[:max_length]
        for x in itertools.count(1):
            if not Comment.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
        instance.save()
        return instance


class CommentReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content':CKEditorWidget(config_name='description_ckeditor')
        }

    def save(self):
        instance = super(CommentReplyForm, self).save(commit=False)
        max_length = Comment._meta.get_field('slug').max_length
        instance.slug = orig = slugify(instance.created_by)[:max_length]
        for x in itertools.count(1):
            if not Comment.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
        instance.save()
        return instance
