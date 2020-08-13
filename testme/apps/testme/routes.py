import random

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from sqlalchemy import desc
from testme import app, db
from .models import Comment, CustomTestme, UserTestme, TestmeQuestion, \
    UserTestmeAnswer, TestmeRightAnswer, TestmeAnswer
from .forms import TestForm, CommentForm
from .services import get_testme_question, get_testme_answers, get_testme_right_answer, get_right_answer_content


@app.route('/testme-list')
def testme_list():
    testme_list = CustomTestme.query.all()
    return render_template('testme/testme_list.html', testme_list=testme_list)


@app.route('/testme-list-by-created')
def testme_list_by_created():
    testme_list = CustomTestme.query.order_by(desc(CustomTestme.date_created)).all()
    return render_template('testme/testme_list.html', testme_list=testme_list)


@app.route('/testme/<int:testme_id>', methods=['POST', 'GET'])
def testme_detail(testme_id):
    testme = CustomTestme.query.get_or_404(testme_id)
    comment_form = CommentForm()
    testme_comment_list = Comment.query.filter_by(testme_id=testme_id)
    user_testme = UserTestme.query.filter_by(testme_id=testme.id, username=current_user.username).first()
    if comment_form.validate_on_submit():
        testme_comment = Comment(
            author=current_user.username,
            user_id=current_user.id,
            testme_id=testme_id,
            content=comment_form.content.data
        )
        db.session.add(testme_comment)
        db.session.commit()
        return redirect(url_for('testme_detail', testme_id=testme_id))
    else:
        return render_template(
            'testme/testme_detail.html',
            testme=testme,
            comment_form=comment_form,
            testme_comment_list=testme_comment_list,
            user_testme=user_testme
        )


@app.route('/testme/create', methods=['POST', 'GET'])
def testme_create():
    testme_form = TestForm()

    if testme_form.add_question.data:
        """Add one more question to testme"""
        testme_form.question.append_entry()
        return render_template('testme/testme_create.html', testme_form=testme_form)

    if testme_form.validate_on_submit():
        testme = CustomTestme(
            title=testme_form.title.data,
            description=testme_form.description.data,
            author_id=current_user.id,
            count_questions=0
        )
        db.session.add(testme)
        db.session.commit()
        for question_data in testme_form.question.data:
            question = get_testme_question(
                testme_id=testme.id,
                title=question_data['question']
            )
            testme_answers = get_testme_answers(
                answer_1=question_data['answer_1'],
                answer_2=question_data['answer_2'],
                answer_3=question_data['answer_3'],
                answer_4=question_data['answer_4'],
                testme_id=testme.id,
                question_id=question.id
            )
            right_answer = get_right_answer_content(
                question_data_right_answer=question_data['right_answer'],
                question_data=question_data
            )
            testme_right_answer = get_testme_right_answer(
                right_answer=right_answer,
                question_id=question.id
            )
            question.answers = testme_answers
            question.right_answer = testme_right_answer
            testme.questions.append(question)
            testme.count_questions += 1
        db.session.commit()
        return redirect(url_for('testme_detail', testme_id=testme.id))

    return render_template('testme/testme_create.html', testme_form=testme_form)


@app.route('/testme/<int:testme_id>/start', methods=['POST', 'GET'])
def testme_start(testme_id):
    """Start testme"""
    testme = CustomTestme.query.get_or_404(testme_id)
    question_list = TestmeQuestion.query.filter_by(testme_id=testme.id)

    if request.method == 'POST':
        passed_testme = UserTestme.query.filter_by(testme_id=testme.id, user_id=current_user.id, username=current_user.username).first()
        if passed_testme:
            db.session.delete(passed_testme)
        user_testme = UserTestme(
            testme_id=testme.id,
            user_id=current_user.id,
            username=current_user.username,
            right_answer_count=0,
            result=0
        )
        db.session.add(user_testme)
        db.session.commit()
        for question_id, answer in request.form.items():
            right_answer = TestmeRightAnswer.query.filter_by(question_id=question_id).first().content
            right_or_not = False
            if answer == str(right_answer):
                right_or_not = True
                user_testme.right_answer_count += 1
                user_testme.result += (1/testme.count_questions)*100
            user_question = UserTestmeAnswer(
                user_username=current_user.username,
                user_testme_id=user_testme.id,
                question_id=question_id,
                content=answer,
                right_or_not=right_or_not
            )
            db.session.add(user_question)
            db.session.commit()
            user_testme.answer_list.append(user_question)
            db.session.commit()
        return redirect(url_for('testme_detail', testme_id=testme.id))
    return render_template('testme/testme_start.html', testme=testme, question_list=question_list)


@app.route('/testme/search')
def search():
    testme_list = CustomTestme.query.filter(CustomTestme.title.contains(str(request.args.get('Q')))).all()
    return render_template('testme/testme_list.html', testme_list=testme_list)


@app.route('/testme/ended')
def user_testme_perfomed():
    testme_list = UserTestme.query.filter_by(
        username=current_user.username
    ).all()
    return render_template('testme/testme_list.html', testme_list=testme_list)


@app.route('/generate-testme')
def generate_testme():
    """Auto-generate testme"""
    for i in range(2):
        last_testme = CustomTestme.query.order_by(desc(CustomTestme.id)).first()
        testme = CustomTestme(
            title='Title of question №' + str(last_testme.id + 1),
            description='Short description.',
            count_questions=0,
            author_id=1,
            execution_count=0
        )
        db.session.add(testme)
        db.session.commit()
        for j in range(random.randint(1, 15)):
            last_question = TestmeQuestion.query.order_by(desc(TestmeQuestion.id)).first()
            testme_question = TestmeQuestion(
                testme_id=testme.id,
                title='Title for question №' + str(last_question.id + 1),
            )
            db.session.add(testme_question)
            db.session.commit()
            testme_answers = TestmeAnswer(
                answer_1='First answer.',
                answer_2='Second answer.',
                answer_3='Third answer.',
                answer_4='Fourth answer.',
                testme_id=testme.id,
                question_id=testme_question.id
            )
            db.session.add(testme_answers)
            db.session.commit()
            right_answer = TestmeRightAnswer(
                content=random.randint(1, 4),
                question_id=testme_question.id
            )
            db.session.add(right_answer)
            db.session.commit()
            testme_question.answers = testme_answers
            testme_question.right_answer = right_answer
            testme.questions.append(testme_question)
            db.session.commit()

    return redirect(url_for('testme_list'))