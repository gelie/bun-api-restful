from flask_restplus import Model, fields
from app.models import User, Group, UserGroupMembership

user_fields = Model('User', {
    'login': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'links': {
        'self': fields.Url('api.user', absolute=True),
        'collection': fields.Url('api.users', absolute=True),
        # 'groups': fields.List(fields.Nested('api.groups'))
    }

})

user_collection = Model('UserList', {
    'users': fields.List(fields.Nested(user_fields))
})

group_fields = Model('Group', {
    # 'login': fields.String,
    'full_name': fields.String,
    'short_name': fields.String,
    'links': {
        'self': fields.Url('api.group', absolute=True),
        'collection': fields.Url('api.groups', absolute=True)
        # 'groups': fields.List(fields.Nested('api.groups'))
    }

})
