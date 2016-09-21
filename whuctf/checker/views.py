# -*- coding: utf-8 -*-

import datetime

from django.shortcuts import render
from django.http import HttpResponse
from .models import Team
from django.core.exceptions import ObjectDoesNotExist

BASE_TIME = datetime.datetime(2016, 9 , 19, 9, 59, 59)
NAMES = [u'xx1', u'xx2', u'xx3', u'xx4', u'xx5',  u'xx6', u'xx7', u'xx8', u'xx9', u'xx10', u'xx11', u'xx12', u'xx13']


def get_name(id):
    return NAMES[id]


def get_round():
    cur_time = datetime.datetime.now()
    delta_seconds = (cur_time-BASE_TIME).total_seconds()
    return int(delta_seconds/300) + 1   # 5 minutes


def format_time(date_time):
    hour = date_time.hour
    minute = date_time.minute
    minute = int(minute/5) * 5
    return str(hour).rjust(2, '0') + ':' + str(minute).rjust(2, '0')


def get_curtime():
    return format_time(datetime.datetime.now())


def get_pretime():
    pre_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
    return format_time(pre_time)
    

def home(request):
    time = get_pretime() + " - " +get_curtime()
    if get_round() == 1:
        teams = []
        for i in range(13):
            team = {}
            team['tid'] = i
            team['name'] = get_name(i)
            team['status'] = [0] * 3
            team['score'] = 0
            teams.append(team)
    else:
        round = get_round() - 1
        for i in range(13):
            try:
                team = Team.objects.get(round=round, tid=i)
            except ObjectDoesNotExist:
                team = Team(tid=i,
                        name=get_name(i),
                        round=round,
                        time = get_pretime(),
                        status=[0,0,0],
                        count=[0,0,0])
                team.save()
                team = Team.objects.get(round=round, tid=i)
                
            p_status = team.getstatus()
            count = team.getcount()
            for i, s in enumerate(p_status):
                if count[i] == 2:
                    if s == 2:
                        p_status[i] = 1
                    elif s == 1:
                        p_status[i] = 0
                        team.status = p_status
                        team.save()

            score = 0
            for s in p_status:
                if s:
                    score -= 50

            if team.score != score:
                team.score = score
                team.save()

        teams = Team.objects.filter(round=round).all()
    return render(request, 'checker/checker.html', {"time": time, "teams": teams})


def check(request):
    try:
        team_id = int(request.GET['t'])
        problem_id = int(request.GET['p'])
        status = int(request.GET['s'])
    except:
        return HttpResponse('param is invalid')

    cur_round = get_round()
    
    try:
        team = Team.objects.get(tid=team_id, round=cur_round)
    except ObjectDoesNotExist:
        team = Team()
        team.tid = team_id
        team.round = cur_round
        team.name = get_name(team_id)
        team.time = get_curtime()
        count = [0] * 3
        count[problem_id-1] = 1
        team.count = count

        p_status = [0] * 3
        p_status[problem_id-1] = status
        team.status = p_status
        team.save()
    else:
        count = team.getcount()
        
        if count[problem_id-1] < 2:
            p_status = team.getstatus()
            p_status[problem_id-1] += status
            count[problem_id-1] += 1

            team.status = p_status
            team.count = count
            team.save()
    return HttpResponse('checked')
