import stripe
import os
from dotenv import load_dotenv

async def createCheckoutSession(request):
    data = await request.json()
    plan = data.get("plan")
    userEmail = data.get("userEmail")
    metadata = {"plan": plan, "userEmail": userEmail}

    if plan == os.getenv("PRODUCT_TYPE_PREMIUM"):
        price_id = os.getenv("PRICE_ID_PREMIUM")
    elif plan == os.getenv("PRODUCT_TYPE_ENTERPRISE"):
        price_id = os.getenv("PRICE_ID_ENTERPRISE")
    
    checkout_session = stripe.checkout.Session.create(
        line_items = [{'price': price_id, 'quantity': 1}],
        mode = 'payment',
        metadata = metadata,
        success_url = os.getenv("CHECKOUT_SUCCESS_URL"),
        cancel_url = os.getenv("CHECKOUT_CANCEL_URL"),
    )

    return {"url": checkout_session.url}


def mainProcess(request):
    load_dotenv()
    stripe.api_key = os.getenv("STRIPE_KEY")
    return createCheckoutSession(request)