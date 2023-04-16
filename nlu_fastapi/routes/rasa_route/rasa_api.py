import requests
from fastapi import HTTPException,APIRouter, Body
from routes.rasa_route.schema import msg_input
from typing import Dict, Any, List, Optional
import json
from modules.db.banking.transfer import *
app=APIRouter()
@app.post("/send_msg")
def send_msg(i:msg_input):
    payload = {'text':i.text}
    headers = {'content-type': 'application/json'}
    r = requests.post('http://52.221.181.187:5005/model/parse', json=payload, headers=headers)
    print(r.text)
    jso=json.loads(r.text)
    return jso
class msg_input2(BaseModel):
    text:str
    note: Optional[str]
@app.post("/flow_transfer")
def flow_transfer(body: Dict[str, Any] = Body(...)):
    value=get_data(body)
    print(value)
    try:
        if body["note_check"]:
            value["entities"].append(dict(entity="note_check",value=body["note_check"]))
            print(value["entities"])
        else:
            value["entities"].append(dict(entity="note_check",value=0))
    except:
        value["entities"].append(dict(entity="note_check",value=0))
    try:
        if body["note"]:
            value["entities"].append(dict(entity="note",value=body["note"]))
            print(value["entities"])
    except:
        value["entities"].append(dict(entity="note",value=0))
    try:
        if body["final_check"]:
            value["entities"].append(dict(entity="final_check",value=body["final_check"]))
            print(value["entities"])
    except:
        value["entities"].append(dict(entity="final_check",value=0))
    sk=section_keeper(stage_value=value,flow_id=10,stage_id=1)
    # # print(type(sk.stage_value))
    sk.insert_stage()
    return sk.define_stage()