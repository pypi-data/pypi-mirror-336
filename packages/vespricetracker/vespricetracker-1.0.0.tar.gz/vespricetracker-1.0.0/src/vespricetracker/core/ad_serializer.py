from vespricetracker.dto.ad_dto import AdDTO
from vespricetracker.enums.payment_method import PaymentMethod


class AdSerializer:
    @staticmethod
    def to_addto(ad_json: dict) -> AdDTO:
        adv = ad_json.get("adv", {})
        advertiser = ad_json.get("advertiser", {})

        min_single_trans_amount = float(adv.get("minSingleTransQuantity", 0))
        max_single_trans_amount = float(adv.get("maxSingleTransQuantity", 0))
        pay_time_limit = adv.get("payTimeLimit")

        merchant_name = advertiser.get("nickName", "NOT_FOUND")
        price = float(adv.get("price", 0))
        month_finish_rate = float(advertiser.get("monthFinishRate", 0)) * 100
        month_order_count = advertiser.get("monthOrderCount", 0)
        trade_methods = adv.get("tradeMethods", [])
        payment_methods = []
        for trade_method in trade_methods:
            trade_method_name = trade_method.get("tradeMethodName", "")
            if trade_method_name:
                payment_method = PaymentMethod.get_from_str(trade_method_name)
                if payment_method:
                    payment_methods.append(payment_method)

        return AdDTO(
            merchant_name=merchant_name,
            merchant_rating=month_finish_rate,
            merchant_order_count=month_order_count,
            min_trade_amount=min_single_trans_amount,
            max_trade_amount=max_single_trans_amount,
            pay_time_limit=pay_time_limit,
            payment_methods=payment_methods,
            price=price,
        )
