# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.syndication.views import Feed
from django.urls import reverse
from eureka.models import Eureka
from concept.models import Concept
from django.utils.feedgenerator import Atom1Feed


class EurekaFeed(Feed):
    title = "eDobromir.pl - Strona główna"
    description = "Eureki którym udało się wejść na stronę główną."
    link = ''

    def items(self):
        return Eureka.objects.filter(is_published=True, is_waiting=False).order_by('-published')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_author_name(self, item):
        return item.created_by

    def item_pubdate(self, item):
        return item.published


class AtomEurekaFeed(EurekaFeed):
    feed_type = Atom1Feed
    subtitle = EurekaFeed.description


class EurekaWaitingFeed(Feed):
    title = "eDobromir.pl - Poczekalnia"
    description = "Eureki czekające na dostanie się na stronę główną"
    link = '/waiting/'

    def items(self):
        return Eureka.objects.filter(is_published=True, is_waiting=True).order_by('-published')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_author_name(self, item):
        return item.created_by

    def item_pubdate(self, item):
        return item.published


class AtomEurekaWaitingFeed(EurekaWaitingFeed):
    feed_type = Atom1Feed
    subtitle = EurekaWaitingFeed.description


class ConceptFeed(Feed):
    title = "eDobromir.pl - Koncepcje"
    description = "Koncepcje"
    link = '/concepts/'

    def items(self):
        return Concept.objects.all().order_by('-created')[:5]

    def item_title(self, item):
        return item.created_by

    def item_description(self, item):
        return item.content

    def item_author_name(self, item):
        return item.created_by

    def item_pubdate(self, item):
        return item.created


class AtomConceptFeed(ConceptFeed):
    feed_type = Atom1Feed
    subtitle = ConceptFeed.description


urlpatterns = [
    url(r'^rss/$', EurekaFeed(), name='rss'),
    url(r'^rss/waiting/$', EurekaWaitingFeed(), name='rss_waiting'),
    url(r'^rss/concepts/$', ConceptFeed(), name='rss_concepts'),

    url(r'^atom/$', AtomEurekaFeed(), name='atom'),
    url(r'^atom/waiting/$', AtomEurekaWaitingFeed(), name='atom_waiting'),
    url(r'^atom/concepts/$', AtomConceptFeed(), name='atom_concepts'),
]