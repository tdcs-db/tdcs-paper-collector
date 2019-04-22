## General
import json
import os
## Google spreadsheet
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def google_cloud_config_path(gc_path=None):
    """Obtain the configurations for google cloud.
    This function searches through a list of path to find the configuration files. A following folder and files should be included.
    1. `sheets/token.json`
    2. `sheets/credentials.json`
    The precedence of path search is:
    1. `GOOGLECLOUDCONFIG` variable set in bash.rc.
    2. `$HOME/.google-cloud`
    """


    if gc_path is None:
        if os.environ.get('GOOGLECLOUDCONFIG'):
            google_cloud_path = os.environ['GOOGLECLOUDCONFIG']
        else:
            try:
                home_dir = os.environ['HOME']
            except Exception as ee:
                raise Exception('Can not get HOME dir')

            if os.path.isfile(home_dir + '/.google-cloud/sheets/token.json'):
                google_cloud_path = home_dir + '/.google-cloud'
            else:
                raise Exception('Can not find google-cloud config files')
    else:
        google_cloud_path = gc_path

    return google_cloud_path


def gsheet_service(token = None, credential = None, scope = None):
    """Create Google Sheet Service. 
    This is used to connect to google sheet. 
    :param token: token file path for google sheet service
    :param credential: credential file path for google sheet service
    :param scope: scope is used to restrict the access to the google sheets. The default value is `readonly`.
    """

    google_cloud_path = google_cloud_config_path()

    if token is None:
        token = google_cloud_path + "/sheets/token.json"
    if credential is None:
        credential = google_cloud_path + "/sheets/credentials.json"
    if scope is None:
        scope = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    
    store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credential, scope)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    return service

def retrieve_sheet(sheet_id, range, service=None, token = None, credential = None, scope = None ):
    """Get values of a google spreadsheet
    Load the values in google spreadsheet to a list.
    :param sheet_id: ID of the spreadsheet
    :param range: Range to be loaded. Normally, many of the cells can be empty. Setting a sensible range can make the data wrangling much easier.
    :param service: google sheet service. This is optional. If this is not set this function will try to create a new google sheet service.
    :param token: token file path for google sheet service
    :param credential: credential file path for google sheet service
    :param scope: scope is used to restrict the access to the google sheets. The default value is `readonly`.
    """

    if service is None:

        google_cloud_path = google_cloud_config_path()

        if token is None:
            token = google_cloud_path + "/sheets/token.json"
        if credential is None:
            credential = google_cloud_path + "/sheets/credentials.json"
        if scope is None:
            scope = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        
        service = gsheet_service(token, credential, scope)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    return values

if __name__ == "__main__":
    # configuration_dictionary = get_config()
    # print(configuration_dictionary )
    # print( configuration_dictionary.keys() )
    print(
        get_config()
    )
    print(
        gsheet_service()
    )

    print('END')
