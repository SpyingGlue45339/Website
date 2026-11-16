#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
python -m pygbag --build --ume_block=1 --title "Totally Accurate Spaceflight Simulator" Llama_Space_Programme
printf '\nBuild complete. Web files: Llama_Space_Programme/build/web/\n'
printf 'Copy the CONTENTS of that folder into Website/TASS/game/.\n'
