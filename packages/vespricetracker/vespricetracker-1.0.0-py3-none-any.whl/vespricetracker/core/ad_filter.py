from vespricetracker.dto.ad_dto import AdDTO
from vespricetracker.enums.payment_method import PaymentMethod


class AdFilter:
    def __init__(
        self,
        expected_merchant_rating: float,
        expected_merchant_order_count: int,
        expected_min_trade_amount: float,
        expected_max_trade_amount: float,
        expected_pay_time_limit: int,
    ) -> None:
        self.expected_merchant_rating = expected_merchant_rating
        self.expected_merchant_order_count = expected_merchant_order_count
        self.expected_min_trade_amount = expected_min_trade_amount
        self.expected_max_trade_amount = expected_max_trade_amount
        self.expected_pay_time_limit = expected_pay_time_limit

    def is_valid(self, ad: AdDTO) -> bool:
        merchant_rating_match = (
            ad.merchant_rating >= self.expected_merchant_rating
        )

        merchant_oder_count_match = (
            ad.merchant_order_count >= self.expected_merchant_order_count
        )

        min_trade_amount_match = (
            ad.min_trade_amount <= self.expected_min_trade_amount
        )

        max_trade_amount_match = (
            ad.max_trade_amount >= self.expected_max_trade_amount
        )

        pay_time_limit_match = (
            ad.pay_time_limit <= self.expected_pay_time_limit
        )

        return (
            PaymentMethod.is_universal_payment(ad.payment_methods)
            and merchant_rating_match
            and merchant_oder_count_match
            and min_trade_amount_match
            and max_trade_amount_match
            and pay_time_limit_match
        )
