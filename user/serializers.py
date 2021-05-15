from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User
import uuid
from core.models import Profile




class UserSerializer(serializers.ModelSerializer):
    """serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('user_id','password', 'facebook_name', 'facebook_image','facebook_id', 'friend','flag','token')
        # fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5},
                        'user_id': {'read_only': True, 'min_length': 5},}

    def create(self, validated_data):
        """create a new user with encrypted password and return it"""
        user=User()
        user_id=uuid.uuid4()
        if validated_data['facebook_id']:
            user=get_user_model().objects.create_user(
                        user_id=user_id,
                        password=validated_data['password'],
                        facebook_id=validated_data['facebook_id'],
                        friend=validated_data['friend'],
                        flag=validated_data['flag'],
                        facebook_image=validated_data['facebook_image'],
                        facebook_name=validated_data['facebook_name'],
                        token=validated_data['token']
            )
        else:
            user=get_user_model().objects.create_user(
                        user_id=user_id,
                        password=validated_data['password'],
                        flag=validated_data['flag'],
                        token=validated_data['token']
            )
        
        return user

    def update(self, instance, validated_data):
        """Update user and setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serialize for user authentication object"""
    user_id = serializers.CharField()
    password = serializers.CharField(
            style = {'input_type': 'password'},
            trim_whitespace = False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        user_id = attrs.get('user_id')
        password = attrs.get('password')

        user = authenticate(
                request = self.context.get('request'),
                username = user_id,
                password = password
        )

        if not user:
            msg = _('Unable to authenticate with providing credintials')
            raise serializers.ValidationError(msg, code = 'authentication')

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    """serializer for the user object"""

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('league_coins','user','friends','my_league','level','score','next_gift',
                            'created','updated','gem','token','is_active')
        # ordering = ['-league_coins','id']
        ordering = ['league_coins']


class ProfileListSerializer(serializers.ModelSerializer):
    friends = ProfileSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = ['friends',]