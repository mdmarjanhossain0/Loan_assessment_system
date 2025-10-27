from django.contrib import admin

from loan.models import (
    LoanApplication,
    LoanDocument
)


admin.site.register(LoanApplication)
admin.site.register(LoanDocument)