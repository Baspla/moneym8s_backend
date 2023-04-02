from ariadne import ObjectType

from api.models import User, Group, LogEntry, TransactionSplit, Transaction

membership = ObjectType("Membership")
membership.set_field("user", lambda obj, info: User.query.get(obj.user_id))
membership.set_field("group", lambda obj, info: Group.query.get(obj.group_id))
membership.set_field("logs", lambda obj, info: LogEntry.query.filter_by(membership_id=obj.id).all())
membership.set_field("splits", lambda obj, info: TransactionSplit.query.filter_by(member_id=obj.id).all())
membership.set_field("paid_transactions", lambda obj, info: Transaction.query.filter_by(paid_by_id=obj.id).all())
membership.set_field("issued_transactions", lambda obj, info: Transaction.query.filter_by(issuer_id=obj.id).all())
membership.set_field("paid_transactions", lambda obj, info: Transaction.query.filter_by(paid_by_id=obj.id).all())