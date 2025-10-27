from django.db import models
from account.models import (
    BaseModel,
    Account
)

class LoanDocument(BaseModel):
    DOC_TYPES = [
        ("job_letter", "Job Letter"),
        ("payslip", "Payslip"),
        ("bank_statement", "Bank Statement"),
    ]
    document_type = models.CharField(max_length=20, choices=DOC_TYPES)
    file = models.FileField(upload_to="loan_documents/")
    extracted_text = models.TextField(blank=True, null=True)
    parsed_data = models.JSONField(blank=True, null=True)


    def __str__(self):
        return f"{self.document_type}"
    

class LoanApplication(BaseModel):
    PENDING = "Pending"
    PROCESSED = "Processed"
    REJECTED = "Rejected"
    APPROVED = "Approved"
    STATUS_CHOICES = [
        (PENDING, PENDING),
        (PROCESSED, PROCESSED),
        (REJECTED, REJECTED),
        (APPROVED, APPROVED),
    ]

    TYPES = [
        ("home_lone", "Home Lone"),
        ("car_lone", "Car Lone"),
        ("sme_lone", "SME Lone"),
        ("personal_lone", "Personal Lone")
    ]

    applicant_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    type = models.CharField(max_length=16, choices=TYPES)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_monthly_debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    dsr = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    credit_summary = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    documents = models.ManyToManyField(LoanDocument, blank=False)

    created_by = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name="referrers", null=True, blank=True)


    def __str__(self):
        return f"{self.applicant_name} - {self.phone_number} : {self.documents.count()} Documents"



