from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vespricetracker.enums.payment_method import PaymentMethod


@dataclass(frozen=True)
class AdDTO:
    merchant_name: str
    merchant_rating: float
    merchant_order_count: int
    min_trade_amount: float
    max_trade_amount: float
    pay_time_limit: int
    payment_methods: list[PaymentMethod]
    price: float

    def __str__(self) -> str:
        return (
            f"{self.price!s}VES -> {self.merchant_name} "
            f"({self.merchant_rating!s}%) {self.merchant_order_count!s} "
            f"orders. Methods: {[x.value for x in self.payment_methods]}"
            f"trade: {self.min_trade_amount} - {self.max_trade_amount}"
        )

    def __lt__(self, other: AdDTO) -> bool:
        if not isinstance(other, AdDTO):
            return NotImplemented

        # Normalize price (higher is better)
        price_min = min(self.price, other.price)
        price_max = max(self.price, other.price)
        if price_max == price_min:
            self_price = 0.5
            other_price = 0.5
        else:
            self_price = (self.price - price_min) / (price_max - price_min)
            other_price = (other.price - price_min) / (price_max - price_min)

        # Normalize merchant_rating (higher is better)
        rating_min = min(self.merchant_rating, other.merchant_rating)
        rating_max = max(self.merchant_rating, other.merchant_rating)
        if rating_max == rating_min:
            self_rating = 0.5
            other_rating = 0.5
        else:
            self_rating = (self.merchant_rating - rating_min) / (
                rating_max - rating_min
            )
            other_rating = (other.merchant_rating - rating_min) / (
                rating_max - rating_min
            )

        # Normalize merchant_order_count (higher is better)
        order_min = min(self.merchant_order_count, other.merchant_order_count)
        order_max = max(self.merchant_order_count, other.merchant_order_count)
        if order_max == order_min:
            self_order = 0.5
            other_order = 0.5
        else:
            self_order = (self.merchant_order_count - order_min) / (
                order_max - order_min
            )
            other_order = (other.merchant_order_count - order_min) / (
                order_max - order_min
            )

        # Composite score (sum of normalized values)
        self_score = self_price + self_rating + self_order
        other_score = other_price + other_rating + other_order

        # Calculate weighted composite scores
        self_score = (
            (0.6 * self_price) + (0.2 * self_rating) + (0.2 * self_order)
        )
        other_score = (
            (0.6 * other_price) + (0.2 * other_rating) + (0.2 * other_order)
        )

        return self_score < other_score

    def __gt__(self, other: AdDTO) -> bool:
        return other < self
