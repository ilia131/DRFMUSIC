from django.urls import path , include , re_path
from rest_framework import routers
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
    ProfileList,
    RetrieveUser,
    RetrieveUser1,
    # EmailVerificationAPIView
    # CurrentUserView,
    
)
from userartist import views
from . import views
router = routers.SimpleRouter()
# router.register(r'users', views.UserViewSet)

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')
router.register('user2', views.RetrieveUser, basename='userid')
router.register('userMe6', views.UuuidView , basename='uuid')
# router.register("posts", views.UserViewSetChild2)

# router.register(r'^users/me/$', views.UserViewSet, basename='users/me'),
# router.register('usersme', views.UserViewSet, basename='usersme')
urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/<int:pk>', ProfileList.as_view(),),
    path('userid/<int:pk>', RetrieveUser1.as_view()),
    path('userME/', views.UserViewSetChild.as_view() , name='users-me'),
    path('userME1/', views.UserViewSetChild1.as_view() , name='users-me'),
    path('userME2/', views.UserViewSetChild2.as_view() , name='users-me'),
    path('userME3/', views.UserViewSetChild3.as_view() , name='users-me'),
    path('userME4/<int:pk>/', views.ProfileDetailsView().as_view, name='user-me1'),
    path('add-comment-to-post/',views.AddCommentToPost.as_view(), name='add-comment-to-post'),
    path('p/<slug:profile_slug>/<slug:comment_slug>/', views.UploadmusicVUE.as_view()),
    path('', include(router.urls))
]
