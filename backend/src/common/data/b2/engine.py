from b2sdk.v2 import B2Api, InMemoryAccountInfo
from common.config import settings

info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", settings.b2_application_key_id, settings.b2_application_key)
b2_bucket = b2_api.get_bucket_by_name(settings.b2_bucket_name)