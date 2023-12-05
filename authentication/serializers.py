from rest_framework import serializers

from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    # password : write only, not send the password back to the user.
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', ]

    def create(self, validated_data):  # validated_data : the data will have benn validated.
        return User.objects.create_user(**validated_data)
