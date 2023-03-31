from sqlalchemy import ForeignKey, Integer, Float, DateTime, String, Boolean
from sqlalchemy.orm import mapped_column, relationship

from database import db


class User(db.Model):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(64), unique=True, index=True)
    guard_id = mapped_column(Integer, unique=True, index=True)
    created_at = mapped_column(DateTime, default=db.func.now())
    memberships = relationship('Membership', back_populates='user', lazy='dynamic', foreign_keys='Membership.user_id')
    log_entries = relationship('LogEntry', back_populates='user', foreign_keys='LogEntry.user_id')

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, guard_id):
        self.username = username
        self.guard_id = guard_id


class Group(db.Model):
    __tablename__ = 'groups'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(64), unique=True, index=True)
    is_personal = mapped_column(Boolean, default=False)
    invite_code = mapped_column(String(64), unique=True, index=True)
    created_at = mapped_column(DateTime, default=db.func.now())
    members = relationship('Membership', back_populates='group', lazy='dynamic', foreign_keys='Membership.group_id')
    transactions = relationship('Transaction', back_populates='group', lazy='dynamic', foreign_keys='Transaction.group_id')
    log_entries = relationship('LogEntry', back_populates='group',lazy='dynamic', foreign_keys='LogEntry.group_id')

    def __repr__(self):
        return '<Group %r>' % self.name

    def __init__(self, name):
        self.name = name


class Membership(db.Model):
    __tablename__ = 'memberships'
    id = mapped_column(Integer, primary_key=True)
    is_admin = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=db.func.now())
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    group_id = mapped_column(Integer, ForeignKey('groups.id'))
    user = relationship('User', back_populates='memberships', foreign_keys='Membership.user_id')
    group = relationship('Group', back_populates='members', foreign_keys='Membership.group_id')
    issued_transactions = relationship('Transaction', back_populates='issuer', lazy='dynamic', foreign_keys='Transaction.issuer_id')
    paid_transactions = relationship('Transaction', back_populates='paid_by', lazy='dynamic', foreign_keys='Transaction.paid_by_id')
    splits = relationship('TransactionSplit', back_populates='member', lazy='dynamic', foreign_keys='TransactionSplit.member_id')
    log_entries = relationship('LogEntry', back_populates='membership', lazy='dynamic', foreign_keys='LogEntry.membership_id')

    def __repr__(self):
        return '<Membership %r>' % self.id

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = mapped_column(Integer, primary_key=True)
    group_id = mapped_column(ForeignKey('groups.id'))
    description = mapped_column(String(128))
    amount = mapped_column(Float)
    issuer_id = mapped_column(Integer, ForeignKey('memberships.id'))
    paid_by_id = mapped_column(Integer, ForeignKey('memberships.id'))
    created_at = mapped_column(DateTime, default=db.func.now())
    group = relationship('Group', back_populates='transactions', foreign_keys='Transaction.group_id')
    issuer = relationship('Membership', back_populates='issued_transactions', foreign_keys='Transaction.issuer_id')
    paid_by = relationship('Membership', back_populates='paid_transactions', foreign_keys='Transaction.paid_by_id')
    splits = relationship('TransactionSplit', back_populates='transaction', lazy='dynamic', foreign_keys='TransactionSplit.transaction_id')
    log_entries = relationship('LogEntry', back_populates='transaction', foreign_keys='LogEntry.transaction_id')

    def __repr__(self):
        return '<Transaction %r>' % self.id

    def __init__(self, group_id, description, amount, issuer_id, paid_by_id):
        self.group_id = group_id
        self.description = description
        self.amount = amount
        self.issuer_id = issuer_id
        self.paid_by_id = paid_by_id


class TransactionSplit(db.Model):
    __tablename__ = 'transaction_splits'
    id = mapped_column(Integer, primary_key=True)
    transaction_id = mapped_column(Integer, ForeignKey('transactions.id'))
    member_id = mapped_column(Integer, ForeignKey('memberships.id'))
    amount = mapped_column(Float)
    created_at = mapped_column(DateTime, default=db.func.now())
    transaction = relationship('Transaction', back_populates='splits', foreign_keys='TransactionSplit.transaction_id')
    member = relationship('Membership', back_populates='splits', foreign_keys='TransactionSplit.member_id')
    log_entries = relationship('LogEntry', back_populates='transaction_split', lazy='dynamic', foreign_keys='LogEntry.transaction_split_id')

    def __repr__(self):
        return '<TransactionSplit %r>' % self.id

    def __init__(self, transaction_id, member_id, amount):
        self.transaction_id = transaction_id
        self.member_id = member_id
        self.amount = amount


class LogEntry(db.Model):
    __tablename__ = 'log_entries'
    id = mapped_column(Integer, primary_key=True)
    description = mapped_column(String(256))
    created_at = mapped_column(DateTime, default=db.func.now())
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='log_entries')
    group_id = mapped_column(Integer, ForeignKey('groups.id'))
    group = relationship('Group', back_populates='log_entries')
    membership_id = mapped_column(Integer, ForeignKey('memberships.id'))
    membership = relationship('Membership', back_populates='log_entries')
    transaction_id = mapped_column(Integer, ForeignKey('transactions.id'))
    transaction = relationship('Transaction', back_populates='log_entries')
    transaction_split_id = mapped_column(Integer, ForeignKey('transaction_splits.id'))
    transaction_split = relationship('TransactionSplit', back_populates='log_entries')

    def __repr__(self):
        return '<LogEntry %r>' % self.id

    def __init__(self, description, user=None, group=None, membership=None, transaction=None, transaction_split=None):
        self.description = description
        self.user = user
        self.group = group
        self.membership = membership
        self.transaction = transaction
        self.transaction_split = transaction_split