import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import os

def send_email(file_paths, receiver_email, jobID):
    print(f"Python JobID {jobID}")
    sender_email = "CLASHub@ufl.edu"
    subject = f"File Download JobID {jobID}"
    base_url = "http://clashhub.rc.ufl.edu"

    # Initialize the message body
    message_lines = ["Hello,\n"]

    # Extract file paths
    if len(file_paths) == 2:
        if (jobID[:4] in ["aqPE", "aqSE", "aqCR"]):
            total_file_path, isoform_file_path = file_paths
            total_file_name = os.path.basename(total_file_path)
            isoform_file_name = os.path.basename(isoform_file_path)
            download_total_link = f"{base_url}/{jobID}/{total_file_name}"
            download_isoform_link = f"{base_url}/{jobID}/{isoform_file_name}"
            download_report_link = f"{base_url}/{jobID}/mirnaseq_Analysis_Report.html"
            message_lines.append(f"Your raw data processing summary is: {download_report_link}\n")
            message_lines.append(f"Your raw miRNA count (total abundance) is: {download_total_link}\n")
            message_lines.append(f"Your raw miRNA count (isoform abundance) is: {download_isoform_link}\n")
        if (jobID[:3] == "CUR"):
            curve_file, target_file = file_paths
            curve_file = os.path.basename(curve_file)
            target_file = os.path.basename(target_file)
            download_curve_link = f"{base_url}/{jobID}/{curve_file}"
            download_targetFile_link = f"{base_url}/{jobID}/{target_file}"

            message_lines.append(f"Your cumulative fraction curve is: {download_curve_link}\n")
            message_lines.append(f"Your merged targets data is: {download_targetFile_link}\n")

    if len(file_paths) == 1:
        total_file_path = file_paths[0]
        total_file_name = os.path.basename(total_file_path)
        download_total_link = f"{base_url}/{jobID}/{total_file_name}"

        if jobID[:3] in ["CLQ", "CLA"]:
            report_name = "_".join(jobID.split("_")[1:]) + "_analysis_report.html"
            download_report_link = f"{base_url}/{jobID}/{report_name}"
            message_lines.append(f"Your analysis report link: {download_report_link}\n")
            message_lines.append(f"Your output's link: {download_total_link}\n")
        if jobID[:5] == "rsDeq":
            download_report_link = f"{base_url}/{jobID}/RNAseq_Analysis_Report.html"
            download_genecount_link = f"{base_url}/{jobID}/gene_count_reordered.csv"
            download_deseq2_link = f"{base_url}/{jobID}/differential_expression_results.csv"
            message_lines.extend([
                f"Your raw fastq data processing summary is: {download_report_link}\n",
                f"Your raw gene count is: {download_genecount_link}\n",
                f"Your differential gene expression analysis results are: {download_deseq2_link}\n"
            ])
        if jobID[:5] == "rsTPM":
            download_report_link = f"{base_url}/{jobID}/RNAseq_Analysis_Report.html"
            download_geneTPM_link = f"{base_url}/{jobID}/geneTPM.csv"
            message_lines.extend([
                f"Your raw fastq data processing summary is: {download_report_link}\n",
                f"Your raw gene TPM is: {download_geneTPM_link}\n"
            ])

    message_lines.append("\nThank you for using CLASHub.\n\nBest regards,\nCLASHub.\n")
    message = "\n".join(message_lines)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP('smtp.ufhpc', 25) as server:
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

if __name__ == "__main__":
    # Collect command-line arguments
    args = sys.argv[1:]
    if len(args) < 3:
        print("Usage: sendEmail.py <file_path(s)> <receiver_email> <jobID>")
        sys.exit(1)
    # The last two arguments are receiver_email and jobID
    receiver_email = args[-2]
    jobID = args[-1]
    # The preceding arguments are file paths
    file_paths = args[:-2]
    send_email(file_paths, receiver_email, jobID)
