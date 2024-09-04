from flask import Blueprint, render_template
from app.models.user import Post
import time
from sqlalchemy.exc import OperationalError, PendingRollbackError
from app import db  # Assuming you have a db instance from SQLAlchemy

main = Blueprint('main', __name__)

def execute_with_retry(query_func, *args, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return query_func(*args)
        except (OperationalError, PendingRollbackError) as e:
            if isinstance(e, PendingRollbackError):
                db.session.rollback()
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e

@main.route('/')
def index():
    news_posts = execute_with_retry(
        lambda: Post.query.filter_by(category='뉴스').order_by(Post.created_at.desc()).limit(3).all()
    )
    announcement_posts = execute_with_retry(
        lambda: Post.query.filter_by(category='공지사항').order_by(Post.created_at.desc()).limit(3).all()
    )
    return render_template('home.html', news_posts=news_posts, announcement_posts=announcement_posts)

@main.route('/construction_materials')
def construction_materials():
    return render_template('construction_materials.html')

@main.route('/construction_machinery')
def construction_machinery():
    return render_template('construction_machinery.html')

@main.route('/specialized_construction')
def specialized_construction():
    return render_template('specialized_construction.html')

@main.route('/greeting')
def greeting():
    return render_template('greeting.html')

@main.route('/business_areas')
def business_areas():
    return render_template('business_areas.html')

@main.route('/directions')
def directions():
    return render_template('directions.html')

@main.route('/product_guide')
def product_guide():
    return render_template('product_guide.html')

@main.route('/certificates')
def certificates():
    return render_template('certificates.html')

@main.route('/concrete_grinder')
def concrete_grinder():
    return render_template('concrete_grinder.html')

@main.route('/as')
def as_service():
    return render_template('as.html')