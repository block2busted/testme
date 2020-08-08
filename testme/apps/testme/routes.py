from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from testme import app, db
from .models import Testme, Comment
from .forms import TestForm, CommentForm


@app.route('/testme-list')
def testme_list():
    testme_list = Testme.query.all()
    return render_template('testme/testme_list.html', testme_list=testme_list)


@app.route('/testme/<int:testme_id>', methods=['POST', 'GET'])
def testme_detail(testme_id):
    testme = Testme.query.get_or_404(testme_id)
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
        print('sss')
        return render_template(
            'testme/testme_detail.html',
            testme=testme,
            comment_form=comment_form,
            testme_comment_list=testme_comment_list
        )
    else:
        return render_template(
            'testme/testme_detail.html',
            testme=testme,
            comment_form=comment_form,
            testme_comment_list=testme_comment_list
        )


@app.route('/testme/new', methods=['POST', 'GET'])
@login_required
def new_test():
    testme_form = TestForm()
    if request.method == 'POST':
        if testme_form.validate_on_submit():
            testme = Testme(
                title=testme_form.title.data,
                description=testme_form.description.data,
                user_id=current_user.id,
                test_author=current_user,
                author=current_user.username
            )
            db.session.add(testme)
            db.session.commit()
            flash('Test was created.', 'success')
            return redirect(url_for('testme_list'))
    else:
        return render_template('testme/new_test.html', testme_form=testme_form)