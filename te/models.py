from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def plant_tree(self, data):
        PlantedTree.objects.create(**data)

    def plant_trees(self, data):
        trees = [PlantedTree(**tree) for tree in data]
        PlantedTree.objects.bulk_create(trees)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username   

class Account(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

class Tree(models.Model):
    name = models.CharField(max_length=50, unique=True)
    scientific_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name 
    
class PlantedTree(models.Model):
    age = models.IntegerField()
    planted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=12, decimal_places=9)
    longitude = models.DecimalField(max_digits=13, decimal_places=9)

    def __str__(self):
        return f"{self.tree.name} planted by {self.user.username}"

    def location(self):
        return f"{self.latitude}, {self.longitude}"