from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DECIMAL, INTEGER, TIMESTAMP
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date

'''TRIAL IMAGE'''


class TrialImage(Base):
    __tablename__ = "trial_image"

    id = Column(String, primary_key=True, nullable=False)
    image_path = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


'''TOKENS'''


class Tokens(Base):
    __tablename__ = "tokens"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    access_token = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship("Users")


'''OTP'''


class OTP(Base):
    __tablename__ = "otp"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    otp = Column(String(6), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship("Users")


'''USER'''


class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    number = Column(String(10), nullable=False)
    password = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


'''USER PAYEMENT'''


class UserPayments(Base):
    __tablename__ = "user_payments"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    payment_type = Column(String, nullable=False)
    expiry = Column(Date,
                    nullable=False, server_default=text("now()"))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship("Users")


'''USER ADDRESS'''


class UserAddress(Base):
    __tablename__ = "user_address"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    pin_code = Column(Integer, nullable=False)
    mobile = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship("Users")


'''UPLOAD IMAGE'''


class UploadImage(Base):
    __tablename__ = "upload_image"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    image_path = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship("Users")


'''PAYMENT DETAILS'''


class PaymentDetails(Base):
    __tablename__ = "payment_details"

    id = Column(String, primary_key=True, nullable=False)
    amount = Column(DECIMAL, nullable=False)
    status = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


'''ORDER DETAILS'''


class OrderDetails(Base):
    __tablename__ = "order_details"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    payment_id = Column(
        String, ForeignKey("payment_details.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    total = Column(DECIMAL, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship("Users")
    payment_details = relationship("PaymentDetails")


'''PRODUCT CATEGORY'''


class ProductCategory(Base):
    __tablename__ = "product_category"

    id = Column(String, primary_key=True, nullable=False)
    category_name = Column(String, nullable=False)
    category_desc = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


'''PRODUCT INVENTORY'''


class ProductInventory(Base):
    __tablename__ = "product_inventory"

    id = Column(String, primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


'''PRODUCTS'''


class Products(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, nullable=False)
    inventory_id = Column(
        String, ForeignKey("product_inventory.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    category_id = Column(
        String, ForeignKey("product_category.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    product_name = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    product_image = Column(String, nullable=False)
    product_desc = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    product_inventory = relationship("ProductInventory")
    product_category = relationship('ProductCategory')


'''PRODUCT IMAGE'''


class ProductImage(Base):
    __tablename__ = "product_image"

    id = Column(String, primary_key=True, nullable=False)
    product_id = Column(
        String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    inventory_id = Column(
        String, ForeignKey("products.inventory_id", ondelete="CASCADE"), nullable=False, unique=True
    )
    category_id = Column(
        String, ForeignKey("products.category_id", ondelete="CASCADE"), nullable=False, unique=True
    )
    image_path = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    products = relationship("Products", foreign_keys=[
                            product_id])
    inventory = relationship("Products", foreign_keys=[
        inventory_id])
    category = relationship("Products", foreign_keys=[
        category_id])


'''ORDER ITEMS'''


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True, nullable=False)
    product_id = Column(
        String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    inventory_id = Column(
        String, ForeignKey("products.inventory_id", ondelete="CASCADE"), nullable=False, unique=True
    )
    category_id = Column(
        String, ForeignKey("products.category_id", ondelete="CASCADE"), nullable=False, unique=True
    )
    order_id = Column(
        String, ForeignKey("order_details.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    payment_id = Column(
        String, ForeignKey("payment_details.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    quantity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship("Users")
    payment_details = relationship("PaymentDetails")
    products = relationship("Products", foreign_keys=[
                            product_id])
    inventory = relationship("Products", foreign_keys=[
        inventory_id])
    category = relationship("Products", foreign_keys=[
        category_id])
    order_details = relationship('OrderDetails')


'''CART'''


class Cart(Base):
    __tablename__ = "cart"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    product_id = Column(
        String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    inventory_id = Column(
        String, ForeignKey("products.inventory_id", ondelete="CASCADE"), nullable=False, unique=True
    )
    category_id = Column(
        String, ForeignKey("products.category_id", ondelete="CASCADE"), nullable=False, unique=True
    )
    quantity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship("Users")
    products = relationship("Products", foreign_keys=[
                            product_id])
    inventory = relationship("Products", foreign_keys=[
        inventory_id])
    category = relationship("Products", foreign_keys=[
        category_id])
