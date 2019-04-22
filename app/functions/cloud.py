## General
import json
import os
import pygsheets

def gsheet_service(sheet_id, config_group = None):
    """Create Google Sheet Service. 
    This is used to connect to google sheet.
    """


    gs_conf = get_gsheets_config(config_group) 
    
    gc = pygsheets.authorize(client_secret=gs_conf)

    gc.open_by_key('1qYjksuavj-GzAGGTEWbeoER1WXDzoSWNDHvwjupUso8')

    return gc



if __name__ == "__main__":

    print('END')
