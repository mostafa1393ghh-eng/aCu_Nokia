BombSquad Party Menu - API 7 and API 9
=========================================

Files:
- party_menu_api7.py : legacy API 7 builds (commonly BombSquad 1.7.19)
- party_menu_api9.py : API 9 builds (commonly BombSquad 1.7.37+)

IMPORTANT:
These are separate files. Install ONLY the file matching your game's API.
Do not install both together.

What the menu provides:
- MOD MENU button patch attempt in Party Window
- Plugin Manager: lists .py files in the mod folder
- Mods Folder: shows the folder path and opens it on desktop where supported
- About: displays usage notes

Limitations:
- Android Python environments often cannot open a folder directly from a game.
  In that case the menu displays the path; open it with your Android file manager.
- This Plugin Manager is a safe file-listing/access helper. It does not load,
  execute, enable, or disable arbitrary plugins.
- BombSquad forks/custom builds can change PartyWindow internals and UI method
  signatures. If the button does not appear, send the exact game version and
  the startup error log so the patch can be adapted to that build.
