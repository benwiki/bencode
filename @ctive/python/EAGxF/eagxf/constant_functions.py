import os

from discord import ButtonStyle

from eagxf.button import Button
from eagxf.constants import (
    APP_NAME,
    QUESTION_NAMES,
    USERS_FOLDER_PATH,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.enums.screen_id import ScreenId


def ANSWERS(search=False) -> str:  # pylint: disable=invalid-name
    prefix = "search_" if search else ""
    return "\n" + "\n".join(
        f"{question['emoji']} __{question['text']}__" f"\n<{prefix}{q_id}_peek>"
        for q_id, question in QUESTION_NAMES.items()
    )


def PROFILE(search=False, name="Your") -> str:  # pylint: disable=invalid-name
    prefix = "search_" if search else ""
    return (
        (
            "***------ Current filters ------***"
            if search
            else f"***------ {name} profile ------***"
        )
        # "\n\n**Metadata**"
        # "\n- 🆔 *User ID:* <id>"
        # "\n- 📅 *Date Joined:* <date_joined>"
        + SIMPLE_PROPS(prefix, before_questions=True)
        + "\n***------❓Questions ------***"
        f"{ANSWERS(search)}"
        "\n***------------------------***"
        + SIMPLE_PROPS(prefix, before_questions=False)
        + f"\n- ***Status:***  <{prefix}status>"
        + "\n***------------------------***"
        + ("\n\nNumber of results: **<number_of_results>**" if search else "")
    )


def SIMPLE_PROPS(prefix, before_questions=True) -> str:  # pylint: disable=invalid-name
    return "".join(
        f"\n- ***{prop['label']}:***  <{prefix}{name}>"
        for name, prop in VISIBLE_SIMPLE_USER_PROPS.items()
        if before_questions == prop["before_questions"]
    )


def INIT_USERS_PATH() -> str:  # pylint: disable=invalid-name
    path = f"{USERS_FOLDER_PATH}/{APP_NAME}_users"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def back_btn(row=None):
    return Button(label="⬅️ Back", takes_to=ScreenId.BACK__, row=row)


def ok_btn(row=None):
    return Button(
        label="OK", style=ButtonStyle.green, takes_to=ScreenId.BACK__, row=row
    )


def home_btn(row=None):
    return Button(
        label="🏠 Home", style=ButtonStyle.primary, takes_to=ScreenId.HOME, row=row
    )


def back_home(row=None):
    return [back_btn(row=row), home_btn(row=row)]


def ok_home(row=None):
    return [ok_btn(row=row), home_btn(row=row)]


def PAGE_REFERENCE(action: str, content: str) -> str:  # pylint: disable=invalid-name
    return (
        "<page_reference>"
        f"\nClick on the corresponding reaction to {action}!"
        f"\n\n{content}\n\n<page_reference>"
    )
