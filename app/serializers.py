from .models import Shipping,Shipping_Cargo,Cargo, User
from rest_framework import serializers
class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['pk','title' , 'price_per_ton', 'short_description' , 'description', 'is_active', 'logo_file_path']
        read_only_fields = ['pk']
    


class Client_Serialzier(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "username"]

class ShippingSerializer(serializers.ModelSerializer):
    client = Client_Serialzier()

    class Meta:
        model = Shipping
        fields = ['pk',"creation_datetime", 'status', "completion_datetime" , 'formation_datetime' ,  'client', 'manager' , 'organization' ,'total_price']
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


# class Cargo_for_shippingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cargo
#         fields = ["pk", "title",  "short_description", "logo_file_path"]


class connection_Serializer(serializers.ModelSerializer):
      cargo = serializers.SerializerMethodField()
      def get_cargo(self, obj):
           return {
            'pk' : obj.id,
            "title": obj.cargo.title,
            "short_description": obj.cargo.short_description,
            "description" : obj.cargo.description,
            "price_per_ton" : obj.cargo.price_per_ton,
            "logo_file_path": obj.cargo.logo_file_path,
        }
      class Meta:
            model = Shipping_Cargo
            fields = ["cargo", 'amount']        


class Shipping_with_info_Serializer(serializers.ModelSerializer):
        cargo_list = serializers.SerializerMethodField()

        def get_cargo_list(self, obj):
            cargo_list = connection_Serializer(obj.shipping_cargo_set, many=True).data
            amount_list = [cargo['amount'] for cargo in cargo_list]

            cargo_list = [cargo['cargo'] for cargo in cargo_list]
            for i,cargo in enumerate(cargo_list):
                 cargo['amount'] = amount_list[i]
  

            return cargo_list
        class Meta:
            model = Shipping
            fields = ['pk', "creation_datetime",  "completion_datetime" , 'client', 'manager' , 'organization', 'cargo_list']