TOTALLY ACCURATE SPACEFLIGHT SIMULATOR - PHASE 1 UI + AUDIO STABILITY UPDATE
================================================================================

CHANGES
-------
1. Removed the Phase 1 footer instruction advertising the G gambling key.
2. Removed the G-key event handler. Gambling remains available through the
   existing clickable sign; shop navigation and Escape behaviour are unchanged.
3. Increased the shared SDL mixer buffer from 2048 to 4096 samples in both
   startup and the audio manager. This gives browser audio more tolerance for
   frame-time spikes during the busier Phase 1 and Phase 3 scenes.
4. Kept the shared mixer architecture and existing audio assets/tracks intact.

INSTALL / BUILD
---------------
Stop the old server with Ctrl+C, replace the old Llama_Space_Programme folder
with the one in this archive, then run from Website/TASS:

  python -m pygbag --ume_block=1 --title "Totally Accurate Spaceflight Simulator" Llama_Space_Programme

Open http://localhost:8000.

NOTES
-----
- The clickable Gambling sign remains; only the G keyboard shortcut and its
  on-screen keyboard instruction have been removed.
- A larger mixer buffer can reduce audio underruns, but cannot compensate for
  severe browser/CPU stalls. Actual browser playback still needs testing.
