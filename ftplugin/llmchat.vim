vim9script

function llmchat#send()
    echo "aaa"
    python3 import importlib
    python3 importlib.reload(llmchat)

    python3 llmchat.communicate()
endf

python3 import llmchat

