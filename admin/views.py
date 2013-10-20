from pyramid.renderers import get_renderer
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from wtforms import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms import validators

from sqlalchemy import desc, Table

from admin import models

MAIN_TEMPLATE = 'admin:templates/template.pt'

def main_template():
    return get_renderer(MAIN_TEMPLATE).implementation()

def views_include(config):
    config.add_route('home', '/')
    config.add_view(home,
                    route_name='home',
                    renderer='admin:templates/home.pt')

    config.add_route('list', '/list')
    config.add_view(plist,
                    route_name='list',
                    permission='body',
                    renderer='admin:templates/list.pt')

    config.add_route('update', '/update/{problem_id}')
    config.add_view(update,
                    route_name='update',
                    permission='body',
                    renderer='admin:templates/update.pt')

    config.add_route('status', '/status')
    config.add_view(status,
                    permission='body',
                    route_name='status')
    
    config.include(account_include)

def get_areas(request):
    body_id = request.user.body_id

    db = request.db
    meta = db._metadata
    tbl_bas = Table("body_areas", meta, autoload=True)
    bas_pks = [tbl_bas.c.body_id, tbl_bas.c.area_id]
    bas = db.map(tbl_bas, primary_key=bas_pks)
    areas = (bas
             .filter_by(body_id=body_id)
             .all())
    return map(lambda a: ',1,13,{area_id}'.format(area_id=a.area_id),
               areas)
    
def home(request):
    if not request.user:
        return HTTPFound(request.route_url('login'))
        
    db = request.db

    areas = get_areas(request)
    problems = (db.problem
                .filter_by(state=u'confirmed')
                .filter(db.problem.areas.in_(areas))
                .order_by(desc(db.problem.id))
                .all())
    if not len(problems):
        return HTTPFound(request.route_url('list'))

    return {'template': main_template(),
            'title': 'Dashboard',
            'problems': problems}

choices = [('investigating', 'investigating'),
           ('planned', 'planned'),
           ('action scheduled', 'action scheduled'),
           ('closed', 'closed'),
           ('fixed', 'fixed'),
           ('not responsible', 'not responsbile'),
           ('unable to fix', 'unable to fix'),
           ('duplicate', 'duplicate'),
           ('hidden', 'hidden')]

class StatusForm(Form):
    state = SelectField('Status', choices=choices)
    
def update(request):
    pid = request.matchdict['problem_id']
    pid = int(pid)

    db = request.db
    areas = get_areas(request)
    query = (db.problem
             .filter(db.problem.areas.in_(areas))
             .filter_by(id=pid))

    problem = query.first()
    if not problem:
        request.session.flash('Invalid Issue Id')
        return HTTPFound(request.referer)

    form = StatusForm(request.POST, problem)
    if request.method == 'POST' and form.validate():
        query.update({'state': form.state.data})
        db.commit()
        request.session.flash('Issue updated!')
        return HTTPFound(request.route_url('list'))

    user = (db.users
            .filter_by(id=problem.user_id)
            .first())
    return {'template': main_template(),
            'title': 'Update Issue',
            'form': form,
            'user': user,
            'problem': problem}
    
def plist(request):
    problem_id = request.params.get('problem_id')

    db = request.db
    areas = get_areas(request)
    query = (db.problem
             .filter(db.problem.areas.in_(areas))
             .order_by(desc(db.problem.id)))

    if not problem_id:
        problems = query.all()

        pending = (db.problem
                   .filter_by(state=u'confirmed')
                   .filter(db.problem.areas.in_(areas))
                   .order_by(desc(db.problem.id))
                   .count())
        if pending:
            return HTTPFound(request.route_url('home'))
    else:
        problem_id = int(problem_id)
        problems = query.filter_by(id=problem_id).all()

    return {'template': main_template(),
            'title': 'Dashboard',
            'problems': problems}

def status(request):
    p = request.params
    action = p.get('action')
    alltrue = p.get('all')
    target = p.get('target')

    db = request.db
    areas = get_areas(request)
    query = (db.problem
             .filter(db.problem.areas.in_(areas)))
    if not alltrue and target:
        problem_id = int(target)
        query = (query.filter_by(id=problem_id))

    if action == 'confirm':
        state = u'investigating'
    elif action == 'delete':
        state = u'hidden'

    query.update({'state': state})
    db.commit()

    request.session.flash('Updated!')
    return HTTPFound(request.referer)
    
def account_include(config):
    config.add_route('login', '/login')
    config.add_view(login,
                    route_name='login',
                    renderer='admin:templates/login.pt')
    
    config.add_route('logout', '/logout')
    config.add_view(logout,
                    route_name='logout')

class LoginForm(Form):
    username = TextField('Login Id', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

def login(request):
    if request.user:
        return HTTPFound(request.route_url('home'))
        
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.validate():
        session = models.DBSession()
        user = (session.query(models.Login)
                .filter(models.Login.username==unicode(form.username.data))
                .first())
        if user and user.check_password(form.password.data):
            headers = remember(request, user.username)
            request.session.flash('Welcome back!')
            return HTTPFound(request.route_url('home'),
                             headers=headers)
        else:
            request.session.flash('Login failed, please try again')
    return {'form':form,
            'template': main_template(),
            'title': 'Account Login'}

def logout(request):
    headers = forget(request)
    request.session.flash("Goodbye. We'll see you soon")
    return HTTPFound(request.route_url('home'),
                     headers=headers)
