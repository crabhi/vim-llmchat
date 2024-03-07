# vim-llmchat

Editable interactive chat with large language models directly in your editor

Unlike some other tools, this plugin uses the buffer directly. Therefore
your conversations can be immediately saved and edited. You can even edit
the chatbot's responses in order to alter the flow of your dialogue.

[![asciicast](https://asciinema.org/a/vdXK5VNZUcXKROPbhVGy7JY9Z.svg)](https://asciinema.org/a/vdXK5VNZUcXKROPbhVGy7JY9Z)

## Installation

With [pathogen](https://github.com/tpope/vim-pathogen), just

    git clone https://github.com/crabhi/vim-llmchat ~/.vim/bundle/vim-llmchat

The plugin also needs the Python OpenAI module

    pip3 install --user openai

It's recommended to map the `llmchat#send()` call to a key sequence. For example
add this into your `~/.vimrc`:

    autocmd FileType llmchat nnoremap <buffer> <C-J> :call llmchat#send()<CR>


## Usage

The plugin works with `llmchat` filetype. You can either open a file named
`something.llmchat` or do `:set ft=llmchat` in any buffer.

The file structure starts with options. Currently, the only supported option
is the model name. The default value is `gpt-3.5-turbo`.

```
MODEL gpt-4-turbo-preview
```

Then, you can modify the chatbot's "personality" with a system prompt.

```
SETUP: You're a mean, mean and evil movie character.
```

What follows is a dialogue where your prompts are started with `>` and the chatbot's
replies are simply printed as paragraphs.

```
> Hi!
```

Now, when you press `CTRL+Enter` (assuming you set your vimrc as recommended above),
the robot will paste the reply below.

```
Hello there. Prepare to face my wrath.
```


The full example file `test.llmchat`:

```
MODEL gpt-3.5-turbo

SETUP: You're a mean, mean and evil movie character.

> Hi!

Hello there. Prepare to face my wrath.

>
```

This is still a plain text file. You can copy, paste, modify anything. Enjoy!

## Supported providers

Only OpenAI at the moment
