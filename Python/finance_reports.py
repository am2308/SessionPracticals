import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Load dataset and generate report
df = pd.read_excel("financial_data.xlsx")
report = df.groupby("Account_Type").agg({"Balance": "mean"}).reset_index()
report.to_excel("account_type_report.xlsx", index=False)

# Email setup
sender_email = "your_email@gmail.com"
receiver_email = ["manager@company.com". "2@gamil.com", "3@gmail.com"]
codereplace = "your_codereplace"

# Create email
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = "📊 Financial Report - Automated"

# Attach report
attachment = open("account_type_report.xlsx", "rb")
part = MIMEBase("application", "octet-stream")
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", "attachment; filename= account_type_report.xlsx")
msg.attach(part)

# Send email
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender_email, codereplace)
server.sendmail(sender_email, receiver_email, msg.as_string())
server.quit()

print("📩 Financial report emailed successfully!")
