from loguru import logger
from sqlalchemy.orm import Session
import stripe

from ..config import get_settings
from ..models import Invoice


class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()
        if self.settings.STRIPE_SECRET_KEY:
            stripe.api_key = self.settings.STRIPE_SECRET_KEY

    def create_payment_intent(self, invoice: Invoice) -> Invoice:
        if not self.settings.STRIPE_SECRET_KEY:
            logger.warning("Stripe secret key not configured. Skipping payment intent creation.")
            return invoice
        if invoice.stripe_payment_intent_id:
            return invoice
        intent = stripe.PaymentIntent.create(
            amount=int(invoice.amount * 100),
            currency="brl",
            metadata={"invoice_id": invoice.id},
            description=f"EsthetiManage invoice #{invoice.id}",
        )
        invoice.stripe_payment_intent_id = intent["id"]
        self.db.commit()
        self.db.refresh(invoice)
        return invoice
