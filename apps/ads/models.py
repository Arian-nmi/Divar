from django.db import models
from django.conf import settings
from apps.users.models import User


class Province(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f"{self.name} - {self.province.name}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def is_leaf(self):
        return not self.children.exists()


class Ad(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ads', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('pending', 'در انتظار تایید'),
        ('active', 'منتشر شده'),
        ('rejected', 'رد شده'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.title} - {self.price}تومان "


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ad')

    def __str__(self):
        return f"{self.user.email} - {self.ad.title}"


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ad_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.ad.title}"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.recipient} | {self.text[:30]}"