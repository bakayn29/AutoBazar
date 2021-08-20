from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', )


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'  # ('id', 'title', 'price', 'category', 'created', 'comments', 'likes')

    def to_representation(self, instance):
        action = self.context.get('action')
        representation = super().to_representation(instance)

        representation['author'] = instance.author.email
        representation['category'] = instance.category.name
        representation['images'] = ProductImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['likes'] = instance.likes.count()

        if action == 'list':
            representation['rating'] = instance.ratings.count()
        elif action == 'retrieve':
            representation['rating'] = RatingSerializer(instance.ratings.all(), many=True).data
            if representation['rating'] == []:
                representation['rating'] = 'Рейтинги не добавлены'

        if action == 'list':
            representation['comments'] = instance.comments.count()
        elif action == 'retrieve':
            representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
            if representation['comments'] == []:
                representation['comments'] = 'Комментариев нет'
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            ProductImage.objects.create(
                image=image,
                product=instance
            )
        return instance


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


class RatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        email = request.user
        product = validated_data.get('product')

        if Rating.objects.filter(author=email, product=product):
            rating = Rating.objects.get(author=email, product=product)
            return rating

        rating = Rating.objects.create(author=request.user, **validated_data)
        return rating


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        product = validated_data.get('product')

        if Like.objects.filter(author=author, product=product):
            like = Like.objects.get(author=author, product=product)
            return like

        like = Like.objects.create(author=author, **validated_data)
        return like





