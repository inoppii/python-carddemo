from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "users"
    usr_id = Column(String(20), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    hashed_password = Column(String(255))
    usr_type = Column(String(1))  # 'A': Admin, 'R': Regular
    created_at = Column(DateTime, default=datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"
    cust_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    address_line_1 = Column(String(100))
    address_line_2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(20))
    zip_code = Column(String(10))
    phone_1 = Column(String(15))
    phone_2 = Column(String(15))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    accounts = relationship("Account", back_populates="customer")

class Account(Base):
    __tablename__ = "accounts"
    acct_id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey("customers.cust_id"))
    acct_balance = Column(Numeric(15, 2), default=0.0)
    acct_status = Column(String(1)) # 'A': Active, 'I': Inactive
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="accounts")
    card_xref = relationship("CardXref", back_populates="account")

class CardXref(Base):
    __tablename__ = "card_xref"
    card_num = Column(String(16), primary_key=True)
    acct_id = Column(Integer, ForeignKey("accounts.acct_id"))
    
    account = relationship("Account", back_populates="card_xref")

class TransactionType(Base):
    __tablename__ = "transaction_types"
    trn_type_cd = Column(String(2), primary_key=True)
    trn_type_desc = Column(String(50))

class TransactionCategory(Base):
    __tablename__ = "transaction_categories"
    trn_type_cd = Column(String(2), ForeignKey("transaction_types.trn_type_cd"), primary_key=True)
    trn_cat_cd = Column(Integer, primary_key=True)
    trn_cat_desc = Column(String(50))

class Transaction(Base):
    __tablename__ = "transactions"
    trn_id = Column(Integer, primary_key=True, autoincrement=True)
    card_num = Column(String(16), ForeignKey("card_xref.card_num"))
    trn_type_cd = Column(String(2), ForeignKey("transaction_types.trn_type_cd"))
    trn_cat_cd = Column(Integer)
    trn_amount = Column(Numeric(15, 2))
    trn_desc = Column(String(100))
    merchant_id = Column(String(15))
    merchant_name = Column(String(50))
    merchant_city = Column(String(50))
    trn_timestamp = Column(DateTime, default=datetime.utcnow)

class CategoryBalance(Base):
    __tablename__ = "category_balances"
    acct_id = Column(Integer, ForeignKey("accounts.acct_id"), primary_key=True)
    type_cd = Column(String(2), primary_key=True)
    cat_cd = Column(Integer, primary_key=True)
    balance = Column(Numeric(15, 2), default=0.0)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuthSummary(Base):
    __tablename__ = "auth_summaries"
    acct_id = Column(Integer, ForeignKey("accounts.acct_id"), primary_key=True)
    total_auth_amount = Column(Numeric(15, 2), default=0.0)
    last_auth_timestamp = Column(DateTime)

class AuthDetail(Base):
    __tablename__ = "auth_details"
    auth_key = Column(String(50), primary_key=True)
    acct_id = Column(Integer, ForeignKey("accounts.acct_id"))
    card_num = Column(String(16))
    auth_amount = Column(Numeric(15, 2))
    auth_response_cd = Column(String(4))
    auth_timestamp = Column(DateTime, default=datetime.utcnow)
    merchant_id = Column(String(15))
    merchant_name = Column(String(50))
    fraud_flag = Column(String(1), default='N') # 'Y' or 'N'

class AuthFraud(Base):
    __tablename__ = "auth_frauds"
    fraud_id = Column(Integer, primary_key=True, autoincrement=True)
    auth_key = Column(String(50), ForeignKey("auth_details.auth_key"))
    reported_by = Column(String(20))
    reported_at = Column(DateTime, default=datetime.utcnow)
    fraud_status = Column(String(1)) # 'F': Reported, 'R': Resolved
