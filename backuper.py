"""
Minecraft Auto-Backuper
Author: Turzimm/Artur
Description: Main script that orchestrates local details and uploads to Google Drive
"""
import os 
import subprocess
from Backuper_cloud import *
from Email_sender import *
import logging
from datetime import datetime
from time import sleep
from dotenv import load_dotenv

load_dotenv()

# ---  Global Setup ---
pasta_saves = os.getenv("CAMINHO_SAVES_MINECRAFT")
WINRAR_PATH = os.getenv("WINRAR_PATH")
DESTINY_DIRECTORY = os.getenv("CAMINHO_DESTINO_BACKUP")

# Email Credenciais
SENDER_EMAIL = os.getenv('EMAIL_REMETENTE')
RECIPIENT_EMAIL = os.getenv('EMAIL_DESTINATARIO')
EMAIL_PASSWORD = os.getenv('EMAIL_SENHA')

Now_Date = datetime.now().strftime('%Y-%m-%d_%H%M%S')

def setup_logging():
    
    """Configure the logs to be saved to a file and displayed in the terminal"""
    
    logger = logging.getLogger('BackupLogger')
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, 'logs')
    
    log_file_path = os.path.join(log_dir, f'backup_log_{Now_Date}.log')
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger

logger = setup_logging()

def get_path():
    
    """Returns the path to the save files. Uses the .env file if available, otherwise it tries the system default"""
    
    base_path = os.path.expanduser('~')
    base_path_Worlds = os.path.join(base_path,'Appdata/Roaming/.minecraft/saves')
    return base_path_Worlds

def get_filtred_list(base_path_Worlds):
    """List only valid directories within the saves folder"""
    
    world_names_list = []
    
    if not os.path.isdir(base_path_Worlds):
        print(f"Error: Saves path does not exist: {base_path_Worlds}")
        return []
    full_list = os.listdir(base_path_Worlds)
    for directory in full_list:
        full_item_path = os.path.join(base_path_Worlds, directory)
        if os.path.isdir(full_item_path):
            world_names_list.append(directory)
    return world_names_list

def copy_and_compact(source_path, name):
    
    """
    Compresses a folder using WinRAR via command line
    Returns: (zip_path, destination_directory) or None in case of failure
    """
    
    os.makedirs(DESTINY_DIRECTORY, exist_ok=True)
    
    zip_file_path = os.path.join(DESTINY_DIRECTORY, f'{name}.zip')
    
    root_dir = source_path 
    
    try:
        # WinRar Flags:
        # a: add, -s: solid, -ep1: delete base path, -r: recursive
        # -iback: background mode, -idq: quiet mode (less output)
        command = [
            WINRAR_PATH,
            'a',
            '-s',
            '-ep1',
            '-r',
            '-iback',
            '-idq',
            zip_file_path,
            '*'
        ]
        
        subprocess.run(command, check=True, cwd=root_dir,stdout=subprocess.PIPE, stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
        
        logger.info(f" Success! Content from the world '{name}' compressed (WinRAR) to: {zip_file_path}")
        return zip_file_path,DESTINY_DIRECTORY
        
    except subprocess.CalledProcessError as e:
        logger.info(f"⚠️ Error compressing with WinRAR for {name}: {e}")
        return None
    except FileNotFoundError:
        logger.info(f"⚠️ Error: The WinRAR executable was not found in {WINRAR_PATH}")
        return None
    
def cleanup_local_backups(destiny_directory):
    
    """Remove local .zip files after uploading to save space"""
    
    logger.info("\n--- Staring Final Clean up ---")
    
    try:
        for filename in os.listdir(destiny_directory):
            if filename.endswith(".zip"):
                file_path = os.path.join(destiny_directory, filename)
                os.remove(file_path)
                logger.info(f"File '{filename}' successfully deleted from the local directory")
        
        logger.info("\n✅ Final Clean up completed")
        return True
    
    except Exception as e:
        logger.error(f"⚠️Error during final clean up: {e}")
        return False
def initialize_and_check(logger):
    logger.info("\n--- 1. Authentication  and Conection ---\n ")
    
    drive_service = google_drive_authenticator()
    
    if not drive_service:
        logger.critical("\n⚠️ Could not connect to Google Drive. Script ending.\n")
        return
    
    drive_folder_id = get_drive_folder_id(drive_service)
    
    logger.info("\n--- 2. Local starting up ---\n")
    
    base_path_worlds = get_path()
    world_list = get_filtred_list(base_path_worlds)
    
    if not world_list:
        
        print("\nNo worlds found to compact. Process finished!\n")
        logger.critical("\nNo worlds found to compact. Process finished!\n")
        
        return None, None, None
    
    print(f"\nFound {len(world_list)} worlds found to backup!\n")
    logger.info(f"\nFound {len(world_list)} worlds found to backup!\n")
    
    return drive_service, drive_folder_id, world_list

def process_backups(logger, drive_service, drive_folder_id, world_list, base_path_worlds):
    
    success_count = 0
    fail_count = 0
    
    logger.info("\n--- 3. Compression and Upload ---\n")
    for world_name in world_list:
        logger.info(f"\n\nProcessing: {world_name}\n")
        source_path = os.path.join(base_path_worlds, world_name)
        local_file_path, destiny_directory = copy_and_compact(source_path, world_name)
        
        if local_file_path and os.path.exists(local_file_path):
            upload_result = upload_and_cleanup(drive_service, drive_folder_id, local_file_path, world_name)
            
            if upload_result:
                success_count += 1
            else:
                fail_count += 1
        else:
            fail_count += 1
            logger.warning(f"⚠️ IGNORED WORLD: Failure to compress '{world_name}'. No upload will be possible.")
            
    return success_count, fail_count, destiny_directory
    
    
def main():
    
    """Main execution function"""
    
    drive_service, drive_folder_id, world_list = initialize_and_check(logger)
    if drive_service is None:
        return
    
    base_path_worlds = get_path()
    
    success_count, fail_count, destiny_directory = process_backups(
        logger, drive_service, drive_folder_id, world_list, base_path_worlds
    )
    # Exibe resumo no log
    logger.info((
        f"\n\nRESULTS\n"
        f"_____________________________________________\n"
        f"   Success (Uploads):   {success_count}\n"
        f"   Failures/Ignored:    {fail_count}\n"
        f"_____________________________________________"
    ))
    
    cleanup_local_backups(destiny_directory)
    latest_log = get_lastest_log_file(LOG_DIR)
    
    if not latest_log:
        print(f"❌ Log File not found (.log) in : {LOG_DIR}")
        return

    print(f" Lastest log found: {os.path.basename(latest_log)}")
    
    send_log_email(latest_log, SENDER_EMAIL, RECIPIENT_EMAIL, EMAIL_PASSWORD)
    sleep(1)
    clean_up_logs(log_file_limit=5)
    
if __name__ == '__main__':
    execution_success = main()