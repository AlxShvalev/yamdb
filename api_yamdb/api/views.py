from django.db.models import Avg
from rest_framework import viewsets, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitleFilter
from .mixins import CreateListDestroyModelViewSet
from .serializers import (
    TitleReadSerializer,
    TitleWriteSerializer,
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer
)
from .permissions import ReadOnly

from reviews.models import Title, Category, Genre, Review
from users.serializers import UserSignupSerializer, \
    TokenSerializer, UserSerializer, AdminSerializer

from users.models import User
from users.confirmation import code_generator
from users.token_generator import get_tokens_for_user
from users.permissions import AdminPermission, ContentModificationPermission
import json


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminPermission | ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(CreateListDestroyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug',)


class GenreViewSet(CreateListDestroyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ContentModificationPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        new_queryset = title.reviews.all()
        return new_queryset.order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(title=title, author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        context.update({'title': title})
        return context


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ContentModificationPermission,)

    def get_queryset(self, *args, **kwargs):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        comments = review.comments.all()
        return comments.order_by('id')

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
        )
        user = get_object_or_404(User, username=self.request.user,)
        serializer.save(author=user, review=review)


class UserSignupViewClass(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        user.confirmation_code = code_generator(user.email)
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthTokenViewClass(APIView):
    permission_classes = (AllowAny,)
    error_message = '{"error":"Неверный код подтверждения"}'

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        if user.confirmation_code \
                == serializer.data.get('confirmation_code') \
                and user.confirmation_code != 0:
            user.confirmation_code = 0
            user.save()
            return Response(get_tokens_for_user(user),
                            status=status.HTTP_201_CREATED)
        return Response(json.loads(self.error_message),
                        status=status.HTTP_400_BAD_REQUEST)


class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminPermission,)
    serializer_class = AdminSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


class UserViewClass(APIView):

    def get(self, request):
        user = request.user
        if user.is_anonymous:
            raise NotAuthenticated
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
