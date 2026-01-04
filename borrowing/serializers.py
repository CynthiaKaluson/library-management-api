from rest_framework import serializers
from .models import BorrowRecord
from books.serializers import BookSerializer


class BorrowRecordSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'user', 'user_username', 'book', 'book_details',
                  'borrowed_at', 'due_date', 'returned_at', 'is_returned']
        read_only_fields = ['borrowed_at', 'returned_at', 'is_returned']