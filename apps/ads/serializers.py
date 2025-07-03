from rest_framework import serializers
from .models import Ad, Category, Province, City, Favorite, AdImage, Message


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True).data


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'province']


class AdSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        write_only=True,
        source='city'
    )
    images = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'title', 'description', 'price', 'is_active','created_at',
            'updated_at', 'category', 'city', 'city_id', 'images', 'owner', 'status'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_category(self, value):
        if not value.is_leaf():
            raise serializers.ValidationError("فقط می‌توانید در دسته‌بندی‌های نهایی آگهی ثبت کنید!")
        return value

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]


class FavoriteSerializer(serializers.ModelSerializer):
    ad = AdSerializer(read_only=True)
    ad_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        write_only=True,
        source='ad'
    )

    class Meta:
        model = Favorite
        fields = ['id', 'ad', 'ad_id', 'created_at']
        read_only_fields = ['id', 'created_at']


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'ad', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class AdStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['status']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'ad', 'text', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp']