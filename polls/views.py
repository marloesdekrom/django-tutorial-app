from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #Return the last 5 published questions
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'    

def vote(request,question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST[choice])
    except (KeyError, Choice.DoesNotExist):
        #redisplay the question voting form
        return render (request, 'polls/detail.html', {'question': p, 'error_message': "You didn't select a choice."})
    else:
        selected_choice.voytes +=1
        selected_choice.save()
        #return a HttpResponseRedirect after dealing with POST data
        #This prevents data from being posted twice
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def results (request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render (request, 'polls/results.html', {'question': question})
