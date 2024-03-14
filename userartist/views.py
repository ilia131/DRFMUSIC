from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework  import status
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import json
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView , TokenVerifyView
from .serializers import ProfileSerializer , UserAccountSerializer , CommentSerializer , CommentSerializer1
from .models import Profile , UserAccount , Comment
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import generics , mixins 
from rest_framework.generics import  RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin 
from .permissons import IsOwnerOrReadOnly, IsOwnerOrPostOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework import permissions, \
    viewsets, generics, status
from rest_framework.parsers import MultiPartParser, FormParser , FileUploadParser , JSONParser
from uploadmusic.views import ShowPostUser
from django.http import Http404 , HttpResponse
from django.db.models import Q
#Djoser VIEWSET ADD+
from djoser import views
from .image import decode_image_from_base64
# from .track import handle_track_change
from PIL import Image
import io
import base64

class UserViewSetChild(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request):
        user = request.user
        serializer = UserAccountSerializer(user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = request.user
        serializer = UserAccountSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    

    

class UserViewSetChild2(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user , self.serializer_class)
        serializer.is_valid()
        return Response(serializer.data)



 
 
class UserViewSetChild1(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    # queryset = Profile.objects.all()

    def create(self, request):
       account = self.request.user
       serializer = ProfileSerializer(data=request.data)
       if serializer.is_valid():
            audio_file = serializer.validated_data['track']
            image_file = serializer.validated_data['image']
            title_file = serializer.validated_data['title']
            description_file = serializer.validated_data['description']
            audio_model = Profile(track=audio_file , 
                                  account=account , title=title_file 
                                  ,image=image_file , 
                                  description=description_file
                                  
                                  )
            audio_model.save()
            return Response({'message': 'Audio file uploaded successfully'}, status=201)
       else:
            return Response(serializer.errors, status=400)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
   
 
    def perform_create(self, serializer):
        account = self.request.user
        serializer.save(account=account)

   
    def get(self, request, *args, **kwargs):
        
        user = request.user
        serializer = UserAccountSerializer(user)
        data = serializer.data
        posts = serializer.user_posts1(user)
        data['posts'] = posts
        return Response(data)
    
    
    
    

    
  
 
 
 
class UuuidView(viewsets.GenericViewSet, mixins.ListModelMixin , mixins.CreateModelMixin):
     permission_classes = [AllowAny]
    #  parser_classes = (MultiPartParser, FormParser)

     queryset = Comment.objects.all()
     serializer_class = CommentSerializer1
     def get_queryset(self):
         text = self.request.query_params.get('query' , None)
         if not text: 
             return self.queryset
         
         return self.queryset.filter(post__unique_id=text) 
     
     
     
     def create(self, request, *args, **kwargs):
        user = request.user
        post_unique_id = request.data.get('post__unique_id')  # تغییر post__id به unique_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # اطمینان حاصل کنید که post_unique_id با مقدار برگردانده شده از get_queryset برابر است
        queryset_result = self.get_queryset()
        if queryset_result.exists():
            post_unique_id = queryset_result.first().post

        serializer.save(author=user, post=post_unique_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
 
 
     def post(self, request, *args, **kwargs):
         return self.create(request, *args, **kwargs)
     



    



 
 
    

class UserViewSetChild3(mixins.CreateModelMixin, generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)


    def create(self, request , *args , **kwargs ):
       account = self.request.user
       data=request.data
       
       serializer = CommentSerializer(data=data)
 
       if serializer.is_valid():
            post_unique_id = serializer.validated_data['post']
            
            post_profile = Profile.objects.get(unique_id=post_unique_id)
            content = serializer.validated_data['content']
            content_model = Comment(content=content,  author=account , post=post_profile)
            content_model.save()
            return Response(status=201)
       else:
            return Response(serializer.errors, status=400)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
  
        
        
    def get(self , request , *arg , **kwargs):
        user = request.user
        serializer = UserAccountSerializer(user)
        posts = serializer.user_posts1(user)
        data = serializer.data
        data['posts'] = posts
        return Response(data)
    
     
 


class ProfileDetailsView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
 
class UploadmusicVUE(APIView):
    
    def get_object(self, profile_slug, comment_slug):
        try:
            return Comment.objects.filter(slug=profile_slug).get(slug=comment_slug)
        except Comment.DoesNotExist:
            raise Http404
    
    def get(self, request, profile_slug, comment_slug, format=None):
        query = self.get_object(profile_slug, comment_slug)
        serializer = CommentSerializer(query)
        return Response(serializer.data)
    
   
class AddCommentToPost(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        post_uuid = request.data.get('post_uuid')
        content = request.data.get('content')
        
        try:
            post = Profile.objects.get(uuid=post_uuid)
        except Profile.DoesNotExist:
            return Response({'message': 'Post not found'}, status=404)
        
        comment = Comment(post=post, content=content)
        comment.save()
        
        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=201)
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
class CategoryVue(APIView):
    def get_object(self, profile_slug):
     
        try:
            return Profile.objects.get(slug=profile_slug)
        except Profile.DoesNotExist:
            raise Http404
      
    def get(self, request, profile_slug, format=None):
        category = self.get_object(profile_slug)
        serializer = ProfileSerializer(category)
        return Response(serializer.data) 
 
    
    





class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args , **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                 'refresh',
                 refresh_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        
        return response
    
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request , *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token:
            request.data['refresh'] = refresh_token
            
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        
        return response

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        
        if access_token: 
            request.data['token']  = access_token
            
        return super().post(request, *args, **kwargs)





  
# class EmailVerificationAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         if user.is_authenticated and not user.is_active:
#             # اینجا باید فرض شود که کد تأیید ایمیل از جانب کاربر ارسال شده است و بررسی شود
#             # اگر کد تأیید صحیح بود، وضعیت فعال بودن کاربر به True تغییر می‌یابد
#             user.is_active = True
#             user.save()
#             return Response({"message": "ایمیل کاربر تأیید شد و حساب کاربری فعال شد."}, status=status.HTTP_200_OK)
#         return Response({"message": "احراز هویت با موفقیت انجام نشد یا حساب کاربری فعال است."}, status=status.HTTP_400_BAD_REQUEST)  
  
  
 
 
 
  
  
  
  
  
  
  
  
    

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        
        return response
    

class RetrieveUser1(generics.RetrieveAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

class RetrieveUser(viewsets.GenericViewSet, mixins.ListModelMixin):
     queryset = UserAccount.objects.all()
     serializer_class = UserAccountSerializer
     
     def get_queryset(self):
         text = self.request.query_params.get('query', None)
         if not text: 
             return self.queryset
         
         return self.queryset.filter(id=text)






class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(account=self.request.user)
        
class ProfileList(generics.RetrieveAPIView):
     queryset = Profile.objects.all()
     serializer_class = ProfileSerializer

     def get_queryset(self):
        email = self.request.user.email
        return Profile.objects.filter(user__email=email)


      
    
    
    
    

