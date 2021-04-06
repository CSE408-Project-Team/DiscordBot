
from google.cloud import dialogflow


def startSession():
    sessionClient = dialogflow.SessionsClient()
    session = sessionClient.session_path()

