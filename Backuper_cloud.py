"""
Module responsible for interacting with the Google Drive v3 API.
Manages OAuth2 authentication and uploads
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from backuper import logger,setup_logging
from dotenv import load_dotenv

load_dotenv()

# .env Setup
ARQUIVO_CREDENCIAIS = os.getenv("CAMINHO_CREDENTIALS")
ARQUIVO_TOKEN = os.getenv("CAMINHO_TOKEN")

setup_logging()
# Permission to read and write files in Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def google_drive_authenticator():
    
    """
    Manages the access token lifecycle (OAuth2)
    Creates or updates the 'token.json' file automatically
    """
    
    creds = None
    if os.path.exists(ARQUIVO_TOKEN):
        creds = Credentials.from_authorized_user_file(ARQUIVO_TOKEN, SCOPES)
        
    # If there are no valid credentials, it initiates login via browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds._refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(ARQUIVO_CREDENCIAIS, SCOPES)
            
            creds = flow.run_local_server(port=0)
        with open(ARQUIVO_TOKEN, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3',credentials=creds)
        logger.info("Google Drive authentication successful!")
        return service
    except Exception as e:
        logger.error(f'Error: {e}')
        return None

DRIVE_FOLDER_NAME = 'Backups_Minecraft_Vanilla'

def get_drive_folder_id(service):
    
    """Search for the backup folder by name. If it doesn't exist, create a new one."""
    
    query = f"mimeType='application/vnd.google-apps.folder' and name='{DRIVE_FOLDER_NAME}'"
    response = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id,name)'
    ).execute()
    
    items = response.get('files',[])
    
    if items:
        logger.info(f"'{DRIVE_FOLDER_NAME}' Found!")
        return items[0]['id']
    else:
        logger.info(f"Folder '{DRIVE_FOLDER_NAME}' not found. Creating it. . . ")
        file_metadata = {
            'name': DRIVE_FOLDER_NAME,
            'mimeType':'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields = 'id').execute()
        logger.info(f" Folder '{DRIVE_FOLDER_NAME}' sucessfully created")
        return folder.get('id')

def upload_and_cleanup(service,folder_id,local_file_path,world_name):
     
    """
    Upload the file
    If the file already exists in Drive, perform an UPDATE (replace) operation
    Otherwise, perform a CREATE operation (create a new file)
    """
    
    file_name = f'{world_name}.zip'
    # Verifies if thefile exists in the target folder
    search_query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    response = service.files().list(
        q=search_query,
        fields='files(id)'
    ).execute()
    
    existing_files = response.get('files', [])
    
    file_metadata = {
        'name': f'{world_name}.zip',
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(local_file_path, resumable=True)
    
    try:
        if existing_files:
            # Updates the existing file (keeps the same ID in Drive)
            existing_file_id = existing_files[0]['id']
            service.files().update(
                fileId = existing_file_id,
                media_body = media
            ).execute()
        else:
            # Creates a new file
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
        logger.info(f"Upload of '{world_name}.zip' to Drive completed.")
        return True
    except Exception as e:
        logger.error(f" Fatal error during upload/cleanup of {world_name}: {e}")
        return False