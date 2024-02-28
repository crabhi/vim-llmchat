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
    SKIP_LINE = re.compile(r'^\s*(#.*|$)')
    OPTION_LINE = re.compile(r'^\s*([a-zA-Z0-9]+)\s+([^\s]+)$')
    OPTIONS = ['model']
    SYSTEM_LINE = re.compile(r'^\s*SYSTEM:\s*(.*?)\s*$')

    def __init__(self, buf):
        self.buf = buf
        self.line = 0
        self.char = 0
        self.options = {'model': 'gpt-3.5-turbo'}
        self.messages = []
        self.errors = []

    def start(self):
        self.parse_options()
        self.parse_system()
        self.parse_conversation()

    def parse_options(self):
        while self.line < len(self.buf):
            line = self.buf[self.line]
            self.line += 1
            if self.SKIP_LINE.match(line):
                continue

            if m := self.OPTION_LINE.match(line):
                if m.group(1).lower() in self.OPTIONS:
                    self.options[m.group(1).lower()] = m.group(2)
                    continue
                else:
                    self.errors.append((self.line, f'Unknown option {m.group(1)}'))
            else:
                self.line -= 1
                break

    def parse_system(self):
        system_message = []
        line = self.buf[self.line]
        self.line += 1
        if m := self.SYSTEM_LINE.match(line):
            system_message.append(m.group(1))
        else:
            self.line -= 1
            return


        while not line.startswith('>') and self.line < len(self.buf):
            line = self.buf[self.line]
            self.line += 1
            if line.startswith('>'):
                self.line -= 1
                break
            system_message.append(line.strip())
            line = self.buf[self.line]

        self.messages.append({'role': 'system', 'content': '\n'.join(system_message)})

    def parse_conversation(self):
        while self.line < len(self.buf):
            line = self.buf[self.line]
            self.line += 1

        if line.strip()









def communicate():
    for line in vim.current.buffer:
        print(line, vim.current.buffer[0])

communicate()

# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))
# print(dir(vim.current.buffer))
