from ariadne import ObjectType

from api.models import Membership, TransactionSplit, LogEntry

transaction = ObjectType("Transaction")
transaction.set_field("issuer", lambda obj, info: Membership.query.get(obj.issuer_id))
transaction.set_field("paid_by", lambda obj, info: Membership.query.get(obj.paid_by_id))
transaction.set_field("splits", lambda obj, info: TransactionSplit.query.filter_by(transaction_id=obj.id).all())
transaction.set_field("logs", lambda obj, info: LogEntry.query.filter_by(transaction_id=obj.id).all())