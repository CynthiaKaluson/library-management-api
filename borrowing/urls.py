from rest_framework.routers import DefaultRouter
from .views import BorrowRecordViewSet

router = DefaultRouter()
router.register(r'borrow', BorrowRecordViewSet, basename='borrow')

urlpatterns = router.urls