from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import BorrowRecord
from .serializers import BorrowRecordSerializer
from books.models import Book


class BorrowRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return BorrowRecord.objects.all()
        return BorrowRecord.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        if book.copies_available < 1:
            return Response({'error': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

        existing_borrow = BorrowRecord.objects.filter(
            user=request.user, book=book, is_returned=False
        ).exists()

        if existing_borrow:
            return Response({'error': 'You already have this book borrowed'},
                            status=status.HTTP_400_BAD_REQUEST)

        due_date = timezone.now().date() + timedelta(days=14)
        borrow_record = BorrowRecord.objects.create(
            user=request.user, book=book, due_date=due_date
        )

        book.copies_available -= 1
        book.save()

        serializer = self.get_serializer(borrow_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrow_record = self.get_object()

        if borrow_record.is_returned:
            return Response({'error': 'Book already returned'},
                            status=status.HTTP_400_BAD_REQUEST)

        borrow_record.is_returned = True
        borrow_record.returned_at = timezone.now()
        borrow_record.save()

        book = borrow_record.book
        book.copies_available += 1
        book.save()

        serializer = self.get_serializer(borrow_record)
        return Response(serializer.data)