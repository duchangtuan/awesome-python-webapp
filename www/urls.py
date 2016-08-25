#urls.py
from transwarp.web import get, view
from apis import api, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError
from models import User, Blog, Comment

@view('blogs.html')
@get('/')
def test_users():
    blogs = Blog.find_all()
    # find the login users
    user = User.find_first('where email=?', 'fengxi1986@gmail.com')
    return dict(blogs=blogs, user=user)

@api
@get('/api/users')
def api_get_users():
    users = User.find_by('order by created_at desc')
    for u in users:
        u.password = '******'
    return dict(users=users)
