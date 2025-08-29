from django.shortcuts import render

from collections import defaultdict
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Expense
from .permissions import IsOwner
from .serializers import ExpenseSerializer, RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        qs = Expense.objects.filter(user=self.request.user)
        # Filters
        start = self.request.query_params.get('startDate')
        end = self.request.query_params.get('endDate')
        category = self.request.query_params.get('category')
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')


        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)
        if category:
            qs = qs.filter(category=category)
        if min_amount:
            qs = qs.filter(amount__gte=min_amount)
        if max_amount:
            qs = qs.filter(amount__lte=max_amount)


        # Ordering (Bonus): ?ordering=date or -amount
        ordering = self.request.query_params.get('ordering') # DRF default name
        if ordering:
            qs = qs.order_by(ordering)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
    # Object-level check on retrieve/update/destroy
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = self.permission_classes + [IsOwner]
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Expense deleted successfully"},
            status=status.HTTP_200_OK
        )
    
class MonthlySummaryView(APIView):
    def get(self, request):
        data = (
            Expense.objects
            .filter(user=request.user)
            .annotate(month=TruncMonth('date'))
            .values('month', 'category')
            .annotate(total=Sum('amount'))
            .order_by('month', 'category')
        )

        out = defaultdict(dict)
        for row in data:
            month_key = row['month'].strftime('%Y-%m') if row['month'] else 'unknown'
            out[month_key][row['category']] = float(row['total'])
        return Response(out)