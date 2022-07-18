# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer
#import arcobattery

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),


# SUPER + SHIFT KEYS

    Key([mod, "shift"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
   # Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    ]

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

keys.extend([
    # MOVE WINDOW TO NEXT SCREEN
    Key([mod,"shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod,"shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
    # SWITCH FOCUS TO NEXT SCREEN
    Key([mod,"shift"], "m" , lazy.next_screen()),
])

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ]

# FOR AZERTY KEYBOARDS
#group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

#group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
#group_labels = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", ]
group_labels = ["  ", " 3 ", "  ", " g  ", "  ", "  ", " 8 ", " 7 ", "  ", " ~ ", ]
# group_labels = ["  ", "  ", "  ", "  ",
#                "  ", "  ", "  ", "  ", "  ", "  ", ]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["ratiotile", "monadtall", "monadtall", "ratiotile",
                 "ratiotile", "spiral", "max", "ratiotile", "monadtall", "monadtall", ]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "max", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.next_screen()),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

# THEMING & COLORING FOR WINDOW BORDERS
def init_layout_theme():
    return {"margin":6,
            "border_width":4,
            "border_focus": "#1fff48",
            "border_normal": "#35aa68"
            }

layout_theme = init_layout_theme()


layouts = [
    # layout.MonadTall(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
    layout.VerticalTile(**layout_theme),
    layout.Spiral(**layout_theme),
    layout.Stack(**layout_theme),
    layout.Tile(**layout_theme),
    # layout.Zoomy(**layout_theme)
]

# COLORS FOR THE BAR
#Theme name : ArcoLinux Default
def init_colors():
#    return [["#2F343F", "#2F343F"], # color 0
#            ["#2F343F", "#2F343F"], # color 1
#            ["#c0c5ce", "#c0c5ce"], # color 2
#            ["#fba922", "#fba922"], # color 3
#            ["#3384d0", "#3384d0"], # color 4
#            ["#f3f4f5", "#f3f4f5"], # color 5
#            ["#cd1f3f", "#cd1f3f"], # color 6
#            ["#62FF00", "#62FF00"], # color 7
#            ["#6790eb", "#6790eb"], # color 8
#            ["#a9a9a9", "#a9a9a9"]] # color 9

    return [["#2F343F", "#2F343F"], # color 0
            ["#2F343F", "#2F343F"], # color 1
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#fba922", "#fba922"], # color 3
            ["#3384d0", "#3384d0"], # color 4
            ["#f3f4f5", "#f3f4f5"], # color 5
            ["#cd1f3f", "#cd1f3f"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#6790eb", "#6790eb"], # color 8
            ["#a9a9a9", "#a9a9a9"]] # color 9

colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize=28,
                padding=16,
                background=colors[1])


widget_defaults = init_widgets_defaults()


def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
        # widget.AGroupBox(
        #    foreground=colors[2],
        #    background=colors[1],
        #    center_aligned=True,
        #    borderwidth=0,
        #    padding_x=-20,
        #    margin_x=20,
        # ),
        # widget.Sep(
        #    linewidth=2,
        #    foreground=colors[2],
        #    background=colors[1]
        # ),
        # widget.CurrentScreen(),
        # widget.Sep(
        #    linewidth=2,
        #    foreground=colors[2],
        #    background=colors[1]
        # ),
        widget.CurrentLayoutIcon(
            scale=0.45,
        ),
        widget.Spacer(
            length=bar.STRETCH,
        ),
        # widget.Sep(
        #    linewidth=2,
        #    foreground=colors[2],
        #    background=colors[1]
        # ),
        # widget.CurrentLayout(
        #    foreground=colors[5],
        #    background=colors[1]
        # ),
        # widget.Sep(
        #    linewidth=2,
        #    foreground=colors[2],
        #    background=colors[1]
        # ),
        #widget.WindowName(
        #    foreground=colors[5],
        #    background=colors[1]
        #),
        widget.GroupBox(font="dripicons-v2",
                        margin_y=2,
                        margin_x=8,
                        padding_y=6,
                        padding_x=4,
                        borderwidth=0,
                        disable_drag=True,
                        active=colors[9],
                        inactive=colors[5],
                        rounded=False,
                        highlight_method="text",
                        this_current_screen_border=colors[8],
                        foreground=colors[2],
                        background=colors[1]
                        ),
        widget.Spacer(
            length=bar.STRETCH,
        ),
        widget.TextBox(
            font="dripicons-v2",
            text=""
        ),
        widget.CPU(
            format="{freq_current}GHz  @",
            update_interval=1,
            padding=0,
        ),
        widget.ThermalZone(
            padding = 16,
            high=70,
            crit=90,
        ),
        #widget.NvidiaSensors(
        #    foreground_alert="ff0000",
        #    format="GPU {temp}°C",
        #),
        #widget.Sep(
        #    linewidth=2,
        #    foreground=colors[2],
        #    background=colors[1]
        #),
        #widget.Sep(
        #    padding=10,
        #    linewidth=2,
        #    foreground=colors[2],
        #    background=colors[1]
        #),
        widget.Sep(
            linewidth=2,
            foreground=colors[2],
            background=colors[1]
        ),
        widget.Wttr(
            lang='de',
            location={
                'Lüneburg': 'Lüneburg',
                # '53.239177,10.282547': 'Lüneburg',
                # '64.127146,-21.873472': 'Reykjavik',
                # '~Vostok Station': 'Nice place',
            },
            format='%M %m',
            #format='%t  %w  %h  %p  %P  %M %m',
            units='m',
            update_interval=10,
        ),
        widget.Sep(
            linewidth=2,
            foreground=colors[2],
            background=colors[1]
        ),
        widget.Clock(
            foreground=colors[5],
            background=colors[1],
            format="%d.%m.%y  /  %H:%M"
        ),
        
    ]
    return widgets_list


def init_widgets_list_2():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list_2 = [
        # widget.AGroupBox(
        #    foreground=colors[2],
        #    background=colors[1],
        #    center_aligned=True,
        #    borderwidth=0,
        #    padding_x=-20,
        #    margin_x=20,
        # ),
        # widget.Sep(
        #    linewidth=2,
        #    foreground=colors[2],
        #    background=colors[1]
        # ),
        # widget.CurrentScreen(),
        # widget.Sep(
        #    linewidth=2,
        #    foreground=colors[5],
        #    background=colors[1]
        # ),
        widget.CurrentLayoutIcon(
            scale=0.45,
        ),
        widget.CPUGraph (
            
        ),
        #widget.NvidiaSensors(
        #    format="{temp}°C {fan_speed}"
        #),
        widget.Spacer(
            length=bar.STRETCH,
        ),
        # widget.CurrentLayout(
        #    foreground=colors[5],
        #    background=colors[1]
        # ),
        # widget.Sep(
        #    linewidth=2,
        #    foreground=colors[2],
        #    background=colors[1]
        # ),
        #widget.WindowName(
        #    foreground=colors[5],
        #    background=colors[1]
        #),
        widget.GroupBox(font="dripicons-v2",
                        margin_y=2,
                        margin_x=8,
                        padding_y=6,
                        padding_x=4,
                        borderwidth=0,
                        # hide_unused=True,
                        disable_drag=True,
                        active=colors[9],
                        inactive=colors[5],
                        rounded=False,
                        highlight_method="text",
                        this_current_screen_border=colors[8],
                        foreground=colors[2],
                        background=colors[1]
                        ),
        widget.Spacer(
            length=bar.STRETCH,
        ),
        widget.Systray(
            background=colors[1],
            icon_size=32,
        ),
        widget.Spacer(
            length=12,
        ),
    ]
    return widgets_list_2

widgets_list = init_widgets_list()
widgets_list_2 = init_widgets_list_2()

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list_2()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=48, opacity=0.8)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=48, opacity=0.8))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    # Press Mod and use Primary (usually left) click to drag a window in floating mode
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    # Press Mod and drag using Secondary (usually right) click to resize a floating window 
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]
dgroups_key_binder = None
dgroups_app_rules = [
    #Rule(Match(wm_class=["firefox"]), group="1"),
    Rule(Match(wm_class=["Code", "code", "emacs" ]), group="2"),
    Rule(Match(wm_class=["firefoxdeveloperedition", "github desktop", "devdocs-desktop"]), group="3"),
    Rule(Match(wm_class=["Obsidian", "obsidian"]), group="4"),
    Rule(Match(wm_class=["ferdium", "Ferdium", "whatsapp-nativefier-d40211", "telegram-desktop", "discord", "zoom "]), group="5"),
    Rule(Match(wm_class=["ticktick", "superproductivity", "Morgen", "morgen"]), group="6"),
    Rule(Match(wm_class=["Inkscape", "Gimp", "Figma", "inkscape", "gimp", "figma"]), group="7"),
    Rule(Match(title=["Figma", "figma", "figma-linux", "Figma-Linux", ]), group="7"),
    Rule(Match(wm_class=["Libreoffice", "libreoffice", "DesktopEditors"]), group="8"),
    #Rule(Match(wm_class=["spotify", "Spotify"]), group="9"),
    #Rule(Match(title=["Spotify"]), group="9"),
    #Rule(Match(net_wm_pid="4000"), group="9"),
    #Rule(Match(wm_instance_class=["spotify"]), group="9"),
    #Rule(Match(wid=["0x6800004"]), group="9"),
    #Rule(Match(wm_name=["spotify", "Spotify"]), group="9"),
    #Rule(Match(wm_name=["Spotify",]), group="8"),
    Rule(Match(wm_class=["pamac-manager", "archlinux-tweak-tool"]), group="0"),
]
# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME



main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules, 
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    #Match(wm_class='Archlinux-tweak-tool.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    #Match(wm_class='archlinux-logout'),
    Match(wm_class='xfce4-terminal'),

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
