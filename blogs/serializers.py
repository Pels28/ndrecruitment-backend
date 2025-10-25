
from rest_framework import serializers
from .models import Post, Author, Category, Tag

class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name')
    email = serializers.CharField(source='user.email')
    avatar = serializers.SerializerMethodField()  # Add this
    
    class Meta:
        model = Author
        fields = ['name', 'avatar', 'email']
    
    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url  # This will now return Cloudinary URL
        return None

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    categories = CategorySerializer(many=True)
    frontmatter = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()  # Add this to override the image field
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'description', 'image', 
            'author', 'categories', 'date', 'frontmatter', 'reading_time'
        ]
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url  # This will now return Cloudinary URL
        return None
    
    def get_frontmatter(self, obj):
        return {
            'title': obj.title,
            'image': obj.image.url if obj.image else None,  # Cloudinary URL
            'author': {
                'name': obj.author.user.get_full_name() or obj.author.user.username,
                'avatar': obj.author.avatar.url if obj.author.avatar else None  # Cloudinary URL
            },
            'date': obj.date.isoformat(),
            'draft': obj.draft
        }
    
    def get_reading_time(self, obj):
        return obj.reading_time()

class PostDetailSerializer(PostListSerializer):
    content = serializers.CharField()
    
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['content', 'tags']