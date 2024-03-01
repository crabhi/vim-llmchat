if exists("b:current_syntax")
    finish
endif

let b:current_syntax = "llmchat"

syntax keyword llmchatKeyword MODEL nextgroup=llmchatKeywordValue
syntax match llmchatKeywordValue "[^\n]*" contained

syntax match llmchatSystemStart "^\s*SETUP:" nextgroup=llmchatSystemPrompt
syntax match llmchatSystemPrompt "[^>].*" nextgroup=llmchatSystemPrompt contained
syntax match llmchatComment "\s*#.*$"


syntax match llmchatUser "^\s*>.*$"

highlight link llmchatKeyword Question
highlight link llmchatKeywordValue String
highlight link llmchatUser Define
highlight link llmchatSystemStart Question
highlight link llmchatSystemPrompt Special
highlight link llmchatComment Comment
