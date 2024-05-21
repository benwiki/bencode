import os

def ANSWERS(search=False) -> str:  # pylint: disable=invalid-name
    from eagxf.constants import QUESTION_NAMES
    prefix = "search_" if search else ""
    return "\n" + "\n".join(
        f"__{question['text']}__" f"\n{question['emoji']}  <{prefix}{q_id}>"
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
    from eagxf.constants import VISIBLE_SIMPLE_USER_PROPS
    return "".join(
        f"\n- ***{prop['label']}:***  <{prefix}{prop_id}>"
        for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
        if before_questions == prop["before_questions"]
    )

def INIT_USERS_PATH() -> str:
    from eagxf.constants import APP_NAME, USERS_FOLDER_PATH
    path = f"{USERS_FOLDER_PATH}/{APP_NAME}_users"
    if not os.path.exists(path):
        os.makedirs(path)
    return path