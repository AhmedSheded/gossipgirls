from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Poll, Choice
from rest_framework import generics, status, viewsets, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import User
from .models import Email
from django.core.mail import send_mail, EmailMessage
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class ModelPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 10
    max_page_size = 100


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    pagination_class = ModelPagination

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied('You can not delete this poll.')
        return super().destroy(request, *args, **kwargs)


class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs['pk'])
        return queryset

    # queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied('You can not create choice for this poll')
        return super().post(request, *args, **kwargs)


class CreateVote(APIView):
    def post(self, request, pk, choice_pk):
        voted_by = request.data.get('voted_by')
        data = {
            'choice': choice_pk,
            'poll': pk,
            'voted_by': voted_by
        }
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class SendEmailsView(APIView):
    def get(self, request):
        latest_email = Email.objects.latest('id')
        subject = latest_email.subject
        message = latest_email.message

        image_path = latest_email.image.path if latest_email.image else None

        users = User.objects.all()
        for user in users:
            recipient_list = [user.email]
            email = EmailMessage(subject, message, None, recipient_list)

            if image_path:
                email.attach_file(image_path)
            email.send()

        return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
