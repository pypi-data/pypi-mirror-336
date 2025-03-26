from __future__ import annotations

from enum import Enum


class PaymentMethod(Enum):
    PAGO_MOVIL = "Pago Movil"
    TRANSFERS_WITH_SPECIFIC_BANK = "Transfers with specific bank"
    BANK_TRANSFER = "Bank Transfer"
    BANCAMIGA = "Bancamiga"
    BNC = "BNC Banco Nacional de Crédito"
    BVC = "Banco Venezolano de Crédito"
    PROVINCIAL_1 = "BBVA"
    PROVINCIAL_2 = "Provincial"
    MERCANTIL = "Mercantil"
    BANESCO = "Banesco"
    BANCARIBE = "Bancaribe"
    BANPLUS = "Banplus"
    BANCO_PLAZA = "Banco Plaza"

    @staticmethod
    def get_all() -> list[PaymentMethod]:
        return list(PaymentMethod)

    @staticmethod
    def get_from_str(candidate: str) -> PaymentMethod | None:
        for x in PaymentMethod.get_all():
            if candidate.lower() == x.value.lower():
                return x

        return None

    @staticmethod
    def is_universal_payment(payment_methods: list[PaymentMethod]) -> bool:
        return (
            PaymentMethod.PAGO_MOVIL in payment_methods
            or PaymentMethod.BANESCO in payment_methods
            and PaymentMethod.BNC in payment_methods
            and PaymentMethod.PROVINCIAL_1 in payment_methods
            and PaymentMethod.MERCANTIL in payment_methods
            or PaymentMethod.BANESCO in payment_methods
            and PaymentMethod.BNC in payment_methods
            and PaymentMethod.PROVINCIAL_2 in payment_methods
            and PaymentMethod.MERCANTIL in payment_methods
        )
