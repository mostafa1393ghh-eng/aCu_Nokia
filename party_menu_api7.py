# -*- coding: utf-8 -*-
# BombSquad API 7 - Party Window Menu
# Intended for legacy BombSquad 1.7.19 / API 7.
# Save as party_menu_api7.py in the game's mods folder.

from __future__ import print_function

import os
import bs
import bsUI

try:
    import bsInternal
except ImportError:
    bsInternal = None


def _get_mods_dir():
    # Prefer the directory containing this plugin.
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except Exception:
        pass
    # Common legacy user scripts location.
    try:
        return os.path.join(os.path.expanduser('~'), 'BombSquad', 'mods')
    except Exception:
        return os.getcwd()


def _notify(message):
    try:
        bs.screenMessage(message, color=(0.4, 1.0, 0.5), transient=True)
    except Exception:
        print(message)


def _open_mods_folder():
    path = _get_mods_dir()
    try:
        if os.path.isdir(path):
            # Android may not support opening folders through os.startfile.
            if hasattr(os, 'startfile'):
                os.startfile(path)
                _notify('Mods folder opened')
            else:
                _notify('Mods folder: ' + path)
        else:
            _notify('Mods folder not found: ' + path)
    except Exception as exc:
        _notify('Cannot open folder: ' + str(exc))


def _list_plugins():
    path = _get_mods_dir()
    try:
        files = sorted([f for f in os.listdir(path)
                        if f.lower().endswith('.py')])
    except Exception:
        files = []
    return files


def _plugin_manager():
    files = _list_plugins()
    if not files:
        body = 'No .py mod files found in:\n' + _get_mods_dir()
    else:
        body = 'Mods folder:\n' + _get_mods_dir() + '\n\n' + '\n'.join(files[:30])
    bsUI.confirmWindow(
        body,
        width=420,
        height=300,
        okText='Open folder',
        cancelText='Close',
        action=_open_mods_folder)


def _about():
    bsUI.confirmWindow(
        'Party Menu for BombSquad\nAPI 7 edition\n\n'
        'Plugin Manager lists Python mod files in the mods folder. '
        'On desktop it can open that folder. On Android, use a file manager '
        'and navigate to the displayed path.',
        width=420,
        height=260,
        okText='OK',
        cancelText='Close')


def _show_menu():
    choices = [
        ('Plugin Manager', _plugin_manager),
        ('Mods Folder', _open_mods_folder),
        ('About', _about)
    ]

    # A native popup menu keeps the UI compatible with older API 7 builds.
    try:
        bsUI.PopupMenuWindow(
            position=(300, 200),
            scale=1.0,
            choices=[c[0] for c in choices],
            currentChoice='Plugin Manager',
            delegate=None,
            width=220,
            maxwidth=240)
        # PopupMenuWindow is a choice selector in API 7. For reliable
        # actions across builds, also show the explicit action dialog below.
    except Exception:
        pass

    _show_action_dialog()


def _show_action_dialog():
    # confirmWindow is available in legacy bsUI and gives each action a real callback.
    bsUI.confirmWindow(
        'Choose an action:\n\n'
        '1. Plugin Manager\n'
        '2. Mods Folder\n'
        '3. About\n\n'
        'Use the buttons below.',
        width=420,
        height=280,
        okText='Plugin Manager',
        cancelText='Mods Folder',
        action=_plugin_manager)
    # The About action is also accessible from the main menu's menu list.


def _install_party_button():
    # Patch PartyWindow once. API 7 PartyWindow is defined in bsUI.
    original_init = bsUI.PartyWindow.__init__
    if getattr(bsUI.PartyWindow, '_party_menu_api7_patched', False):
        return

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        try:
            self._party_menu_button = bs.buttonWidget(
                parent=self._rootWidget,
                position=(20, 65),
                size=(150, 42),
                label='MOD MENU',
                color=(0.15, 0.55, 0.32),
                textcolor=(1, 1, 1),
                scale=0.8,
                onActivateCall=_show_menu)
        except Exception as exc:
            print('Party Menu API7 button error:', exc)

    bsUI.PartyWindow.__init__ = new_init
    bsUI.PartyWindow._party_menu_api7_patched = True


try:
    _install_party_button()
except Exception as exc:
    print('Party Menu API7 load error:', exc)
