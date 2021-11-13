from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Category, Task
import json
from django.shortcuts import redirect

# Create your views here.


def list_task(request):
    # test_list = [{'id':1, 'name':'exer1'}]
    # test_list_str = json.dumps(test_list)
    # print(json.loads(test_list_str))
    # print(type(json.loads(test_list_str)))
    # tasks = Task.objects.all()
    tasks = list(Task.objects.values())
    return JsonResponse(tasks, safe=False)


def retrieve_task(request, task_id):
    # print(dir(Task.objects.filter(id=task_id)))
    # retrieve_task = list(Task.objects.filter(id=task_id).values())
    # final_task = []
    # if retrieve_task:
    #     final_task = retrieve_task[0]
    final_task = Task.objects.filter(id=task_id).values().first()

    return JsonResponse(final_task, safe=False)


@require_http_methods(['POST'])
@csrf_exempt
def create_task(request):
    jsonify_body = json.loads(request.body)

    category, created_category = Category.objects.get_or_create(
        name=jsonify_body.get('category_name'))

    print(category, created_category)

    task, created_task = Task.objects.get_or_create(name=jsonify_body.get('name'),
                                                    cat=category)
    print(task, created_task)
    print(task.id)
    return redirect(to='retrieve-view', task_id=task.id)

