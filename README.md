from g_python.gextension import Extension
from g_python.hmessage import Direction, HMessage
from g_python.hpacket import HPacket
from g_python import hparsers
from g_python import htools
from time import sleep

import sys
import requests

extension_info = {
    "title": "GViaCEP",
    "description": "Digite um CEP para usar.",
    "version": "1.0",
    "author": "Jonas BH"
}

ext = Extension(extension_info, sys.argv)
ext.start()


def buscacep(p):
    text, _, _ = p.packet.read('sii')
    link = f"https://viacep.com.br/ws/{text}/json/"
    if text.startswith(text):
        requisicao = requests.get(link)
        dic_requisicao = requisicao.json()
        p.is_blocked = True
        talk(dic_requisicao["logradouro"])
        talk(dic_requisicao["localidade"])
        talk(dic_requisicao["uf"])

def talk(message):
    ext.send_to_server(HPacket("Chat", message, 0))

ext.intercept(Direction.TO_SERVER, buscacep, "Chat")
