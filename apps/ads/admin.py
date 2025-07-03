from django.contrib import admin
from .models import Ad, Category, AdImage, Favorite


admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(AdImage)
admin.site.register(Favorite)
