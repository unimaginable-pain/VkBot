import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
from optparse import OptionParser
from configparser import ConfigParser
import os
from classes import *
from methods import *

# option parser
parser = OptionParser()
parser.add_option("-c", "--config", metavar="FILE", dest="CONFIGFILE", help="override standard config file (vkbot.ini)")
parser.add_option("-m", "--mode", metavar="public/private", dest="BOTMODE", help="is other users able to use commands?", default="private")

# parse arguments, get config file
(OPTIONS, ARGUMENTS) = parser.parse_args()
CFGFILE = "vkbot.ini"
is_public = OPTIONS.BOTMODE == "public"
if f := OPTIONS.CONFIGFILE:
    CFGFILE = f
# if config file doesn't exist0
if not os.path.exists(CFGFILE):
    print("Error: config file \"%s\" does not exist." % CFGFILE)
    exit()

# read config file and get methods file
cfg = ConfigParser()
cfg.read(CFGFILE)
METHODTABLE = cfg["Core"]["methods"]

# get api and longpoll
session = vk_api.VkApi(token=cfg["Core"]["token"])
vk = session.get_api()
lp = VkLongPoll(session)

# if methods.json doesn't exist
if not os.path.exists(METHODTABLE):
    print("Error: method definition file \"%s\" does not exist." % METHODTABLE)
    exit()

TABLE = json.load(open(METHODTABLE, 'r', encoding="utf-8"))
SYMTABLE = {}

for ACTION in TABLE:
    result = None
    match ACTION["function"]["type"]:
        case "web-get":
            t_func = ACTION["function"]
            SYMTABLE[ACTION["command"]] = AutoFormatter(WebGetter(t_func["url"], t_func["result_json"], t_func["json_layers"], t_func["json_domains"]),
                                                        ACTION["responce_text"])
        # TODO: implement more, like math, random, etc.

for event in lp.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if not is_public and not event.from_me:
            continue
        if event.text.startswith("/"):
            cend = event.text.find(' ')
            if cend < 1:
                msg = event.text[1:]
            else:
                msg = event.text[1:cend]
            if not (msg in SYMTABLE):
                vk.messages.edit(peer_id=event.peer_id, message_id=event.message_id,
                                        message=("%s\n===\nError: command \"%s\" does not exist." % (event.text, msg)))
            result = SYMTABLE[msg]()
            vk.messages.edit(peer_id=event.peer_id, message_id=event.message_id,
                            message=event.text + "\n===\n" + SYMTABLE[msg]())

