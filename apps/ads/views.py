from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser

from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from .models import Ad, Category, Province, City, Favorite, AdImage, Message
from .serializers import (AdSerializer, CategorySerializer, ProvinceSerializer,
                          CitySerializer, FavoriteSerializer, AdImageSerializer,
                          AdStatusUpdateSerializer, MessageSerializer)


class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'city']
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Ad.objects.all()

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProvinceListView(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [AllowAny]


class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]


class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    lookup_field = 'ad_id'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class AdImageUploadView(generics.CreateAPIView):
    queryset = AdImage.objects.all()
    serializer_class = AdImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save()


class AdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AdBumpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            ad = Ad.objects.get(pk=pk)
        except Ad.DoesNotExist:
            return Response({"detail": "آگهی پیدا نشد!"}, status=status.HTTP_404_NOT_FOUND)

        if ad.owner != request.user:
            return Response({"detail": "شما اجازه نردبان کردن این آگهی را ندارید!"}, status=status.HTTP_403_FORBIDDEN)

        ad.created_at = timezone.now()
        ad.save()

        return Response({"detail": "آگهی با موفقیت نردبان شد."}, status=status.HTTP_200_OK)


class MyAdListView(generics.ListAPIView):
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ad.objects.filter(owner=self.request.user).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AdStatusUpdateView(generics.UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdStatusUpdateSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ad_id = self.request.query_params.get('ad')
        return Message.objects.filter(
            ad__id=ad_id
        ).filter(
            Q(sender=self.request.user)
            |
            Q(recipient=self.request.user)
        ).order_by('timestamp')


class ChatInboxView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        messages = Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).select_related('ad', 'sender', 'recipient').order_by('-timestamp')

        chat_dict = {}
        for msg in messages:
            ad_id = msg.ad.id
            other_user = msg.recipient if msg.sender == user else msg.sender
            key = (ad_id, other_user.id)

            if key not in chat_dict:
                chat_dict[key] = {
                    'ad_id': ad_id,
                    'ad_title': msg.ad.title,
                    'with_user': other_user.email,
                    'last_message': msg.text,
                    'last_time': msg.timestamp
                }

        return Response(list(chat_dict.values()))
