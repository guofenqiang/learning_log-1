import django
django.setup()
from django.shortcuts import render

# Create your views here.
import json
from random import randrange

from django.http import HttpResponse
from rest_framework.views import APIView

# from pyecharts.charts import Line
# from pyecharts import options as opts
from django.views.decorators.csrf import csrf_exempt
import time
from upgrade.data_process import FileOperate
import threading
from django.http import Http404
from django.contrib.auth.decorators import login_required
from learning_logs.models import Topic
from multiprocessing import Process
import datetime
import re


class DataProcess:
    def __init__(self):
        self.progress = 0
        self.status = 0

    def data_update(self):
        if self.status == 1:
            time.sleep(1)
            self.progress += 1
            if self.progress >= 99:
                self.progress = 99
        elif self.status == 2:
            self.progress = 100
        return {'value': self.progress}

    def status_update(self, status=0):
        if status == 0:
            self.progress = 0
        self.status = status


dp = DataProcess()
fo = FileOperate()


# Create your views here.
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


env_info = {}


class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        # js = json.loads(line_base())
        # js = dp.data_update()
        global env_info
        env_id = request.GET['env_id']
        env_id = int(env_id)
        if env_id in env_info.keys():
            if env_info[env_id]['tid'].is_alive():
                env_info[env_id]['flag'] = 0
                start_time = env_info[env_id]['start_time']
                now_time = datetime.datetime.now()
                env_info[env_id]['cost_time'] = (now_time - start_time).seconds

        if env_info.get(env_id, None) and env_info.get(env_id, None).get('cost_time', None):
            js = {'value': env_info[env_id]['cost_time']}
        else:
            js = {'value': 0}
        form = {"username": "root", "password": "root"}
        info = dict(js, **form)
        return JsonResponse(info)


cnt = 9


class ChartUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        global cnt
        cnt = cnt + 1
        return JsonResponse({"name": cnt, "value": randrange(0, 100)})


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        """显示单个主题及其所有条目"""
        env_id = request.GET['env_id']
        topic = Topic.objects.get(id=int(env_id[1:]))

        # 确认请求的主题属于当前用户
        if topic.owner != request.user:
            raise Http404

        entries = topic.entry_set.order_by('-date_added')
        context = {'topic': topic, 'entries': entries}
        return render(request, 'index.html', context)


@csrf_exempt
@login_required
def reset(request, topic_id):
    global env_info
    data = {}
    vars_li = list(fo.read_json('config.json').keys())
    s = [''] * len(vars_li)
    dic = dict(zip(vars_li, s))
    locals().update(dic)

    """显示单个主题及其所有条目"""
    topic = Topic.objects.get(id=topic_id)

    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')

    if request.method == 'POST':
        dp.status_update(status=0)
        for var in vars_li:
            vars()[var] = request.POST[var]
            data[var] = eval(var)
        print(data)
        print(entries[0].text)
        # if context['username'] != '1' or context['password'] != '1':
        #     return render(request, 'index.html', {'data': context})
        dp.status_update(status=1)
        # wait = WaitFinishWork()
        # wait.start()
        action = request.POST['action']
        if action == "reset":
            if topic_id not in env_info.keys():
                t = Process(target=reset_os, args=(entries[0].text,))
                t.start()
            elif topic_id in env_info and env_info[topic_id]['tid'].is_alive():
                env_info[topic_id]['tid'].terminate()
                env_info[topic_id]['tid'].join()
                t = Process(target=reset_os, args=(entries[0].text,))
                t.start()
            elif topic_id in env_info and not env_info[topic_id]['tid'].is_alive():
                t = Process(target=reset_os, args=(entries[0].text,))
                t.start()
            else:
                t = None
            start_time = datetime.datetime.now()
            env_info[topic_id] = {"tid": t, 'start_time': start_time, 'cost_time': 0, 'flag': 0}
        elif action == "stop":
            if env_info.get(topic_id, None):
                env_info[topic_id]['tid'].terminate()
                env_info[topic_id]['tid'].join()

    context = {'topic': topic, 'entries': entries, 'data': data}
    return render(request, 'index.html', context)


@csrf_exempt
@login_required
def upgrade_home(request):
    """显示所有的主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'upgrade_home.html', context)


class WaitFinishWork(threading.Thread):
    def run(self):
        time.sleep(20)
        dp.status_update(status=2)


def reset_os(info):
    for i in range(100):
        print(i, info)
        time.sleep(1)

