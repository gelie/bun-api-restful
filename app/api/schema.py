from app.models import User, Group, UserGroupMembership
from app import ma
from marshmallow import fields
# from .routes import UserPage


    
class GroupSchema(ma.ModelSchema):
    class Meta:
        model = Group
        fields = ('group_id', 'short_name', 'full_name', 'links')
        
    links = ma.Hyperlinks({
        'self': ma.URLFor('api.group', group_id='<group_id>', _external=1),
        'collection': ma.URLFor('api.groups', _external=1)
    })

class UserMembership(ma.ModelSchema):
    class Meta:
        model = UserGroupMembership
        fields = ('group', 'links')
        
    links = ma.Hyperlinks({
        'self': ma.URLFor('api.group', group_id='<group_id>', _external=1),
        # 'collection': ma.URLFor('api.groups', _external=1)
    })


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        # fields = ('user_id', 'first_name', 'last_name', 'email', 'user_memberships', 'mygroups', 'links')
    mygroups = fields.Method('get_group_count')
    links = ma.Hyperlinks({
        'self': ma.URLFor('api.user', user_id='<user_id>', _external=1),
        'collection': ma.URLFor('api.users', _external=1),
        'groups': ma.URLFor('api.mygroups', user_id='<user_id>', _external=True)
    })
    def get_group_count(self, obj):
        return len(obj.user_memberships)
    
