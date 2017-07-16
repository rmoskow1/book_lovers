from rest_framework import serializers

from book_lovers.books.models import Book, Publisher


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    # Book serializer for a non admin user
    users_who_favorite = serializers.StringRelatedField(read_only=True, many=True)
    tags = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'pen_name', 'date', 'publisher', 'text', 'uploader',
                  'author', 'users_who_favorite', 'tags', 'isPublished')
        read_only_fields = ('uploader', 'author')  # cannot be changed by user, set during creation in BookViewSet
        extra_kwargs = {
            'isPublished': {'write_only': True}
        }


class BookAdminSerializer(BookSerializer):
    # different from BookSerializer in that it contains the field - 'isVerified', which only an admin has any access to

    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ('isVerified',)
        extra_kwargs = {
            'isPublished': {'write_only': False}
        }
