#!/bin/bash

color_red=$(tput setaf 1)
color_green=$(tput setaf 2)
color_yellow=$(tput setaf 3)
color_normal=$(tput sgr0)
setopt aliases


required_python_version_path_name="3.11"
required_python_version="3.11.6"

if [ $UID -eq 0 ]; then
    printf "%s\n" "${color_red}ERROR:${color_normal}Please DO NOT run this script with sudo"
    return 1
fi

cp git-hooks/commit-msg ./.git/hooks 
cp git-hooks/pre-commit ./.git/hooks

current_python_version=$(python -V | sed 's/Python //;s/+//')
if ! dpkg --compare-versions "$current_python_version" eq "$required_python_version";then
    printf "%s\n" ""
    printf "%s\n" "${color_red}ERROR${color_normal}: Current Python is $current_python_version but $required_python_version required"
    printf "%s\n" ""
    return 1
fi

python -m venv "$HOME"/venv/vespricetracker
# shellcheck source=/dev/null
. "$HOME"/venv/vespricetracker/bin/activate
if [ "$VIRTUAL_ENV" != "$HOME"/venv/vespricetracker ]; then
    printf "%s\n" ""
    printf "%s\n" "${color_red}ERROR${color_normal}: Attempted to set venv to: $HOME/venv/vespricetracker but current venv is $VIRTUAL_ENV"
    printf "%s\n" ""
    return 1
fi
pip install -r requirements.txt

export PYTHONPATH=$VIRTUAL_ENV/lib/python"$required_python_version_path_name"/site-packages/


printf "%s\n" "${color_yellow}ATTENTION:${color_normal} Need sudo to install Google Chrome"
sudo mkdir -p /usr/share/keyrings && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list && \
    sudo apt-get update && \
    sudo apt-get install -y google-chrome-stable && \
    sudo rm -rf /var/lib/apt/lists/*
