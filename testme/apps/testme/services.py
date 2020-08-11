from .models import TestmeQuestion, TestmeAnswer, TestmeRightAnswer
from testme import db


def get_testme_question(testme_id, title):
    """Return question"""
    question = TestmeQuestion(
        testme_id=testme_id,
        title=title
    )
    db.session.add(question)
    db.session.commit()
    return question


def get_testme_answers(answer_1, answer_2, answer_3, answer_4, testme_id, question_id):
    """Return answers to question"""
    testme_answers = TestmeAnswer(
        answer_1=answer_1,
        answer_2=answer_2,
        answer_3=answer_3,
        answer_4=answer_4,
        testme_id=testme_id,
        question_id=question_id
    )
    db.session.add(testme_answers)
    return testme_answers


def get_testme_right_answer(right_answer, question_id):
    """Return right answer"""
    testme_right_answer = TestmeRightAnswer(
        content=right_answer,
        question_id=question_id
    )
    db.session.add(testme_right_answer)
    return testme_right_answer


def get_testme_poll():
    """Return """


def get_right_answer_content(question_data_right_answer, question_data):
    right_answer_number = ''
    if question_data_right_answer == 1:
        right_answer_number = question_data['answer_1']
    elif question_data_right_answer == 2:
        right_answer_number = question_data['answer_2']
    elif question_data_right_answer == 3:
        right_answer_number = question_data['answer_3']
    elif question_data_right_answer == 4:
        right_answer_number = question_data['answer_4']
    return right_answer_number
