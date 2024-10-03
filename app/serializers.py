from .models import Shipping,Shipping_Cargo,Cargo, User
from rest_framework import serializers
class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['pk','title' , 'price_per_ton', 'short_description' , 'description', 'is_active', 'logo_file_path']
        read_only_fields = ['pk']

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['pk',"creation_datetime", 'status', "completion_datetime" , 'client', 'manager' , 'organization' ,'total_price']
        # read_only_fields = ['status']

class Shipping_CargosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping_Cargo
        fields = ['shipping', 'cargo', 'amount']

class ResolveShipping(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['status']


class Adding_to_shippingSerializer(serializers.ModelSerializer):
        class Meta:
            model = Shipping
            fields = ['pk',"creation_datetime",  "completion_datetime" , 'client', 'manager' , 'organization' ,'total_price' ,'status']
            read_only_fields = ['pk',"creation_datetime",  "completion_datetime" , 'client', 'manager'  ,'total_price', 'status']
            extra_kwargs = {
            'organization': {'read_only': False}
        }




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']


class Cargo_for_shippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ["pk", "title",  "short_description", "logo_file_path"]


class connection_Serializer(serializers.ModelSerializer):
    cargo = Cargo_for_shippingSerializer()

    class Meta:
        model = Shipping_Cargo
        fields = ["pk", "cargo", "amount"]        


class Shipping_with_info_Serializer(serializers.ModelSerializer):
        cargo_list = connection_Serializer(source='shipping_cargo_set', many=True)
        class Meta:
            model = Shipping
            fields = ['pk', "creation_datetime",  "completion_datetime" , 'client', 'manager' , 'organization', 'cargo_list']