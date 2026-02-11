"""
Utility for sending emails with attachments (Logs)
Independent of environment variables to facilitate reuse
"""

import os
import glob
import smtplib
from email.message import EmailMessage
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

def get_lastest_log_file(log_dir):
    """Finds the lastest log in the folder"""
    
    try:
        list_of_files = glob.glob(os.path.join(log_dir, '*.log'))
        if not list_of_files:
            return None

        lastest_file = max(list_of_files, key=os.path.getmtime)
        return lastest_file
    except Exception as e:
        print(f"\nError most recent log file not found!: {e}\n")
        return None

def send_log_email(log_file_path,sender,recipient,password):
    
    """Sends the specified log via email using SMTP SSL"""
    
    try:
        msg = EmailMessage()
        
        log_timestamp = os.path.getmtime(log_file_path)
        log_date_str = datetime.fromtimestamp(log_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        msg['Subject'] = f"Minecraft Backup Relatory - {log_date_str}"
        msg['From'] = sender
        msg['To'] = recipient
        
        log_file_name = os.path.basename(log_file_path)
        
        
        msg.set_content(f"Hey,\n\nAttached is the most recent log report from the backup script.\n\nLog Date: {log_date_str}\n\nSincerely,\nYour Backup Script.")

        with open(log_file_path, "rb") as attachment:
            attachment_data = attachment.read()
        msg.add_attachment(attachment_data,maintype='application', subtype='octet-stream', filename=log_file_name)
        
    except Exception as e:
        print(f"Attchment ERROR: {e}")
        return False
    
    try:
        print("\nConnecting to SMTP server...\n")
        
        # Safe connection with Gmail
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        
       
        print("Log Email succefully send!!")
        return True
    except smtplib.SMTPAuthenticationError:
        print("\n⚠️ AUTHENTICATION ERROR: Check your email/password or Gmail App Key.")
        return False
    except Exception as e:
        print(f"\n⚠️ SENDING EMAIL ERROR: {e}")
        return False
def clean_up_logs(log_file_limit=5):
    
    """It keeps only the most recent N logs, deleting the older ones"""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, 'logs')
    
    log_files = glob.glob(os.path.join(log_dir,'*.log'))
    
    current_log_count = len(log_files)
    
    print("\n--- Logs Clean up Verification ---")
    print(f"\nCurrent log files: {current_log_count}")
    
    if current_log_count >= log_file_limit:
        print(f'⚠️ LIMIT REACHED! Deleting {current_log_count} logs (Limit: {log_file_limit}).')
        
        deleted_count = 0
        
        try:
            for file_path in log_files:
                os.remove(file_path)
                deleted_count+=1
            print(f'Log cleanup complete. {deleted_count} files deleted.')
            return True
        except Exception as e:
            print(f"Logs deleting error: {e}")
            return False
    else:
        print(f"No logs deleted. The count is below the limit of {log_file_limit}.")
        return False