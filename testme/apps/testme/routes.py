from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from testme import app, db
from .models import Comment, CustomTestme, TestmeAnswer, TestmeRightAnswer, TestmeQuestion
from .forms import TestForm, CommentForm


@app.route('/testme-list')
def testme_list():
    testme_list = CustomTestme.query.all()
    return render_template('testme/testme_list.html', testme_list=testme_list)


@app.route('/testme/<int:testme_id>', methods=['POST', 'GET'])
def testme_detail(testme_id):
    testme = CustomTestme.query.get_or_404(testme_id)
    comment_form = CommentForm()
    testme_comment_list = Comment.query.filter_by(testme_id=testme_id)
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
            testme_comment_list=testme_comment_list
        )


@app.route('/testme/create', methods=['POST', 'GET'])
def testme_create():
    testme_form = TestForm()

    if testme_form.add_question.data:
        """Add one more question to testme"""
        testme_form.question.append_entry()
        return render_template('testme/testme_create.html', testme_form=testme_form)

    if testme_form.validate_on_submit():
        testme = CustomTestme(title=testme_form.title.data, author_id=1)
        db.session.add(testme)
        for question_data in testme_form.question.data:
            question = TestmeQuestion(
                testme_id=testme.id,
                title=question_data['question']
            )
            db.session.add(question)

            testme_answers = TestmeAnswer(
                answer_1=question_data['answer_1'],
                answer_2=question_data['answer_2'],
                answer_3=question_data['answer_3'],
                answer_4=question_data['answer_4'],
                question_id=question.id
            )
            db.session.add(testme_answers)

            testme_right_answer = TestmeRightAnswer(
                right_answer_number=question_data['right_answer'],
                question_id=question.id
            )
            db.session.add(testme_right_answer)

            question.answers = testme_answers
            question.right_answer = testme_right_answer
            testme.questions.append(question)
        db.session.commit()
        return redirect(url_for('testme_detail', testme_id=testme.id))

    return render_template('testme/testme_create.html', testme_form=testme_form)