from os import environ

from ariadne import ObjectType, SchemaDirectiveVisitor
from graphql import default_field_resolver

from config import DEBUG


class DebugDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        if not DEBUG:
            field.resolve = default_field_resolver


"""
class PrivateDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve or default_field_resolver

        if object_type.name == "User":
            def user_resolver(obj, info, **kwargs):
                print(obj)
                if info.context.get('userid') is None:
                    raise GraphQLError("Not logged in")
                elif info.context.get('userid') == obj.id:
                    return original_resolver(obj, info, **kwargs)
                else:
                    raise GraphQLError("Not authorized")

            field.resolve = user_resolver

# Query all users that are in a group that the logged in user is in
def getRelatedUsers(userid, include_self=False):
    uquery = User.query.join(Membership, Membership.user_id == User.id) \
        .filter(Membership.group_id == Membership.query.filter(User.id==userid).first().group_id)
    if not include_self:
        uquery = uquery.filter(User.id != userid)
    return uquery
"""
