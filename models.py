from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy_utils.types import ChoiceType

class User(Base):
    """Represent a User.
    
    Attributes:
        id (int): The user id
        username (str): The username.
        email (str): The user email.
        password (str): The user password.
        is_active (bool): Check if user is active
        is_staff (bool): The user role
    """
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)


    def __repr__(self):
        return f"<User {self.username}>"


class Order(Base):
    """Represent an orders.
    
    Attributes:
        id (int): The order id
        quantity (int): The order quantity.
        order_status (str): The order status.
        catfish_size (str): The catfish size
        user_id (int): The user id
    """

    ORDER_STATUES=(
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered')
    )

    CATFISH_SIZES = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large')
    )
    __tablename__='orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUES), default=PENDING)
    catfish_size = Column(ChoiceType(choices=CATFISH_SIZES), default=SMALL)
    user_id = Column(Integer, ForeignKey('user.id'))


