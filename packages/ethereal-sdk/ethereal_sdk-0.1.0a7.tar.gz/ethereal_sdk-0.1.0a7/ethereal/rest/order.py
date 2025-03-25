import time
from typing import List, Optional, Union

from ethereal.constants import API_PREFIX
from ethereal.rest.util import generate_nonce, uuid_to_bytes32
from ethereal.models.rest import (
    OrderDto,
    OrderDryRunDto,
    ListOfOrderDtos,
    ListOfOrderFillDtos,
    ListOfTradeDtos,
    SubmitOrderDto,
    SubmitDryOrderDto,
    SubmitOrderLimitDtoData,
    SubmitOrderMarketDtoData,
    CancelOrderDto,
    CancelOrderDtoData,
    CancelOrderResultDto,
    V1OrderGetParametersQuery,
    V1OrderFillGetParametersQuery,
    V1OrderTradeGetParametersQuery,
)


def list_orders(self, **kwargs) -> ListOfOrderDtos:
    """Lists orders for a subaccount.

    Endpoint: GET v1/order

    Returns:
        ListOfOrderDtos: List of order information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/order",
        request_model=V1OrderGetParametersQuery,
        response_model=ListOfOrderDtos,
        **kwargs,
    )
    return res.data


def list_fills(
    self,
    **kwargs,
) -> ListOfOrderFillDtos:
    """Lists order fills.

    Endpoint: GET v1/order/fill

    Returns:
        ListOfOrderFillDtos: List of order fill information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/order/fill",
        request_model=V1OrderFillGetParametersQuery,
        response_model=ListOfOrderFillDtos,
        **kwargs,
    )
    return res.data


def list_trades(
    self,
    **kwargs,
) -> ListOfTradeDtos:
    """Lists order trades.

    Endpoint: GET v1/order/trade

    Args:
        productId (str, optional): UUID of the product.

    Returns:
        ListOfTradeDtos: List of trade information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/order/trade",
        request_model=V1OrderTradeGetParametersQuery,
        response_model=ListOfTradeDtos,
        **kwargs,
    )
    return res.data


def get_order(self, id: str, **kwargs) -> OrderDto:
    """Gets a specific order by ID.

    Endpoint: GET v1/order/{id}

    Args:
        id (str): UUID of the order.

    Returns:
        OrderDto: Order information.
    """
    endpoint = f"{API_PREFIX}/order/{id}"
    response = self.get(endpoint, **kwargs)
    return OrderDto(**response)


def submit_order(
    self,
    sender: str,
    price: str,
    quantity: str,
    side: int,
    subaccount: str,
    onchainId: float,
    orderType: str,
    timeInForce: Optional[str] = None,
    postOnly: Optional[bool] = False,
    reduceOnly: Optional[bool] = False,
    dryrun: Optional[bool] = False,
    **kwargs,
) -> Union[OrderDto, OrderDryRunDto]:
    """Submits a new order.

    Endpoint: POST v1/order/submit

    Args:
        sender (str): Address of the sender.
        price (str): Order price.
        quantity (str): Order quantity.
        side (Side): Order side (BUY/SELL).
        subaccount (str): Subaccount address.
        onchainId (float): On-chain product ID.
        orderType (str): Type of order (LIMIT/MARKET).
        timeInForce (str, optional): Time in force for limit orders.
        postOnly (bool, optional): Post-only flag for limit orders.
        reduceOnly (bool, optional): Reduce-only flag.
        dryrun (bool, optional): Dry-run flag.

    Returns:
        OrderDto: Created order information.
    """
    domain = self.rpc_config.domain.model_dump(mode="json")
    primary_type = "TradeOrder"
    types = self.chain.get_signature_types(self.rpc_config, primary_type)

    signedAt = str(int(time.time()))
    nonce = generate_nonce()

    # Common order data
    order_data = {
        "sender": sender,
        "subaccount": subaccount,
        "quantity": quantity,
        "price": price,
        "side": side,
        "engineType": 0,  # PERP
        "onchainId": onchainId,
        "nonce": nonce,
        "type": orderType,
        "reduceOnly": reduceOnly,
        "signedAt": signedAt,
    }

    message = {
        "sender": sender,
        "subaccount": subaccount,
        "quantity": int(float(quantity) * 1e9),
        "price": int(float(price) * 1e9),
        "reduceOnly": reduceOnly,
        "side": side,
        "engineType": 0,
        "productId": int(onchainId),
        "nonce": nonce,
        "signedAt": signedAt,
    }

    # Create specific order data based on type
    if orderType == "LIMIT":
        order_data.update(
            {
                "timeInForce": timeInForce,
                "postOnly": postOnly,
            }
        )
        data_model: Union[SubmitOrderLimitDtoData, SubmitOrderMarketDtoData] = (
            SubmitOrderLimitDtoData.model_validate(order_data)
        )
    elif orderType == "MARKET":
        data_model = SubmitOrderMarketDtoData.model_validate(order_data)
    else:
        raise ValueError(f"Invalid order type: {orderType}")

    if dryrun:
        submit_order_dry = SubmitDryOrderDto(data=data_model)

        endpoint = f"{API_PREFIX}/order/dry-run"
        res = self.post(
            endpoint, data=submit_order_dry.model_dump(mode="json"), **kwargs
        )
        return OrderDryRunDto.model_validate(res)
    else:
        # Prepare signature
        signature = self.chain.sign_message(
            self.chain.private_key, domain, types, primary_type, message
        )
        submit_order = SubmitOrderDto(data=data_model, signature=signature)

        endpoint = f"{API_PREFIX}/order/submit"
        res = self.post(endpoint, data=submit_order.model_dump(mode="json"), **kwargs)
        return OrderDto(**res)


def cancel_order(
    self, orderId: str, sender: str, subaccount: str, **kwargs
) -> List[CancelOrderResultDto]:
    """Cancels an existing order.

    Endpoint: POST v1/order/cancel

    Args:
        orderId (str): UUID of the order to cancel.
        sender (str): Address of the sender.
        subaccount (str): Subaccount address.

    Returns:
        List[OrderDto]: List of canceled orders.
    """
    endpoint = f"{API_PREFIX}/order/cancel"

    domain = self.rpc_config.domain.model_dump(mode="json")
    primary_type = "CancelOrder"
    types = self.chain.get_signature_types(self.rpc_config, primary_type)

    nonce = generate_nonce()

    data = CancelOrderDtoData(
        sender=sender, subaccount=subaccount, nonce=nonce, orderIds=[orderId]
    )

    # Prepare message for signing
    message = data.model_dump(mode="json")
    message["orderIds"] = [uuid_to_bytes32(orderId)]

    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )

    cancel_order = CancelOrderDto(data=data, signature=signature)

    response = self.post(endpoint, data=cancel_order.model_dump(mode="json"), **kwargs)
    return [CancelOrderResultDto(**o) for o in response.get("data", [])]
