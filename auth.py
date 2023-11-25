from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pymongo import MongoClient
import stripe

router = APIRouter()
stripe.api_key = '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'

mongo_uri = "mongodb+srv://devguru13580:hXcQgMDBinZ8wlo4@cluster0.ehilact.mongodb.net/"
client = MongoClient(mongo_uri)
db = client["harmony"]
users_collection = db["users"]

class UserSignIn(BaseModel):
    email: str
    password: str

class UserSignUp(BaseModel):
    username: str
    email: str
    password: str

@router.post("/signin")
def sign_in(user: UserSignIn):
    # Find the user by email and password in the MongoDB collection
    result = users_collection.find_one({"email": user.email, "password": user.password})

    if result:
        return {"message": "Sign-in successful", "name": result["username"], "mail": result["email"], "level": result["lvl"], "expire": result["expire_day"]}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signup")
def sign_up(user: UserSignUp):
    # Check if the username or email already exists in the MongoDB collection
    existing_user = users_collection.find_one({"$or": [{"username": user.username}, {"email": user.email}]})

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Insert the new user into the MongoDB collection
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "lvl": 0,
        "expire_day": None
    }
    users_collection.insert_one(new_user)

    return {"message": "Sign-up successful"}

@router.get("/")
def helps():
    print("Running")
    return {"message": "Connection successful"}


@router.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    data = await request.json()
    plan = data.get("plan")

    if plan == "premium":
        price_id = "price_1OBn3kItQ91j83DindUoX85a"  # Replace with your actual price ID
    elif plan == "professional":
        price_id = "price_1OBn6GItQ91j83Di0JWVJmlx"  # Replace with your actual price ID
    else:
        raise HTTPException(status_code=400, detail="Invalid plan selected")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url='your_success_url_here',
            cancel_url='your_cancel_url_here',
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.json()  # This line extracts the JSON payload from the request

    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, "we_1OCOuVItQ91j83DiPPMX5hgi"
        )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail=f"Invalid payload: {e}")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail=f"Invalid signature: {e}")

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        # Payment succeeded, update your database or perform other actions
        print('Payment succeeded!')

    return {"status": "success"}
