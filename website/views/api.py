from ninja import NinjaAPI
from ninja import Schema

api = NinjaAPI()

class Notification(Schema):
    txn_status: str
    txn_id: str

@api.post("payement_state/notification/")
def notification_url(request, item:Notification):
    if item.txn_status=='success':
        return {'code':200,'message':'success'}
    else:
        return {'code':400,'message':'failled'}