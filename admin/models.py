from sqlalchemy import (
    Table,
    Column,
    Integer,
    UnicodeText,
    Unicode,
    Boolean,
    ForeignKey,
    DateTime,
    LargeBinary,
    Date,
    Float,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relation
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
metadata = Base.metadata

alert = Table(u'alert', metadata,
    Column(u'id', Integer, primary_key=True, nullable=False),
    Column(u'alert_type', UnicodeText, ForeignKey('alert_type.ref'), nullable=False),
    Column(u'parameter', UnicodeText),
    Column(u'parameter2', UnicodeText),
    Column(u'user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column(u'confirmed', Integer, nullable=False),
    Column(u'lang', UnicodeText, nullable=False),
    Column(u'cobrand', UnicodeText, nullable=False),
    Column(u'cobrand_data', UnicodeText, nullable=False),
    Column(u'whensubscribed', DateTime, nullable=False),
    Column(u'whendisabled', DateTime),
)

body = Table(u'body', metadata,
    Column(u'id', Integer, primary_key=True, nullable=False),
    Column(u'name', UnicodeText, nullable=False),
    Column(u'parent', Integer, ForeignKey('body.id')),
    Column(u'endpoint', UnicodeText),
    Column(u'jurisdiction', UnicodeText),
    Column(u'api_key', UnicodeText),
    Column(u'send_method', UnicodeText),
    Column(u'send_comments', Boolean, nullable=False),
    Column(u'comment_user_id', Integer, ForeignKey('users.id')),
    Column(u'suppress_alerts', Boolean, nullable=False),
    Column(u'can_be_devolved', Boolean, nullable=False),
    Column(u'send_extended_statuses', Boolean, nullable=False),
    Column(u'deleted', Boolean, nullable=False),
)

comment = Table(u'comment', metadata,
    Column(u'id', Integer, primary_key=True, nullable=False),
    Column(u'problem_id', Integer, ForeignKey('problem.id'), nullable=False),
    Column(u'user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column(u'anonymous', Boolean, nullable=False),
    Column(u'name', UnicodeText),
    Column(u'website', UnicodeText),
    Column(u'created', DateTime, nullable=False),
    Column(u'confirmed', DateTime),
    Column(u'text', UnicodeText, nullable=False),
    Column(u'photo', LargeBinary()),
    Column(u'state', UnicodeText, nullable=False),
    Column(u'cobrand', UnicodeText, nullable=False),
    Column(u'lang', UnicodeText, nullable=False),
    Column(u'cobrand_data', UnicodeText, nullable=False),
    Column(u'mark_fixed', Boolean, nullable=False),
    Column(u'mark_open', Boolean, nullable=False),
    Column(u'problem_state', UnicodeText),
    Column(u'external_id', UnicodeText),
    Column(u'extra', UnicodeText),
    Column(u'send_fail_count', Integer, nullable=False),
    Column(u'send_fail_reason', UnicodeText),
    Column(u'send_fail_timestamp', DateTime),
    Column(u'whensent', DateTime),
)

alert_sent = Table(u'alert_sent', metadata,
    Column(u'alert_id', Integer, ForeignKey('alert.id'), nullable=False),
    Column(u'parameter', UnicodeText),
    Column(u'whenqueued', DateTime, nullable=False),
)

body_areas = Table(u'body_areas', metadata,
    Column(u'body_id', Integer, ForeignKey('body.id'), nullable=False),
    Column(u'area_id', Integer, nullable=False),
)

debugdate = Table(u'debugdate', metadata,
    Column(u'override_today', Date),
)

flickr_imported = Table(u'flickr_imported', metadata,
    Column(u'id', UnicodeText, nullable=False),
    Column(u'problem_id', Integer, ForeignKey('problem.id'), nullable=False),
)

secret = Table(u'secret', metadata,
    Column(u'secret', UnicodeText, nullable=False),
)

textmystreet = Table(u'textmystreet', metadata,
    Column(u'name', UnicodeText, nullable=False),
    Column(u'email', UnicodeText, nullable=False),
    Column(u'postcode', UnicodeText, nullable=False),
    Column(u'mobile', UnicodeText, nullable=False),
)

class Abuse(Base):
    __tablename__ = 'abuse'

    __table_args__ = {}

    #column definitions
    email = Column(u'email', UnicodeText, primary_key=True, nullable=False)

    #relation definitions


class AdminLog(Base):
    __tablename__ = 'admin_log'

    __table_args__ = {}

    #column definitions
    action = Column(u'action', UnicodeText, nullable=False)
    admin_user = Column(u'admin_user', UnicodeText, nullable=False)
    id = Column(u'id', Integer, primary_key=True, nullable=False)
    object_id = Column(u'object_id', Integer, nullable=False)
    object_type = Column(u'object_type', UnicodeText, nullable=False)
    whenedited = Column(u'whenedited', DateTime, nullable=False)

    #relation definitions


class Alert(Base):
    __table__ = alert


    #relation definitions
    alert_type = relation('AlertType', primaryjoin='Alert.alert_type==AlertType.ref')
    users = relation('User', primaryjoin='Alert.user_id==User.id')


class AlertType(Base):
    __tablename__ = 'alert_type'

    __table_args__ = {}

    #column definitions
    head_description = Column(u'head_description', UnicodeText, nullable=False)
    head_link = Column(u'head_link', UnicodeText, nullable=False)
    head_sql_query = Column(u'head_sql_query', UnicodeText, nullable=False)
    head_table = Column(u'head_table', UnicodeText, nullable=False)
    head_title = Column(u'head_title', UnicodeText, nullable=False)
    item_description = Column(u'item_description', UnicodeText, nullable=False)
    item_link = Column(u'item_link', UnicodeText, nullable=False)
    item_order = Column(u'item_order', UnicodeText, nullable=False)
    item_table = Column(u'item_table', UnicodeText, nullable=False)
    item_title = Column(u'item_title', UnicodeText, nullable=False)
    item_where = Column(u'item_where', UnicodeText, nullable=False)
    ref = Column(u'ref', UnicodeText, primary_key=True, nullable=False)
    template = Column(u'template', UnicodeText, nullable=False)

    #relation definitions
    users = relation('User', primaryjoin='AlertType.ref==Alert.alert_type', secondary=alert, secondaryjoin='Alert.user_id==User.id')


class Body(Base):
    __table__ = body


    #relation definitions
    body = relation('Body', primaryjoin='Body.parent==Body.id')
    users = relation('User', primaryjoin='Body.id==Body.parent', secondary=body, secondaryjoin='Body.comment_user_id==User.id')


class Comment(Base):
    __table__ = comment


    #relation definitions
    problem = relation('Problem', primaryjoin='Comment.problem_id==Problem.id')
    users = relation('User', primaryjoin='Comment.user_id==User.id')


class Contact(Base):
    __tablename__ = 'contacts'

    __table_args__ = {}

    #column definitions
    api_key = Column(u'api_key', UnicodeText)
    body_id = Column(u'body_id', Integer, ForeignKey('body.id'), nullable=False)
    category = Column(u'category', UnicodeText, nullable=False)
    confirmed = Column(u'confirmed', Boolean, nullable=False)
    deleted = Column(u'deleted', Boolean, nullable=False)
    editor = Column(u'editor', UnicodeText, nullable=False)
    email = Column(u'email', UnicodeText, nullable=False)
    endpoint = Column(u'endpoint', UnicodeText)
    extra = Column(u'extra', UnicodeText)
    id = Column(u'id', Integer, primary_key=True, nullable=False)
    jurisdiction = Column(u'jurisdiction', UnicodeText)
    non_public = Column(u'non_public', Boolean)
    note = Column(u'note', UnicodeText, nullable=False)
    send_method = Column(u'send_method', UnicodeText)
    whenedited = Column(u'whenedited', DateTime, nullable=False)

    #relation definitions
    body = relation('Body', primaryjoin='Contact.body_id==Body.id')


class ContactsHistory(Base):
    __tablename__ = 'contacts_history'

    __table_args__ = {}

    #column definitions
    body_id = Column(u'body_id', Integer, nullable=False)
    category = Column(u'category', UnicodeText, nullable=False)
    confirmed = Column(u'confirmed', Boolean, nullable=False)
    contact_id = Column(u'contact_id', Integer, nullable=False)
    contacts_history_id = Column(u'contacts_history_id', Integer, primary_key=True, nullable=False)
    deleted = Column(u'deleted', Boolean, nullable=False)
    editor = Column(u'editor', UnicodeText, nullable=False)
    email = Column(u'email', UnicodeText, nullable=False)
    note = Column(u'note', UnicodeText, nullable=False)
    whenedited = Column(u'whenedited', DateTime, nullable=False)

    #relation definitions


class PartialUser(Base):
    __tablename__ = 'partial_user'

    __table_args__ = {}

    #column definitions
    email = Column(u'email', UnicodeText, nullable=False)
    id = Column(u'id', Integer, primary_key=True, nullable=False)
    name = Column(u'name', UnicodeText, nullable=False)
    nsid = Column(u'nsid', UnicodeText, nullable=False)
    phone = Column(u'phone', UnicodeText, nullable=False)
    service = Column(u'service', UnicodeText, nullable=False)

    #relation definitions


class Problem(Base):
    __tablename__ = 'problem'

    __table_args__ = {}

    #column definitions
    anonymous = Column(u'anonymous', Boolean, nullable=False)
    areas = Column(u'areas', UnicodeText, nullable=False)
    bodies_str = Column(u'bodies_str', UnicodeText)
    category = Column(u'category', UnicodeText, nullable=False)
    cobrand = Column(u'cobrand', UnicodeText, nullable=False)
    cobrand_data = Column(u'cobrand_data', UnicodeText, nullable=False)
    confirmed = Column(u'confirmed', DateTime)
    created = Column(u'created', DateTime, nullable=False)
    detail = Column(u'detail', UnicodeText, nullable=False)
    external_body = Column(u'external_body', UnicodeText)
    external_id = Column(u'external_id', UnicodeText)
    external_source = Column(u'external_source', UnicodeText)
    external_source_id = Column(u'external_source_id', UnicodeText)
    external_team = Column(u'external_team', UnicodeText)
    extra = Column(u'extra', UnicodeText)
    flagged = Column(u'flagged', Boolean, nullable=False)
    geocode = Column(u'geocode', LargeBinary())
    id = Column(u'id', Integer, primary_key=True, nullable=False)
    interest_count = Column(u'interest_count', Integer)
    lang = Column(u'lang', UnicodeText, nullable=False)
    lastupdate = Column(u'lastupdate', DateTime, nullable=False)
    latitude = Column(u'latitude', Float(precision=53), nullable=False)
    longitude = Column(u'longitude', Float(precision=53), nullable=False)
    name = Column(u'name', UnicodeText, nullable=False)
    non_public = Column(u'non_public', Boolean)
    photo = Column(u'photo', LargeBinary())
    postcode = Column(u'postcode', UnicodeText, nullable=False)
    send_fail_count = Column(u'send_fail_count', Integer, nullable=False)
    send_fail_reason = Column(u'send_fail_reason', UnicodeText)
    send_fail_timestamp = Column(u'send_fail_timestamp', DateTime)
    send_method_used = Column(u'send_method_used', UnicodeText)
    send_questionnaire = Column(u'send_questionnaire', Boolean, nullable=False)
    service = Column(u'service', UnicodeText, nullable=False)
    state = Column(u'state', UnicodeText, nullable=False)
    subcategory = Column(u'subcategory', UnicodeText)
    title = Column(u'title', UnicodeText, nullable=False)
    used_map = Column(u'used_map', Boolean, nullable=False)
    user_id = Column(u'user_id', Integer, ForeignKey('users.id'), nullable=False)
    whensent = Column(u'whensent', DateTime)

    #relation definitions
    users = relation('User', primaryjoin='Problem.id==Comment.problem_id', secondary=comment, secondaryjoin='Comment.user_id==User.id')


class Questionnaire(Base):
    __tablename__ = 'questionnaire'

    __table_args__ = {}

    #column definitions
    ever_reported = Column(u'ever_reported', Boolean)
    id = Column(u'id', Integer, primary_key=True, nullable=False)
    new_state = Column(u'new_state', UnicodeText)
    old_state = Column(u'old_state', UnicodeText)
    problem_id = Column(u'problem_id', Integer, ForeignKey('problem.id'), nullable=False)
    whenanswered = Column(u'whenanswered', DateTime)
    whensent = Column(u'whensent', DateTime, nullable=False)

    #relation definitions
    problem = relation('Problem', primaryjoin='Questionnaire.problem_id==Problem.id')


class Session(Base):
    __tablename__ = 'sessions'

    __table_args__ = {}

    #column definitions
    expires = Column(u'expires', Integer)
    id = Column(u'id', Unicode(length=72), primary_key=True, nullable=False)
    session_data = Column(u'session_data', UnicodeText)

    #relation definitions


class Token(Base):
    __tablename__ = 'token'

    __table_args__ = {}

    #column definitions
    created = Column(u'created', DateTime, nullable=False)
    data = Column(u'data', LargeBinary(), nullable=False)
    scope = Column(u'scope', UnicodeText, primary_key=True, nullable=False)
    token = Column(u'token', UnicodeText, primary_key=True, nullable=False)

    #relation definitions


class User(Base):
    __tablename__ = 'users'

    __table_args__ = {}

    #column definitions
    email = Column(u'email', UnicodeText, nullable=False)
    flagged = Column(u'flagged', Boolean, nullable=False)
    from_body = Column(u'from_body', Integer, ForeignKey('body.id'))
    id = Column(u'id', Integer, primary_key=True, nullable=False)
    name = Column(u'name', UnicodeText)
    password = Column(u'password', UnicodeText, nullable=False)
    phone = Column(u'phone', UnicodeText)
    title = Column(u'title', UnicodeText)

    #relation definitions
    body = relation('Body', primaryjoin='User.from_body==Body.id')
    alert_types = relation('AlertType', primaryjoin='User.id==Alert.user_id', secondary=alert, secondaryjoin='Alert.alert_type==AlertType.ref')
    bodies = relation('Body', primaryjoin='User.id==Body.comment_user_id', secondary=body, secondaryjoin='Body.parent==Body.id')
    problems = relation('Problem', primaryjoin='User.id==Comment.user_id', secondary=comment, secondaryjoin='Comment.problem_id==Problem.id')
