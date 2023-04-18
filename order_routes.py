from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder

# Specify route URL
order_router=APIRouter(
    prefix='/orders',
    tags=['orders']
)

session = Session(bind=engine)

@order_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    """
        ## A sample hello world endpoint
        This returns Hello World
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaid Token"
        )
    return {"message":"Hello World 2"}


@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order:OrderModel, Authorize:AuthJWT=Depends()):
    """
        ## Placing an order endpoint
        This requires the following fields:
        - quantity (int): The order quantity.
        - catfish_size (str): The catfish size.
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username==current_user).first()

    new_order = Order(
        catfish_size = order.catfish_size,
        quantity = order.quantity
    )

    new_order.user=user
    session.add(new_order)
    session.commit()

    response = {
        "catfish_size": new_order.catfish_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)


@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends()):
    """
        ## List all orders endpoint
        This lists all orders made. Can only be access by superusers
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaid Token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()

        return jsonable_encoder(orders)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )


@order_router.get('/orders/{id}')
async def get_order_by_id(id:int, Authorize:AuthJWT=Depends()):
    """
        ## Get order by ID for superuser endpoint
        This gets an order by ID. Can only be access by superusers
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaid Token"
        )
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not allowed to perform this request"
        )



@order_router.get('/user/orders')
async def get_user_orders(Authorize:AuthJWT=Depends()):
    """
        ## Get current user orders endpoint
        This lists the orders made by the currently logged in users
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaid Token"
        )
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.orders)


@order_router.get('/user/order/{id}/')
async def get_specific_order(id:int, Authorize:AuthJWT=Depends()):
    """
        ## Get user's specific order endpoint
        This returns an order by ID for the currently logged in users
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaid Token"
        )
    
    subject = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username==subject).first()
    orders = current_user.orders

    for ord in orders:
        if ord.id == id:
            return jsonable_encoder(ord)
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="No order with such id"
    )


@order_router.put('/order/update/{id}/')
async def update_order(id:int, order:OrderModel, Authorize:AuthJWT=Depends()):
    """
        ## Update an order endpoint
        This updates an order and requires the following fields:
        - quantity (int): The order quantity.
        - catfish_size (str): The catfish size.
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaid Token"
        )
    
    order_to_update = session.query(Order).filter(Order.id==id).first()
    order_to_update.quantity=order.quantity
    order_to_update.catfish_size=order.catfish_size

    session.commit()

    response = {
                "id": order_to_update.id,
                "quantity": order_to_update.quantity,
                "catfist_size": order_to_update.catfish_size,
                "order_status": order_to_update.order_status,
            }

    return jsonable_encoder(order_to_update)


@order_router.patch('/order/update/{id}/')
async def update_order_status(id:int, order:OrderStatusModel, Authorize:AuthJWT=Depends()):
    """
        ## Update an order status for superuser endpoint
        This updates an order status and requires the following field:
        - order_status (str): The order status.
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaid Token"
        )
    
    username = Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==username).first()

    if current_user.is_staff:
        order_to_update = session.query(Order).filter(Order.id==id).first()
        order_to_update.order_status=order.order_status
        
        session.commit()

        response = {
                "id": order_to_update.id,
                "quantity": order_to_update.quantity,
                "catfist_size": order_to_update.catfish_size,
                "order_status": order_to_update.order_status,
            }

        return jsonable_encoder(response)


@order_router.delete('/order/delete/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id:int, Authorize:AuthJWT=Depends()):
    """
        ## Delete an order endpoint
        This deletes an order by its ID
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaid Token"
        )
    
    order_to_delete = session.query(Order).filter(Order.id==id).first()
    
    session.delete(order_to_delete)
    session.commit()

    return order_to_delete