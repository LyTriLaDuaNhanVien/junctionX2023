# from modules.db.banking.require import *
# from modules.db.banking.schema import *
import os
from dotenv import load_dotenv
load_dotenv()
import pymongo
from typing import Optional
mongo_conection_string=os.getenv("CONNECTION_STRING")

from pydantic import BaseModel
class bank_detail_class(BaseModel):
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
    date:str
    flow_id:str
    stage_value:dict

class banking_detail:
    def __init__(self,account_number,account_name,bank_name,balance=None) -> None:
        self.account_number=account_number
        self.account_name=account_name
        self.bank_name=bank_name
        self.balance=balance
        self.res=dict(account_number=account_number,account_name=account_name,bank_name=bank_name,balance=balance)
    def get_col(self):
        client_mg = pymongo.MongoClient(mongo_conection_string)
        db = client_mg["junx"]
        col = db["banking_detail"]
        return col
    def get_col_recept(self):
        client_mg = pymongo.MongoClient(mongo_conection_string)
        db = client_mg["junx"]
        col = db["recept"]
        return col
    def insert_detail(self):
        col=self.get_col()
        query={"account_number":self.account_number,"bank_name":self.bank_name}
        doc=col.find_one(query)
        if doc:
            pass
        else:
            col.insert_one(self.res)
            res=col.find_one({"account_number": self.account_number,"bank_name":self.bank_name},{"_id":0})
            return res
    def transfer(self,receiver_account,amount,):
        col=self.get_col()
        query_s={"account_number":self.account_number}
        query_r={"account_nubmer":receiver_account}
        document = col.find_one(query_s)
        document_receiver=col.find_one(query_r)
        if document_receiver:
            value_sent=document["balance"]-amount
            value_receiver=document_receiver["balance"]+amount
            new_values_s = { "$set": { "balance": value_sent} }
            new_values_r = { "$set": { "balance": value_receiver} }
            col.update_one(query_s, new_values_s)
            col.update_one(query_r, new_values_r)
            res=col.find_one({"account_number":self.account_number,"bank_name":self.bank_name})
            return res
        else:
            return {"error":"not found the receiver"}
    def tranfer_recept(self):
        col=self.get_col_recept()
        res=dict(
            receiver_account="1235431",
            receiver_name="Le Duy Son",
            receiver_bank="MB Bank",
            ammount="-500000",
            sent_account="1235431321543",
            date="16/04/2023"
            )
        col.insert_one(res)
        col_user=self.get_col()
        u1=col_user.find_one({"account_number":"1235431321543","bank_name":"TPBank"})
        balance=u1["balance"]
        col_user.find_one_and_update({"account_number":"1235431321543","bank_name":"TPBank"},{"$set":{"balance":balance-50000}})
        return res
# bank123=banking_detail(account_name="",bank_name="Sacombank",balance=12000,account_number="321543")
# bank123.insert_detail()
class section_keeper:
    def __init__(self,stage_id=None,stage_value=None,flow_id=None) -> None:
        self.stage_value=stage_value
        if stage_id is None:
            self.stage_id=self.stage_define()
        else:
            self.stage_id=stage_id
        self.msg=""
        self.flow_id=flow_id
        self.res=dict(stage_id=stage_id,stage_value=stage_value,flow_id=flow_id)
    def get_col(self):
        client_mg = pymongo.MongoClient(mongo_conection_string)
        db = client_mg["junx"]
        col = db["stage"]
        return col
    def insert_stage(self):
        col=self.get_col()
        res=col.find_one({"flow_id":self.flow_id})
        if res is None:
            col.insert_one(self.res)
            res=col.find_one({"flow_id":self.flow_id})
        return res
    def delete_stage(self):
        col=self.get_col()
        col.delete_one({"flow_id":self.flow_id})
        return 1
    def get_stage_define(self):
        col=self.get_col()
        res=col.find_one({"flow_id":self.flow_id},{"_id":0})
        return res 
    def stage_define(self):
        # print(self.stage_value)
        list_key=self.stage_value["entities"]
        print(list_key)
        if len(list_key)==0:
            self.stage_id=1
        elif len(list_key)<4:
            self.stage_id=2
        elif len(list_key)==4:
            self.stage_id=3
        elif len(list_key)==5:
            self.stage_id=4
            if self.stage_value["entities"] == 1:
                self.stage_id=5   
            else:
                self.stage_id=6
        elif len(list_key)==6:
            if self.stage_value["entities"] == 1:
                self.stage_id=7
            else:
                self.stage_id=8
        elif len(list_key)==10:
            self.stage_id=9
        else:
            pass
        return self.stage_id
    def get_entinity(self):
        col=self.get_col() 
        doc=col.find_one({"flow_id":self.flow_id})
        self.stage_id=doc["stage_id"]
        dict_stage={}
        for i in self.stage_value["entities"]:
            dict_stage[i["entity"]]=i["value"]
        return dict_stage
    def define_stage(self):
        col=self.get_col()
        doc=col.find_one({"flow_id":self.flow_id})
        print(doc["stage_id"])
        if doc["stage_id"] is None:
          self.stage_id="0"
        else:
          self.stage_id=doc["stage_id"]
        print(self.stage_id)
        # dict_stage={}
        dict_stage=self.get_entinity()
        if "BANK_NAME" in dict_stage:
            bank_name=dict_stage["BANK_NAME"]
        else:
            bank_name="MB Bank"
        if "AMOUNT" in dict_stage:
            amount=dict_stage["AMOUNT"]
        else:
            amount=500000
        if "CREDITCARD_NUMBER" in dict_stage:
            creditcard_number=dict_stage["CREDITCARD_NUMBER"]
        else:
            creditcard_number="1235431"
        if "CARDHOLDER" in dict_stage:
            cardholder=dict_stage["CARDHOLDER"]
        else:
            cardholder='Lê Duy Sơn'
        if "note" in dict_stage:
            note=dict_stage["note"]
        else:
            note=""
        if self.stage_id=="0":
            self.msg="Xin chào tôi là Ngọc Thảo chuyên viên ảo hỗ trợ bạn. Bạn hãy đưa ra yêu cầu"
            self.stage_id=1
            col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":self.stage_id}})
            col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
            print(self.msg)
            return dict(stage_id=self.stage_id,msg=self.msg)
        elif self.stage_id==1:
            self.msg="Dạ vâng bạn hãy cho tôi yêu cầu chuyển khoản của bạn"
            list_key=list(dict_stage.keys())
            # print(list_key)
            # print(self.msg)
            if len(list_key)<=2:
                self.stage_id=2
                col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":self.stage_id}})
                col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
                return dict(stage_id=self.stage_id,msg=self.msg)
            else:
                self.stage_id=3
                col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":self.stage_id}})
                col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
                return dict(stage_id=self.stage_id,msg=self.msg)
        elif self.stage_id==2:
            self.msg="Chúng tôi đã kiểm tra và không tìm thấy tài khoản bạn yêu cầu chuyển tiền mời bạn đọc lại yêu cầu"
            self.stage_id==1
            col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":self.stage_id}})
            col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
            return dict(stage_id=self.stage_id,msg=self.msg)
        elif self.stage_id==3:
            self.msg=f"Xác nhận chuyển tiền đến ngân hàng {bank_name} số tài khoản {creditcard_number} chủ tài khoản {cardholder} số tiền là {amount}. Quý khách có muốn bổ sung lời nhắn"
            #To-do neu ma co note
            self.stage_id==6
            col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":self.stage_id}})
            col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
            return dict(stage_id=self.stage_id,msg=self.msg)
        elif self.stage_id==5:
            self.msg=f"Mời bạn đọc lời nhắn"
            if "note_check" in dict_stage:
                if dict_stage["note_check"] == 1:
                  self.stage_id==7
                  col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":self.stage_id}})
                  col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
                  return dict(stage_id=self.stage_id,msg=self.msg)
                elif dict_stage["note_check"] == 0:
                  self.stage_id==6
                  col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":self.stage_id}})
                  col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
                  return dict(stage_id=self.stage_id,msg=f"Chúng tôi xin gửi lại thông tin chuyển khoản của Quý khách: \nChuyển khoản tới ngân hàng {bank_name} số tài khoản {creditcard_number} {cardholder} Số tiền {amount} Mời bạn xác nhận là là có nếu muốn thực hiện")
        elif self.stage_id==6:
            self.msg=f"Chúng tôi xin gửi lại thông tin chuyển khoản của Quý khách: \nChuyển khoản tới ngân hàng {bank_name} số tài khoản {creditcard_number} {cardholder} Số tiền {amount} Mời bạn xác nhận là là có nếu muốn thực hiện"
            if "final_check" in dict_stage:
                if dict_stage["final_check"] == 1:
                  self.stage_id=8
                  col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":self.stage_id}})
                  col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
                  return dict(stage_id=self.stage_id,msg=self.msg)
                else:
                  self.stage_id=9
                  self.delete_stage()
                  return dict(stage_id=self.stage_id,msg=self.msg)
        elif self.stage_id==7:
            self.msg=f"Chúng tôi xin gửi lại thông tin chuyển khoản của Quý khách: \nChuyển khoản tới ngân hàng {bank_name} số tài khoản {creditcard_number} {cardholder} Số tiền {amount} Với lời nhắn  {note}  Mời bạn xác nhận là có nếu muốn thực hiện"
            if "final_check" in dict_stage:
              if dict_stage["final_check"] == 1:
                self.stage_id=8
                col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":self.stage_id}})
                col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
                return dict(stage_id=self.stage_id,msg=self.msg)
              else:
                self.stage_id=9
                self.delete_stage()
                return dict(stage_id=self.stage_id,msg=self.msg)
        elif self.stage_id==8:
            self.msg="Xác nhận"
            bd=banking_detail("1235431321543","Khuat Quang Vinh","TPBank")
            res=bd.tranfer_recept()
            return res
        elif self.stage_id==9:
            self.msg="Đã hủy"
    #     if self.stage_id==2:
    #         self.delete_stage()
    #     elif self.stage_id=="0":
    #         col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+1)}})
    #         col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #     elif self.stage_id==5:
    #         for i in self.stage_value["entities"]:
    #             dict_stage[i["entities"]]=i["value"]
    #         if dict_stage["note"] is None:
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+1)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #         else:
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+2)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #     elif self.stage_id==1:
    #         if len(list(dict_stage.keys()))<4:
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+1)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #         else:
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+1)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #     elif self.stage_id==3:
    #         if dict_stage["note"] !="0":
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+2)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #         else:
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+1)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #     elif self.stage_id==4:
    #         if dict_stage["note_phrase"] !="0":
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+1)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #         else:
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+2)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #     elif self.stage_id==6:
    #         if dict_stage["confirm"] == 1:
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+1)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #         else:
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+1)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #     elif self.stage_id==7:
    #         if dict_stage["confirm"] == 1:
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+1)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #         else:
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_id":str(int(self.stage_id)+1)}})
    #             col.find_one_and_update({"flow_id":self.flow_id},{"$set":{"stage_value":self.stage_value}})
    #     elif self.stage_id in [8,9]:
    #         self.delete_stage()     
    #     return 1
    # def handle_stage(self):
    #     dict_stage={}
    #     for i in self.stage_value["entities"]:
    #         # print(i)
    #         dict_stage[i["entity"]] = i["value"]
    #         # dict_stage[i["entities"]]=i["value"]
    #     if "BANK_NAME" in dict_stage:
    #         bank_name=dict_stage["BANK_NAME"]
    #     else:
    #         bank_name=None
    #     if "AMOUNT" in dict_stage:
    #         amount=dict_stage["AMOUNT"]
    #     else:
    #         amount=None
    #     if "CREDITCARD_NUMBER" in dict_stage:
    #         creditcard_number=dict_stage["CREDITCARD_NUMBER"]
    #     if "CARDHOLDER" in dict_stage:
    #         cardholder=dict_stage["CARDHOLDER"]
    #     if "note" in dict_stage:
    #         note=dict_stage["note"]
    #     if "confirm" in dict_stage:
    #         confirm=dict_stage["confirm"]
    #     if "note_phrase" in dict_stage:
    #         note_phrase=dict_stage["note_phrase"]
        # if self.stage_id=="0":
        #     self.msg="Xin chào tôi là Ngọc Thảo chuyên viên ảo hỗ trợ bạn. Bạn hãy đưa ra yêu cầu"
        # if self.stage_id==1:
        #     self.msg="Dạ vâng bạn hãy cho tôi yêu cầu chuyển khoản của bạn"
        # elif self.stage_id==2:
        #     self.msg="Chúng tôi đã kiểm tra và không tìm thấy tài khoản bạn yêu cầu chuyển tiền mời bạn đọc lại yêu cầu"
        # elif self.stage_id==3:
        #     self.msg=f"Xác nhận chuyển tiền đến ngân hàng {bank_name} số tài khoản {creditcard_number} chủ tài khoản {cardholder} số tiền là {amount}. Quý khách có muốn bổ sung lời nhắn"
        # elif self.stage_id==5:
        #      self.msg=f"Mời bạn đọc lời nhắn"
        # elif self.stage_id==6:
        #     self.msg=f"Chúng tôi xin gửi lại thông tin chuyển khoản của Quý khách: \nChuyển khoản tới ngân hàng {bank_name} số tài khoản {creditcard_number} {cardholder} Số tiền {amount} Mời bạn xác nhận là là có nếu muốn thực hiện"
        # elif self.stage_id==7:
        #     self.msg=f"Chúng tôi xin gửi lại thông tin chuyển khoản của Quý khách: \nChuyển khoản tới ngân hàng {bank_name} số tài khoản {creditcard_number} {cardholder} Số tiền {amount} Với lời nhắn {note}  Mời bạn xác nhận là là có nếu muốn thực hiện"
        # elif self.stage_id==8:
        #     self.msg="Xác nhận"
        # elif self.stage_id==9:
        #     self.msg="Đã hủy"
    #     self.update_stage()
    #     return dict(stage_id=self.stage_id,msg=self.msg)
import json
import requests
# from routes.rasa_route.schema import msg_input
from pydantic import BaseModel
class msg_input(BaseModel):
    text:str
    note: Optional[str]
def get_data(i):
    print("debug")
    print(i)
    payload = {'text':i["text"]}
    headers = {'content-type': 'application/json'}
    r = requests.post('http://52.221.181.187:5005/model/parse', json=payload, headers=headers)
    print(r.text)
    jso=json.loads(r.text)  
    res={}
    res["entities"]=jso["entities"]
    res["intent"]=jso["intent"]["name"]
    return res
# value={
#   "text": "Chuyển khoản cho tôi 500k tới Nguyễn Việt Anh ngân hàng ngoại thương số tài khoản 123456789",
#   "intent": {
#     "name": "transfer_money",
#     "confidence": 0.9999849796295166
#   },
#   "entities": [
#     {
#       "entity": "AMOUNT",
#       "start": 21,
#       "end": 25,
#       "confidence_entity": 0.9992362260818481,
#       "value": "500k",
#       "extractor": "DIETClassifier",
#       "processors": [
#         "EntitySynonymMapper"
#       ]
#     },
#     {
#       "entity": "CARDHOLDER",
#       "start": 30,
#       "end": 45,
#       "confidence_entity": 0.9339396357536316,
#       "value": "Nguyen Viet Anh",
#       "extractor": "DIETClassifier",
#       "processors": [
#         "EntitySynonymMapper"
#       ]
#     },
#     {
#       "entity": "BANK_NAME",
#       "start": 56,
#       "end": 68,
#       "confidence_entity": 0.9938573837280273,
#       "value": "Techcombank",
#       "extractor": "DIETClassifier",
#       "processors": [
#         "EntitySynonymMapper"
#       ]
#     },
#     {
#       "entity": "CREDITCARD_NUMBER",
#       "start": 82,
#       "end": 91,
#       "confidence_entity": 0.9823033213615417,
#       "value": "42321543",
#       "extractor": "DIETClassifier"
#     }
#   ],
#   "text_tokens": [
#     [
#       0,
#       6
#     ],
#     [
#       7,
#       12
#     ],
#     [
#       13,
#       16
#     ],
#     [
#       17,
#       20
#     ],
#     [
#       21,
#       25
#     ],
#     [
#       26,
#       29
#     ],
#     [
#       30,
#       36
#     ],
#     [
#       37,
#       41
#     ],
#     [
#       42,
#       45
#     ],
#     [
#       46,
#       50
#     ],
#     [
#       51,
#       55
#     ],
#     [
#       56,
#       61
#     ],
#     [
#       62,
#       68
#     ],
#     [
#       69,
#       71
#     ],
#     [
#       72,
#       75
#     ],
#     [
#       76,
#       81
#     ],
#     [
#       82,
#       91
#     ]
#   ],
#   "intent_ranking": [
#     {
#       "name": "transfer_money",
#       "confidence": 0.9999849796295166
#     },
#     {
#       "name": "bot_challenge",
#       "confidence": 0.0000034983509067387786
#     },
#     {
#       "name": "deny",
#       "confidence": 0.0000033258747862419114
#     },
#     {
#       "name": "ask_ability",
#       "confidence": 0.000002257611185996211
#     },
#     {
#       "name": "new_credit_card_related",
#       "confidence": 0.0000021107648535689805
#     },
#     {
#       "name": "greet",
#       "confidence": 0.0000010168711241931305
#     },
#     {
#       "name": "mood_unhappy",
#       "confidence": 5.948101033936837e-7
#     },
#     {
#       "name": "mood_great",
#       "confidence": 5.203089017413731e-7
#     },
#     {
#       "name": "credit_card_info",
#       "confidence": 4.357803788934689e-7
#     },
#     {
#       "name": "human_handoff",
#       "confidence": 3.6517536727842526e-7
#     }
#   ],
#   "response_selector": {
#     "all_retrieval_intents": [],
#     "default": {
#       "response": {
#         "responses": "null",
#         "confidence": 0,
#         "intent_response_key": "null",
#         "utter_action": "utter_None"
#       },
#       "ranking": []
#     }
#   }
# }

# sk=section_keeper(stage_value=value,flow_id=10,stage_id=1)
# # # print(type(sk.stage_value))
# sk.insert_stage()
# print(sk.define_stage())