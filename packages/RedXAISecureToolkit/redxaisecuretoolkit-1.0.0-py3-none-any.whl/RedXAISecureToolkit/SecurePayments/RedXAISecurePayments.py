import os
import json
import random
import secrets
import string
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import stripe
from dotenv import load_dotenv
from RedXAISecureToolkit.RedXAISecureToolkit.FireCloud.RedXAIFireCloud import*
import firebase_admin
from firebase_admin import db

# rest of your file continues unchanged...


# 🔐 State
_RedXAI_PURCHASE_STATE = {
    "users_initialized": False,
    "user_path": None,
    "lifetime_folder": None,
    "subscription_folder": None,
    "active_mode": None
}

# ✅ Smart .env loader
def RedXAIEnvVar(var_name, env_path=None, error_if_missing=True):
    def find_env_file(start_path):
        for root, dirs, files in os.walk(start_path):
            if ".env" in files:
                return os.path.join(root, ".env")
        return None

    if env_path is None:
        env_path = find_env_file(os.getcwd())
        if not env_path:
            raise FileNotFoundError("⚠️ .env file not found in project directory.")

    load_dotenv(env_path)
    value = os.getenv(var_name)

    if value is None and error_if_missing:
        raise KeyError(f"❌ Environment variable '{var_name}' not found in {env_path}")
    
    return value

# ✅ Initialize Users Table
def RedXAIInitializeUsers(user_data_path):
    if not user_data_path:
        raise RuntimeError("❌ User data path is required.")

    _RedXAI_PURCHASE_STATE["user_path"] = user_data_path
    _RedXAI_PURCHASE_STATE["users_initialized"] = True

    if not RedXAIFireSearch(user_data_path, key="Initialized", detail_level="k"):
        RedXAIFireTableAdd(user_data_path, "Initialized", True)

    return user_data_path

# ✅ Lifetime Mode
def RedXAIInitializeLifetimeCodes(folder_name):
    if not _RedXAI_PURCHASE_STATE["users_initialized"]:
        raise RuntimeError("Call RedXAIInitializeUsers() first.")

    path = f"{_RedXAI_PURCHASE_STATE['user_path']}[{folder_name}]"
    if not RedXAIFireSearch(path, key="Initialized", detail_level="k"):
        RedXAIFireTableAdd(path, "Initialized", True)

    _RedXAI_PURCHASE_STATE["lifetime_folder"] = path
    _RedXAI_PURCHASE_STATE["active_mode"] = "lifetime"
    return path

# ✅ Subscription Mode
def RedXAIInitializeSubscriptions(folder_name):
    if not _RedXAI_PURCHASE_STATE["users_initialized"]:
        raise RuntimeError("Call RedXAIInitializeUsers() first.")

    path = f"{_RedXAI_PURCHASE_STATE['user_path']}[{folder_name}]"
    if not RedXAIFireSearch(path, key="Initialized", detail_level="k"):
        RedXAIFireTableAdd(path, "Initialized", True)

    _RedXAI_PURCHASE_STATE["subscription_folder"] = path
    _RedXAI_PURCHASE_STATE["active_mode"] = "subscription"
    return path

# ✅ Add App Entry
def RedXAIAddApp(app_name, lifetime_folder=None, subscription_folder=None):
    if not _RedXAI_PURCHASE_STATE["users_initialized"]:
        raise RuntimeError("InitializeUsers() must be called first.")
    if app_name == "BlankApp":
        raise ValueError("❌ 'BlankApp' is reserved.")

    added_any = False

    def _add_app(path, keys):
        RedXAIFireTableAdd(path, "Initialized", True)
        for k, v in keys.items():
            RedXAIFireTableAdd(path + "[Users][UserValue]", k, v)

    if lifetime_folder:
        path = f"{lifetime_folder}[{app_name}]"
        if not RedXAIFireSearch(lifetime_folder, key=app_name, detail_level="k"):
            _add_app(path, {
                "UsernameOrEmail": "",
                "UID": "",
                "LifetimeCode": "",
                "LimitedCode": ""
            })
            added_any = True

    if subscription_folder:
        path = f"{subscription_folder}[{app_name}]"
        if not RedXAIFireSearch(subscription_folder, key=app_name, detail_level="k"):
            _add_app(path, {
                "UsernameOrEmail": "",
                "UID": "",
                "Subscription": False
            })
            added_any = True

    if not added_any:
        print("⚠️ App already exists or no folder provided.")

# ✅ Combo Setup
def RedXAIInitializeAll(users_path, lifetime_path, subscription_path):
    u = RedXAIInitializeUsers(users_path)
    l = RedXAIInitializeLifetimeCodes(lifetime_path)
    s = RedXAIInitializeSubscriptions(subscription_path)
    return u, l, s

# ✅ Key Generator
def RedXAIGenerateLifetimeKey(username_or_email, module_name="FireCloudModule"):
    if not firebase_admin._apps:
        raise RuntimeError("Firebase not initialized.")

    base_path = _RedXAI_PURCHASE_STATE["lifetime_folder"] + "[Users]"
    user_path = f"{base_path}[{username_or_email}]"

    if RedXAIFireSearch(base_path, key=username_or_email, detail_level="k"):
        existing = db.reference(user_path.replace("[", "/").replace("]", "")).get()
        print(f"⚠️ Already exists: {existing['LifetimeCode']}")
        return existing

    code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(24))
    uid = len(db.reference(base_path.replace("[", "/").replace("]", "")).get() or {})

    data = {
        "Activated": True,
        "LifetimeCode": code,
        "UID": uid,
        "Module": module_name
    }
    db.reference(user_path.replace("[", "/").replace("]", "")).set(data)
    return data

# ✅ Stripe QuickBuy
def QuickBuy(price_usd, email=None, ConsoleSale=True, stripe_api_key=None):
    def is_valid(e): return isinstance(e, str) and "@" in e and "." in e

    if ConsoleSale:
        print(f"💰 Price: ${price_usd:.2f}")
        email = input("📧 Email: ").strip()
        if not is_valid(email): return print("❌ Invalid email.")
        if input(f"Confirm ({email})? (y/n): ").lower() != 'y': return print("❌ Cancelled.")
        if input("🛒 Proceed to purchase? (y/n): ").lower() != 'y': return print("❌ Cancelled.")

    if not is_valid(email):
        print("❌ Invalid email.")
        return None

    stripe.api_key = stripe_api_key or RedXAIEnvVar("StripeApiKey", error_if_missing=True)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(price_usd * 100),
                    'product_data': {
                        'name': "Red-XAI Purchase",
                        'description': "Premium access or credits"
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            customer_email=email,
            success_url='https://RedXAI.com/success',
            cancel_url='https://RedXAI.com/cancel'
        )
        print("✅ Launching Stripe Checkout...")
        webbrowser.open(session.url)
        return email
    except Exception as e:
        print("❌ Stripe error:", e)
        return None

# ✅ Email Verification Sender
def SendVerificationEmail(email, username, full_path, sender_email=None, sender_password=None):
    code = str(random.randint(100000, 999999))
    db.reference(f"{full_path}/EmailCode").set({"code": code})

    message = f"Hi {username},\n\nYour Red XAI verification code is: {code}\n\nIf you did not request this, ignore this email."

    msg = MIMEText(message)
    msg['Subject'] = "Red XAI Email Verification"
    msg['From'] = sender_email or RedXAIEnvVar("EMAIL_SENDER")
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email or RedXAIEnvVar("EMAIL_SENDER"),
                        sender_password or RedXAIEnvVar("EMAIL_PASSWORD"))
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
        print("✅ Verification email sent.")
    except Exception as e:
        print("❌ Email send failed:", e)
