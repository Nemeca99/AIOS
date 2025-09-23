
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def upload_to_drive():
    try:
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
        
        # Search for existing file named reflections.txt
        file_list = drive.ListFile({'q': "title='reflections.txt' and trashed=false"}).GetList()
        if file_list:
            file = file_list[0]
        else:
            file = drive.CreateFile({'title': 'reflections.txt'})
        
        file.SetContentFile('reflections.txt')
        file.Upload()
        print("☁️ Uploaded reflections.txt to Google Drive.")
    except Exception as e:
        print(f"⚠️ Google Drive upload failed: {e}")
