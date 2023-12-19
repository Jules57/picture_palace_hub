from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movie_shows.api.serializers import OrderReadSerializer
from users.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email']


class CustomerOrderSerializer(serializers.ModelSerializer):

    orders = OrderReadSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'username', 'orders', 'total_amount']

    def get_total_amount(self, instance):
        total_amount = instance.orders.aggregate(Sum('total_cost')).get('total_cost__sum')
        return total_amount or 0


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True, source='auth_token.key')

    class Meta:
        model = Customer
        fields = ['id', 'username', 'password', 'password2', 'token']
        write_only_fields = ['password', 'password2']
        read_only_fields = ['id']

    def validate(self, attrs):
        if Customer.objects.filter(username=attrs['username']).count():
            raise ValidationError('This username is already taken.')

        if attrs['password'] != attrs['password2']:
            raise ValidationError('Passwords did not match.')
        attrs.pop('password2')
        return attrs
