from flask_restplus import Api, Resource, marshal_with
from app import db
from app.api import bp
from app.models import User, UserGroupMembership, Group

from .schema import user_fields, group_fields
from base64 import b64encode

api = Api(bp, version='1.0', title='Bungeni API',
          description='Bungeni API',)


@api.route('/users/<int:user_id>', endpoint='user')
@api.doc(params={'user_id': 'A User ID'})
class UserPage(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        if user.image is not None:
            user.image = b64encode(user.image)
        return user


@api.route('/users', endpoint='users')
@api.doc("Returns 10 users at a time")
class UserList(Resource):
    @marshal_with(user_fields, envelope='items')
    def get(self):
        users = User.query.paginate(1, 10, False).items
        for user in users:
            if user.image is not None:
                user.image = b64encode(user.image)
        return users


@api.route('/groups/<int:group_id>', endpoint='group')
@api.doc(params={'group_id': 'A Group ID'})
class GroupPage(Resource):
    @marshal_with(group_fields)
    def get(self, group_id):
        group = Group.query.get(group_id)
        return group


@api.route('/groups', endpoint='groups')
@api.doc(params={'start_page': 'Starting page', 'number_of_items': 'Number of Items to display'})
class GroupList(Resource):
    @marshal_with(group_fields, envelope='items')
    def get(self, start_page=1, number_of_items=10):
        groups = Group.query.paginate(int(start_page), int(number_of_items), False).items
        return groups


# class Membership(Resource):
    # def get(self, user_id):
        # mygroups = User.user_memberships
        # memberships = UserGroupMembership.query.filter(UserGroupMembership.user_id==user_id).all()
        # return membership_schema.dump(memberships).data


# api.add_resource(Membership, '/mygroups/<int:user_id>', endpoint='mygroups')
