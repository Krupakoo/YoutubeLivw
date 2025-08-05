import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timezone

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate():
    creds = None

    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret_2_617843538356-k35er9gv6v6arap0gg5nf6ovbpd8qjfb.apps.googleusercontent.com.json",
                SCOPES
            )
            creds = flow.run_local_server(port=8080, prompt='consent')

        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)


def create_broadcast(youtube, title, start_time):
    request = youtube.liveBroadcasts().insert(
        part="snippet,status,contentDetails",
        body={
            "snippet": {
                "title": title,
                "scheduledStartTime": start_time,
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": True
            },
            "contentDetails": {
                "enableAutoStart": True,
                "enableAutoStop": True
            }
        }
    )
    response = request.execute()
    print("Broadcast created successfully")
    return response["id"]


if __name__ == "__main__":
    youtube = authenticate()

    start_time = (datetime.now(timezone.utc)).isoformat()


    title = "Test Broadcast"
    broadcast_id = create_broadcast(youtube, title, start_time)
    print(f"Broadcast created with ID: {broadcast_id}")
