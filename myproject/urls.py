"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', user_views.profile.as_view(), name='profile'),
    path('login/', user_views.login_cas, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    re_path(r'^register/$', user_views.signup, name='register'),
    path('activate/<uidb64>/<token>/', user_views.activate, name='activate'),
    path('password-reset/', user_views.reset_password, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', user_views.reset_password_confirm, name='password_reset_confirm'),
    path('profile/<slug:username>/', user_views.Profile_page.as_view(), name='user-inf'),
    path('change-password/', user_views.change_password, name='password_change'),

    path('login/api/', include('social_django.urls', namespace='social')),

    path('', include('fumetsu.urls')),
    path('', include('anime.urls')),

]

#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
