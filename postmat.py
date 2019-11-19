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
        """
        Try to receive data from api and return it as json
        :return: json data
        """
        http = urllib3.PoolManager()
        r = http.request('GET', self.postmat_url)
        if r.status == 200:
            data = json.loads(r.data)
            return data
        else:
            return None


    def data_setter(self):
        """
        Set data to object variables
        :return: True or False but actually nothing
        """
        postmat_data = self.get_data()
        if postmat_data != None:
            self.name = postmat_data['name']
            self.address = postmat_data['address']
            self.status = postmat_data['status']
            self.description = postmat_data['description']
            self.work_today = self.is_it_work_today(postmat_data['working_hours'])
        else:
            return False


    def is_it_work_today(self, working_hours):
        """
        Yeeeeeeeeah, it'a bonus part ;)
        :param working_hours: json data
        :return: str
        """
        day_today = datetime.datetime.today().weekday()
        time_now = datetime.datetime.now().time()
        time_open = working_hours[day_today]['time_open'][:2]
        time_close = working_hours[day_today]['time_close'][:2]
        if int(time_open) <= time_now.hour and int(time_close) >= time_now.hour:
            return 'Открыто'
        else:
            return 'Закрыто'


x = Postmat(103)
print(x.work_today)