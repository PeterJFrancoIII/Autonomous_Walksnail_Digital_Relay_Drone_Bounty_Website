#!/usr/bin/env python3
"""
MODULE: bounty_funding_engine.py
DESCRIPTION: 
This module acts as the financial backend for the Relay Drone bounty system.
It is designed to be integrated into a Django application utilizing MongoDB 
(via mongoengine) as the primary datastore. 

It performs three critical functions:
1. Defines the MongoDB schema for tracking individual donations and the master pool.
2. Provides a webhook receiver to catch live 'payment_intent.succeeded' events from Stripe.
3. Provides an API endpoint that the frontend can poll to display the live bounty 
   amounts and the calculated prize tier distributions.

EFFECT ON PROGRAM:
When deployed, this script ensures that every time the community donates, the 
database is securely updated, and the public-facing prize pool ticker increases 
in real-time, fostering trust and competition.
"""

import os
import json
import stripe
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from mongoengine import Document, StringField, FloatField, DateTimeField, connect
from datetime import datetime

# --- CONFIGURATION ---
# Initialize Stripe with the secret key (Should be stored in environment variables)
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_placeholder')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_placeholder')

# Connect to the local or cloud MongoDB database
connect('relay_bounty_db', host='mongodb://localhost:27017/relay_bounty_db')

# --- MONGODB MODELS ---

class DonationRecord(Document):
    """
    MongoDB Schema representing a single successful donation.
    We store the Stripe transaction ID to prevent double-counting.
    """
    transaction_id = StringField(required=True, unique=True)
    donor_name = StringField(default="Anonymous FPV Pilot")
    amount_usd = FloatField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)
    
    meta = {'collection': 'bounty_donations'}

class MasterBountyPool(Document):
    """
    MongoDB Schema representing the current aggregate state of the bounty.
    Storing this separately prevents us from having to sum thousands of 
    DonationRecords every time a user loads the webpage.
    """
    total_funds_usd = FloatField(default=0.0)
    last_updated = DateTimeField(default=datetime.utcnow)
    
    meta = {'collection': 'bounty_master_pool'}

# --- CORE VIEWS / LOGIC ---

@csrf_exempt
def stripe_webhook(request):
    """
    ENDPOINT: /api/webhooks/stripe/
    DESCRIPTION: 
    This view listens for incoming POST requests from Stripe. When a user donates 
    on the frontend via a Stripe Checkout link, Stripe pings this URL.
    We verify the signature, extract the money amount, and update MongoDB.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        # Verify the payload is actually from Stripe
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the successful payment intent
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        tx_id = payment_intent['id']
        
        # Stripe processes amounts in cents. We convert to standard dollars.
        amount_dollars = payment_intent['amount'] / 100.0
        
        # Check if we already processed this transaction (Idempotency check)
        if not DonationRecord.objects(transaction_id=tx_id).first():
            
            # 1. Save the individual donation record
            new_donation = DonationRecord(
                transaction_id=tx_id,
                amount_usd=amount_dollars
            )
            new_donation.save()
            
            # 2. Update the Master Pool
            # Get or create the master record
            pool = MasterBountyPool.objects.first()
            if not pool:
                pool = MasterBountyPool()
                
            pool.total_funds_usd += amount_dollars
            pool.last_updated = datetime.utcnow()
            pool.save()
            
            print(f"SUCCESS: Added ${amount_dollars} to the Relay Drone Bounty!")

    return HttpResponse(status=200)

def get_live_bounty_data(request):
    """
    ENDPOINT: /api/bounty/live-stats/
    DESCRIPTION: 
    The frontend dashboard hits this endpoint to get the current prize money.
    It fetches the total from MongoDB and automatically calculates the tiers
    (1st Place 60%, 2nd Place 20%, 3rd Place 10%, VIP 10%).
    """
    pool = MasterBountyPool.objects.first()
    total = pool.total_funds_usd if pool else 0.0
    
    response_data = {
        "status": "success",
        "grand_total_usd": total,
        "prize_tiers": {
            "first_place": round(total * 0.60, 2),   # 60% Grand Prize
            "second_place": round(total * 0.20, 2),  # 20% Innovator Award
            "third_place": round(total * 0.10, 2),   # 10% Bronze
            "vip_pool": round(total * 0.05, 2),      # 5% Community Contributors
            "admin_award": round(total * 0.05, 2)    # 5% Administrative Costs
        },
        "last_updated": pool.last_updated.isoformat() if pool else None
    }
    
    # Allows Cross-Origin requests if the frontend is hosted separately
    response = JsonResponse(response_data)
    response["Access-Control-Allow-Origin"] = "*"
    return response
