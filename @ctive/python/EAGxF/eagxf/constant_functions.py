# pylint: disable=invalid-name

import os

from eagxf.constants import (
    APP_NAME,
    QUESTION_PROPS,
    USERS_FOLDER_PATH,
    VISIBLE_SIMPLE_USER_PROPS,
)


def ANSWERS(search=False) -> str:
    prefix = "search_" if search else ""
    return "\n" + "\n".join(
        f"{question['emoji']} __{question['text']}__" f"\n<{prefix}{q_id}_peek>"
        for q_id, question in QUESTION_PROPS.items()
    )


def PROFILE(search=False, name="Your") -> str:
    prefix = "search_" if search else ""
    return (
        (
            f"{"\\_" * 7} ***Current filters*** {"\\_" * 7}"
            if search
            else f"{"\\_" * 7} ***{name} profile*** {"\\_" * 7}"
        )
        # "\n\n**Metadata**"
        # "\n- 🆔 *User ID:* <id>"
        # "\n- 📅 *Date Joined:* <date_joined>"
        + SIMPLE_PROPS(prefix, before_questions=True)
        + f"\n{"\\_" * 7}***❓Questions*** {"\\_" * 7}"
        f"{ANSWERS(search)}"
        f"\n{"\\_" * 27}"
        + SIMPLE_PROPS(prefix, before_questions=False)
        + f"\n- ***Status:***  <{prefix}status>"
        f"\n{"\\_" * 27}"
        + ("\n\nNumber of results: **<number_of_results>**" if search else "")
    )


def SIMPLE_PROPS(prefix, before_questions=True) -> str:
    return "".join(
        f"\n- ***{prop['label']}:***  <{prefix}{name}>"
        for name, prop in VISIBLE_SIMPLE_USER_PROPS.items()
        if before_questions == prop["before_questions"]
    )


def INIT_USERS_PATH() -> str:
    path = f"{USERS_FOLDER_PATH}/{APP_NAME}_users"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def PAGE_REFERENCE(action: str, content: str) -> str:
    return (
        "<page_reference>"
        f"\nClick on the corresponding reaction to {action}!"
        f"\n\n{content}\n\n"
        "<page_reference>"
    )
