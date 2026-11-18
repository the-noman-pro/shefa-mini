from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        source="wallet.balance", max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = User
        fields = ["id", "name", "email", "date_joined", "balance"]
        read_only_fields = ["id", "email", "date_joined", "balance"]

    def validate_name(self, value):
        value = " ".join(value.split())
        if len(value) < 2:
            raise serializers.ValidationError("Please enter your full name.")
        return value


class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_name(self, value):
        value = " ".join(value.split())
        if len(value) < 2:
            raise serializers.ValidationError("Please enter your full name.")
        return value

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def validate_password(self, value):
        # Field-level, so a weak password is reported together with any name or email error.
        candidate = User(
            name=str(self.initial_data.get("name", "")), email=str(self.initial_data.get("email", ""))
        )
        try:
            password_validation.validate_password(value, user=candidate)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages)) from exc
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            email=attrs["email"].strip().lower(),
            password=attrs["password"],
        )
        if user is None:
            raise serializers.ValidationError({"non_field_errors": ["Email or password is incorrect."]})
        attrs["user"] = user
        return attrs
