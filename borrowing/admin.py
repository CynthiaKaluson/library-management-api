from django.contrib import admin
from .models import BorrowRecord

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrowed_at', 'due_date', 'is_returned']
    list_filter = ['is_returned', 'borrowed_at']
    search_fields = ['user__username', 'book__title']