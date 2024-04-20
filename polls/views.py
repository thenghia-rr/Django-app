# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.template import loader
# from django.db.models import F
# from django.urls import reverse

# from .models import Question, Choice


# # Create your views here.
# def index(request):
#     # Way 1
#     # latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # template = loader.get_template('polls/index.html')
#     # context = {
#     #     "latest_question_list": latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))

#     # Way 2
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

# # -------------------------------------------------------------------------------
# def detail(request, question_id):
#     #  Way 1
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question not found")

#     # context = {'question': question}
#     # return render(request, "polls/detail.html", context)

#     # Way 2
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {'question': question})
# # -------------------------------------------------------------------------------

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

# # -------------------------------------------------------------------------------

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes = F("votes") + 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# =======================================USE GENERIC VIEWS =======================================
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.utils import timezone

from .models import Choice, Question
import asyncio

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

class AboutView(generic.ListView):
    template_name = 'polls/about.html'
    
    def get_queryset(self):
        return None

# Asynchronous class-based views
class AsyncView(generic.View):
    async def get(self, request, *args, **kwargs):
        # Perform io-blocking view logic using await, sleep for example.
        await asyncio.sleep(2)
        return HttpResponse("Hello async world!")