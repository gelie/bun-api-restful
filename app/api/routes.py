from flask_restplus import Api, Resource, marshal_with, reqparse
from flask import url_for
from app import db
from app.api import bp
from app.models import User, UserGroupMembership, Group

from .schema import user_fields, group_fields, user_collection
from base64 import b64encode

api = Api(bp, version='1.0', title='Bungeni API',
          description='Bungeni API')

parser = reqparse.RequestParser()
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help="'page' cannot be converted")
parser.add_argument(
    'per_page',
    type=int,
    help="'per_page' cannot be converted")


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
@api.doc(
    params={
        'page': 'Starting page',
        'per_page': 'Number of Items to display'})
@api.doc("Returns 20 users at a time unless 'per_page' are suplied")
class UserList(Resource):
    @marshal_with(user_collection)
    def get(self):
        args = parser.parse_args()
        page = args['page']
        print(type(page))
        per_page = args['per_page']
        users = User.query.paginate(page, per_page, error_out=True)
        print(type(users))
        print(type(users.items))
        print(users.items)
        # for user in users:
            # if user.image is not None:
                # user.image = b64encode(user.image)
        return users.items


@api.route('/groups/<int:group_id>', endpoint='group')
@api.doc(params={'group_id': 'A Group ID'})
class GroupPage(Resource):
    @marshal_with(group_fields)
    def get(self, group_id):
        group = Group.query.get(group_id)
        return group


@api.route('/groups', endpoint='groups')
@api.doc(
    params={
        'page': 'Starting page',
        'per_page': 'Number of Items to display'})
class GroupList(Resource):
    @marshal_with(group_fields, envelope='items')
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('page', type=int, help="'page' cannot be converted")
        # parser.add_argument('per_page', type=int, help="'per_page' cannot be converted")
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        groups = Group.query.paginate(page, per_page, error_out=True).items
        return groups


# class Membership(Resource):
    # def get(self, user_id):
        # mygroups = User.user_memberships
        # memberships = UserGroupMembership.query.filter(UserGroupMembership.user_id==user_id).all()
        # return membership_schema.dump(memberships).data

# api.add_resource(Membership, '/mygroups/<int:user_id>', endpoint='mygroups')
