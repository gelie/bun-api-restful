from flask_restful import Api, Resource

from app import db
from app.api import bp
api = Api(bp)

from app.models import User, UserGroupMembership, Group
from app.api.schema   import UserSchema, GroupSchema, UserMembership
from base64 import b64encode

user_schema = UserSchema()
users_schema = UserSchema(many=True)
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
membership_schema = UserMembership(many=True)

class UserPage(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user.image is not None:
            user.image = b64encode(user.image)
        return user_schema.dump(user).data
        

class UserList(Resource):
    def get(self):
        users = User.query.paginate(1,10, False).items
        for user in users:
            if user.image is not None:
                user.image = b64encode(user.image)
        return users_schema.dump(users).data
        
class GroupPage(Resource):
    def get(self, group_id):
        group = Group.query.get(group_id)
        return group_schema.dump(group).data
        

class GroupList(Resource):
    def get(self):
        groups = Group.query.paginate(1,10, False).items
        return groups_schema.dump(groups).data


class Membership(Resource):
    def get(self, user_id):
        mygroups = User.user_memberships
        memberships = UserGroupMembership.query.filter(UserGroupMembership.user_id==user_id).all()
        return membership_schema.dump(memberships).data

        
api.add_resource(UserPage, '/users/<int:user_id>', endpoint='user')
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(GroupPage, '/groups/<int:group_id>', endpoint='group')
api.add_resource(GroupList, '/groups', endpoint='groups')
api.add_resource(Membership, '/mygroups/<int:user_id>', endpoint='mygroups')
