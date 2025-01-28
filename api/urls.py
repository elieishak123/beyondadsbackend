from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceViewSet,
    ClientViewSet,
    HeroContentView,
    CTAContentView,
    FooterContentView,
    ProcessPhotoDetailView,
    ContactUsContentView,
    AboutContentView,
    ShortListView,
    ProcessPhotoListView,
    SubmitFormView,
    SubmissionListView,
    SubmissionActionView
)


urlpatterns = [
    path('services/', ServiceViewSet.as_view({'get': 'list', 'post': 'create'}), name='service-list-create'),
    path('services/<int:pk>/', ServiceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='service-detail-update-delete'),

    path('clients/', ClientViewSet.as_view({'get': 'list', 'post': 'create'}), name='client-list-create'),
    path('clients/<int:pk>/', ClientViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='client-detail-update-delete'),

    path('hero-content/', HeroContentView.as_view(), name='hero-content'),
    path('cta-content/', CTAContentView.as_view(), name='get_cta_content'),
    path('cta-content/update/', CTAContentView.as_view(), name='update_cta_content'),
    path('footer-content/', FooterContentView.as_view(), name='footer-content'),

    path('process-photo/', ProcessPhotoListView.as_view(), name='list-create-photo'),
    path('process-photo/<int:pk>/', ProcessPhotoDetailView.as_view(), name='photo-detail'),
    

    path('contact-us/', ContactUsContentView.as_view(), name='contact-us'),

    path('shorts/', ShortListView.as_view(), name='short-list'),
    path('shorts/<int:pk>/', ShortListView.as_view(), name='short-retrieve-update'),

    path('about-content/', AboutContentView.as_view(), name='about-content'),

    path('submit/', SubmitFormView.as_view(), name='submit-form'),
    path('submissions/', SubmissionListView.as_view(), name='admin-submissions'),
    path('submissions/<int:pk>/', SubmissionActionView.as_view(), name='admin-submission-action'),
    path('submissions/<int:pk>/mark-read/', SubmissionActionView.as_view(), name='mark-read'),
    path('submissions/<int:pk>/toggle-hidden/', SubmissionActionView.as_view(), name='toggle_hidden'),
]

