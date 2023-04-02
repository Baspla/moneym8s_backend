from ariadne import ObjectType

from api.models import User, Group, Membership, Transaction, TransactionSplit

log_entry = ObjectType("LogEntry")
log_entry.set_field("user", lambda obj, info: User.query.get(obj.user_id))
log_entry.set_field("group", lambda obj, info: Group.query.get(obj.group_id))
log_entry.set_field("membership", lambda obj, info: Membership.query.get(obj.membership_id))
log_entry.set_field("transaction", lambda obj, info: Transaction.query.get(obj.transaction_id))
log_entry.set_field("transaction_split", lambda obj, info: TransactionSplit.query.get(obj.transaction_split_id))