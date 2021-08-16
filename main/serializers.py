from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'category', 'created', 'comments')

    def to_representation(self, instance):
        action = self.context.get('action')
        representation = super().to_representation(instance)

        representation['author'] = instance.author.email
        representation['category'] = instance.category.name
        representation['images'] = ProductImageSerializer(instance.images.all(), many=True, context=self.context).data

        if action == 'list':
            representation['rating'] = instance.ratings.count()
        elif action == 'retrieve':
            representation['rating'] = CreateRatingSerializer(instance.ratings.all(), many=True).data

        if action == 'list':
            representation['comments'] = instance.comments.count()
        elif action == 'retrieve':
            representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        product = Product.objects.create(**validated_data)
        return product


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', )

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comments = Comment.objects.create(
            author=request.user,
            **validated_data
        )
        return comments


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = ("star", "product")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            product=validated_data.get('product', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating


