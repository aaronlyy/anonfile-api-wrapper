'''
lib for accessing the anonfile.com API.\n
------------------------------------\n
author: Aaron Levi // aaronlyy\n
website: https://aaronlyy.me/\n
------------------------------------
'''

import requests
import os

class Anonfile:
    '''
    upload files & get info about uploaded files
    '''
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.api_info = 'https://api.anonfile.com/v2/file/{id}/info'
        if api_key:
            self.api_upload = 'https://api.anonfile.com/upload?token={key}'.format(key=api_key)
        else:
            self.api_upload = 'https://api.anonfile.com/upload'

    def __repr__(self):
        return 'Object: Anonfile ({})'.format('anonfile.com')
    
    def isUp(self):
        '''
        checks if the anonfile.com server is up.\n
        returns True or False.
        '''
        res = requests.get('https://anonfile.com/')
        if res.status_code == 200:
            return True
        else:
            return False

    def upload(self, filepath):
        '''
        uploads the given file to anonfile.com.\n
        if apikey is given, uploads directly in account.\n
        returns container with response keys.\n
        on error returns error dict.
        '''
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                response = requests.post(self.api_upload, files={'file': f})
            return AnonfileUploadResponse(response.json())
        else:
            res_json = {
                "status": False,
                "error": {
                    "message": 'File to upload not found!',
                    "type": "LOCAL_FILE_NOT_FOUND",
                    "code": -1
                }
            }
            return AnonfileUploadResponse(res_json)
    

class AnonfileUploadResponse:
    '''
    contains response from Anonfile Upload
    '''

    def __init__(self, res_json):
        if res_json['status'] == True:
            self.res_dict = {
                'status': res_json['status'],
                'url_full': res_json['data']['file']['url']['full'],
                'url_short': res_json['data']['file']['url']['short'],
                'file_id': res_json['data']['file']['metadata']['id'],
                'name': res_json['data']['file']['metadata']['name'],
                'size': res_json['data']['file']['metadata']['size']['bytes']
            }
        else:
            self.res_dict = {
                'status': res_json['status'],
                'error_msg': res_json['error']['message'],
                'error_type': res_json['error']['type'],
                'error_code': res_json['error']['code']
            }

    def __repr__(self):
        return 'Object: AnonfileUploadResponse (status: {})'.format(self.res_dict['status'])

    def __getattr__(self, attr):
        if attr in self.res_dict:
            return self.res_dict[attr]
        else:
            return None

    def getfullres(self):
        return self.res_dict