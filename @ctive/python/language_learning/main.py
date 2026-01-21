from __future__ import annotations

import os
from kivy.utils import platform as kivy_platform
from typing import Any, Dict, Optional, Tuple

import json

# Workaround: On some Windows setups Kivy's wm_pen input provider can spam
# "Exception ignored on calling ctypes callback function". Disabling it avoids
# the noise and doesn't affect typical mouse/touch usage.
os.environ.setdefault("KIVY_NO_WM_PEN", "1")

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle, Canvas
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from langtext import Lang, LangText

from vocab_learner_model import (
    ChoiceNode,
    GroupNode,
    InputNode,
    Kit,
    VocabLearnerModel,
    PracticeSession,
    PromptNode,
    collect_prompt_data,
)


# Mobile friendly keyboard behavior: keep focused input visible.
Window.softinput_mode = "pan"

# Peach theme
PEACH_BG = (1.0, 0.94, 0.91, 1)  # very light peach
PEACH_CARD = (1.0, 0.89, 0.84, 1)  # card
PEACH_ACCENT = (0.96, 0.55, 0.42, 1)  # accent button
PEACH_ACCENT_DARK = (0.88, 0.43, 0.30, 1)
PEACH_ACCENT_LIGHT = (0.98, 0.67, 0.57, 1)
TEXT_DARK = (0.25, 0.18, 0.16, 1)
TEXT_MUTED = (0.55, 0.52, 0.50, 1)

Window.clearcolor = PEACH_BG


def _resolve_data_dir(*, app_dir: str) -> str:
    """Return the directory to store user-editable data.

    Desktop: use app_dir (current behavior).
    Android: prefer external app-specific storage so users can see/edit files:
      /storage/emulated/0/Android/data/<package>/files/language_learning

    Override with env var VOCAB_DATA_DIR.
    """

    override = os.environ.get("VOCAB_DATA_DIR")
    if override:
        try:
            os.makedirs(override, exist_ok=True)
        except Exception:
            pass
        return override

    if kivy_platform == "android":
        try:
            from jnius import autoclass  # type: ignore

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            # This returns something like:
            #   /storage/emulated/0/Android/data/<package>/files
            # and is the most reliable way to locate app-specific external storage.
            ext_dir = PythonActivity.mActivity.getExternalFilesDir(None)
            if ext_dir is None:
                return app_dir

            external_files = str(ext_dir.getAbsolutePath())
            data_dir = os.path.join(external_files, "language_learning")
            os.makedirs(data_dir, exist_ok=True)
            return data_dir
        except Exception:
            # Fall back to app_dir / internal user_data_dir behavior.
            return app_dir

    return app_dir


class RoundedButton(Button):
    def __init__(self, **kwargs):
        self._fill_color = kwargs.pop("fill_color", (1, 1, 1, 1))
        self._radius = kwargs.pop("radius", dp(12))
        super().__init__(**kwargs)

        # Disable default image background; we draw our own rounded background.
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:
            self._bg_color_instr = Color(*self._fill_color)
            self._bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[(self._radius, self._radius)] * 4,
            )

        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *_):
        if hasattr(self, "_bg_rect"):
            self._bg_rect.pos = self.pos
            self._bg_rect.size = self.size

    def set_fill_color(self, rgba) -> None:
        self._fill_color = rgba
        if hasattr(self, "_bg_color_instr"):
            self._bg_color_instr.rgba = rgba


class PeachButton(RoundedButton):
    def __init__(self, **kwargs):
        super().__init__(fill_color=PEACH_ACCENT, **kwargs)
        self.color = (1, 1, 1, 1)


class PeachSecondaryButton(RoundedButton):
    def __init__(self, **kwargs):
        super().__init__(fill_color=PEACH_CARD, **kwargs)
        self.color = TEXT_DARK


class PeachIconSquare(RoundedButton):
    def __init__(self, **kwargs):
        super().__init__(fill_color=PEACH_ACCENT_LIGHT, **kwargs)
        self.color = (1, 1, 1, 1)


class OptionItemButton(RoundedButton):
    def __init__(self, text: str, *, selected: bool = False, on_release=None, **kwargs):
        self._selected = bool(selected)
        fill = PEACH_ACCENT if self._selected else PEACH_CARD
        super().__init__(text=text, fill_color=fill, **kwargs)
        self.color = (1, 1, 1, 1) if self._selected else TEXT_DARK
        if on_release is not None:
            self.bind(on_release=on_release)

    def set_selected(self, selected: bool) -> None:
        self._selected = bool(selected)
        self.set_fill_color(PEACH_ACCENT if self._selected else PEACH_CARD)
        self.color = (1, 1, 1, 1) if self._selected else TEXT_DARK


class OptionList(BoxLayout):
    """Scrollable list of option buttons with a single selected value."""

    def __init__(
        self,
        options,
        *,
        selected: Optional[str] = None,
        height: float = 0,
        on_select=None,
        **kwargs,
    ):
        super().__init__(orientation="vertical", spacing=dp(6), **kwargs)
        # If a fixed height is provided, keep it. Otherwise, let the list expand
        # to fill the remaining available space in its parent layout.
        if height:
            self.size_hint_y = None
            self.height = height
        else:
            self.size_hint_y = 1
        self.on_select = on_select
        self.selected = selected

        self._scroll = ScrollView(size_hint=(1, 1))
        self._box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(6))
        self._box.bind(minimum_height=self._box.setter("height"))
        self._scroll.add_widget(self._box)
        self.add_widget(self._scroll)

        self._buttons: Dict[str, OptionItemButton] = {}
        self.set_options(list(options), selected=selected)

    def set_options(self, options, *, selected: Optional[str] = None) -> None:
        self._box.clear_widgets()
        self._buttons = {}

        if selected is not None:
            self.selected = selected
        if self.selected not in options:
            self.selected = None

        def choose(value: str):
            self.selected = value
            for v, btn in self._buttons.items():
                btn.set_selected(v == value)
            if self.on_select:
                try:
                    self.on_select(value)
                except Exception:
                    pass

        for opt in options:
            btn = OptionItemButton(
                text=str(opt),
                selected=(opt == self.selected),
                size_hint_y=None,
                height=dp(44),
                on_release=(lambda _btn, v=str(opt): choose(v)),
            )
            self._buttons[str(opt)] = btn
            self._box.add_widget(btn)


class BackArrowSquare(PeachIconSquare):
    """Square button with a drawn left-arrow icon (no unicode text)."""

    def __init__(self, **kwargs):
        kwargs.pop("text", None)
        super().__init__(text="", **kwargs)
        self.bind(pos=self._redraw, size=self._redraw)
        self._redraw()

    def _redraw(self, *_):
        self.canvas.after.clear()
        w = float(self.width)
        h = float(self.height)
        if w <= 0 or h <= 0:
            return

        # Draw a simple left arrow with line segments
        pad = min(w, h) * 0.28
        x0 = self.x + pad
        x1 = self.right - pad
        yc = self.y + h / 2
        head = min(w, h) * 0.18

        with self.canvas.after:
            Color(1, 1, 1, 1)
            Line(
                points=[
                    x1,
                    yc,
                    x0,
                    yc,
                    x0 + head,
                    yc + head,
                    x0,
                    yc,
                    x0 + head,
                    yc - head,
                ],
                width=dp(2),
                cap="round",
                joint="round",
            )


class HamburgerSquare(PeachIconSquare):
    """Square button with a drawn hamburger icon (no unicode text)."""

    def __init__(self, **kwargs):
        kwargs.pop("text", None)
        super().__init__(text="", **kwargs)
        self.bind(pos=self._redraw, size=self._redraw)
        self._redraw()

    def _redraw(self, *_):
        self.canvas.after.clear()
        w = float(self.width)
        h = float(self.height)
        if w <= 0 or h <= 0:
            return

        pad_x = min(w, h) * 0.28
        x0 = self.x + pad_x
        x1 = self.right - pad_x
        yc = self.y + h / 2
        gap = min(w, h) * 0.18

        with self.canvas.after:
            Color(1, 1, 1, 1)
            for y in (yc + gap, yc, yc - gap):
                Line(points=[x0, y, x1, y], width=dp(2), cap="round")


class TopHalf(BoxLayout):
    """Convenience layout: reserve upper half for editable inputs."""


class KitForm(BoxLayout):
    """Renders kit-driven extra properties and collects values."""

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical", spacing=dp(6), **kwargs
        )
        self._nodes: Tuple[PromptNode, ...] = tuple()
        self.selections: Dict[str, str] = {}
        self.inputs: Dict[str, str] = {}

    def set_nodes(self, nodes: Tuple[PromptNode, ...]) -> None:
        self._nodes = nodes
        self.selections = {}
        self.inputs = {}
        self._rebuild()

    def _rebuild(self) -> None:
        self.clear_widgets()
        for node in self._nodes:
            self._add_node(node)

    def _add_node(self, node: PromptNode) -> None:
        self._add_node_to(self, node)

    def _add_node_to(self, container: BoxLayout, node: PromptNode) -> None:
        if isinstance(node, GroupNode):
            # Skip hidden <type> group
            if node.label == "<type>":
                return
            # "word type" is labeled outside the scrollable list in the Add Word UI.
            if node.label.strip().lower() == "word type":
                for child in node.children:
                    self._add_node_to(container, child)
                return
            header = Label(
                text=node.label,
                size_hint_y=None,
                height=dp(24),
                halign="left",
                valign="middle",
                color=TEXT_DARK,
            )
            header.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
            container.add_widget(header)
            for child in node.children:
                self._add_node_to(container, child)
            return

        if isinstance(node, InputNode):
            input_key = node.key
            row = BoxLayout(
                orientation="vertical", size_hint_y=None, height=dp(70), spacing=dp(2)
            )
            lbl = Label(
                text=node.label,
                size_hint_y=None,
                height=dp(22),
                halign="left",
                valign="middle",
                color=TEXT_DARK,
            )
            lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
            ti = TextInput(multiline=False, size_hint_y=None, height=dp(40))

            def on_text(_, value: str):
                self.inputs[input_key] = value

            ti.bind(text=on_text)
            row.add_widget(lbl)
            row.add_widget(ti)
            container.add_widget(row)
            return

        if isinstance(node, ChoiceNode):
            # Let the choice block take remaining space when possible.
            is_word_type = node.label.strip().lower() == "word type"
            block = BoxLayout(orientation="vertical", spacing=dp(6))

            if node.label.strip().lower() != "word type":
                lbl = Label(
                    text=node.label,
                    size_hint_y=None,
                    height=dp(22),
                    halign="left",
                    valign="middle",
                    color=TEXT_DARK,
                )
                lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
                block.add_widget(lbl)

            children_box = BoxLayout(
                orientation="vertical", size_hint_y=None, spacing=dp(6)
            )
            children_box.bind(minimum_height=children_box.setter("height"))

            def rebuild_children(selection: str):
                self.selections[node.label] = selection
                children_box.clear_widgets()
                for child in node.option_children.get(selection, tuple()):
                    # Render children inside the choice block
                    self._add_node_to(children_box, child)

            choice_label = node.label

            def on_select(value: str):
                # Rebuild by resetting whole form (simpler + reliable)
                self.selections[choice_label] = value
                self._rebuild()

            self.selections[node.label] = self.selections.get(node.label, node.default)
            opt_list = OptionList(
                list(node.options),
                selected=self.selections[node.label],
                on_select=on_select,
            )
            # For Word type selection: split the available space 50/50 between
            # the option list and the dependent detail inputs (scrollable).
            if is_word_type:
                opt_list.size_hint_y = 1
                children_scroll = ScrollView(do_scroll_x=False, size_hint_y=1)
                children_scroll.add_widget(children_box)
                block.add_widget(opt_list)

                # Initial render
                rebuild_children(self.selections[node.label])
                block.add_widget(children_scroll)
            else:
                block.add_widget(opt_list)

                # Initial render
                rebuild_children(self.selections[node.label])
                block.add_widget(children_box)
            container.add_widget(block)
            return

    def collect(self) -> Dict[str, Any]:
        return collect_prompt_data(
            self._nodes, selections=self.selections, inputs=self.inputs
        )


class MenuScreen(Screen):
    pass


class AddGlossaryScreen(Screen):
    error = StringProperty("")


class AddWordScreen(Screen):
    error = StringProperty("")


class PracticeSetupScreen(Screen):
    error = StringProperty("")


class SettingsScreen(Screen):
    error = StringProperty("")


class PracticeScreen(Screen):
    prompt = StringProperty("")
    status = StringProperty("")
    summary = StringProperty("")

    menu_open = BooleanProperty(False)
    ended = BooleanProperty(False)

    session: Optional[PracticeSession] = None

    def go_menu(self) -> None:
        # Keep session for resume (unless user ended with '#')
        app = App.get_running_app()
        try:
            app.practice_session = self.session
        except Exception:
            pass
        if self.manager is not None:
            self.manager.current = "menu"

    def toggle_menu(self) -> None:
        self.menu_open = not self.menu_open

    def _focus_input(self) -> None:
        try:
            Clock.schedule_once(lambda _dt: setattr(self.ids.answer_input, "focus", True), 0)  # type: ignore[attr-defined]
        except Exception:
            pass

    def next_action(self) -> None:
        if not self.session:
            return
        if self.menu_open:
            self.menu_open = False

        app = App.get_running_app()
        ti = self.ids.answer_input  # type: ignore[attr-defined]
        if self.session.needs_ok():
            self.session.acknowledge_ok()
            app._update_practice_screen(self)
            self._focus_input()
            return

        self.session.submit(ti.text)
        if not bool(getattr(self.session, "last_was_close", False)):
            ti.text = ""
        app._update_practice_screen(self)
        self._focus_input()

    def do_learned(self) -> None:
        self.menu_open = False
        if not self.session:
            return
        self.session.command_max_points()
        App.get_running_app()._update_practice_screen(self)
        self._focus_input()

    def do_hard(self) -> None:
        self.menu_open = False
        if not self.session:
            return
        self.session.command_boost()
        App.get_running_app()._update_practice_screen(self)
        self._focus_input()

    def do_stop(self) -> None:
        self.menu_open = False
        if not self.session:
            return
        self.session.stop()
        App.get_running_app()._update_practice_screen(self)
        self._focus_input()


class VocabLearnerRoot(ScreenManager):
    model = ObjectProperty(None)


class VocabLearnerApp(App):
    def build(self):
        app_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = _resolve_data_dir(app_dir=app_dir)
        self.data_dir = data_dir
        self.model = VocabLearnerModel(Kit.LATIN, base_dir=data_dir, app_dir=app_dir)

        self._ui_settings_path = os.path.join(data_dir, "ui_settings.json")
        self.lang: Lang = self._load_ui_lang()
        self.text: LangText = self.lang.text()
        self.practice_session: Optional[PracticeSession] = None

        root = VocabLearnerRoot()
        root.model = self.model

        # -------- Menu
        menu = MenuScreen(name="menu")
        menu.add_widget(self._build_menu(root))
        root.add_widget(menu)

        # -------- Add Glossary
        addg = AddGlossaryScreen(name="add_glossary")
        addg.add_widget(self._build_add_glossary(root, addg))
        root.add_widget(addg)

        # -------- Add Word
        addw = AddWordScreen(name="add_word")
        addw.add_widget(self._build_add_word(root, addw))
        root.add_widget(addw)

        # -------- Practice Setup
        ps = PracticeSetupScreen(name="practice_setup")
        ps.add_widget(self._build_practice_setup(root, ps))
        root.add_widget(ps)

        # -------- Settings
        st = SettingsScreen(name="settings")
        st.add_widget(self._build_settings(root, st))
        root.add_widget(st)

        # -------- Practice
        pr = PracticeScreen(name="practice")
        root.add_widget(pr)

        return root

    # ---------------- UI builders

    def _build_menu(self, root: VocabLearnerRoot) -> BoxLayout:
        box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        box.add_widget(
            Label(
                text="Vocab Learner",
                size_hint_y=None,
                height=dp(40),
                color=TEXT_DARK,
                font_size="22sp",
            )
        )

        def nav(name: str):
            root.current = name

        def go_practice(_):
            if (
                self.practice_session is not None
                and not self.practice_session.ended_by_user
            ):
                pr_screen: PracticeScreen = root.get_screen("practice")  # type: ignore
                pr_screen.session = self.practice_session
                self._update_practice_screen(pr_screen)
                root.current = "practice"
            else:
                root.current = "practice_setup"

        box.add_widget(
            PeachButton(
                text="Practice", size_hint_y=None, height=dp(48), on_release=go_practice
            )
        )
        box.add_widget(
            PeachButton(
                text="Add word",
                size_hint_y=None,
                height=dp(48),
                on_release=lambda *_: nav("add_word"),
            )
        )
        box.add_widget(
            PeachButton(
                text="Add glossary",
                size_hint_y=None,
                height=dp(48),
                on_release=lambda *_: nav("add_glossary"),
            )
        )
        box.add_widget(
            PeachButton(
                text="Settings",
                size_hint_y=None,
                height=dp(48),
                on_release=lambda *_: nav("settings"),
            )
        )
        box.add_widget(
            PeachSecondaryButton(
                text="Quit",
                size_hint_y=None,
                height=dp(48),
                on_release=lambda *_: App.get_running_app().stop(),
            )
        )

        box.add_widget(
            Label(
                text=f"Languages: {self.model.mlang} / {self.model.learnlang}",
                color=TEXT_DARK,
            )
        )
        return box

    def _load_ui_lang(self) -> Lang:
        try:
            if os.path.exists(self._ui_settings_path):
                with open(self._ui_settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                raw = str(data.get("lang", "")).strip()
                if raw in Lang.__members__:
                    return Lang[raw]
        except Exception:
            pass
        return Lang.ENGLISH

    def _save_ui_lang(self, lang: Lang) -> None:
        data = {"lang": lang.name}
        with open(self._ui_settings_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def set_ui_language(self, lang: Lang) -> None:
        self.lang = lang
        self.text = lang.text()
        if self.practice_session is not None:
            self.practice_session.text = self.text
        self._save_ui_lang(lang)

    def _build_settings(self, root: VocabLearnerRoot, screen: SettingsScreen) -> BoxLayout:
        outer = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        outer.add_widget(
            Label(
                text="Settings",
                size_hint_y=None,
                height=dp(40),
                color=TEXT_DARK,
                font_size="22sp",
            )
        )

        outer.add_widget(
            Label(
                text="UI language",
                size_hint_y=None,
                height=dp(22),
                halign="left",
                valign="middle",
                color=TEXT_DARK,
            )
        )

        display_to_lang: Dict[str, Lang] = {
            "English": Lang.ENGLISH,
            "German": Lang.GERMAN,
            "Hungarian": Lang.HUNGARIAN,
        }
        lang_to_display: Dict[Lang, str] = {v: k for k, v in display_to_lang.items()}
        selected_display = lang_to_display.get(getattr(self, "lang", Lang.ENGLISH), "English")

        def on_select(value: str) -> None:
            lang = display_to_lang.get(value, Lang.ENGLISH)
            self.set_ui_language(lang)

        opts = OptionList(
            list(display_to_lang.keys()),
            selected=selected_display,
            on_select=on_select,
        )
        outer.add_widget(opts)

        # Data directory (where glossaries/ and kits/ live)
        data_dir = str(getattr(self, "data_dir", "") or getattr(self.model, "base_dir", ""))
        outer.add_widget(
            Label(
                text="Data folder",
                size_hint_y=None,
                height=dp(22),
                halign="left",
                valign="middle",
                color=TEXT_DARK,
            )
        )
        data_ti = TextInput(
            text=data_dir,
            readonly=True,
            multiline=True,
            size_hint_y=None,
            height=dp(48),
            cursor_blink=False,
            background_normal="",
            background_active="",
            background_color=PEACH_CARD,
            foreground_color=TEXT_DARK,
        )
        outer.add_widget(data_ti)

        btns = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(48), spacing=dp(10)
        )
        btns.add_widget(
            PeachSecondaryButton(
                text="Back", on_release=lambda *_: setattr(root, "current", "menu")
            )
        )
        outer.add_widget(btns)
        return outer

    def _build_add_glossary(
        self, root: VocabLearnerRoot, screen: AddGlossaryScreen
    ) -> BoxLayout:
        outer = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        top = BoxLayout(orientation="vertical", size_hint_y=0.55, spacing=dp(8))
        top.add_widget(
            Label(
                text="New glossary name",
                size_hint_y=None,
                height=dp(24),
                halign="left",
                valign="middle",
                color=TEXT_DARK,
            )
        )
        ti = TextInput(multiline=False, size_hint_y=None, height=dp(44))
        top.add_widget(ti)
        outer.add_widget(top)

        status = Label(text="", size_hint_y=None, height=dp(24), color=TEXT_DARK)
        outer.add_widget(status)

        btns = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(48), spacing=dp(10)
        )

        def add(_):
            name = (ti.text or "").strip()
            try:
                self.model.add_glossary(name)
                status.text = "Added."
                ti.text = ""
            except Exception as e:
                status.text = str(e)

        btns.add_widget(PeachButton(text="Add", on_release=add))
        btns.add_widget(
            PeachSecondaryButton(
                text="Back", on_release=lambda *_: setattr(root, "current", "menu")
            )
        )
        outer.add_widget(btns)
        return outer

    def _build_add_word(self, root: VocabLearnerRoot, screen: AddWordScreen) -> BoxLayout:
        outer = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        # App bar
        appbar = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(56))

        def _appbar_bg(_inst, _val):
            appbar.canvas.before.clear()
            with appbar.canvas.before:
                Color(*PEACH_CARD)
                Rectangle(pos=appbar.pos, size=appbar.size)

        appbar.bind(pos=_appbar_bg, size=_appbar_bg)
        _appbar_bg(None, None)
        appbar.add_widget(
            Label(
                text="Add word",
                color=TEXT_DARK,
                font_size="22sp",
                halign="left",
                valign="middle",
            )
        )
        outer.add_widget(appbar)

        # Responsive content area (portrait: stacked, landscape: side-by-side)
        main = BoxLayout(orientation="vertical", size_hint_y=1, spacing=dp(10))
        outer.add_widget(main)

        left = BoxLayout(orientation="vertical", spacing=dp(8))
        right = BoxLayout(orientation="vertical", spacing=dp(8))

        selected_glossary = self.model.glossaries[0] if self.model.glossaries else None

        def on_glossary_select(value: str):
            nonlocal selected_glossary
            selected_glossary = value

        gloss_options = OptionList(
            list(self.model.glossaries),
            selected=selected_glossary,
            on_select=on_glossary_select,
        )

        gloss_label = Label(
            text="Glossary",
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle",
            color=TEXT_DARK,
        )
        gloss_label.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
        left.add_widget(gloss_label)
        left.add_widget(gloss_options)

        mw = TextInput(
            hint_text=f"{self.model.mlang} word",
            multiline=False,
            size_hint_y=None,
            height=dp(44),
        )
        lw = TextInput(
            hint_text=f"{self.model.learnlang} word",
            multiline=False,
            size_hint_y=None,
            height=dp(44),
        )
        left.add_widget(mw)
        left.add_widget(lw)

        word_type_label = Label(
            text="Word type",
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle",
            color=TEXT_DARK,
        )
        word_type_label.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))

        # Kit-driven fields: the OptionList widgets inside are already scrollable,
        # so avoid wrapping the whole form in another ScrollView.
        kit_form = KitForm()
        kit_form.set_nodes(self.model.learninglang_prompt_tree())

        right.add_widget(word_type_label)
        right.add_widget(kit_form)

        def _apply_responsive_layout(*_):
            # During orientation changes, Android can fire multiple rapid size events.
            # Guard against transient widget-tree states and avoid hard-crashing.
            try:
                # When rebuilding, left/right may still be attached to an old container
                # that was removed from `main`. Detach them first to avoid
                # "Widget already has a parent" and leaving `main` empty.
                for w in (left, right):
                    try:
                        if w.parent is not None:
                            w.parent.remove_widget(w)
                    except Exception:
                        pass

                is_landscape = Window.width > Window.height
                main.clear_widgets()
                if is_landscape:
                    row = BoxLayout(orientation="horizontal", spacing=dp(10))
                    left.size_hint = (0.55, 1)
                    right.size_hint = (0.45, 1)
                    row.add_widget(left)
                    row.add_widget(right)
                    main.add_widget(row)
                else:
                    col = BoxLayout(orientation="vertical", spacing=dp(10))
                    left.size_hint = (1, 0.50)
                    right.size_hint = (1, 0.50)
                    col.add_widget(left)
                    col.add_widget(right)
                    main.add_widget(col)
            except Exception:
                return

        _layout_trigger = Clock.create_trigger(_apply_responsive_layout, 0)

        def rebuild_layout(*_):
            _layout_trigger()

        try:
            Window.bind(size=rebuild_layout)
        except Exception:
            pass
        _layout_trigger()

        status = Label(text="", size_hint_y=None, height=dp(24), color=TEXT_DARK)
        outer.add_widget(status)

        btns = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(48), spacing=dp(10)
        )

        def refresh_glossaries():
            nonlocal selected_glossary
            if selected_glossary not in self.model.glossaries:
                selected_glossary = (
                    self.model.glossaries[0] if self.model.glossaries else None
                )
            gloss_options.set_options(
                list(self.model.glossaries),
                selected=selected_glossary,
            )

        # Ensure newly-added glossaries show up when entering this screen.
        try:
            screen.bind(on_pre_enter=lambda *_: refresh_glossaries())
        except Exception:
            pass

        def save(_):
            gloss = selected_glossary
            if gloss not in self.model.glossaries:
                status.text = "Select a glossary."
                return
            mword = (mw.text or "").strip()
            lword = (lw.text or "").strip()
            if not mword or not lword:
                status.text = "Enter both words."
                return

            # only learning language has kit props in this kit
            lprops = kit_form.collect()
            try:
                self.model.add_word(gloss, mword, lword, mprops={}, lprops=lprops)
                status.text = "Saved."
                mw.text = ""
                lw.text = ""
                kit_form.set_nodes(self.model.learninglang_prompt_tree())
            except Exception as e:
                status.text = str(e)

        def back(_):
            refresh_glossaries()
            root.current = "menu"

        btns.add_widget(PeachButton(text="Save", on_release=save))
        btns.add_widget(PeachSecondaryButton(text="Back", on_release=back))
        outer.add_widget(btns)

        return outer

    def _build_practice_setup(
        self, root: VocabLearnerRoot, screen: PracticeSetupScreen
    ) -> BoxLayout:
        outer = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        # App bar
        appbar = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(56))

        def _appbar_bg(_inst, _val):
            appbar.canvas.before.clear()
            with appbar.canvas.before:
                Color(*PEACH_CARD)
                Rectangle(pos=appbar.pos, size=appbar.size)

        appbar.bind(pos=_appbar_bg, size=_appbar_bg)
        _appbar_bg(None, None)

        appbar.add_widget(
            Label(
                text="Practice setup",
                color=TEXT_DARK,
                font_size="22sp",
                halign="left",
                valign="middle",
            )
        )
        outer.add_widget(appbar)

        top = BoxLayout(orientation="vertical", size_hint_y=0.55, spacing=dp(8))

        selected_glossary = self.model.glossaries[0] if self.model.glossaries else None
        selected_lang = self.model.learnlang

        def on_glossary_select(value: str):
            nonlocal selected_glossary
            selected_glossary = value

        def on_lang_select(value: str):
            nonlocal selected_lang
            selected_lang = value

        gloss_options = OptionList(
            list(self.model.glossaries),
            selected=selected_glossary,
            on_select=on_glossary_select,
        )
        lang_options = OptionList(
            [self.model.mlang, self.model.learnlang],
            selected=selected_lang,
            on_select=on_lang_select,
        )

        gloss_label = Label(
            text="Glossary",
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle",
            color=TEXT_DARK,
        )
        gloss_label.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))

        lang_label = Label(
            text="Input language",
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle",
            color=TEXT_DARK,
        )
        lang_label.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))

        gloss_col = BoxLayout(orientation="vertical", spacing=dp(6))
        gloss_col.add_widget(gloss_label)
        gloss_col.add_widget(gloss_options)

        lang_col = BoxLayout(orientation="vertical", spacing=dp(6))
        lang_col.add_widget(lang_label)
        lang_col.add_widget(lang_options)

        selectors = BoxLayout(orientation="vertical", spacing=dp(8))
        top.add_widget(selectors)

        def _apply_responsive_selectors(*_):
            try:
                # Same reparenting issue as Add Word: detach before moving between
                # the portrait/landscape containers.
                for w in (gloss_col, lang_col):
                    try:
                        if w.parent is not None:
                            w.parent.remove_widget(w)
                    except Exception:
                        pass

                is_landscape = Window.width > Window.height
                selectors.clear_widgets()
                if is_landscape:
                    row = BoxLayout(orientation="horizontal", spacing=dp(10))
                    gloss_col.size_hint = (0.6, 1)
                    lang_col.size_hint = (0.4, 1)
                    row.add_widget(gloss_col)
                    row.add_widget(lang_col)
                    selectors.add_widget(row)
                else:
                    col = BoxLayout(orientation="vertical", spacing=dp(10))
                    # In portrait, let option lists expand to take remaining space.
                    gloss_col.size_hint = (1, 0.6)
                    lang_col.size_hint = (1, 0.4)
                    col.add_widget(gloss_col)
                    col.add_widget(lang_col)
                    selectors.add_widget(col)
            except Exception:
                return

        _selectors_trigger = Clock.create_trigger(_apply_responsive_selectors, 0)

        def rebuild_selectors(*_):
            _selectors_trigger()

        try:
            Window.bind(size=rebuild_selectors)
        except Exception:
            pass
        _selectors_trigger()
        outer.add_widget(top)

        status = Label(text="", size_hint_y=None, height=dp(24), color=TEXT_DARK)
        outer.add_widget(status)

        btns = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(48), spacing=dp(10)
        )

        def refresh_glossaries():
            nonlocal selected_glossary
            if selected_glossary not in self.model.glossaries:
                selected_glossary = (
                    self.model.glossaries[0] if self.model.glossaries else None
                )
            gloss_options.set_options(
                list(self.model.glossaries),
                selected=selected_glossary,
            )

        # Ensure newly-added glossaries show up when entering this screen.
        try:
            screen.bind(on_pre_enter=lambda *_: refresh_glossaries())
        except Exception:
            pass

        def start(_):
            gloss = selected_glossary
            if gloss not in self.model.glossaries:
                status.text = "Select a glossary."
                return
            answer_lang = selected_lang
            if answer_lang not in (self.model.mlang, self.model.learnlang):
                status.text = "Select a language."
                return
            if not self.model.words.get(gloss):
                status.text = "Nothing to practice."
                return

            pr_screen: PracticeScreen = root.get_screen("practice")  # type: ignore
            self.practice_session = PracticeSession(
                self.model, gloss=gloss, answer_lang=answer_lang, text=self.text
            )
            pr_screen.session = self.practice_session
            self._update_practice_screen(pr_screen)
            root.current = "practice"

        def back(_):
            refresh_glossaries()
            root.current = "menu"

        btns.add_widget(PeachButton(text="Start", on_release=start))
        btns.add_widget(PeachSecondaryButton(text="Back", on_release=back))
        outer.add_widget(btns)

        return outer

    def _update_practice_screen(self, screen: PracticeScreen) -> None:
        if not screen.session:
            return

        kind, text = screen.session.current_prompt()

        # Keep type + main word visible even during details
        t = screen.session.current_type()
        screen.ids.type_lbl.text = t  # type: ignore[attr-defined]
        screen.ids.word_lbl.text = (
            screen.session.cur_word[screen.session.question_lang]["szo"]
            if screen.session.cur_word
            else ""
        )  # type: ignore[attr-defined]

        # Prompt label (what are we entering right now?)
        if kind == "word":
            screen.ids.prompt_lbl.text = f"Enter {screen.session.answer_lang} translation"  # type: ignore[attr-defined]
        elif kind == "detail":
            screen.ids.prompt_lbl.text = f"{text}"  # type: ignore[attr-defined]
        else:
            screen.ids.prompt_lbl.text = text  # type: ignore[attr-defined]

        # Total history (session-wide) for the upper half
        hist = screen.session.total_history_markup()
        # If the user hasn't scrolled up, keep the view anchored to the bottom
        # so the latest entry is always visible.
        keep_bottom = True
        try:
            keep_bottom = float(screen.ids.history_scroll.scroll_y) <= 0.02  # type: ignore[attr-defined]
        except Exception:
            keep_bottom = True
        screen.ids.history_lbl.text = hist  # type: ignore[attr-defined]
        if keep_bottom:
            try:
                Clock.schedule_once(
                    lambda _dt: setattr(screen.ids.history_scroll, "scroll_y", 0), 0  # type: ignore[attr-defined]
                )
            except Exception:
                pass

        ended = bool(getattr(screen.session, "ended_by_user", False))
        screen.ended = ended

        # If user stopped practice: show only the score panel.
        if ended:
            screen.menu_open = False
            total = int(screen.session.correct_pt + screen.session.incorrect_pt)
            pct = 0.0 if total == 0 else (screen.session.correct_pt / total) * 100.0

            screen.ids.summary_lbl.text = (
                f"Correct: {screen.session.correct_pt}\n"
                f"Incorrect: {screen.session.incorrect_pt}\n"
                f"{pct:.2f}%"
            )  # type: ignore[attr-defined]
            return

        # Normal status display
        screen.ids.status_lbl.text = screen.session.message  # type: ignore[attr-defined]

        # Auto-focus input whenever we render a prompt
        try:
            Clock.schedule_once(
                lambda _dt: setattr(screen.ids.answer_input, "focus", True), 0  # type: ignore[attr-defined]
            )
        except Exception:
            pass


if __name__ == "__main__":
    VocabLearnerApp().run()
