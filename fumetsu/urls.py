from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='fumetsu-home'),
    path('about/', About.as_view(), name='fumetsu-about'),
    path('announcements/', Announcements.as_view(), name='fumetsu-announcements'),
    path('privacy-policy/', PrivacyPolicy.as_view(), name='fumetsu-privacy-policy'),
    path('terms-of-service/', TermsOfService.as_view(), name='fumetsu-terms-of-service'),
    path('edit-comment/<uuid:pk>', EditComment.as_view(), name='edit-cmt'),
    path('delete-comment/<uuid:pk>', DeleteComment.as_view(), name='del-cmt'),
]

