from pydantic import BaseModel
class bank_detail(BaseModel):
    customer_code:str
    customer_name:str
    balance:int
    account_number:str

class bank_transfer(BaseModel):
    receiver_account:str
    receiver_name:str
    receiver_bank:str
    amount:int
    msg:str
    sent_account:str