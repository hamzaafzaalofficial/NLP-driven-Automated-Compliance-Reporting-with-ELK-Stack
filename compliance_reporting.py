import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Elasticsearch Configuration
ES_HOST = "http://142.93.213.134:9200"  # Update with your Elasticsearch host
INDEX = "syslog-*"

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "haal.official@gmail.com"
EMAIL_PASSWORD = ""
EMAIL_TO = ["haial@gmail.com"]
EMAIL_SUBJECT = "Automated Compliance"

# Query Elasticsearch
def fetch_compliance_data():
    es = Elasticsearch(ES_HOST)
    s = Search(using=es, index=INDEX).query("match", message="PII")
    response = s.execute()
    report = [hit.to_dict() for hit in response]
    return report

# Generate Report
def generate_report(report_data, report_file):
    with open(report_file, "w") as f:
        json.dump(report_data, f, indent=4)
    print(f"Report saved to {report_file}")

# Send Email with Report
def send_email(report_file):
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = ", ".join(EMAIL_TO)
    msg['Subject'] = EMAIL_SUBJECT

    # Add body
    body = "Please find the attached compliance report."
    msg.attach(MIMEText(body, 'plain'))

    # Attach report
    with open(report_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={report_file}",
        )
        msg.attach(part)

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
    print("Email sent successfully!")

# Main Function
def main():
    report_file = "compliance_report.json"
    report_data = fetch_compliance_data()
    generate_report(report_data, report_file)
    send_email(report_file)

if __name__ == "__main__":
    main()