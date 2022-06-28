#!/usr/bin/env bash

# GIT FUNCTIONS
git_branch() {
    git branch 2>/dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
# TERMINAL PROMP
PS1="\[\e[0;93m\]\u\[\e[m\]@\h"    # username
PS1+=" "    # spac
PS1+="(\[\e[0;95m\]\W\[\e[m\])"    # current directory
PS1+="\[\e[0;92m\]\$(git_branch)\[\e[m\]"    # current branch
PS1+=" "    # space
PS1+="\n" # new line
PS1+="$ "    # end prompt
export PS1;
export CLICOLOR=1
export LSCOLORS=ExFxBxDxCxegedabagacad
