"""Dobromir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from ckeditor_uploader import views as ckeditor_views
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap

from profile_account import urls as profile_accounts_urls
from comments import urls as comments_urls
from errors import urls as errors_urls
from eureka import urls as eureka_urls
from search import urls as search_urls
from votes import urls as vote_urls
from content import urls as content_urls
from concept import urls as concept_urls
from tags import urls as tags_urls
from linked import urls as linked_urls
from moderation import urls as moderation_urls
from notification import urls as notification_urls
from favorites import urls as favorites_urls
import sitemaps as sitemaps_urls
import rss as rss_urls


urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^panel/sterowania/swiatem/', include(admin.site.urls)),  # admin site

    url(r'^', include(search_urls, namespace='search')),
    url(r'^', include(eureka_urls, namespace='eureka')),
    url(r'^', include(errors_urls, namespace='errors')),
    url(r'^', include(vote_urls, namespace='votes')),
    url(r'^', include(comments_urls,  namespace='comments')),
    url(r'^', include(content_urls,  namespace='content')),
    url(r'^', include(concept_urls,  namespace='concept')),
    url(r'^', include(tags_urls,  namespace='tags')),
    url(r'^', include(linked_urls,  namespace='linked')),
    url(r'^', include(moderation_urls,  namespace='moderation')),
    url(r'^', include(notification_urls,  namespace='notification')),
    url(r'^', include(favorites_urls,  namespace='favorites')),
    url(r'^', include(profile_accounts_urls)),
    url(r'^', include(sitemaps_urls)),
    url(r'^', include(rss_urls)),

    url(r'^ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    url(r'^ckeditor/browse/', login_required(ckeditor_views.browse), name='ckeditor_browse'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
