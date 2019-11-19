import urllib3
import json
import datetime


class Postmat:

    API_URL = 'https://api.tport.online/v2/public-stations/'

    def __init__(self, postmat_id):
        self.postmat_id = postmat_id
        self.postmat_url = self.API_URL + str(self.postmat_id)
        self.name = None
        self.address = None
        self.status = None
        self.description = None
        # it's a bonus part of a challenge =)
        self.work_today = None
        self.data_setter()


    def get_data(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.postmat_url)
        data = json.loads(r.data)
        return data


    def data_setter(self):
        postmat_data = self.get_data()
        self.name = postmat_data['name']
        self.address = postmat_data['address']
        self.status = postmat_data['status']
        self.description = postmat_data['description']
        self.work_today = self.is_it_work_today(postmat_data['working_hours'])


    def is_it_work_today(self, working_hours):
        day_today = datetime.datetime.today().weekday()
        time_now = datetime.datetime.now().time()
        time_open = working_hours[day_today]['time_open'][:2]
        time_close = working_hours[day_today]['time_close'][:2]
        if int(time_open) <= time_now.hour and int(time_close) >= time_now.hour:
            return 'Открыто'
        else:
            return 'Закрыто'
