from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SendMessageView, MessageListView, like_user, dislike_user, UserListView

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send_message/', SendMessageView.as_view(), name='send_message'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('users_list/', UserListView.as_view(), name='api_users'),
    path('users/<int:user_id>/like/', like_user, name='like_user'),
    path('users/<int:user_id>/dislike/', dislike_user, name='dislike_user'),
]