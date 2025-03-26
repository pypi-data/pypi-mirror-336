from dataclasses import dataclass


@dataclass(frozen=True)
class AdRequestDTO:
    url: str
    payload: dict
    headers: dict
    expected_merchant_rating: float
    expected_merchant_order_count: int
    expected_merchant_min_trade_amount: float
    expected_merchant_max_trade_amount: float
    expected_pay_time_limit: int
