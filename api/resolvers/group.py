from ariadne import ObjectType

from api.models import Membership, Transaction, LogEntry

group = ObjectType("Group")
group.set_field("members", lambda obj, info: Membership.query.filter_by(group_id=obj.id).all())
group.set_field("transactions", lambda obj, info: Transaction.query.filter_by(group_id=obj.id).all())
group.set_field("logs", lambda obj, info: LogEntry.query.filter_by(group_id=obj.id).all())