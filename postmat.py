import urllib3
import json


class Postmat:

    API_URL = 'https://api.tport.online/v2/public-stations/'

    def __init__(self, postmat_id):
        self.postmat_id = postmat_id
        self.postmat_url = self.API_URL + str(self.postmat_id)

    def get_data(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.postmat_url)
        data = json.loads(r.data)
        return data
