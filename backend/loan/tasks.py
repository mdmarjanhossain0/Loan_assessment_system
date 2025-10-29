from celery import shared_task

from loan.models import (
    LoanApplication,
    LoanDocument
)
from loan.utils import (
    calculate_dsr,
    extract_text_from_image,
    generate_credit_summary,
    parse_salary_info,
    extract_text_from_pdf
)

import json

def parse_object(document):
    if document.file.path.split(".")[-1].lower() == "pdf":
        text = extract_text_from_pdf(document.file.path)
    else:
        text = extract_text_from_image(document.file.path)
    document.extracted_text = text
    parsed_data = parse_salary_info(text)
    document.parsed_data = parsed_data
    document.is_ai_parsed = True
    document.save()
    return document

@shared_task
def parse_document(document_pk):
    print(f"Document parsed {document_pk}")
    document = LoanDocument.objects.get(pk=document_pk)
    parse_object(document)
    


@shared_task
def check_applications():
    applications = LoanApplication.objects.filter(is_ai_processed=False)
    print(f"Total appllications {len(applications)}")
    for application in applications:
        documents = application.documents.all()

        count = 0
        gmi = 0.0
        emo = 0.0
        avg_dsr = 0.0
        for document in documents:
            if document.is_ai_parsed:
                document = parse_object(document)
            try:
                print(document.parsed_data)
                data = document.parsed_data
                count += 1
                gmi += float(data.get("gmi", 0))
                emo += float(data.get("emo", 0))
                avg_dsr += float(data.get("dsr", 0))
                if count < 1:
                    count = 1
                avg_dsr = avg_dsr / count
                summary = f"Total gmi: {gmi}, emo: {emo}, average dsr: {avg_dsr}"
                application.credit_summary = summary
                print(summary)
                application.is_ai_processed = True
                application.save()
            except BaseException as e:
                print(e)
        
        