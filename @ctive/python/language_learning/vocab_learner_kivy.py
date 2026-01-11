from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

# Workaround: On some Windows setups Kivy's wm_pen input provider can spam
# "Exception ignored on calling ctypes callback function". Disabling it avoids
# the noise and doesn't affect typical mouse/touch usage.
os.environ.setdefault("KIVY_NO_WM_PEN", "1")

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty  # type: ignore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

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
        if height:
            self.size_hint_y = None
            self.height = height
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
            orientation="vertical", spacing=dp(6), size_hint_y=None, **kwargs
        )
        self.bind(minimum_height=self.setter("height"))
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
            block = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(6))
            block.bind(minimum_height=block.setter("height"))

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
                height=dp(44) * 3,
                on_select=on_select,
            )
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


class PracticeScreen(Screen):
    prompt = StringProperty("")
    status = StringProperty("")
    summary = StringProperty("")

    session: Optional[PracticeSession] = None


class VocabLearnerRoot(ScreenManager):
    model = ObjectProperty(None)


class VocabLearnerApp(App):
    def build(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = VocabLearnerModel(Kit.LATIN, base_dir=base_dir)
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

        # -------- Practice
        pr = PracticeScreen(name="practice")
        pr.add_widget(self._build_practice(root, pr))
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
            height=dp(44) * 3,
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

        # Kit-driven fields (scrollable): includes the word type selector and its dependent fields
        kit_scroll = ScrollView()
        kit_form = KitForm()
        kit_form.set_nodes(self.model.learninglang_prompt_tree())
        kit_scroll.add_widget(kit_form)

        right.add_widget(word_type_label)
        right.add_widget(kit_scroll)

        def rebuild_layout(*_):
            # Landscape if width > height
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
                left.size_hint = (1, 0.55)
                right.size_hint = (1, 0.45)
                col.add_widget(left)
                col.add_widget(right)
                main.add_widget(col)

        try:
            Window.bind(size=rebuild_layout)
        except Exception:
            pass
        rebuild_layout()

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
            height=dp(44) * 3,
            on_select=on_glossary_select,
        )
        lang_options = OptionList(
            [self.model.mlang, self.model.learnlang],
            selected=selected_lang,
            height=dp(44) * 2,
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

        sep_h = Widget(size_hint_y=None, height=dp(1))
        sep_v = Widget(size_hint_x=None, width=dp(1))

        def _sep_bg(widget: Widget):
            def _draw(_inst, _val):
                widget.canvas.before.clear()
                with widget.canvas.before:
                    Color(*TEXT_MUTED)
                    Rectangle(pos=widget.pos, size=widget.size)

            widget.bind(pos=_draw, size=_draw)
            _draw(None, None)

        _sep_bg(sep_h)
        _sep_bg(sep_v)

        selectors = BoxLayout(orientation="vertical", spacing=dp(8))
        top.add_widget(selectors)

        def rebuild_selectors(*_):
            is_landscape = Window.width > Window.height
            selectors.clear_widgets()
            if is_landscape:
                row = BoxLayout(orientation="horizontal", spacing=dp(10))
                gloss_col.size_hint = (0.55, 1)
                lang_col.size_hint = (0.45, 1)
                row.add_widget(gloss_col)
                row.add_widget(sep_v)
                row.add_widget(lang_col)
                selectors.add_widget(row)
            else:
                col = BoxLayout(orientation="vertical", spacing=dp(10))
                gloss_col.size_hint = (1, None)
                lang_col.size_hint = (1, None)
                col.add_widget(gloss_col)
                col.add_widget(sep_h)
                col.add_widget(lang_col)
                selectors.add_widget(col)

        try:
            Window.bind(size=rebuild_selectors)
        except Exception:
            pass
        rebuild_selectors()
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
                self.model, gloss=gloss, answer_lang=answer_lang
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

    def _build_practice(self, root: VocabLearnerRoot, screen: PracticeScreen) -> BoxLayout:
        outer = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        # Top bar: Return to menu
        topbar = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(48), spacing=dp(0)
        )
        back_icon = BackArrowSquare(size_hint_x=None, width=dp(52))
        back_btn = PeachButton(text="Return to menu", size_hint_x=1)
        topbar.add_widget(back_icon)
        topbar.add_widget(back_btn)
        outer.add_widget(topbar)

        # Upper half: total history (at the bottom) on PEACH_CARD background
        upper = BoxLayout(orientation="vertical", size_hint_y=0.50, spacing=dp(6))

        def _upper_bg(_inst, _val):
            upper.canvas.before.clear()
            with upper.canvas.before:
                Color(*PEACH_CARD)
                Rectangle(pos=upper.pos, size=upper.size)

        upper.bind(pos=_upper_bg, size=_upper_bg)
        _upper_bg(None, None)

        upper.add_widget(Widget(size_hint_y=0.25))

        total_history_scroll = ScrollView(size_hint_y=0.75)
        total_history = Label(
            text="",
            markup=True,
            size_hint_y=None,
            halign="left",
            valign="top",
            color=TEXT_DARK,
        )
        total_history.bind(size=lambda inst, _: setattr(inst, "text_size", (inst.width, None)))
        total_history.bind(texture_size=lambda inst, val: setattr(inst, "height", max(val[1], dp(10))))
        total_history_scroll.add_widget(total_history)
        upper.add_widget(total_history_scroll)
        outer.add_widget(upper)

        # Separator line between halves
        sep = BoxLayout(size_hint_y=None, height=dp(1))

        def _sep_bg(_inst, _val):
            sep.canvas.before.clear()
            with sep.canvas.before:
                Color(*TEXT_MUTED)
                Rectangle(pos=sep.pos, size=sep.size)

        sep.bind(pos=_sep_bg, size=_sep_bg)
        _sep_bg(None, None)
        outer.add_widget(sep)

        # Lower half: status/summary + type/word/prompt/input (directly above buttons) + controls
        status_lbl = Label(
            text="",
            size_hint_y=None,
            height=dp(24),
            halign="left",
            valign="middle",
            color=TEXT_DARK,
        )
        status_lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
        summary_lbl = Label(
            text="",
            size_hint_y=None,
            height=dp(24),
            halign="left",
            valign="top",
            color=TEXT_DARK,
        )
        summary_lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
        summary_lbl.bind(texture_size=lambda inst, val: setattr(inst, "height", max(val[1], 0)))
        outer.add_widget(status_lbl)
        outer.add_widget(summary_lbl)

        type_lbl = Label(
            text="",
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle",
            color=TEXT_MUTED,
        )
        type_lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))

        word_lbl = Label(
            text="",
            size_hint_y=None,
            height=dp(48),
            halign="left",
            valign="middle",
            color=TEXT_DARK,
            font_size="22sp",
        )
        word_lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))

        prompt_lbl = Label(
            text="",
            size_hint_y=None,
            height=dp(30),
            halign="left",
            valign="middle",
            color=TEXT_DARK,
            font_size="16sp",
        )
        prompt_lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))

        ti = TextInput(multiline=False, size_hint_y=None, height=dp(44))

        outer.add_widget(type_lbl)
        outer.add_widget(word_lbl)
        outer.add_widget(prompt_lbl)
        outer.add_widget(ti)

        # Bottom controls: hamburger + NEXT, with a drop-up menu overlay
        menu_open = {"open": False}

        bar_h = dp(52)
        menu_h = dp(44)
        menu_gap = dp(6)

        bottom = BoxLayout(orientation="vertical", size_hint_y=None, height=bar_h, spacing=0)

        bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=bar_h, spacing=menu_gap)
        menu_btn = HamburgerSquare(size_hint=(None, None), width=dp(52), height=bar_h)
        next_btn = PeachButton(text="NEXT", size_hint_y=None, height=bar_h)
        bar.add_widget(menu_btn)
        bar.add_widget(next_btn)

        menu_box = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=0,
            spacing=dp(6),
            opacity=0,
            disabled=True,
        )

        learned_btn = PeachButton(text="learned")
        hard_btn = PeachButton(text="hard")
        stop_btn = PeachButton(text="stop")
        menu_box.add_widget(learned_btn)
        menu_box.add_widget(hard_btn)
        menu_box.add_widget(stop_btn)
        bottom.add_widget(menu_box)

        bottom.add_widget(bar)

        def set_menu(open_: bool) -> None:
            menu_open["open"] = open_
            menu_box.opacity = 1 if open_ else 0
            menu_box.disabled = not open_
            menu_box.height = menu_h if open_ else 0
            bottom.spacing = menu_gap if open_ else 0
            bottom.height = (bar_h + menu_gap + menu_h) if open_ else bar_h

        def toggle_menu(_):
            set_menu(not menu_open["open"])

        def go_menu(_):
            # Keep session for resume (unless user ended with '#')
            self.practice_session = screen.session
            root.current = "menu"

        def next_action(_):
            if not screen.session:
                return
            if menu_open["open"]:
                set_menu(False)
            if screen.session.needs_ok():
                screen.session.acknowledge_ok()
                self._update_practice_screen(screen)
                Clock.schedule_once(lambda _dt: setattr(ti, "focus", True), 0)
                return
            screen.session.submit(ti.text)
            ti.text = ""
            self._update_practice_screen(screen)
            Clock.schedule_once(lambda _dt: setattr(ti, "focus", True), 0)

        def do_learned(_):
            set_menu(False)
            if not screen.session:
                return
            screen.session.command_max_points()
            self._update_practice_screen(screen)
            Clock.schedule_once(lambda _dt: setattr(ti, "focus", True), 0)

        def do_hard(_):
            set_menu(False)
            if not screen.session:
                return
            screen.session.command_boost()
            self._update_practice_screen(screen)
            Clock.schedule_once(lambda _dt: setattr(ti, "focus", True), 0)

        def do_stop(_):
            set_menu(False)
            if not screen.session:
                return
            screen.session.stop()
            self._update_practice_screen(screen)
            Clock.schedule_once(lambda _dt: setattr(ti, "focus", True), 0)

        back_icon.bind(on_release=go_menu)
        back_btn.bind(on_release=go_menu)
        next_btn.bind(on_release=next_action)
        menu_btn.bind(on_release=toggle_menu)
        learned_btn.bind(on_release=do_learned)
        hard_btn.bind(on_release=do_hard)
        stop_btn.bind(on_release=do_stop)

        outer.add_widget(bottom)

        # Keep references for updating
        screen._type_lbl = type_lbl  # type: ignore[attr-defined]
        screen._word_lbl = word_lbl  # type: ignore[attr-defined]
        screen._prompt_lbl = prompt_lbl  # type: ignore[attr-defined]
        screen._status_lbl = status_lbl  # type: ignore[attr-defined]
        screen._summary_lbl = summary_lbl  # type: ignore[attr-defined]
        screen._history_lbl = total_history  # type: ignore[attr-defined]
        screen._ti = ti  # type: ignore[attr-defined]
        screen._bottom = bottom  # type: ignore[attr-defined]

        # Enter triggers NEXT
        ti.bind(on_text_validate=next_action)
        return outer

    def _update_practice_screen(self, screen: PracticeScreen) -> None:
        if not screen.session:
            return

        kind, text = screen.session.current_prompt()

        # Keep type + main word visible even during details
        t = screen.session.current_type()
        screen._type_lbl.text = t  # type: ignore[attr-defined]
        screen._word_lbl.text = screen.session.cur_word[screen.session.question_lang]["szo"] if screen.session.cur_word else ""  # type: ignore[attr-defined]

        # Prompt label (what are we entering right now?)
        if kind == "word":
            screen._prompt_lbl.text = f"Enter {screen.session.answer_lang} translation"  # type: ignore[attr-defined]
        elif kind == "detail":
            screen._prompt_lbl.text = f"{text}"  # type: ignore[attr-defined]
        else:
            screen._prompt_lbl.text = text  # type: ignore[attr-defined]

        # Total history (session-wide) for the upper half
        hist = screen.session.total_history_markup()
        screen._history_lbl.text = hist  # type: ignore[attr-defined]

        # Default: hide score line during normal practice.
        screen._summary_lbl.text = ""  # type: ignore[attr-defined]
        screen._summary_lbl.opacity = 0  # type: ignore[attr-defined]
        screen._summary_lbl.height = 0  # type: ignore[attr-defined]

        # If user stopped practice: hide lower controls and show only the score.
        if getattr(screen.session, "ended_by_user", False):
            total = int(screen.session.correct_pt + screen.session.incorrect_pt)
            pct = 0.0 if total == 0 else (screen.session.correct_pt / total) * 100.0

            screen._status_lbl.text = ""  # type: ignore[attr-defined]
            screen._status_lbl.opacity = 0  # type: ignore[attr-defined]
            screen._status_lbl.height = 0  # type: ignore[attr-defined]

            screen._type_lbl.text = ""  # type: ignore[attr-defined]
            screen._type_lbl.opacity = 0  # type: ignore[attr-defined]
            screen._type_lbl.height = 0  # type: ignore[attr-defined]

            screen._word_lbl.text = ""  # type: ignore[attr-defined]
            screen._word_lbl.opacity = 0  # type: ignore[attr-defined]
            screen._word_lbl.height = 0  # type: ignore[attr-defined]

            screen._prompt_lbl.text = ""  # type: ignore[attr-defined]
            screen._prompt_lbl.opacity = 0  # type: ignore[attr-defined]
            screen._prompt_lbl.height = 0  # type: ignore[attr-defined]

            screen._ti.text = ""  # type: ignore[attr-defined]
            screen._ti.disabled = True  # type: ignore[attr-defined]
            screen._ti.opacity = 0  # type: ignore[attr-defined]
            screen._ti.height = 0  # type: ignore[attr-defined]

            try:
                screen._bottom.disabled = True  # type: ignore[attr-defined]
                screen._bottom.opacity = 0  # type: ignore[attr-defined]
                screen._bottom.height = 0  # type: ignore[attr-defined]
            except Exception:
                pass

            screen._summary_lbl.text = (
                f"Correct: {screen.session.correct_pt}\n"
                f"Incorrect: {screen.session.incorrect_pt}\n"
                f"{pct:.2f}%"
            )  # type: ignore[attr-defined]
            screen._summary_lbl.opacity = 1  # type: ignore[attr-defined]
            # height will auto-adjust via texture_size binding
            return

        # Normal status display
        screen._ti.disabled = False  # type: ignore[attr-defined]
        screen._ti.opacity = 1  # type: ignore[attr-defined]
        if float(getattr(screen._ti, "height", 0)) == 0:
            screen._ti.height = dp(44)  # type: ignore[attr-defined]

        try:
            screen._bottom.disabled = False  # type: ignore[attr-defined]
            screen._bottom.opacity = 1  # type: ignore[attr-defined]
            if float(getattr(screen._bottom, "height", 0)) == 0:
                screen._bottom.height = dp(52)  # type: ignore[attr-defined]
        except Exception:
            pass

        screen._status_lbl.text = screen.session.message  # type: ignore[attr-defined]
        screen._status_lbl.opacity = 1  # type: ignore[attr-defined]
        if float(getattr(screen._status_lbl, "height", 0)) == 0:
            screen._status_lbl.height = dp(24)  # type: ignore[attr-defined]
        # Auto-focus input whenever we render a prompt
        try:
            Clock.schedule_once(lambda _dt: setattr(screen._ti, "focus", True), 0)  # type: ignore[attr-defined]
        except Exception:
            pass


if __name__ == "__main__":
    VocabLearnerApp().run()
