from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from testme import app, db
from .models import Testme
from .forms import TestForm


@app.route('/testme-list')
def testme_list():
    testme_list = Testme.query.all()
    return render_template('testme/testme_list.html', testme_list=testme_list)


@app.route('/testme/<int:testme_id>')
def testme_detail(testme_id):
    testme = Testme.query.get_or_404(testme_id)
    return render_template('testme/testme_detail.html', testme=testme)


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