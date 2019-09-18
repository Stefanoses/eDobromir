from django import template


register = template.Library()


@register.inclusion_tag('diary_detail.html')
def render_diary_detail(diaryObject):
    return {'diaryObject': diaryObject}