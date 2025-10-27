from django.urls import path, include
from rest_framework.routers import DefaultRouter
from loan.api.views import LoanApplicationViewSet

router = DefaultRouter()
router.register("applications", LoanApplicationViewSet, basename="loan-application")


app_name = "loan_api"


urlpatterns = [
    path("", include(router.urls)),
]
