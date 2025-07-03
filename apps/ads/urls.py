from django.urls import path
from .views import (
    AdListCreateView, CategoryListView, ProvinceListView, CityListView,
    FavoriteListCreateView, FavoriteDeleteView, AdImageUploadView,
    AdRetrieveUpdateDestroyView, AdBumpView, MyAdListView,
    AdStatusUpdateView, MessageCreateView, MessageListView, ChatInboxView
)


urlpatterns = [
    path('', AdListCreateView.as_view(), name='ads-list-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('provinces/', ProvinceListView.as_view(), name='province-list'),
    path('cities/', CityListView.as_view(), name='city-list'),
    path('favorites/', FavoriteListCreateView.as_view(), name='favorite-list-create'),
    path('favorites/<int:ad_id>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
    path('images/upload/', AdImageUploadView.as_view(), name='ad-image-upload'),
    path('<int:pk>/', AdRetrieveUpdateDestroyView.as_view(), name='ad-detail'),
    path('<int:pk>/bump/', AdBumpView.as_view(), name='ad-bump'),
    path('my/', MyAdListView.as_view(), name='my-ads'),
    path('<int:pk>/status/', AdStatusUpdateView.as_view(), name='ad-status-update'),
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/send/', MessageCreateView.as_view(), name='message-send'),
    path('messages/inbox/', ChatInboxView.as_view(), name='message-inbox'),
]
