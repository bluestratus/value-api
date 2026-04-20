import os

APP_ENV = os.getenv("APP_ENV", "dev")
ENABLE_INTERNAL_ROUTES = os.getenv("ENABLE_INTERNAL_ROUTES", "true").lower() == "true"

MY_API_KEY = os.getenv("MY_API_KEY", "local-dev-key")

VRM_API_URL = os.getenv("VRM_API_URL", "https://example.com/vrm")
VRM_API_KEY = os.getenv("VRM_API_KEY", "")

CANPRICE_API_URL = os.getenv("CANPRICE_API_URL", "https://example.com/canprice")
CANPRICE_API_KEY = os.getenv("CANPRICE_API_KEY", "")

PAIDVALUE_API_URL = os.getenv("PAIDVALUE_API_URL", "https://example.com/paidvalue")
PAIDVALUE_API_KEY = os.getenv("PAIDVALUE_API_KEY", "")