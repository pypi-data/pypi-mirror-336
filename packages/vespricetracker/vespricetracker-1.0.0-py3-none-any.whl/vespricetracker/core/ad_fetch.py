from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING

import requests

from vespricetracker.core.ad_filter import AdFilter
from vespricetracker.core.ad_serializer import AdSerializer
from vespricetracker.util.vespricetracker_logger import VespricetrackerLogger

if TYPE_CHECKING:
    from vespricetracker.dto.ad_dto import AdDTO
    from vespricetracker.dto.ad_request_dto import AdRequestDTO


class AdFetch:
    def __init__(self, ad_request_dto: AdRequestDTO) -> None:
        self.url = ad_request_dto.url
        self.payload = ad_request_dto.payload
        self.headers = ad_request_dto.headers
        self.filter = AdFilter(
            ad_request_dto.expected_merchant_rating,
            ad_request_dto.expected_merchant_order_count,
            ad_request_dto.expected_merchant_min_trade_amount,
            ad_request_dto.expected_merchant_max_trade_amount,
            ad_request_dto.expected_pay_time_limit,
        )

    def get(self) -> list[AdDTO]:
        filtered = []
        total = -1
        page = 0
        while total != 0:
            page = page + 1
            time.sleep(random.randrange(4, 8))  # noqa: S311
            self.payload["page"] = page + 1
            response = requests.post(
                self.url, json=self.payload, headers=self.headers, timeout=10
            )
            data = response.json()

            total = data.get("total", 0)

            for ad in data["data"]:
                ad_dto = AdSerializer.to_addto(ad)

                if self.filter.is_valid(ad_dto):
                    filtered.append(ad_dto)

        description = f"Received {len(filtered)} filtered Binance ads"
        VespricetrackerLogger.get_console_logger().info(description)

        return sorted(filtered, reverse=True)
