from rest_framework.serializers import ModelSerializer
from te.models import User, Account, Tree, PlantedTree

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'active']

class TreeSerializer(ModelSerializer):
    class Meta:
        model = Tree
        fields = ['id', 'name', 'scientific_name']

class PlantedTreeSeriallizer(ModelSerializer):
    tree = TreeSerializer()
    class Meta:
        model = PlantedTree
        fields = ['id', 'tree', 'age', 'planted_at', 'latitude', 'longitude', 'user', 'account']
