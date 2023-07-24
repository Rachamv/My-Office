from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # These are claims, you can add custom claims
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        token['profile_picture'] = str(user.profile.profile_picture)
        token['verified'] = user.profile.verified
        token['date_of_birth'] = user.profile.date_of_birth
        token['office_phone_number'] = user.profile.office_phone_number
        token['mobile_number'] = user.profile.mobile_number
        token['alternate_number'] = user.profile.alternate_number
        token['language'] = user.profile.language
        token['address_line_1'] = user.profile.address_line_1
        token['address_line_2'] = user.profile.address_line_2
        token['city'] = user.profile.city
        token['state'] = user.profile.state
        token['postal_code'] = user.profile.postal_code
        token['country'] = user.profile.country
        token['receive_notifications'] = user.profile.receive_notifications
        token['theme'] = user.profile.theme
        token['facebook_url'] = user.profile.facebook_url
        token['twitter_url'] = user.profile.twitter_url
        token['linkedin_url'] = user.profile.linkedin_url
        
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']

        )

        user.set_password(validated_data['password'])
        user.save()

        return user