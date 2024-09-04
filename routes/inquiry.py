from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.user import Post, Comment, User, Like, Dislike
from app import db

inquiry = Blueprint('inquiry', __name__)

@inquiry.route('/inquiry')
@login_required
def inquiry_board():
    category = request.args.get('category', '공지사항')
    search_query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    query = Post.query.filter_by(category=category)
    if search_query:
        query = query.filter(Post.title.contains(search_query) | Post.content.contains(search_query))
    
    posts_pagination = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    posts_with_users = []
    for post in posts_pagination.items:
        user = User.query.get(post.user_id)
        comment_count = Comment.query.filter_by(post_id=post.id).count()
        posts_with_users.append({
            'post': post,
            'user': user,
            'comment_count': comment_count
        })
    return render_template('inquiry.html', posts=posts_with_users, pagination=posts_pagination, selected_category=category, search_query=search_query)

@inquiry.route('/inquiry/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category', '공지사항')  # 기본값 설정
        post = Post(title=title, content=content, user_id=current_user.id, category=category)
        db.session.add(post)
        db.session.commit()
        flash('게시물이 작성되었습니다.', 'success')
        return redirect(url_for('inquiry.inquiry_board'))
    return render_template('new_post.html')

@inquiry.route('/inquiry/<int:post_id>')
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.views += 1  # 조회수 증가
    db.session.commit()
    user = User.query.get(post.user_id)
    comments_with_users = []
    for comment in post.comments:
        comment_user = User.query.get(comment.user_id)
        comments_with_users.append({
            'comment': comment,
            'user': comment_user
        })
    user_liked = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first() is not None
    user_disliked = Dislike.query.filter_by(user_id=current_user.id, post_id=post_id).first() is not None
    return render_template('view_post.html', post=post, user=user, comments=comments_with_users, user_liked=user_liked, user_disliked=user_disliked)

@inquiry.route('/inquiry/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('이 게시물을 수정할 권한이 없습니다.', 'danger')
        return redirect(url_for('inquiry.view_post', post_id=post.id))
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.category = request.form.get('category', post.category)  # 기본값 설정
        db.session.commit()
        flash('게시물이 수정되었습니다.', 'success')
        return redirect(url_for('inquiry.view_post', post_id=post.id))
    
    return render_template('edit_post.html', post=post)

@inquiry.route('/inquiry/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('이 게시물을 삭제할 권한이 없습니다.', 'danger')
        return redirect(url_for('inquiry.view_post', post_id=post.id))
    
    db.session.delete(post)
    db.session.commit()
    flash('게시물이 삭제되었습니다.', 'success')
    return redirect(url_for('inquiry.inquiry_board'))

@inquiry.route('/inquiry/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form['content']
    comment = Comment(content=content, user_id=current_user.id, post_id=post.id)
    db.session.add(comment)
    db.session.commit()
    flash('댓글이 작성되었습니다.', 'success')
    return redirect(url_for('inquiry.view_post', post_id=post.id))

@inquiry.route('/inquiry/<int:comment_id>/edit_comment', methods=['POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        flash('이 댓글을 수정할 권한이 없습니다.', 'danger')
        return redirect(url_for('inquiry.view_post', post_id=comment.post_id))
    
    content = request.form['content']
    if not content:
        flash('내용을 입력해주세요.', 'danger')
        return redirect(url_for('inquiry.view_post', post_id=comment.post_id))
    
    comment.content = content
    db.session.commit()
    flash('댓글이 수정되었습니다.', 'success')
    return redirect(url_for('inquiry.view_post', post_id=comment.post_id))

@inquiry.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        flash('이 댓글을 삭제할 권한이 없습니다.', 'danger')
        return redirect(url_for('inquiry.view_post', post_id=comment.post_id))
    
    db.session.delete(comment)
    db.session.commit()
    flash('댓글이 삭제되었습니다.', 'success')
    return redirect(url_for('inquiry.view_post', post_id=comment.post_id))

@inquiry.route('/inquiry/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # 자신이 작성한 게시물인 경우 아무 동작도 하지 않음
    if post.user_id == current_user.id:
        return jsonify({'likes': post.like_count, 'dislikes': post.dislike_count})

    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    dislike = Dislike.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if like:
        db.session.delete(like)
        post.like_count -= 1
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        post.like_count += 1
        if dislike:
            db.session.delete(dislike)
            post.dislike_count -= 1

    db.session.commit()
    return jsonify({'likes': post.like_count, 'dislikes': post.dislike_count})

@inquiry.route('/inquiry/<int:post_id>/dislike', methods=['POST'])
@login_required
def dislike_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # 자신이 작성한 게시물인 경우 아무 동작도 하지 않음
    if post.user_id == current_user.id:
        return jsonify({'likes': post.like_count, 'dislikes': post.dislike_count})

    dislike = Dislike.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if dislike:
        db.session.delete(dislike)
        post.dislike_count -= 1
    else:
        new_dislike = Dislike(user_id=current_user.id, post_id=post_id)
        db.session.add(new_dislike)
        post.dislike_count += 1
        if like:
            db.session.delete(like)
            post.like_count -= 1

    db.session.commit()
    return jsonify({'likes': post.like_count, 'dislikes': post.dislike_count})