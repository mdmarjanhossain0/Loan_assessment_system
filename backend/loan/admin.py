from django.contrib import admin

from loan.models import (
    LoanApplication,
)


admin.site.register(LoanApplication)
# admin.site.register(LoanDocument)