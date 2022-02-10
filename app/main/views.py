from flask import render_template, request, redirect, url_for, abort
from . import main
from ..models import User, Pitch, Comment,Downvote,Upvote
from .. import db, photos
from .forms import PitchForm, CommentForm, updateProfile
from flask_login import login_required, current_user
import datetime


@main.route('/')
def index():
    pickup=Pitch.query.filter_by(category='pickup').all()
    interview=Pitch.query.filter_by(category='interview').all()
    product=Pitch.query.filter_by(category='product').all()
    promotion=Pitch.query.filter_by(category='promotion').all()
    all_pitch = Pitch.query.all()
    return render_template('index.html', pitches=all_pitch,pickup=pickup,interview=interview,product=product,promotion=promotion,uname=current_user)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    pitches_count = Pitch.count_pitches(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, pitches=pitches_count, date=user_joined)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = updateProfile()

    if form.validate_on_submit():
        user.bio = form.biography.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route('/pitch/new', methods=['GET', 'POST'])
@login_required
def new_pitch():
    new_form = PitchForm()
    if new_form.validate_on_submit():
        title = new_form.title.data
        category = new_form.category.data
        pitch = new_form.pitch.data

        new_pitch = Pitch(title=title, pitch=pitch, category=category,user=current_user)

        # Save pitch method
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    return render_template('new_pitch.html',  pitch_form=new_form)


@main.route('/upvote/<id>', methods=['GET', 'POST'])
@login_required
def upVote(id):
    votes = Upvote.get_upvotes(id)
    output = f'{current_user.id}:{id}'
    for vote in votes:
        result = f'{vote}'
        if output == result:
            return redirect(url_for('main.index', id=id))
        else:
            continue
    new_upvote = Upvote(user=current_user, pitch_id=id)
    new_upvote.save()
    return redirect(url_for('main.index', id=id))


@main.route('/downvote/<id>', methods=['GET', 'POST'])
@login_required
def downVote(id):
    votes = Downvote.get_downvotes(id)
    output = f'{current_user.id}:{id}'
    for vote in votes:
        result = f'{vote}'
        if output == result:
            return redirect(url_for('main.index', id=id))
        else:
            continue
    new_downvote = Downvote(user=current_user, pitch_id=id)
    new_downvote.save()
    return redirect(url_for('main.index', id=id))

@main.route('/comment/<id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    pitch = Pitch.query.get(id)
    fetch_all_comments = Comment.query.filter_by(pitch_id=id).all()
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        pitch_id = id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment=comment, user_id=user_id, pitch_id=pitch_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', id=pitch_id))
    return render_template('comments.html', comment_form=comment_form, pitch=pitch, all_comments=fetch_all_comments)


@main.route('/pickup')
def pickup():

    pickup = Pitch.query.filter_by(category='pickup').all()
    return render_template('pickup.html', pitches=pickup)

@main.route('/interview')
def interview():

    interview = Pitch.query.filter_by(category='interview').all()
    return render_template('interview.html', pitches=interview)

@main.route('/product')
def product():

    product = Pitch.query.filter_by(category='product').all()
    return render_template('product.html', pitches=product)

@main.route('/promotion')
def promotion():

    promotion = Pitch.query.filter_by(category='promotion').all()
    print(promotion)
    return render_template('promotion.html', pitches=promotion)