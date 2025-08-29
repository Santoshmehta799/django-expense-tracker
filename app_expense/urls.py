from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import ExpenseViewSet, MonthlySummaryView, RegisterView


router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')


urlpatterns = [
path('register/', RegisterView.as_view(), name='register'),
path('summary/monthly/', MonthlySummaryView.as_view(), name='monthly-summary'),
path('', include(router.urls)),
]