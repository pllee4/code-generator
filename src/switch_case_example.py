''' 
   switch_case_example.py
   Created on: Jun 05, 2021 19:18
   Description: 
   
   Copyright (c) 2021 Pin Loon Lee (pllee4)
 ''' 
 
import os.path
import sys
import cfile as C

FILE_NAME = "switch_case_generated.c"
FILE_PATH_NAME = os.path.dirname(__file__) + "/../generated_code/" + FILE_NAME

MESSAGE_FILE_NAME = "switch_case_message"
MESSAGE_FILE_PATH_NAME = os.path.dirname(__file__) + "/../file/" + MESSAGE_FILE_NAME

generated = C.cfile(FILE_NAME)
generated.code.append(C.sysinclude("stdio.h"))
generated.code.append(C.blank())

FUNCTION_NAME = "DecodePllee4Transfer"
MESSAGE_NAME = "Pllee4"

## Function
generated.code.append(
    C.function(
        FUNCTION_NAME,
        "bool",
    )
    .add_param(C.variable("transfer", "const Pllee4Transfer", pointer=1))
    .add_param(C.variable(MESSAGE_NAME + "Message", "msg", pointer=1))
)
## Function body
body = C.block(innerIndent=3)
body.append(C.statement("bool decode_status = false"))
body.append(C.statement("msg->type = " + MESSAGE_NAME + "MsgUnknown"))

## Switch case body
switch_case_body = C.block(head="switch(transfer->port_id)")
all_case_body = C.block()

file = open(MESSAGE_FILE_PATH_NAME, "r")
message = file.readlines()
## Message case body
for line in message:
    msg = line.strip()
    small_leters = msg.lower()
    seperator_index = small_leters.find("_")
    removed_seperator = small_leters.replace("_", "")
    capitalized_letters = (
        removed_seperator[:seperator_index].capitalize()
        + removed_seperator[seperator_index:].capitalize()
    )
    message_case_body = C.block(
        innerIndent=3, head="case " + MESSAGE_NAME.upper() + "_" + msg + "_ID:"
    )
    message_case_body.append(
        C.statement("msg->type = " + MESSAGE_NAME + "Msg" + capitalized_letters)
    )
    function_body = C.statement(
        C.fcall(
            "decode_status = DecodeTransfer",
            args=[
                capitalized_letters,
                "&msg->body." + msg.lower() + "_" + MESSAGE_NAME.lower(),
                "(uint8_t *)(transfer->payload)",
                "transfer->payload_size",
            ],
        )
    )
    message_case_body.append(function_body)
    message_case_body.append(C.statement("break"))
    all_case_body.append(message_case_body)

switch_case_body.append(all_case_body)

switch_case_body.append(C.statement("default: break"))

body.append(switch_case_body)
body.append(C.statement("return decode_status"))

generated.code.append(body)
sys.stdout = open(FILE_PATH_NAME, "w")
print(str(generated))
sys.stdout.close()
