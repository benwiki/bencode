from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from nyelv_model import (
    ChoiceNode,
    GroupNode,
    InputNode,
    Kit,
    NyelvModel,
    PracticeSession,
    PromptNode,
    collect_prompt_data,
)


# Mobile friendly keyboard behavior: keep focused input visible.
Window.softinput_mode = "pan"


class TopHalf(BoxLayout):
    """Convenience layout: reserve upper half for editable inputs."""


class KitForm(BoxLayout):
    """Renders kit-driven extra properties and collects values."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(6), size_hint_y=None, **kwargs)
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
        if isinstance(node, GroupNode):
            # Skip hidden <type> group
            if node.label == "<type>":
                return
            header = Label(text=node.label, size_hint_y=None, height=dp(24), halign="left", valign="middle")
            header.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
            self.add_widget(header)
            for child in node.children:
                self._add_node(child)
            return

        if isinstance(node, InputNode):
            input_key = node.key
            row = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(70), spacing=dp(2))
            lbl = Label(text=node.label, size_hint_y=None, height=dp(22), halign="left", valign="middle")
            lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
            ti = TextInput(multiline=False, size_hint_y=None, height=dp(40))

            def on_text(_, value: str):
                self.inputs[input_key] = value

            ti.bind(text=on_text)
            row.add_widget(lbl)
            row.add_widget(ti)
            self.add_widget(row)
            return

        if isinstance(node, ChoiceNode):
            block = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(120), spacing=dp(6))
            top = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(44), spacing=dp(8))
            lbl = Label(text=node.label, size_hint_x=0.45, halign="left", valign="middle")
            lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
            sp = Spinner(text=node.default, values=list(node.options), size_hint_x=0.55)
            top.add_widget(lbl)
            top.add_widget(sp)
            block.add_widget(top)

            children_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(6))
            children_box.bind(minimum_height=children_box.setter("height"))

            def rebuild_children(selection: str):
                self.selections[node.label] = selection
                children_box.clear_widgets()
                for child in node.option_children.get(selection, tuple()):
                    # Render children inside the same form; this is safe because we track inputs/selections centrally.
                    self._add_node(child)

            choice_label = node.label

            def on_select(_, value: str):
                # Rebuild by resetting whole form (simpler + reliable)
                self.selections[choice_label] = value
                self._rebuild()

            sp.bind(text=on_select)
            self.selections[node.label] = node.default

            # Initial render
            rebuild_children(node.default)
            block.add_widget(children_box)
            self.add_widget(block)
            return

    def collect(self) -> Dict[str, Any]:
        return collect_prompt_data(self._nodes, selections=self.selections, inputs=self.inputs)


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


class NyelvRoot(ScreenManager):
    model = ObjectProperty(None)


class NyelvApp(App):
    def build(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = NyelvModel(Kit.LATIN, base_dir=base_dir)

        root = NyelvRoot()
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

    def _build_menu(self, root: NyelvRoot) -> BoxLayout:
        box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        box.add_widget(Label(text="Nyelv (Kivy)", size_hint_y=None, height=dp(40)))

        def nav(name: str):
            root.current = name

        box.add_widget(Button(text="Practice", size_hint_y=None, height=dp(48), on_release=lambda *_: nav("practice_setup")))
        box.add_widget(Button(text="Add word", size_hint_y=None, height=dp(48), on_release=lambda *_: nav("add_word")))
        box.add_widget(Button(text="Add glossary", size_hint_y=None, height=dp(48), on_release=lambda *_: nav("add_glossary")))
        box.add_widget(Button(text="Quit", size_hint_y=None, height=dp(48), on_release=lambda *_: App.get_running_app().stop()))

        box.add_widget(Label(text=f"Languages: {self.model.mlang} / {self.model.learnlang}"))
        return box

    def _build_add_glossary(self, root: NyelvRoot, screen: AddGlossaryScreen) -> BoxLayout:
        outer = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        top = BoxLayout(orientation="vertical", size_hint_y=0.55, spacing=dp(8))
        top.add_widget(Label(text="New glossary name", size_hint_y=None, height=dp(24), halign="left", valign="middle"))
        ti = TextInput(multiline=False, size_hint_y=None, height=dp(44))
        top.add_widget(ti)
        outer.add_widget(top)

        status = Label(text="", size_hint_y=None, height=dp(24))
        outer.add_widget(status)

        btns = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48), spacing=dp(10))

        def add(_):
            name = (ti.text or "").strip()
            try:
                self.model.add_glossary(name)
                status.text = "Added."
                ti.text = ""
            except Exception as e:
                status.text = str(e)

        btns.add_widget(Button(text="Add", on_release=add))
        btns.add_widget(Button(text="Back", on_release=lambda *_: setattr(root, "current", "menu")))
        outer.add_widget(btns)
        return outer

    def _build_add_word(self, root: NyelvRoot, screen: AddWordScreen) -> BoxLayout:
        outer = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        # Upper half: text inputs
        top = BoxLayout(orientation="vertical", size_hint_y=0.55, spacing=dp(8))

        gloss_spinner = Spinner(text="(select glossary)", values=list(self.model.glossaries), size_hint_y=None, height=dp(44))
        top.add_widget(gloss_spinner)

        mw = TextInput(hint_text=f"{self.model.mlang} word", multiline=False, size_hint_y=None, height=dp(44))
        lw = TextInput(hint_text=f"{self.model.learnlang} word", multiline=False, size_hint_y=None, height=dp(44))
        top.add_widget(mw)
        top.add_widget(lw)

        outer.add_widget(top)

        # Lower half: kit-driven fields (scrollable)
        kit_scroll = ScrollView(size_hint_y=0.35)
        kit_form = KitForm()
        kit_form.set_nodes(self.model.learninglang_prompt_tree())
        kit_scroll.add_widget(kit_form)
        outer.add_widget(kit_scroll)

        status = Label(text="", size_hint_y=None, height=dp(24))
        outer.add_widget(status)

        btns = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48), spacing=dp(10))

        def refresh_glossaries():
            gloss_spinner.values = list(self.model.glossaries)
            if gloss_spinner.text not in gloss_spinner.values:
                gloss_spinner.text = "(select glossary)"

        def save(_):
            gloss = gloss_spinner.text
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

        btns.add_widget(Button(text="Save", on_release=save))
        btns.add_widget(Button(text="Back", on_release=back))
        outer.add_widget(btns)

        return outer

    def _build_practice_setup(self, root: NyelvRoot, screen: PracticeSetupScreen) -> BoxLayout:
        outer = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        top = BoxLayout(orientation="vertical", size_hint_y=0.55, spacing=dp(8))

        gloss_spinner = Spinner(text="(select glossary)", values=list(self.model.glossaries), size_hint_y=None, height=dp(44))
        lang_spinner = Spinner(text=self.model.learnlang, values=[self.model.mlang, self.model.learnlang], size_hint_y=None, height=dp(44))

        top.add_widget(Label(text="Practice setup", size_hint_y=None, height=dp(30)))
        top.add_widget(gloss_spinner)
        top.add_widget(lang_spinner)
        outer.add_widget(top)

        status = Label(text="", size_hint_y=None, height=dp(24))
        outer.add_widget(status)

        btns = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48), spacing=dp(10))

        def refresh_glossaries():
            gloss_spinner.values = list(self.model.glossaries)
            if gloss_spinner.text not in gloss_spinner.values:
                gloss_spinner.text = "(select glossary)"

        def start(_):
            gloss = gloss_spinner.text
            if gloss not in self.model.glossaries:
                status.text = "Select a glossary."
                return
            answer_lang = lang_spinner.text
            if answer_lang not in (self.model.mlang, self.model.learnlang):
                status.text = "Select a language."
                return
            if not self.model.words.get(gloss):
                status.text = "Nothing to practice."
                return

            pr_screen: PracticeScreen = root.get_screen("practice")  # type: ignore
            pr_screen.session = PracticeSession(self.model, gloss=gloss, answer_lang=answer_lang)
            self._update_practice_screen(pr_screen)
            root.current = "practice"

        def back(_):
            refresh_glossaries()
            root.current = "menu"

        btns.add_widget(Button(text="Start", on_release=start))
        btns.add_widget(Button(text="Back", on_release=back))
        outer.add_widget(btns)

        return outer

    def _build_practice(self, root: NyelvRoot, screen: PracticeScreen) -> BoxLayout:
        outer = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        # Upper half: question + input
        top = BoxLayout(orientation="vertical", size_hint_y=0.55, spacing=dp(8))
        prompt_lbl = Label(text="", size_hint_y=None, height=dp(80), halign="left", valign="middle")
        prompt_lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
        ti = TextInput(multiline=False, size_hint_y=None, height=dp(44))
        top.add_widget(prompt_lbl)
        top.add_widget(ti)
        outer.add_widget(top)

        # Lower half: status/summary + controls
        status_lbl = Label(text="", size_hint_y=None, height=dp(24), halign="left", valign="middle")
        status_lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
        summary_lbl = Label(text="", size_hint_y=None, height=dp(24), halign="left", valign="middle")
        summary_lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
        outer.add_widget(status_lbl)
        outer.add_widget(summary_lbl)

        btns = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48), spacing=dp(10))

        def submit(_):
            if not screen.session:
                return
            screen.session.submit(ti.text)
            ti.text = ""
            self._update_practice_screen(screen)

        def stop(_):
            if screen.session:
                screen.session.stop()
                self._update_practice_screen(screen)

        def maxpt(_):
            if screen.session:
                screen.session.command_max_points()
                self._update_practice_screen(screen)

        def boost(_):
            if screen.session:
                screen.session.command_boost()
                self._update_practice_screen(screen)

        def back(_):
            screen.session = None
            root.current = "menu"

        btns.add_widget(Button(text="Submit", on_release=submit))
        btns.add_widget(Button(text="Stop", on_release=stop))
        btns.add_widget(Button(text="Max", on_release=maxpt))
        btns.add_widget(Button(text="Boost", on_release=boost))
        btns.add_widget(Button(text="Back", on_release=back))
        outer.add_widget(btns)

        # Keep references for updating
        screen._prompt_lbl = prompt_lbl  # type: ignore[attr-defined]
        screen._status_lbl = status_lbl  # type: ignore[attr-defined]
        screen._summary_lbl = summary_lbl  # type: ignore[attr-defined]

        # Enter submits
        ti.bind(on_text_validate=submit)
        return outer

    def _update_practice_screen(self, screen: PracticeScreen) -> None:
        if not screen.session:
            return

        kind, text = screen.session.current_prompt()
        screen._prompt_lbl.text = text  # type: ignore[attr-defined]
        screen._status_lbl.text = screen.session.message  # type: ignore[attr-defined]
        screen._summary_lbl.text = screen.session.summary()  # type: ignore[attr-defined]


if __name__ == "__main__":
    NyelvApp().run()
