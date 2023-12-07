from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from accounts.models import User
from api.serializers import UserSerializer, MessageSerializer
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from orandevu.models.message import Message
from django.http import JsonResponse
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'], url_path='give-like')
    def like(self, request, pk=None):
        user_to_like = self.get_object()
        request.user.liked_users.add(user_to_like)
        return JsonResponse({'status': 'success', 'action': 'liked'})

    @action(detail=True, methods=['post'], url_path='give-dislike')
    def dislike(self, request, pk=None):
        user_to_dislike = self.get_object()
        request.user.disliked_users.add(user_to_dislike)
        return JsonResponse({'status': 'success', 'action': 'disliked'})


class SendMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        if response.status_code == 400:
            JsonResponse("Validation errors:", status=400)

        return response

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.request.query_params.get('other_user_id', None)
        if other_user_id is not None:
            other_user = User.objects.get(id=other_user_id)
            return Message.objects.filter(
                Q(sender=user, receiver=other_user) |
                Q(sender=other_user, receiver=user)
            ).distinct()
        else:
            return Message.objects.none()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_user(request, user_id):
    if user_id == request.user.id:
        return JsonResponse({'status': 'error', 'message': 'Нельзя лайкнуть самого себя'}, status=400)
    try:
        user_to_like = User.objects.get(pk=user_id)
        request.user.liked_users.add(user_to_like)
        return JsonResponse({'status': 'success'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'status': 'not_found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_user(request, user_id):
    if user_id == request.user.id:
        return JsonResponse({'status': 'error', 'message': 'Нельзя дизлайкнуть самого себя'}, status=400)
    try:
        user_to_dislike = User.objects.get(pk=user_id)
        request.user.disliked_users.add(user_to_dislike)
        return JsonResponse({'status': 'success'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'status': 'not_found'}, status=404)


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        liked_users = user.liked_users.all()
        disliked_users = user.disliked_users.all()
        return User.objects.exclude(id__in=liked_users).exclude(id__in=disliked_users).exclude(id=user.id)

