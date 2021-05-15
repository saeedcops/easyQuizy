from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer,ProfileSerializer,ProfileListSerializer
from core.models import Profile
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from push_notifications.models import  GCMDevice
from django.core.exceptions import ValidationError

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for a user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Mange the authenticated user"""
    serializer_class = ProfileSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        profile= Profile.objects.get(user=self.request.user)
        profile.is_active=True
        profile.save()
        return profile

    def put(self, request, *args, **kwargs):
        
        body_unicode = request.body.decode('utf-8')
        profile= Profile.objects.get(user=self.request.user)
        if "user_id" in body_unicode:
            profile =Profile.objects.get(pk=request.POST['user_id'])
            serializer = ProfileSerializer(profile)
        
            return Response(serializer.data)

        elif "delete" in body_unicode:
            if request.POST['delete']==str(profile.id):
                try:
                    GCMDevice.objects.get(
                        cloud_message_type="FCM",
                        user=self.request.user).delete()
                except GCMDevice.DoesNotExist:
                    pass
                self.request.user.delete()
                print("Send"+str(request.POST['delete']))
                print("user"+str(profile.id))
                serializer = ProfileSerializer(profile)
                return Response(serializer.data)
            else:
                print("Not E")
                
                raise ValidationError("You have forgotten about Fred!")

        elif "league_prize" in body_unicode:
            profile.league_prize=False

        elif "daily_coins" in body_unicode:
            profile.coins+=1000
            profile.daily_coins=False

        elif "video" in body_unicode:
            profile.coins+=250
            profile.gem+=1
           
        elif "name" not in body_unicode:
            profile.is_active=False

        if "gem" in body_unicode:
            profile.gem-=1
            profile.save()
            print("Take gem")

        if "image" in body_unicode:

            profile.name=request.POST['name']
            profile.image=request.POST['image']
            profile.flag=request.POST['flag']

        if "facebook_id" in body_unicode:

            profile.name=request.POST['name']
            profile.image=request.POST['image']
            profile.flag=request.POST['flag']
            profile.facebook_id=request.POST['facebook_id']
            profile.user.facebook_id=request.POST['facebook_id']
            profile.user.save()
                   
            if request.POST['send_friend'] :
                friend=request.POST['send_friend']
                for item in friend:
                    try:
                         user=Profile.objects.get(facebook_id=item)
                         profile.friends.add(user)
                    # fp= Profile.objects.get(user=user)
                         user.friends.add(profile)
                         user.save()
                    except ObjectDoesNotExist:
                        pass
        
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ManageUserFriendsView(generics.RetrieveUpdateAPIView):
    """Mange the authenticated user"""
    serializer_class = ProfileListSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        profile= Profile.objects.get(user=self.request.user)
        return profile
