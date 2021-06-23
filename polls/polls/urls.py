"""polls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView


from polls import views as polls_views

from django.contrib.auth import views as auth_views

from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
import debug_toolbar

urlpatterns = [

    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),
    path('contact/', include('contactforms.urls')),
    #path('',TemplateView.as_view(template_name="userindexview.html")),

    path('__debug__/', include(debug_toolbar.urls)),
    path('users/', include('django.contrib.auth.urls')),
    path('captcha/', include('captcha.urls')),

    path('admin/defender/', include('defender.urls')), # defender admin

    path("password-reset", auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
         name="password_reset"),
    path("password-reset_done/",
         auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>",
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("password-reset-complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_reset_complete"),

]

urlpatterns += i18n_patterns (
    path('', include('pollapp.urls',namespace='pollapp'))
)
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

settings.LOGIN_URL = '/logout'
