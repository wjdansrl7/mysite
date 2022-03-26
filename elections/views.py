from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from .models import Candidate, Poll, Choice
from django.db.models import Sum
import datetime

def index(request):
   candidates = Candidate.objects.all()
   context = {'candidates':candidates}
   return render(request, 'elections/index.html',context)

def candidates(request, name):
   candidate = get_object_or_404(Candidate, name=name) # 예외처리 없이 오류 처리
   #try:
   #   candidate = Candidate.objects.get(name=name)
   #except:
   #   raise Http404 # 우리가 흔히 자주 쓰는 404페이지 입력
   return HttpResponse(candidate.name)
# HttpresponseNotFound # 예외처리시 우리가 직접 입력하는 것

def areas(request, area):
   today = datetime.datetime.now()
   try:
       poll = Poll.objects.get(area=area, start_date__lte =
         today, end_date__gte=today)
       candidates = Candidate.objects.filter(area=area)
   except:
       poll = None
       candidates = None
   context = {'candidates': candidates,
   'area':area, 'poll':poll}
   return render(request, 'elections/area.html',context)

def polls(request, poll_id):
   poll = Poll.objects.get(pk=poll_id)
   selection = request.POST['choice']
   try:
      choice = Choice.objects.get(poll_id = poll_id, candidate_id = 
         selection)
      choice.votes+=1
      choice.save()
   except:
      choice = Choice(poll_id = poll_id, candidate_id = selection, votes=1)
      choice.save()

   return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    candidates = Candidate.objects.filter(area = area)
    polls = Poll.objects.filter(area = area)
    poll_results = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date

        # poll.id에 해당하는 전체 투표수
        total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes'))
        result['total_votes'] = total_votes['votes__sum']

        rates = [] #지지율
        for candidate in candidates:
            # choice가 하나도 없는 경우 - 예외처리로 0을 append
            try:
                choice = Choice.objects.get(poll = poll, candidate = candidate)
                rates.append(
                    round(choice.votes * 100 / result['total_votes'], 1)
                    )
            except :
                rates.append(0)
        result['rates'] = rates
        poll_results.append(result)

    context = {'candidates':candidates, 'area':area,
    'poll_results' : poll_results}
    return render(request, 'elections/result.html', context)
