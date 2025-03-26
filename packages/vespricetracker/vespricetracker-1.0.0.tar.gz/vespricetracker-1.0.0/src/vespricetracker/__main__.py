from __future__ import annotations

import statistics
import sys

from requests.exceptions import Timeout

from vespricetracker.core.ad_fetch import AdFetch
from vespricetracker.core.bcv_fetch import BcvFecth
from vespricetracker.dto.ad_request_dto import AdRequestDTO
from vespricetracker.exception.bootstrap_error import BootstrapError
from vespricetracker.util.file_importer import FileImporter
from vespricetracker.util.vespricetracker_logger import VespricetrackerLogger


def main() -> tuple[float, float]:
    bootstrap_paths_dto = FileImporter.bootstrap()

    log_dir = bootstrap_paths_dto.log_dir

    log_config_file_path = (
        FileImporter.get_project_root()
        / "vespricetracker"
        / "config"
        / "log_config.yaml"
    )

    log_config = FileImporter.get_logging_config(log_config_file_path)

    VespricetrackerLogger(log_dir, log_config)

    binance_price = 0.00
    bcv_price = 0.00

    try:
        url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        payload = {
            "fiat": "VES",
            "rows": 20,
            "tradeType": "SELL",
            "asset": "USDT",
            "countries": [],
            "proMerchantAds": False,
            "shieldMerchantAds": False,
            "publisherType": "merchant",
            "payTypes": [],
        }
        headers = {"Content-Type": "application/json"}
        request = AdRequestDTO(
            url=url,
            payload=payload,
            headers=headers,
            expected_merchant_rating=97,
            expected_merchant_order_count=1500,
            expected_merchant_min_trade_amount=50,
            expected_merchant_max_trade_amount=100,
            expected_pay_time_limit=30,
        )

        ads = AdFetch(request).get()
        sorted(ads, reverse=True)
        ads = ads[:5]

        binance_price = round(statistics.mean([x.price for x in ads]), 2)
        bcv_price = BcvFecth().get()

    except SystemExit as e:
        if e.code == 0:
            description = "Successful System Exit"
            VespricetrackerLogger.get_logger().debug(description)
        else:
            description = "\n=====Unexpected Error=====\n" f"{e!s}"
            VespricetrackerLogger.get_logger().exception(description)
            raise

    except Timeout as e:
        sys.tracebacklimit = 0
        description = "\n=====Binance Ad Fetch Timeout Error=====\n" f"{e!s}"
        VespricetrackerLogger.get_logger().error(description)

    # No regular logger can be expected to be initialized
    except BootstrapError as e:
        description = "\n=====Program Initialization Error=====\n" f"{e!s}"
        e.args = (description,)
        raise

    except Exception as e:  # noqa: BLE001
        description = "\n=====Unexpected Error=====\n" f"{e!s}"
        VespricetrackerLogger.get_logger().exception(description)

    description = f"BCV: {bcv_price}\n" f"Binance: {binance_price}"
    VespricetrackerLogger.get_console_logger().info(description)
    return (bcv_price, binance_price)


if __name__ == "__main__":
    main()
