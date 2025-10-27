from rest_framework import serializers
from loan.models import LoanApplication, LoanDocument


class LoanDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDocument
        fields = "__all__"


class LoanApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanApplication
        fields = "__all__"
    
    def validate_documents(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("At least one document is required.")
        return value
