from rest_framework import serializers

from .models import Profile , UserAccount , Comment
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated



 






class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        # permission_classes = [IsAuthenticated]
        model = UserAccount
        fields = ['id', 'first_name', 'last_name',  'email', 'get_image', 'get_background', 'profile_pic' , 'background' , 'artistname' ]
        
        
    def user_posts(self, account):

        posts = Profile.objects.filter(account=account)
        return ProfileSerializer(posts, many=True).data



        
        
    def user_posts1(self, account ):

        posts = Profile.objects.filter(account=account)
        return ProfileSerializer1(posts, many=True).data
    

    def user_posts2(self , unique_id):

         posts = Profile.objects.filter(unique_id=unique_id)
         return ProfileSerializer1(posts, many=True).data
    



    
    
    
    
class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(default = 'avatar.png', max_length=250)
    author = serializers.CharField(source='author.artistname', read_only=True)
    post = serializers.CharField(source='post.unique_id'  )
    class Meta: 
        model = Comment
        fields = ('content' ,  'id', 'author' , 'updated', 'created', 'post' )

class CommentSerializer1(serializers.ModelSerializer):
    content = serializers.CharField(default = 'avatar.png', max_length=250)
    author = serializers.CharField(source='author.artistname', read_only=True)
    post = serializers.CharField()
    class Meta: 
        model = Comment
        fields = ('content' ,  'id', 'author' , 'updated', 'created', 'post'  )

  
    
    
class ProfileSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True , required=False) 
    image = serializers.ImageField(default='avatar.png'  ,allow_empty_file=False)
    track = serializers.FileField(default='avatar.png' ,max_length=None,allow_empty_file=False )
    title = serializers.CharField(default='avatar.png',max_length=250 ,)
    description = serializers.CharField(default='avatar.png',max_length=250)
    class Meta:  
        model = Profile
        fields = ('id', 'title', 'description' , 'unique_id'  , 'image', 'get_image', 'track', 'tracks', 'unique_id' ) #if have problem add 'account'  
    
    def user_comment(self, unique_id):

        comment = Comment.objects.filter(unique_id=unique_id)
        return Comment(comment, many=True).data
    
    
class ProfileSerializer1(serializers.ModelSerializer):
   
    comments = CommentSerializer(many=True) 
    image = serializers.ImageField(default='avatar.png'  ,allow_empty_file=False)
    track = serializers.FileField(default='avatar.png' ,max_length=None,allow_empty_file=False )
    title = serializers.CharField(default='avatar.png',max_length=250 ,)
    description = serializers.CharField(default='avatar.png',max_length=250)
    class Meta:  
        model = Profile
        fields = ('id', 'title', 'description' , 'unique_id'  , 'image', 'get_image', 'track', 'tracks' , 'comments' )    




class ProfileSerializer2(serializers.ModelSerializer):
   
    comments = CommentSerializer(many=True) 
    image = serializers.ImageField(default='avatar.png'  ,allow_empty_file=False)
    track = serializers.FileField(default='avatar.png' ,max_length=None,allow_empty_file=False )
    title = serializers.CharField(default='avatar.png',max_length=250 ,)
    description = serializers.CharField(default='avatar.png',max_length=250)
    class Meta:  
        model = Profile
        fields = ('id', 'title', 'description' , 'slug', 'unique_id'  , 'image', 'get_image', 'track', 'tracks' , 'comments' , 'key', 'ky')   







    
    
class ProfileSerializer3(serializers.ModelSerializer):
   
  
    class Meta:  
        model = Profile
        fields = '__all__'  
    
        
  
    

