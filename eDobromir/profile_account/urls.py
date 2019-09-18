from django.conf.urls import url, include
from views import *
from allauth.account.views import PasswordChangeView
from allauth.socialaccount import providers
from importlib import import_module
from allauth.socialaccount import views as social_views
from axes.decorators import watch_login


urlpatterns = [
    # settings
    url(r'^account/login_signup/$', watch_login(LoginSignupView.as_view()), name='account_login_signup'),
    url(r'^account/user/(?P<username>[-\w]+)/$', ProfileDetail.as_view(), name='account_profile_detail'),
    url(r'^account/settings/profile/$', SettingsProfileView.as_view(), name='account_settings_profile'),
    url(r'^account/settings/avatar/$', SettingsAvatarView.as_view(), name='account_settings_avatar'),

    # actions
    url(r'^account/signup/$', SignupView.as_view(), name="account_signup"),
    url(r'^account/login/$', watch_login(login), name="account_login"),
    url(r'^account/logout/$', logout, name="account_logout"),
    url(r'^account/password/change/$', SettingsPasswordUpdateView.as_view(), name="account_change_password"),
    url(r"^account/password/set/$", password_set, name="account_set_password"),
    url(r"^account/inactive/$", account_inactive, name="account_inactive"),

    # E-mail
    url(r'^account/email/$', SettingsEmailUpdateView.as_view(), name="account_email"),
    url(r'^account/confirm-email/$', email_verification_sent, name="account_email_verification_sent"),
    url(r'^account/confirm-email/(?P<key>[-:\w]+)/$', confirm_email, name="account_confirm_email"),

    # password reset
    url(r'^account/password/reset/$', password_reset, name="account_reset_password"),
    url(r'^account/password/reset/done/$', password_reset_done, name="account_reset_password_done"),
    url(r'^account/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$', password_reset_from_key, name="account_reset_password_from_key"),
    url(r'^account/password/reset/key/done/$', password_reset_from_key_done, name="account_reset_password_from_key_done"),

    # social
    url('^account/social/login/cancelled/$', social_views.login_cancelled, name='socialaccount_login_cancelled'),
    url('^account/social/login/error/$', social_views.login_error, name='socialaccount_login_error'),
    url('^account/social/signup/$', social_views.signup, name='socialaccount_signup'),
    url('^account/social/connections/$', SettingsSocialUpdateView.as_view(), name='socialaccount_connections'),

    # activiti
    url(r'^account/rank/$', RankListView.as_view(), name='account_rank'),
    url(r'^account/user/(?P<username>[-\w]+)/activity/eureka/$', ProfileActivityEurekaView.as_view(), name='account_profile_activity_eureka'),
    url(r'^account/user/(?P<username>[-\w]+)/activity/eureka/waiting/$', ProfileActivityEurekaWaitingView.as_view(), name='account_profile_activity_eureka_waiting'),
    url(r'^account/user/(?P<username>[-\w]+)/activity/eureka/vote/$', ProfileActivityEurekaVoteView.as_view(), name='account_profile_activity_eureka_vote'),
    url(r'^account/user/(?P<username>[-\w]+)/activity/eureka/sketch/$', ProfileActivityEurekaSketchView.as_view(), name='account_profile_activity_eureka_sketch'),
    url(r'^account/user/(?P<username>[-\w]+)/activity/eureka/favorite/$', ProfileActivityEurekaFavoriteView.as_view(), name='account_profile_activity_eureka_favorite'),

    url(r'^account/user/(?P<username>[-\w]+)/activity/concept/$', ProfileActivityConceptView.as_view(), name='account_profile_activity_concept'),
    url(r'^account/user/(?P<username>[-\w]+)/activity/concept/vote/$', ProfileActivityConceptVoteView.as_view(), name='account_profile_activity_concept_vote'),
    url(r'^account/user/(?P<username>[-\w]+)/activity/concept/favorite/$', ProfileActivityConceptFavoriteView.as_view(), name='account_profile_activity_concept_favorite'),

    url(r'^account/user/(?P<username>[-\w]+)/activity/observers/$', ProfileActivityObservers.as_view(), name='account_profile_activity_observers'),
    url(r'^account/user/(?P<username>[-\w]+)/activity/followers/$', ProfileActivityFollowers.as_view(), name='account_profile_activity_followers'),

]

for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        urlpatterns += prov_urlpatterns
