from django.urls import path

from .views import base_view, create_question, create_answer, create_child_question, create_child_answer

urlpatterns= [
    path('post-comments', base_view),
    path('create-question', create_question, name='question_create'),
    path('create-answer', create_answer, name='answer_create'),
    path('create-child-question', create_child_question, name='question_child_create'),
    path('create-child-answer', create_child_answer, name='answer_child_create'),
]
