from functools import partial
from typing import Callable

from eagxf.constants import MAX_PROP_LENGTH, QUESTION_PROPS, REACTION_PROPERTIES
from eagxf.date import Date
from eagxf.enums.property import Property
from eagxf.enums.screen_id import ScreenId
from eagxf.managers.output_manager import OutputManager
from eagxf.typedefs import DcMessage
from eagxf.user import User


class TextinputManager:
    def __init__(self, output_mng: OutputManager) -> None:
        self.output_mng = output_mng
        self.users = output_mng.users

        self.message_funcs: dict[Property, Callable] = {
            Property.MEETING_REQUEST: self.handle_meeting_date,
            Property.CHANGE_MEETING_DATE: partial(
                self.handle_meeting_date, change=True
            ),
            **{  # ABOUT_ME, ..., CONCERNS
                q: partial(self.handle_question_change, q_to_change=q)
                for q in QUESTION_PROPS
            },
            **{  # SEARCH_ABOUT_ME, ..., SEARCH_CONCERNS
                q: partial(self.handle_question_change, q_to_change=q)
                for q in [q.to_search() for q in QUESTION_PROPS]
            },
        }

    async def handle_input(self, msg: DcMessage) -> None:
        user = self.users.get(msg.author.id)
        if user is None or user.change is None or user.change in REACTION_PROPERTIES:
            return

        await user.delete_message()

        prop_to_change = user.change
        searching = prop_to_change.is_search()
        if searching:  # chop off the "search_" prefix
            prop_to_change = prop_to_change.from_search()

        change_user = user
        if searching and user.search_filter is not None:
            change_user = user.search_filter
        elif searching:
            return

        plural = prop_to_change in [Property.KEYWORDS, Property.LANGUAGES]
        kw_needed = plural or searching and prop_to_change in QUESTION_PROPS
        new_prop_value = msg.content

        if kw_needed:
            need_caps = prop_to_change == Property.LANGUAGES
            evenly_spaced_kws = self.evenly_space(msg.content, need_caps)
            new_prop_value = evenly_spaced_kws

        if message_function := self.message_funcs.get(prop_to_change):
            await message_function(user, new_prop_value, msg)
        else:
            setattr(change_user, prop_to_change.to_str, new_prop_value)
            changed_prop = f"changed {prop_to_change.to_str}"
            await self.output_mng.send_succesful_prop_change(
                user, changed_from=changed_prop, changed_to=new_prop_value, msg=msg
            )

    def evenly_space(self, text: str, capitalize: bool) -> str:
        return ", ".join(
            " & ".join(
                w.capitalize() if capitalize else w
                for w in map(str.strip, kw.split("&"))  # type: ignore
            )
            for kw in map(str.strip, text.split(","))  # type: ignore
        )

    async def handle_meeting_date(
        self, user: User, date_str: str, msg: DcMessage, change: bool = False
    ) -> None:
        if not Date.valid_future_date(date_str):
            await msg.add_reaction("❌")
            await self.output_mng.send_screen(ScreenId.INVALID_DATE, user)
            return
        assert user.selected_user, "(Error #34) No selected user for meeting!"
        if change:
            user.cancel_meeting_with_selected()
        user.request_meeting_with_selected(Date.from_str(date_str))
        verb = "changed your" if change else "requested a new"
        changed_prop = f"{verb} meeting with ***{user.selected_user.name}***"
        await self.output_mng.send_succesful_prop_change(
            user, changed_from=changed_prop, changed_to=date_str, msg=msg
        )
        if not change:
            user.selected_user.replace.update({
                "<notification_sender>": user.name,
            })
            notification = ScreenId.NOTI_MEETING_REQUESTED
            await self.output_mng.send_notification(user.selected_user, notification)

    async def handle_question_change(
        self, user: User, new_val: str, msg: DcMessage, q_to_change: Property
    ) -> None:
        if searching := q_to_change.is_search():
            q_to_change = q_to_change.from_search()
        question = QUESTION_PROPS[q_to_change]
        changed_prop = f"changed answer to the question '**{question['label']}**'"
        if len(new_val) > MAX_PROP_LENGTH:
            await msg.add_reaction("❌")
            await self.too_long_question(user, changed_prop, new_val)
            return
        user.set_new_question_val(q_to_change, new_val, searching)
        await self.output_mng.send_succesful_prop_change(
            user, changed_from=changed_prop, changed_to=new_val, msg=msg
        )

    async def too_long_question(
        self, user: User, changed_prop: str, new_val: str
    ) -> None:
        user.replace.update({
            "<changed_prop>": f"The {changed_prop}",
            "<exceeding_number>": str(len(new_val) - MAX_PROP_LENGTH),
            "<to_cut_off>": new_val[MAX_PROP_LENGTH:],
        })
        await self.output_mng.send_screen(ScreenId.TOO_LONG_PROP_TEXT, user)
