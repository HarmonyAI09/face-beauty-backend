from fastapi import APIRouter, Request, HTTPException
import stripe
import os
import Auth
from schemas import PremiumSchema

from dotenv import load_dotenv
load_dotenv()
stripe.api_key = os.getenv("STRIPE_KEY")

router = APIRouter()

@router.post('/cash/create-checkout-session')
async def createCheckoutSession(request : Request):
    data = await request.json()
    plan = data.get("plan")
    mail = data.get("userEmail")
    metaData = {
        "plan" : plan,
        "userEmail" : mail,
    }

    if plan == os.getenv("PRODUCT_TYPE_PREMIUM"):
        price_id = os.getenv("PRICE_ID_PREMIUM")
    if plan == os.getenv("PRODUCT_TYPE_ENTERPRISE"):
        price_id = os.getenv("PRICE_ID_ENTERPRISE")

    checkoutSession = stripe.checkout.Session.create(
        line_items = [{'price': price_id, 'quantity': 1}],
        mode = 'payment',
        metadata = metaData,
        success_url = os.getenv("CHECKOUT_SUCCESS_URL"),
        cancel_url = os.getenv("CHECKOUT_CANCEL_URL"),
    )

    return {"url" : checkoutSession.url}

@router.post('/webhook')
async def catchWebhook(request : Request):
    print('inside webhook')
    payload = await request.body()
    sign = request.headers.get('stripe-signature')
    event = None


    try:
        event = stripe.Webhook.construct_event(payload, sign, os.getenv("WEBHOOK_SK"))
    except ValueError:
        raise HTTPException(status_code = 400)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code = 400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        plan = session['metadata']['plan']
        mail = session['metadata']['userEmail']

        print(session['metadata'])

        if plan == os.getenv("PRODUCT_TYPE_PREMIUM"):
            if Auth.update(PremiumSchema(mail, 1)).modified_count:
                return {"success": True, "status" : "Buy-premium success."}
            else:
                return {"success": False, "status" : "Buy-premium failed."}
        elif plan == os.getenv("PRODUCT_TYPE_ENTERPRISE"):
            if Auth.update(PremiumSchema(mail, 2)).modified_count:
                return {"success": True, "status" : "Buy-enterprise success."}
            else:
                return {"success": False, "status" : "Buy-enterprise failed."}