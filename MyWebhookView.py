import stripe
from fastapi import HTTPException
from datetime import datetime, timedelta
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DB_NAME")]
users_collection = db[os.getenv("DB_COLLECTION")]

stripe.api_key = os.getenv("STRIPE_KEY")
endpoint_secret = os.getenv("WEBHOOK_SK")

def calculate_expiration_date():    
    return datetime.now() + timedelta(days=30)

async def myWebhookView(request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    event = None
    

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        raise HTTPException(status_code=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        raise HTTPException(status_code=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        plan = session['metadata']['plan']
        userEmail = session['metadata']['userEmail']
        expire_date = calculate_expiration_date()

        if(plan == os.getenv("PRODUCT_TYPE_PREMIUM")):
            result = users_collection.update_one({"email": userEmail}, {"$set": {"lvl": 1, "expire_day": expire_date}})
            if result.modified_count:
              return {"message": "Premium plan purchased successfully, expires on: " + expire_date.strftime("%Y-%m-%d")}
            else:
              raise HTTPException(status_code=404, detail="User not found or already on premium level")
        elif(plan == os.getenv("PRODUCT_TYPE_ENTERPRISE")):
          result = users_collection.update_one({"email": userEmail}, {"$set": {"lvl": 2, "expire_day": expire_date}})
          if result.modified_count:
              return {"message": "Professional plan purchased successfully, expires on: " + expire_date.strftime("%Y-%m-%d")}
          else:
              raise HTTPException(status_code=404, detail="User not found or already on premium level")


def mainProcess(request):
    return myWebhookView(request)