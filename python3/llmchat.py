import vim
import os
from pathlib import Path
import re
import sys

import openai

CONF_DIR = Path.home() / '.config/vim-llmchat'
APIKEY_FILE = CONF_DIR / 'apikey.txt'


def get_api_key():
    if not CONF_DIR.exists():
        CONF_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)

    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        return api_key

    try:
        import keyring

        key = keyring.get_password('vim-llmchat', 'openai')
        if key:
            return key

        pref_storage = 'keyring'
    except ImportError:
        pref_storage = 'file'

    if APIKEY_FILE.exists():
        return APIKEY_FILE.read_text('utf-8').strip()

    key = None
    while not (key and key.strip()):
        key = vim.eval('input("Enter your OpenAI API key from https://platform.openai.com/api-keys: ")')

    if pref_storage == 'keyring':
        keyring.set_password('vim-llmchat', 'openai', key.strip())
    else:
        APIKEY_FILE.write_text(key.strip() + '\n', 'utf-8')

    return key.strip()


class Parser:
    SKIP_LINE = re.compile(r'^\s*(#.*|$)')
    OPTION_LINE = re.compile(r'^\s*([a-zA-Z0-9]+)\s+([^\s]+)$')
    OPTIONS = ['model']
    SYSTEM_LINE = re.compile(r'^\s*SETUP:\s*(.*?)\s*$')
    USER_LINE = re.compile(r'^\s*>\s*(.*)$')

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
            if self.SKIP_LINE.match(line):
                continue
            if self.USER_LINE.match(line):
                self.line -= 1
                break
            system_message.append(line.strip())
            line = self.buf[self.line]

        self.messages.append({'role': 'system', 'content': '\n'.join(system_message)})

    def parse_conversation(self):
        role = 'user'
        message_lines = []
        while self.line < len(self.buf):
            line = self.buf[self.line]
            self.line += 1

            if self.SKIP_LINE.match(line):
                continue

            if user_line_match := self.USER_LINE.match(line):
                new_role = 'user'
                line = user_line_match.group(1)
            else:
                new_role = 'assistant'

            if role != new_role and message_lines:
                self.messages.append({'role': role, 'content': '\n'.join(message_lines)})
                message_lines = []
                role = new_role

            if role == 'user' and not user_line_match:
                self.errors.append((self.line, 'Expected the conversation to start with '
                                               f'user prompt - ">" symbol. Got {line}'))
            else:
                message_lines.append(line)

        if message_lines:
            self.messages.append({'role': role, 'content': '\n'.join(message_lines)})



def communicate():
    p = Parser(vim.current.buffer)
    p.start()

    if p.errors:
        vim.command('let s:errors = []')
        vim_errors = vim.bindeval('s:errors')
        for line, error in p.errors:
            vim_errors.extend([vim.Dictionary(
                bufnr=vim.current.buffer.number,
                lnum=line,
                text=error,
                type='e',
            )])
        vim.command('echo s:errors')
        vim.command("call setqflist([], 'a', {'items': s:errors, 'title': 'Errors'})")
        vim.command('copen')
        return

    vim.command('cclose')

    client = openai.OpenAI(api_key=get_api_key())

    try:
        stream = client.chat.completions.create(
          stream=True,
          model=p.options['model'],
          messages=p.messages
        )
    except openai.APIError as e:
        print(f'{e.type}: {e.body.get("message")}', file=sys.stderr)
        return

    buf = vim.current.buffer
    if buf[-1].strip():
        # Extra newline to separate response
        buf.append('')
    buf.append('')

    generated = False
    for chunk in stream:
        textchunk = chunk.choices[0].delta.content or ''
        for i, line in enumerate(textchunk.split('\n')):
            if i > 0:
                buf.append('')
            buf[-1] += line
        generated = True
        vim.current.window.cursor = len(buf), len(buf[-1])
        vim.command('redraw')

    if generated:
        buf.append('')
        buf.append('> ')
        vim.current.window.cursor = len(buf), len(buf[-1])
