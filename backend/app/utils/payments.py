import razorpay
from ..core.config import settings

client = None

def get_razorpay_client():
    global client
    if not client and settings.RAZORPAY_KEY_ID and settings.RAZORPAY_SECRET:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET))
    return client

def create_order(amount: int, currency: str = "INR") -> dict:
    rz_client = get_razorpay_client()
    if not rz_client:
        return {"error": "Razorpay not configured"}
    
    data = {"amount": amount * 100, "currency": currency, "receipt": f"txn_{hash(amount)}"}
    order = rz_client.order.create(data=data)
    return order

def verify_payment(order_id: str, payment_id: str, signature: str) -> bool:
    rz_client = get_razorpay_client()
    if not rz_client:
        return False
    try:
        rz_client.utility.verify_payment_signature({"razorpay_order_id": order_id, "razorpay_payment_id": payment_id, "razorpay_signature": signature})
        return True
    except:
        return False