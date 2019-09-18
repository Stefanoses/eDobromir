from django.conf.urls import url
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from eureka.models import Eureka
from django.contrib import sitemaps
from django.urls import reverse
from concept.models import Concept
from django.contrib.auth.models import User


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['content:content_add',
                'content:content_idea',
                'content:content_cookies',
                'content:content_policy',
                'content:content_help',
                'content:content_contact',
                'content:content_regulations']

    def location(self, item):
        return reverse(item)


class UserViewSitemap(sitemaps.Sitemap):
    priority = 0.3
    changefreq = 'daily'
    date_field = 'date_joined'

    def items(self):
        return User.objects.filter(is_active=True).order_by('-date_joined')

    def location(self, item):
        return reverse('account_profile_detail', kwargs={'username': item.username})

info_eureka = {
    'queryset': Eureka.objects.filter(is_published=True).order_by('-published'),
    'date_field': 'published',
}

info_concept = {
    'queryset': Concept.objects.all().order_by('-created'),
    'date_field': 'created',
}

sitemaps = {
    'static': StaticViewSitemap,
    'eureka': GenericSitemap(info_eureka, priority=0.8, changefreq = 'daily'),
    'concept': GenericSitemap(info_concept, priority=0.7, changefreq = 'daily'),
    'user': UserViewSitemap,
}

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]