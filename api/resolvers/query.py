from ariadne import ObjectType
from graphql import GraphQLError

from api.models import Membership, LogEntry, User, Group, Transaction, TransactionSplit


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
