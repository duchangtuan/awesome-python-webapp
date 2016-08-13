#urls.py
from transwarp.web import get, view
from models import User, Blog, Comment

@view('blogs.html')
@get('/')
def test_users():
    blogs = Blog.find_all()
    # find the login users
    user = User.find_first('where email=?', 'fengxi1986@gmail.com')
    return dict(blogs=blogs, user=user)
