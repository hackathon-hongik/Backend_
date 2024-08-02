from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'password', 'password2')

    def validate(self, data):
        # 비밀번호 일치 여부 검사
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "The two password fields didn't match."})
        
        # 이메일 중복 여부 검사
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        
        # 닉네임 중복 여부 검사
        if User.objects.filter(nickname=data['nickname']).exists():
            raise serializers.ValidationError({"nickname": "This nickname is already in use."})
        
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password']
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname',)

    def validate_nickname(self, value):
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(nickname=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("This nickname is already in use.")
        return value
