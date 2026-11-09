# -*- coding: utf-8 -*-
# BombSquad API 9 - Party Window Menu
# Intended for API 9 builds (for example 1.7.37+).
# Save as party_menu_api9.py in the game's mods folder.

from __future__ import annotations

import os
import ba
import bauiv1 as bui


def _mods_dir():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except Exception:
        return os.path.join(os.path.expanduser('~'), 'BombSquad', 'mods')


def _screen(message):
    try:
        ba.screenmessage(message, color=(0.4, 1.0, 0.5), transient=True)
    except Exception:
        print(message)


def _open_folder():
    path = _mods_dir()
    try:
        if os.path.isdir(path) and hasattr(os, 'startfile'):
            os.startfile(path)
            _screen('Mods folder opened')
        else:
            _screen('Mods folder: ' + path)
    except Exception as exc:
        _screen('Cannot open folder: ' + str(exc))


def _plugin_manager():
    path = _mods_dir()
    try:
        files = sorted(f for f in os.listdir(path) if f.lower().endswith('.py'))
    except Exception:
        files = []
    listing = '\n'.join(files[:35]) if files else 'No Python mod files found.'
    bui.BasicWindow(
        root_widget=bui.containerwidget(
            size=(520, 420),
            transition='in_scale',
            scale=1.0,
            stack_offset=(0, 0)),
        transition='in_scale')
    bui.screenmessage('Plugin Manager: ' + str(len(files)) + ' Python files found',
                      color=(0.4, 1.0, 0.5), transient=True)
    bui.confirm(
        'Mods folder:\n' + path + '\n\n' + listing +
        '\n\nUse a file manager to add, remove, or edit .py mods.',
        ok_text='Open folder',
        cancel_text='Close',
        action=_open_folder)


def _about():
    bui.confirm(
        'Party Menu for BombSquad\nAPI 9 edition\n\n'
        'Plugin Manager lists .py files in the mods folder. '
        'It does not execute arbitrary files or enable/disable mods; '
        'use the game mod loader for that.',
        ok_text='OK')


def _show_menu():
    choices = ['Plugin Manager', 'Mods Folder', 'About']
    bui.PopupMenuWindow(
        position=(300, 200),
        scale=1.0,
        choices=choices,
        current_choice='Plugin Manager',
        delegate=_MenuDelegate())


class _MenuDelegate:
    def get_popup_menu_selected_choice(self, popup_window, choice):
        if choice == 'Plugin Manager':
            _plugin_manager()
        elif choice == 'Mods Folder':
            _open_folder()
        elif choice == 'About':
            _about()


def _patch_party_window():
    # API 9 UI classes live in bauiv1. Keep patch guarded against duplicate loads.
    party_cls = getattr(bui, 'PartyWindow', None)
    if party_cls is None or getattr(party_cls, '_party_menu_api9_patched', False):
        return

    original_init = party_cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        try:
            root = getattr(self, '_root_widget', None)
            if root is None:
                root = getattr(self, '_rootWidget', None)
            if root is None:
                return
            bui.buttonwidget(
                parent=root,
                position=(20, 65),
                size=(150, 42),
                label='MOD MENU',
                color=(0.15, 0.55, 0.32),
                textcolor=(1, 1, 1),
                scale=0.8,
                on_activate_call=_show_menu)
        except Exception as exc:
            print('Party Menu API9 button error:', exc)

    party_cls.__init__ = new_init
    party_cls._party_menu_api9_patched = True


try:
    _patch_party_window()
except Exception as exc:
    print('Party Menu API9 load error:', exc)
