from ariadne import ObjectType

"""
    createGroup(name: String!, is_personal: Boolean!, invite_code: String!): Group
    createMembership(user_id: ID!, group_id: ID!, is_admin: Boolean!): Membership
    createTransaction(group_id: ID!, description: String!, total: Float!, issuer_id: ID!, paid_by_id: ID!): Transaction
    createTransactionSplit(transaction_id: ID!, member_id: ID!, amount: Float!): TransactionSplit
    updateUser(id: ID!, username: String, guard_id: String): User
    updateGroup(id: ID!, name: String, is_personal: Boolean, invite_code: String): Group
    updateMembership(id: ID!, user_id: ID, group_id: ID, is_admin: Boolean): Membership
    updateTransaction(id: ID!, group_id: ID, description: String, total: Float, issuer_id: ID, paid_by_id: ID): Transaction
    updateTransactionSplit(id: ID!, transaction_id: ID, member_id: ID, amount: Float): TransactionSplit
    deleteUser(id: ID!): User
    deleteGroup(id: ID!): Group
    deleteMembership(id: ID!): Membership
    deleteTransaction(id: ID!): Transaction
    deleteTransactionSplit(id: ID!): TransactionSplit
"""


def create_group(obj, info, name, is_personal, invite_code):
    print("create_group")
    pass


def create_membership(obj, info, user_id, group_id, is_admin):
    print("create_membership")
    pass


def create_transaction(obj, info, group_id, description, total, issuer_id, paid_by_id):
    print("create_transaction")
    pass


def create_transaction_split(obj, info, transaction_id, member_id, amount):
    print("create_transaction_split")
    pass


def update_user(obj, info, id, username, guard_id):
    print("update_user")
    pass


def update_group(obj, info, id, name, is_personal, invite_code):
    print("update_group")
    pass


def update_membership(obj, info, id, user_id, group_id, is_admin):
    print("update_membership")
    pass


def update_transaction(obj, info, id, group_id, description, total, issuer_id, paid_by_id):
    print("update_transaction")
    pass


def update_transaction_split(obj, info, id, transaction_id, member_id, amount):
    print("update_transaction_split")
    pass


def delete_user(obj, info, id):
    print("delete_user")
    pass


def delete_group(obj, info, id):
    print("delete_group")
    pass


def delete_membership(obj, info, id):
    print("delete_membership")
    pass


def delete_transaction(obj, info, id):
    print("delete_transaction")
    pass


def delete_transaction_split(obj, info, id):
    print("delete_transaction_split")
    pass


mutation = ObjectType("Mutation")
mutation.set_field("createGroup", create_group)
mutation.set_field("createMembership", create_membership)
mutation.set_field("createTransaction", create_transaction)
mutation.set_field("createTransactionSplit", create_transaction_split)
mutation.set_field("updateUser", update_user)
mutation.set_field("updateGroup", update_group)
mutation.set_field("updateMembership", update_membership)
mutation.set_field("updateTransaction", update_transaction)
mutation.set_field("updateTransactionSplit", update_transaction_split)
mutation.set_field("deleteUser", delete_user)
mutation.set_field("deleteGroup", delete_group)
mutation.set_field("deleteMembership", delete_membership)
mutation.set_field("deleteTransaction", delete_transaction)
mutation.set_field("deleteTransactionSplit", delete_transaction_split)
