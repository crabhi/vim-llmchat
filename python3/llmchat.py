import vim
import os
import re

from openai import OpenAI


def get_api_key():
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        return api_key

    import keyring
    # TODO keyring integration


class Parser:
    OPTIONS = ['MODEL']

    def __init__(self, buf):
        self.buf = buf
        self.line = 0
        self.char = 0
        self.options = {'model': 'gpt-3.5-turbo'}
        self.messages = []

    def start(self):
        if m := self.buf[self.line]


def communicate():
    for line in vim.current.buffer:
        print(line, vim.current.buffer[0])

communicate()

# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))
# print(dir(vim.current.buffer))
