
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def ensure_file_exists(drive, filename):
    file_list = drive.ListFile({'q': f"title='{filename}' and trashed=false"}).GetList()
    if file_list:
        print(f"✅ '{filename}' already exists on Drive.")
        return file_list[0]['id']
    else:
        file = drive.CreateFile({'title': filename})
        file.Upload()
        print(f"📁 Created '{filename}' on Drive.")
        return file['id']

def main():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")
    
    drive = GoogleDrive(gauth)
    
    # Create both files if they don't exist
    ensure_file_exists(drive, "reflections.txt")
    ensure_file_exists(drive, "memory_log.txt")

if __name__ == "__main__":
    main()
