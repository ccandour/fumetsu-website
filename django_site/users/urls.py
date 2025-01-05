from django.contrib import admin
from django.urls import path, include, re_path
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', user_views.EditProfile.as_view(), name='edit_profile'),
    path('login/', user_views.login_cas, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    re_path(r'^register/$', user_views.signup, name='register'),
    path('activate/<uidb64>/<token>/', user_views.activate, name='activate'),
    path('password-reset/', user_views.reset_password, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', user_views.reset_password_confirm, name='password_reset_confirm'),
    path('profile/<slug:username>/', user_views.ProfilePage.as_view(), name='profile'),
    path('change-password/', user_views.change_password, name='password_change'),

    path('login/api/', include('social_django.urls', namespace='social')),

]