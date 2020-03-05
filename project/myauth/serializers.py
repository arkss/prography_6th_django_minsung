from rest_framework import serializers as sz
from .models import Profile


class ProfileSerializer(sz.ModelSerializer):
    password = sz.CharField()

    def create(self, validated_data):
        print("create")
        print(validated_data)
        password = validated_data.pop('password')
        print(validated_data)
        print(password)
        profile = Profile(**validated_data)
        profile.set_password(password)
        profile.save()
        return profile

    class Meta:
        model = Profile
        fields = [
            'username',
            'email',
            'password'
        ]
