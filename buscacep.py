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
    comando = ":cep "
    _, text = p.packet.read('is')
    link = ""
    if text.startswith(comando):
        link = f"https://viacep.com.br/ws/{text}/json/"
        link = link.replace(comando, "")
        requisicao = requests.get(link)
        if requisicao.status_code != 200:
            return
        dic_requisicao = requisicao.json()
        talk(dic_requisicao["logradouro"])
        talk(dic_requisicao["localidade"])
        talk(dic_requisicao["uf"])

def talk(message):
    ext.send_to_server(HPacket("Chat", message, 0))

ext.intercept(Direction.TO_CLIENT, buscacep, "Chat")
