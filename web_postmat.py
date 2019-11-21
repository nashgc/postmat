"""
Simple Flask app for easy work with TelePort API
"""


from flask import Flask
from flask import render_template
from flask import request
import urllib3
import json
import datetime
import re
app = Flask(__name__)

API_URL = 'https://api.tport.online/v2/public-stations/'


def get_data():
    """
    Try to receive data from api and return it as json
    :return: json data
    """
    http = urllib3.PoolManager()
    r = http.request('GET', API_URL)
    if r.status == 200:
        data = json.loads(r.data)
        return data
    else:
        return None

def parse_data(data):
    result = {}
    for postmat in data:
        result[postmat['id']] = {
            'name': postmat['name'],
            'status': postmat['status'],
            'working_hours': is_it_work_today(postmat['working_hours'])
        }
    return result


def filter_parse_data(data, filter_id):
    """
    Just filter data by regex
    :param data: json data
    :param filter_id: number from form
    :return: dict
    """
    result = {}
    for postmat in data:
        if re.match(filter_id, str(postmat['id'])):
            result[postmat['id']] = {
                'name': postmat['name'],
                'status': postmat['status'],
                'working_hours': is_it_work_today(postmat['working_hours'])
            }
    return result


def is_it_work_today(working_hours):
    """
    Yeeeeeeeeah, it'a bonus part ;)
    :param working_hours: json data
    :return: str
    """
    day_today = datetime.datetime.today().weekday()
    time_now = datetime.datetime.now().time()
    if len(working_hours) > 0:
        time_open = working_hours[day_today]['time_open']
        time_close = working_hours[day_today]['time_close']
        if int(time_open[:2]) <= time_now.hour and int(time_close[:2]) >= time_now.hour:
            return 'Открыто'
        else:
            return 'Закрыто'
    else:
        return 'not available'


@app.route('/')
def index():
    data = parse_data(get_data())
    return render_template('index.html', data=data)


@app.route('/filter/', methods=['GET'])
def filter():
    if request.method == 'GET':
        id = request.args.get('id')
        data = filter_parse_data(get_data(), id)
        return render_template('index.html', data=data)