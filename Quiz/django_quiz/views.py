import json
from django.shortcuts import render, redirect
from .models import Question, Answer, Choice, Category
from django.http.response import Http404

from django.views.generic import DetailView, ListView, View
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator


# Create your views here.


def question_detail(request, question_id):
    if request.method == 'GET':
        context = {}
        try:
            qs = Question.objects.get(id=question_id)
            context['qs'] = qs
            return render(request, 'question-detail.html', context)
        except:
            raise Http404('page not found')


class QuestionDetail(DetailView):
    context_object_name = 'qs'
    model = Question
    template_name = 'question-detail.html'
    pk_url_kwarg = 'question_id'


class QuestionList(ListView):
    context_object_name = 'qs'
    # queryset = Question.objects.all().order_by('-cat','id')
    template_name = 'questions-list.html'

    # def get_queryset(self):
    #     queryset = Question.objects.all().order_by('-cat', 'id')
    #     cat_arg = self.request.GET.get('cat', None)
    #     difficulty_arg = self.request.GET.get('diff', None)
    #     if cat_arg:
    #         queryset = queryset.filter(cat__name__icontains=cat_arg)
    #     if difficulty_arg:
    #         queryset = queryset.filter(difficulty=difficulty_arg)
    #     return queryset

    def get_queryset(self):
        queryset = Question.objects.only('title').order_by('-cat', 'id').select_related('cat').prefetch_related(
            'choice_set')
        cat_arg = self.request.GET.get('cat', None)
        difficulty_arg = self.request.GET.get('diff', None)

        if cat_arg and difficulty_arg:
            # queryset = queryset.filter(cat__name__icontains=cat_arg)\
            #            | queryset.filter(difficulty=difficulty_arg)
            #
            queryset = Question.objects.filter \
                (Q(cat__name__icontains=cat_arg) | Q(difficulty=difficulty_arg)).order_by('-cat', 'id')
            # queryset = Question.objects.filter \
            #     (cat__name__icontains=cat_arg, difficulty=difficulty_arg)
        elif cat_arg and not difficulty_arg:
            queryset = queryset.filter(cat__name__icontains=cat_arg)
        elif not cat_arg and difficulty_arg:
            queryset = queryset.filter(difficulty=difficulty_arg)

        return queryset

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=None, **kwargs)
    #
    #     context['mohammad'] = 'ashkan'
    #     print(context)
    #     return context


@csrf_exempt
def answer_question(request, question_id):
    if request.method == 'POST':
        try:
            question_obj = Question.objects.get(id=question_id)

            body = request.body
            jsonify_body = json.loads(body)
            if jsonify_body.get('answer_number') == 0:
                Answer.objects.create(question=question_obj)
                question_obj.not_answered_count += 1
                question_obj.save()
                return JsonResponse('you dont answer this question', safe=False)

            try:
                correct_choice = question_obj.choice_set.get(is_correct=True)
                client_choice = Choice.objects.filter(
                    question=question_obj,
                    number=jsonify_body.get('answer_number')).first()
                Answer.objects.create(question=question_obj, choice=client_choice)
                if jsonify_body.get('answer_number') == correct_choice.number:
                    question_obj.correct_answer += 1
                    question_obj.save()
                    return JsonResponse('you are correct', safe=False)
                else:
                    question_obj.wrong_count += 1
                    question_obj.save()
                    return JsonResponse('you are wrong', safe=False)
            except:
                return JsonResponse('this question have more than one correct chioce or zero correct choice')
        except:
            return JsonResponse('this question doesnt exist', safe=False)


class AnswerCount(DetailView):
    template_name = 'question_answer_counts.html'
    pk_url_kwarg = 'question_id'
    model = Question


class AnswerCountAnnotation(DetailView):
    template_name = 'question_answer_counts_annotation.html'
    pk_url_kwarg = 'question_id'
    context_object_name = 'qs'
    queryset = Question.objects.annotate(
        answer_count_annt=Count('answer'),
        correct_answer_count_annt=Count('answer', filter=Q(answer__choice__is_correct=True)),
        wrong_answer_count_annt=Count('answer', filter=Q(answer__choice__is_correct=False)),
        not_answered_count_annt=Count('answer', filter=Q(answer__choice=None)))


@method_decorator(csrf_exempt, name='dispatch')
class CreateQuestion(View):
    def post(self, request):
        body = self.request.body
        jsonify_body = json.loads(body)
        temp_dict = {}
        cat_name = jsonify_body.get('cat')
        cat, cat_created = Category.objects.get_or_create(name=cat_name)
        temp_dict['title'] = jsonify_body.get('title')
        temp_dict['difficulty'] = jsonify_body.get('difficulty')
        temp_dict['cat'] = cat
        question, question_created = Question.objects.get_or_create(**temp_dict)
        if not question_created:
            return JsonResponse('this question already exist', safe=False)

        choices_list = jsonify_body.get('choices_list')
        correct_choice = jsonify_body.get('correct_choice')
        choices_objs = []
        for index, choice_title in enumerate(choices_list, start=1):
            if correct_choice == index:
                choices_objs.append(Choice(title=choice_title,
                                           number=index,
                                           question=question,
                                           is_correct=True))
            else:
                choices_objs.append(Choice(title=choice_title,
                                           number=index,
                                           question=question,
                                           is_correct=False))

        choices = Choice.objects.bulk_create(choices_objs)

        return redirect('question-detail', question_id=question.id)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateQuestion(View):
    def patch(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
            body = self.request.body
            jsonify_body = json.loads(body)
            title = jsonify_body.get('title')
            difficulty = jsonify_body.get('difficulty')
            cat_name = jsonify_body.get('cat')
            cat, cat_created = Category.objects.get_or_create(name=cat_name)
            question.title = title
            question.difficulty = difficulty
            question.cat = cat

            choices_list = jsonify_body.get('choices_list')
            correct_choice = jsonify_body.get('correct_choice')
            if choices_list and correct_choice:
                question.choice_set.all().delete()
                choices_objs = []
                for index, choice_title in enumerate(choices_list, start=1):
                    if correct_choice == index:
                        choices_objs.append(Choice(title=choice_title,
                                                   number=index,
                                                   question=question,
                                                   is_correct=True))
                    else:
                        choices_objs.append(Choice(title=choice_title,
                                                   number=index,
                                                   question=question,
                                                   is_correct=False))

                choices = Choice.objects.bulk_create(choices_objs)

            question.save()
            return redirect('question-detail', question_id=question.id)
        except:
            return JsonResponse('question with this id doesnt exist', safe=False)
