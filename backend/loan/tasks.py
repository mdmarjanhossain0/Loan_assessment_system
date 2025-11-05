from celery import shared_task

from loan.models import (
    LoanApplication,
    # LoanDocument
)
from loan.utils import (
    calculate_dsr,
    extract_text_from_image,
    generate_credit_summary,
    parse_salary_info,
    extract_text_from_pdf
)

import json
from decouple import config
from google import genai

from google.genai import types
from google.genai.types import Part
import re
import os
import base64

GEMINI_API_KEY = config("GEMINI_API_KEY")

MODEL = "gemini-2.5-flash"
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return "data:application/pdf;base64," + encoded





def create_detailed_prompt(loan_amount):
    return f"""
    Analyzes customer documents and behavioral patterns to emulate a trained loan officer’s decision-making, providing a fair, transparent, and data-driven loan recommendation for approval and loan amount qualified in real time.

    ***AI provides reasoning for every decision***

    INPUTS:
        - The customer wanted the loan amount: {loan_amount}

    Your response must be a single JSON object.

    ATTRIBUTES:
        - document_type,
        - dsr
        - dsr_explanation,
        - creadit_risk_score,
        - creadit_risk_score_explanation,
        - max_loan_eligibility,
        - max_loan_eligibility_explanation,
        - creadit_summary,
        - behavioral_responsibility_scoring,
        - behavioral_responsibility_scoring_explanation
        - loan_status


    CONDITIONAL VALUES:
    - document_type: ["Job Letter", "Payslip", "Bank Statement", "Other"]
    - creadit_risk_score: Combines all data into a 0–100 score:
        - ≥80: Low risk (full approval)
        - 60–79: Medium (partial)
        - <60: High (decline/guarantor)
    - loan_status: ["Approved", "Declined"]
    - creadit_summary: Describes the creditworthiness of the customer.

    ADDITIONAL INFORMATION:
    - dsr = (Total debt obligations ÷ Gross income) × 100
    - max_loan_eligibility: According to DSR, AI flags if DSR exceeds 70% then suggests max eligible loan amount under DSR threshold. Adjusts for irregular income, business earnings, or freelance jobs.
    - behavioral_responsibility_scoring: Uses historical customer data (repayment punctuality, missed payments, spending patterns). Adds qualitative factors such as reference credibility and consistency of employment. Predictive model forecasts repayment probability based on similar profiles.
    - Explainable AI (XAI) Layer:
    Every decision is accompanied by rationale:
        “Approved: stable income, regular salary inflow, clean credit history.”
        “Declined: high existing debt, inconsistent deposits.”
    """

def extract_attributes_gemini(file_path, loan_amount):
    uploaded_file = pdf_to_base64(file_path)

    prompt = create_detailed_prompt(loan_amount)
    print(prompt)
    
    contents = [ 
        uploaded_file, 
        prompt,
    ]


    config = types.GenerateContentConfig(
        system_instruction="You are an expert product attributes analyzer. Your response must be a single JSON object.",        
        response_mime_type="application/json",
    )

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config,
    )

    print(response.text)
    return json.loads(response.text)





def parse_object(application):

    print(f"File path {application.file.path} Loan amount {application.loan_amount}")
    response = extract_attributes_gemini(application.file.path, application.loan_amount)
    application.parsed_data = response
    application.credit_summary = response.get("creadit_summary")
    application.dsr = response.get("dsr")
    application.document_type = response.get("document_type")
    application.ai_status = response.get("loan_status")
    application.is_ai_processed = True
    application.save()
    return application


@shared_task
def parse_document(application_pk):
    print(f"Document parsed {application_pk}")
    application = LoanApplication.objects.get(pk=application_pk)
    parse_object(application)
    


@shared_task
def check_applications():
    applications = LoanApplication.objects.filter(is_ai_processed=False)
    print(f"Total appllications {len(applications)}")
    for application in applications:
        parse_object(application)

# @shared_task
# def check_applications():
#     applications = LoanApplication.objects.filter(is_ai_processed=False)
#     print(f"Total appllications {len(applications)}")
#     for application in applications:
#         documents = application.documents.all()

#         count = 0
#         gmi = 0.0
#         emo = 0.0
#         avg_dsr = 0.0
#         for document in documents:
#             if document.is_ai_parsed:
#                 document = parse_object(document)
#             try:
#                 print(document.parsed_data)
#                 data = document.parsed_data
#                 count += 1
#                 gmi += float(data.get("gmi", 0))
#                 emo += float(data.get("emo", 0))
#                 avg_dsr += float(data.get("dsr", 0))
#                 if count < 1:
#                     count = 1
#                 avg_dsr = avg_dsr / count
#                 summary = f"Total gmi: {gmi}, emo: {emo}, average dsr: {avg_dsr}"
#                 application.credit_summary = summary
#                 print(summary)
#                 application.is_ai_processed = True
#                 application.save()
#             except BaseException as e:
#                 print(e)
        
        