from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


class Vendor(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=150, blank=True, null=True)
    shop_name = models.CharField(max_length=200)
    shop_place = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        # Return vendor name if set, else username
        return self.name if self.name else self.username

class OrganicFood(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    fish_type = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Suggestion(models.Model):
    food = models.ForeignKey(OrganicFood, on_delete=models.CASCADE)
    fish_type = models.CharField(max_length=100)

    def __str__(self):
        return f"Suggest {self.food.name} for {self.fish_type}"
