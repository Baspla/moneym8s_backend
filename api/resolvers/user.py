from ariadne import ObjectType
from graphql import GraphQLError

from api.models import LogEntry, Membership, Group


def user_groups(obj, info, **kwargs):
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    if info.context.get('userid') != obj.id:
        usergroupsquery = Group.query.filter(Group.id == Membership.group_id).filter(Membership.user_id == obj.id)
        contextgroupsquery = Group.query.filter(Group.id == Membership.group_id).filter(
            Membership.user_id == info.context.get('userid'))
        return usergroupsquery.intersect(contextgroupsquery).all()
    else:
        return Group.query.filter(Group.id == Membership.group_id).filter(Membership.user_id == obj.id).all()


def user_memberships(obj, info, **kwargs):
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    if info.context.get('userid') != obj.id:
        usermembershipsquery = Membership.query.filter(Membership.user_id == obj.id)
        contextmembershipsquery = Membership.query.filter(Membership.user_id == info.context.get('userid'))
        return usermembershipsquery.intersect(contextmembershipsquery).all()
    else:
        return Membership.query.filter(Membership.user_id == obj.id).all()


# Not complete
def user_logs(obj, info, **kwargs):
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    if info.context.get('userid') == obj.id:
        return LogEntry.query.filter(LogEntry.user_id == obj.id).all()





user = ObjectType("User")
user.set_field("memberships", lambda obj, info: Membership.query.filter_by(user_id=obj.id).all())
user.set_field("logs", lambda obj, info: LogEntry.query.filter_by(user_id=obj.id).all())
user.set_field("groups", user_groups)