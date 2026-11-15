#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python -m pygbag --build --title "Totally Accurate Spaceflight Simulator" Llama_Space_Programme
printf '\nBuild complete. Web files: Llama_Space_Programme/build/web/\n'
printf 'Copy the CONTENTS of that folder into your website game/ directory.\n'
