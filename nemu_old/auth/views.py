from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny
from serializers import UserSerializer
from permissions import IsStaffOrTargetUser
from authentication import QuietBasicAuthentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
 
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),


def AuthLogin(request):
        return render(request, 'auth/index.html')


@login_required()
def AuthLogout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('login/')


class AuthView(APIView):
    authentication_classes = (QuietBasicAuthentication,)

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(UserSerializer(request.user).data)


    def delete(self, request, *args, **kwargs):
        logout(request)
        HttpResponseRedirect('/')
        return Response({})
