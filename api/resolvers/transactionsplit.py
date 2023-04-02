from ariadne import ObjectType

from api.models import Membership, Transaction, LogEntry

transaction_split = ObjectType("TransactionSplit")
transaction_split.set_field("member", lambda obj, info: Membership.query.get(obj.member_id))
transaction_split.set_field("transaction", lambda obj, info: Transaction.query.get(obj.transaction_id))
transaction_split.set_field("logs", lambda obj, info: LogEntry.query.filter_by(transaction_split_id=obj.id).all())
