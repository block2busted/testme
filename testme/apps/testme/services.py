from .models import TestmeQuestion, TestmeAnswer, TestmeRightAnswer
from testme import db


def get_question(testme_id, title):
    """Return question"""
    question = TestmeQuestion(
        testme_id=testme_id,
        title=title
    )
    db.session.add(question)
    return question


def get_testme_answers(answer_1, answer_2, answer_3, answer_4, question_id):
    """Return answers to question"""
    testme_answers = TestmeAnswer(
        answer_1=answer_1,
        answer_2=answer_2,
        answer_3=answer_3,
        answer_4=answer_4,
        question_id=question_id
    )
    db.session.add(testme_answers)
    return testme_answers


def get_testme_right_answer(right_answer_number, question_id):
    """Return right answer"""
    testme_right_answer = TestmeRightAnswer(
        right_answer_number=right_answer_number,
        question_id=question_id
    )
    db.session.add(testme_right_answer)
    return testme_right_answer
