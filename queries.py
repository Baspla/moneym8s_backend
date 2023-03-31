from os import environ

from ariadne import ObjectType, SchemaDirectiveVisitor
from graphql import default_field_resolver, GraphQLError, GraphQLObjectType

from config import DEBUG
from models import User, LogEntry, Group, Membership, Transaction, TransactionSplit


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


def query_membership(obj, info, id, **kwargs):
    mem = Membership.query.get(id)
    if mem is None:
        return None
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    elif info.context.get('userid') == mem.user_id:
        return mem


def query_user(obj, info, id, **kwargs):
    user = User.query.get(id)
    if user is None:
        return None
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    else:
        # Prüft ob eine Gruppe existiert, in der der angemeldete Benutzer Mitglied ist und der Benutzer mit der ID ist.
        groups = Group.query.filter(Group.id == Membership.group_id) \
            .filter(Membership.user_id == info.context.get('userid')).all()
        for group in groups:
            if Membership.query.filter(Membership.group_id == group.id) \
                    .filter(Membership.user_id == user.id).first() \
                    is not None:
                return user


def query_group(obj, info, id, **kwargs):
    group = Group.query.get(id)
    if group is None:
        return None
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    elif Membership.query.filter_by(group_id=group.id,
                                    user_id=info.context.get('userid')).first() is not None:
        return group


def query_transaction(obj, info, id, **kwargs):
    transaction = Transaction.query.get(id)
    if transaction is None:
        return None
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    elif Membership.query.filter_by(group_id=transaction.group_id,
                                    user_id=info.context.get('userid')).first() is not None:
        return transaction


def query_transaction_split(obj, info, id, **kwargs):
    transaction_split = TransactionSplit.query.get(id)
    if transaction_split is None:
        return None
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    elif Membership.query.filter_by(group_id=transaction_split.transaction.group_id,
                                    user_id=info.context.get('userid')).first() is not None:
        return transaction_split


def query_groups(obj, info, **kwargs):
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    return Group.query.filter(Membership.group_id == Group.id).filter(
        Membership.user_id == info.context.get('userid')).all()


def query_users(obj, info, **kwargs):
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    return User.query.filter(User.id == info.context.get('userid')).all()


def query_transactions(obj, info, **kwargs):
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    return Transaction.query.filter(Transaction.group_id == Membership.group_id).filter(
        Membership.user_id == info.context.get('userid')).all()



def query_transaction_splits(obj, info, **kwargs):
    if info.context.get('userid') is None:
        raise GraphQLError("Not logged in")
    return TransactionSplit.query.filter(TransactionSplit.transaction_id == Transaction.id).filter(
        Transaction.group_id == Membership.group_id).filter(Membership.user_id == info.context.get('userid')).all()


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


query = ObjectType("Query")
query.set_field("users", query_users)
query.set_field("groups", query_groups)
query.set_field("memberships", lambda obj, info: Membership.query.filter_by(user_id=info.context.get('userid')).all())
query.set_field("transactions", query_transactions)
query.set_field("transactionSplits", query_transaction_splits)
query.set_field("logEntries", lambda obj, info: LogEntry.query.all())

query.set_field("user", query_user)
query.set_field("group", query_group)
query.set_field("membership", query_membership)
query.set_field("transaction", query_transaction)
query.set_field("transactionSplit", query_transaction_split)
query.set_field("logEntry", lambda obj, info, id: LogEntry.query.get(id))

user = ObjectType("User")
user.set_field("memberships", lambda obj, info: Membership.query.filter_by(user_id=obj.id).all())
user.set_field("logs", lambda obj, info: LogEntry.query.filter_by(user_id=obj.id).all())
user.set_field("groups", user_groups)

group = ObjectType("Group")
group.set_field("memberships", lambda obj, info: Membership.query.filter_by(group_id=obj.id).all())
group.set_field("transactions", lambda obj, info: Transaction.query.filter_by(group_id=obj.id).all())
group.set_field("logs", lambda obj, info: LogEntry.query.filter_by(group_id=obj.id).all())

membership = ObjectType("Membership")
membership.set_field("user", lambda obj, info: User.query.get(obj.user_id))
membership.set_field("group", lambda obj, info: Group.query.get(obj.group_id))
membership.set_field("logs", lambda obj, info: LogEntry.query.filter_by(membership_id=obj.id).all())
membership.set_field("splits", lambda obj, info: TransactionSplit.query.filter_by(member_id=obj.id).all())
membership.set_field("paidTransactions", lambda obj, info: Transaction.query.filter_by(paid_by_id=obj.id).all())
membership.set_field("transactions",
                     lambda obj, info: Transaction.query.filter(TransactionSplit.member_id == obj.id).all())

transaction = ObjectType("Transaction")
transaction.set_field("issuer", lambda obj, info: Membership.query.get(obj.issuer_id))
transaction.set_field("paidBy", lambda obj, info: Membership.query.get(obj.paid_by_id))
transaction.set_field("splits", lambda obj, info: TransactionSplit.query.filter_by(transaction_id=obj.id).all())
transaction.set_field("logs", lambda obj, info: LogEntry.query.filter_by(transaction_id=obj.id).all())

transaction_split = ObjectType("TransactionSplit")
transaction_split.set_field("member", lambda obj, info: Membership.query.get(obj.member_id))
transaction_split.set_field("transaction", lambda obj, info: Transaction.query.get(obj.transaction_id))
transaction_split.set_field("logs", lambda obj, info: LogEntry.query.filter_by(transaction_split_id=obj.id).all())

log_entry = ObjectType("LogEntry")
log_entry.set_field("user", lambda obj, info: User.query.get(obj.user_id))
log_entry.set_field("group", lambda obj, info: Group.query.get(obj.group_id))
log_entry.set_field("membership", lambda obj, info: Membership.query.get(obj.membership_id))
log_entry.set_field("transaction", lambda obj, info: Transaction.query.get(obj.transaction_id))
log_entry.set_field("transactionSplit", lambda obj, info: TransactionSplit.query.get(obj.transaction_split_id))
