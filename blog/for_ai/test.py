from rest_framework.response import Response
from rest_framework.decorators import api_view
from celery import shared_task
import google.generativeai as genai
import time
from blogg.settings import GEMINI_KEY

genai.configure(api_key=GEMINI_KEY)

@shared_task
def generate_content_task(i):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(i)
    time.sleep(10)
    print(response.text)
    return response.text

@api_view(['POST'])
def ok(request):
    i = request.data.get('i')
    # Call the Celery task asynchronously
    task = generate_content_task.delay(i)
    # Return task ID or some other immediate response
    return Response({'task_id': task.id, 'status': 'Processing'})
    
from celery.result import AsyncResult

@api_view(['POST'])
def task_status(request):
    id=request.data.get('o')
    result = AsyncResult(id)
    if result.state == 'PENDING':
        # task has not started yet
        response = {
            'task_id': id,
            'status': 'pending',
        }
    elif result.state != 'FAILURE':
        # task is running or finished
        response = {
            'task_id': id,
            'status': result.state,
            'result': result.result if result.state == 'SUCCESS' else None,
        }
    else:
        # task failed
        response = {
            'task_id': id,
            'status': 'failure',
            'error': str(result.result),  # Contains the exception raised
        }

    return Response(response)

