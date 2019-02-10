from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.conf import settings

import json
import os
import requests

# Create your views here


def read_result():
    with open(os.path.join(settings.MEDIA_ROOT, 'result.json')) as file:
        data = json.load(file)
    return data


def index(request):
    template = loader.get_template('vocabulary/index.html')
    result = read_result()
    print(result)
    return HttpResponse(template.render(result[0], request))


def extract(request):
    credentials = {
        'username': request.POST['username'],
        'password': request.POST['password']
    }
    cookies = requests.post(
        'http://flashycards.co/api/authentication/login/', data=credentials).json()
    headers = {
        'Authorization': "Token " + cookies['token'],
        "Content-Type": "application/json; charset=utf8"
    }
    result = read_result()
    lesson = prepare_lesson(result[0])
    r = requests.post(
        'http://flashycards.co/api/lessons/lessons/',
        data=json.dumps(lesson),
        headers=headers
    )
    return HttpResponseRedirect("/")


def prepare_lesson(result):
    lesson = {}
    lesson['name'] = result['title']
    lesson['description'] = 'from dw'
    lesson['concepts'] = []
    lesson['audience'] = {'id': 1}
    id = 0
    for row in result['data']:
        concept = {}
        concept['id'] = id - 1
        concept['card_a'] = {'text': row['german'],
                             'audio': row['audio'], 'media': None}
        concept['card_b'] = {'text': row['english'], 'media': None}
        lesson['concepts'].append(concept)
    lesson['concepts'].pop()
    return lesson
