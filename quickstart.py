from __future__ import print_function

import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']


def start_authentication():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('docs', 'v1', credentials=creds)
        update_local_document(service)
        return service

    except HttpError as error:
        print(f'An error occurred: {error}')


def update_local_document(service):
    # If document already exists
    if os.path.exists('document_info.json'):
        print("Attempting to access document_info.json...")
        with open('document_info.json', 'r') as info:
            doc_info = json.load(info)

            try:
                doc_id = doc_info["documentId"]
            # If document_info.json is corrupted for whatever reason
            except KeyError as error:
                print("Document id not found.")
                create_new_document(service)
                return
            info.close()

        try:
            doc = service.documents().get(documentId=doc_id).execute()
            save_document_info(doc)
            print("Successfully updated local data.")
        except HttpError as error:
            print(f"Document with id {doc_id} not found on Google Drive.")
            create_new_document(service)

    else:
        print("Document not found.")
        create_new_document(service)


def update_cloud_document(service, new_info: str):
    update_local_document(service)
    with open('document_info.json', 'r') as info:
        doc_info = json.load(info)
        doc_id = doc_info["documentId"]
        end_index = doc_info["body"]["content"][1]["endIndex"]
        requests = []
        if end_index > 2:
            requests.append(
                {"deleteContentRange": {
                    "range": {
                        "startIndex": 1,
                        "endIndex": end_index - 1
                    }
                }})
        requests.append(
            {"insertText": {
                "location": {
                    "index": 1
                },
                "text": new_info
            }})
        service.documents().batchUpdate(documentId=doc_id, body={
            "requests": requests
        }).execute()
        info.close()


def get_document_data():
    with open('document_info.json', 'r') as info:
        doc_info = json.load(info)
        doc_text = doc_info["body"]["content"][1]["paragraph"]["elements"] \
            [0]["textRun"]["content"].rstrip("\n")
        doc_text = doc_text.replace('\u201c', '"')
        doc_text = doc_text.replace('\u201d', '"')
        info.close()
        if doc_text == "":
            doc_text = "[]"
    return eval(f'{doc_text}')


def create_new_document(service):
    print("Creating new document...")
    title = 'Deerhacks Wellness Data'
    body = {
        'title': title
    }
    doc = service.documents().create(body=body).execute()
    print('Created document with title: {0}'.format(doc.get('title')))
    save_document_info(doc)
    update_cloud_document(service, "[]")


def save_document_info(doc):
    with open('document_info.json', 'w') as info:
        json.dump(doc, info)


if __name__ == '__main__':
    start_authentication()
