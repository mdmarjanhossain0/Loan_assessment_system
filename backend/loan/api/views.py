from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework.authentication import BasicAuthentication

from rest_framework.parsers import MultiPartParser, FormParser

from account.models import Account
from loan.models import (
    LoanApplication,
    LoanDocument
)

from loan.api.serializers import (
    LoanApplicationSerializer,
    LoanDocumentSerializer
)
from mysite.constants import (
    SUCCESS,
    ERROR
)


from account.permissions import (
    OrPermission,
    LoanPostermission
)
from loan.utils import (
    calculate_dsr,
    extract_text_from_image,
    generate_credit_summary,
    parse_salary_info
)


class LoanApplicationViewSet(viewsets.ModelViewSet):
    queryset = LoanApplication.objects.all().order_by("-pk")
    serializer_class = LoanApplicationSerializer
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [LoanPostermission]



    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == "GET" and self.action == "retrieve":
            context["depth"] = 1
        return context

    

    @action(detail=False, methods=["post"], parser_classes=[MultiPartParser, FormParser], serializer_class=LoanDocumentSerializer)
    def upload_document(self, request):
        doc_type = request.data.get("document_type")
        file = request.FILES.get("file")

        document = LoanDocument.objects.create(
            document_type=doc_type, file=file
        )

        text = extract_text_from_image(document.file.path)
        document.extracted_text = text
        parsed_data = parse_salary_info(text)
        document.parsed_data = parsed_data
        document.save()

        # Update application income if parsed
        # if parsed_data.get("monthly_salary"):
        #     application.monthly_income = parsed_data["monthly_salary"]
        #     application.save()

        return Response(LoanDocumentSerializer(document).data)


    @action(detail=True, methods=["post"])
    def process_application(self, request, pk=None):
        application = self.get_object()
        dsr = calculate_dsr(application.monthly_income, application.total_monthly_debt or 0)
        summary = generate_credit_summary(dsr, {})

        application.dsr = dsr
        application.credit_summary = summary
        application.status = "processed"
        application.save()

        return Response(LoanApplicationSerializer(application).data)

