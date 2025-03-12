# pylint: disable=broad-exception-caught

import asyncio
from functools import partial
from typing import Callable, Iterable, Iterator, Optional

import discord

from eagxf.button import Button
from eagxf.constant_functions import PROFILE
from eagxf.constants import (
    ADMINS,
    NUM_EMOJI,
    PRIO_LIST_LENGTH,
    QUESTION_PROPS,
    SPECIAL_DESTINATIONS,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.enums.effect import Effect
from eagxf.enums.meeting_time import MtgTime
from eagxf.enums.screen_id import ScreenId
from eagxf.managers.user_manager import UserManager
from eagxf.recommendations import Recommendation
from eagxf.screen import Screen
from eagxf.screens import SCREENS
from eagxf.status import STATUS_EMOJI
from eagxf.typedefs import DcButton, DcInteraction, DcMessage, DcView
from eagxf.user import User
from eagxf.util import peek, to_emojis


class OutputManager:
    def __init__(self, user_mng: UserManager) -> None:
        self.user_mng = user_mng
        self.users = user_mng.users
        self.debugging: bool = False

        self.replace_funcs: dict[str, Callable[[User], str]] = {
            "<search_results>": self.get_short_profiles,
            "<best_matches>": self.get_short_profiles,
            # lambda u: self.get_formatted_results_for(
            #     u, additional=u.get_score_summary
            # ),
            "<interests_sent>": self.get_short_profiles,
            "<interests_received>": self.get_short_profiles,
            "<mutual_interests>": self.get_short_profiles,
            "<selected_user_name>": lambda u: self.get_name_of(u.selected_user),
            "<selected_user_profile>": self.selected_user_profile,
            "<selected_user_meetings>": lambda u: self.get_meetings(
                u, MtgTime.FUTURE, selected=True, full=False
            ),
            "<future_meetings_peek>": lambda u: self.get_meetings(
                u, MtgTime.FUTURE, full=False
            ),
            "<past_meetings_peek>": lambda u: self.get_meetings(
                u, MtgTime.PAST, full=False
            ),
            "<future_meetings>": lambda u: self.get_meetings(u, MtgTime.FUTURE),
            "<past_meetings>": lambda u: self.get_meetings(u, MtgTime.PAST),
            "<recommendations_sent>": self.get_recommendations,
            "<recommendations_received>": partial(self.get_recommendations, sent=False),
            "<recommendations_sent_peek>": partial(
                self.get_recommendations, peek_=True
            ),
            "<recommendations_received_peek>": partial(
                self.get_recommendations, sent=False, peek_=True
            ),
            "<recommendation_receiver_name>": lambda u: self.get_name_of(
                self.users[u.selected_recommendation.receiver]
                if u.selected_recommendation
                else None
            ),
            "<recommended_person_name>": lambda u: self.get_name_of(
                self.users[u.selected_recommendation.person]
                if u.selected_recommendation
                else None
            ),
        }

    def start(self) -> None:
        self.init_screens()
        for user in self.users.values():
            asyncio.create_task(self.send_starting_message_to(user))
        asyncio.create_task(self.refresh_loop())

    async def send_starting_message_to(self, user: User) -> None:
        await self.send_screen(ScreenId.DELETING_OLD_MESSAGES, user)
        await self.remove_past_messages(user)
        # if user.id == 329635441433116674:
        #     # await user.delete_message()
        #     return
        await self.send_screen(ScreenId.HOME, user)

    async def remove_past_messages(self, user: User) -> None:
        if dc_user := self.user_mng.get_user(user.id):
            async for msg in dc_user.history(limit=None):
                if msg.author.id != dc_user.id and user.can_delete(msg.id):
                    await msg.delete()

    def init_screens(self) -> None:
        for screen_id, screen in SCREENS.items():
            screen.id = screen_id
            if screen.paged:
                screen.init_pagination()
            for button in screen.buttons:
                self.init_button_with(button, screen)

    def init_button_with(self, button: Button, screen: Screen) -> None:
        go_to_screen = SCREENS.get(button.takes_to) if button.takes_to else None
        button.callback = self.get_callback_to_screen(  # type: ignore
            go_to_screen, button=button
        )
        if screen.after_button_effects:
            button.effects += screen.after_button_effects

    def get_callback_to_screen(
        self,
        screen: Optional[Screen | ScreenId] = None,
        button: Optional[Button] = None,
    ):
        async def callback(interaction: DcInteraction) -> None:
            await interaction.response.defer()

            if button and button.effects:
                for effect in button.effects:
                    await self.apply_effect(effect, interaction)

            user = self.users[interaction.user.id]
            if button and button.takes_to in SPECIAL_DESTINATIONS:
                await self.send_special_screen(user, button)
            elif screen:
                await self.send_screen(screen, user)
            else:
                print(f"(Error #24) No screen found for the button '{button}'!")
            await user.msg_bundle.delete_front_spacer()

        return callback

    async def apply_effect(self, effect: Effect, interaction: DcInteraction) -> None:
        user = self.users[interaction.user.id]
        notification = None
        match effect:
            case Effect.GO_TO_PREVIOUS_PAGE:
                user.page -= 1
            case Effect.GO_TO_NEXT_PAGE:
                user.page += 1
            case Effect.DELETE_MESSAGE:
                await user.delete_message()
            case Effect.SAVE_BEST_MATCHES:
                user.save_priority_order()
            case Effect.RESET_NEW_PRIO_ORDER:
                user.best_match_prio_order_new = []
            case Effect.DEFAULT_BEST_MATCHES:
                user.update_priority_order(list(range(PRIO_LIST_LENGTH)))
            case Effect.RESET_USER_PROPERTY_CHANGE:
                user.change = None
            case Effect.EMPTY_RESULTS:
                user.results = []
                user.page = 0
            case Effect.SEND_INTEREST:
                user.send_interest_to_selected()
                assert user.selected_user, "(Error #25)"
                if user.interest_received_from_selected:
                    notification = ScreenId.NOTI_INTEREST_CONFIRMED
                else:
                    notification = ScreenId.NOTI_INTEREST_RECEIVED
            case Effect.CANCEL_INTEREST:
                user.cancel_interest_to_selected()
                assert user.selected_user, "(Error #26)"
                if user.interest_received_from_selected:
                    notification = ScreenId.NOTI_INTEREST_CANCELLED
            case Effect.CANCEL_MEETING:
                user.cancel_meeting_with_selected()
                notification = ScreenId.NOTI_MEETING_CANCELLED
            case Effect.START_CALL:
                client = self.user_mng.client
                await user.start_video_call_with_selected(client)
                notification = ScreenId.NOTI_CALL_STARTED
            case Effect.CANCEL_CALL:
                client = self.user_mng.client
                await user.cancel_video_call_with_selected(client)
                notification = ScreenId.NOTI_CALL_CANCELLED
            case Effect.CANCEL_RECOMMENDATION:
                user.cancel_selected_recommendation()
            case Effect.REMOVE_NOTIFICATION:
                if not interaction.message:
                    print("(Error #27)")
                    return
                await user.remove_notification(interaction.message.id)
            case Effect.SELECT_NOTIFICATION_SENDER:
                assert (
                    interaction.message
                ), "(Error #28) No message found for the interaction!"
                noti_id = interaction.message.id
                user.selected_user = self.users[user.notification_inbox[noti_id]]
            case Effect.RESET:
                dc_user = await self.user_mng.fetch_user(user.id)
                await user.msg_bundle.send_front_spacer(dc_user)
                await user.delete_message(spacer_too=True)
        if notification:
            assert user.selected_user, "(Error #29)"
            user.selected_user.replace.update({"<notification_sender>": user.name})
            m_id = await self.send_notification(user.selected_user, notification)
            user.selected_user.notification_inbox[m_id] = user.id

    async def send_notification(self, user: User, notification: ScreenId) -> int:
        screen = SCREENS[notification]
        msg, dc_view = await self.get_msg_and_dc_view(user, screen)
        noti = user.add_notification(msg, dc_view=dc_view)
        dc_user = await self.user_mng.client.fetch_user(user.id)
        await noti.send_to(dc_user)
        assert noti.dc_message, "(Error #30) No message found for the notification!"
        return noti.dc_message.id

    async def send_special_screen(self, user: User, button: Button) -> None:
        match button.takes_to:
            case ScreenId.BACK__ if user.last_screen:
                if user.can_go_back:
                    user.remove_last_screen()
                await self.send_screen(user.last_screen, user)
            case ScreenId.BACK_UNTIL_STOP__:
                user.remove_screens_until_stop()
                last_screen = user.last_screen
                assert (
                    last_screen is not None
                ), "(Error #31) No screen found for the button!"
                await self.send_screen(last_screen, user)

    async def refresh_loop(self) -> None:
        while True:
            await asyncio.sleep(30)
            await self.refresh_all()

    async def refresh_all(self) -> None:
        for user in self.user_mng.users.values():
            if user.last_screen and not user.sleeping:
                await self.try_refreshing(user)

    async def try_refreshing(self, user: User) -> None:
        try:
            await self.send_screen(user.last_screen, user)
        except Exception as e:
            print(f"Error while refreshing {user.name}: {e}")

    async def send_screen(self, screen: Screen | ScreenId, user: User) -> None:
        if isinstance(screen, ScreenId):
            screen = SCREENS[screen]
        just_refreshed = user.last_screen == screen
        user.stack(screen)
        user.results = self.screen_to_data(user, screen.id)

        msg, dc_view = await self.get_msg_and_dc_view(user, screen)
        user.update_message(msg, dc_view=dc_view)
        dc_user = self.user_mng.fetch_user(user.id)
        await user.send_message(receiver_future=dc_user)

        if screen.changed_property:
            user.change = screen.changed_property

        if user.add_reactions and not just_refreshed:
            if screen.reactions:
                for emoji in screen.reactions:
                    await user.add_reaction_to_message(emoji)
            if screen.paged:
                await user.add_selection_reactions()

    def screen_to_data(self, user: User, screen_id: ScreenId) -> list:
        match screen_id:
            case ScreenId.SEARCH | ScreenId.SHOW_SEARCH_RESULTS:
                return self.user_mng.search_users_for(user)
            case ScreenId.BEST_MATCHES:
                return self.user_mng.search_best_matches_for(user)
            case ScreenId.INTERESTS_SENT:
                return user.interests_sent_not_received
            case ScreenId.INTERESTS_RECEIVED:
                return user.interests_received_not_sent
            case ScreenId.MUTUAL_INTERESTS:
                return user.mutual_interests
            case ScreenId.FUTURE_MEETINGS:
                return list(sorted(user.future_meetings))
            case ScreenId.PAST_MEETINGS:
                return list(sorted(user.past_meetings))
            case ScreenId.RECOMMEND_USER:
                return user.recommendables
            case ScreenId.RECOMMENDATIONS_SENT:
                return user.recommendations_sent
            case ScreenId.RECOMMENDATIONS_RECEIVED:
                return user.recommendations_received
            case _:
                return []

    async def get_msg_and_dc_view(
        self, user: User, screen: Screen
    ) -> tuple[str, DcView]:
        if not user.screen_conditions_apply_for(screen):
            ok_button = Button.ok()
            ok_button.callback = self.get_callback_to_screen(None, ok_button)  # type: ignore
            dc_view = self.get_dc_view([ok_button], user)
            message = screen.condition_message
            user.add_reactions = False
        else:
            buttons: Iterator[Button] = filter(
                user.btn_conditions_apply_for, screen.buttons
            )
            dc_view = self.get_dc_view(buttons, user)
            message = self.replace_placeholders(screen.message, user)
            user.add_reactions = True

        # message_text = SPACER + message if screen.spacer else message
        return message, dc_view

    def get_dc_view(
        self, buttons: Iterable[Button | DcButton], user: Optional[User] = None
    ) -> DcView:
        dc_view = DcView()
        for button in buttons:
            dc_view.add_item(button)
        if self.debugging and (not user or user.id in ADMINS):
            print("Adding DEBUGGING button to view.")
            stop_btn = Button(label="STOP", style=discord.ButtonStyle.red)
            stop_btn.callback = self.stop_callback  # type: ignore
            dc_view.add_item(stop_btn)
        return dc_view

    async def stop_callback(self, interaction: DcInteraction) -> None:
        await interaction.response.defer()
        await self.stop_request_by(interaction.user.id)

    async def stop_request_by(self, user_id: int) -> None:
        if user_id not in ADMINS:
            print("(Error #32) Unauthorized user ", end="")
            print(f"(id: {user_id}) tried to stop the bot.")
            return
        await self.user_mng.stop()

    async def toggle_debug(self, user_id: int) -> bool:
        if user_id not in ADMINS:
            print("(Error #33) Unauthorized user ", end="")
            print(f"(id: {user_id}) tried to toggle debug.")
            return False
        self.debugging = not self.debugging
        await self.refresh_all()
        return True

    def replace_placeholders(self, msg: str, user: User | None) -> str:
        if user:
            msg = user.replace_placeholders(msg)
            for placeholder, function in self.replace_funcs.items():
                if placeholder in msg:
                    msg = msg.replace(placeholder, function(user))
        return msg

    def get_formatted_results_for(
        self,
        user: User,
        additional: Optional[Callable[[User], str]] = None,
    ) -> str:
        if not user.results:
            return "***No results to show.***"
        separator = "***========================***\n"
        return separator + f"\n\n{separator}".join(
            f"{to_emojis(i+1)} .: ***{u.name}*** :. "
            f"(Status: {STATUS_EMOJI[u.status]} "
            f"({u.status.value}))"
            f"{additional(u) if additional else ''}"
            + "".join(
                f"\n- *{p['label']}:* {getattr(u, p_id.to_str)}"
                for p_id, p in VISIBLE_SIMPLE_USER_PROPS.items()
                if p_id != "name"
            )
            + "\n***------❓Questions ------***"
            + "".join(
                f"\n- *{q['label']}:* {peek(u.questions[q_id])}"
                for q_id, q in QUESTION_PROPS.items()
            )
            for i, u in enumerate(self.user_mng.get_results_for(user))
        )

    def get_short_profiles(self, user: User) -> str:
        if not user.results:
            return "***No one to show here.***"
        return "\n".join(
            f"{user.page_prefix(i+1)}{NUM_EMOJI[i]} "
            f"{u.name} {STATUS_EMOJI[u.status]}\n- Job: {u.job}\n- Company: {u.company}\n"
            for i, u in enumerate(self.user_mng.get_results_for(user))
        )

    def get_meetings(self, user: User, time: MtgTime, selected=False, full=True) -> str:
        meetings = {
            MtgTime.FUTURE: sorted(user.future_meetings),
            MtgTime.PAST: sorted(user.past_meetings, reverse=True),
        }.get(time, [])

        if selected and user.selected_user:
            meetings = [m for m in meetings if m.partner_id == user.selected_user.id]
        if not meetings:
            return "***No meetings to show.***"

        dots_needed = False
        if full:
            meetings = user.paged_list_of(meetings)
        else:
            dots_needed = len(meetings) > 5
            meetings = meetings[:5]

        return "\n".join(
            ("- " if not full else f"{user.page_prefix(i+1)}{NUM_EMOJI[i]} ")
            + f"**{m.date}**"
            + (f" with ***{self.users[m.partner_id].name}***" if not selected else "")
            for i, m in enumerate(meetings)
        ) + ("\n**...**" if dots_needed else "")

    def get_recommendations(
        self, user: User, sent: bool = True, peek_: bool = False
    ) -> str:
        recommendations = (
            user.recommendations_sent if sent else user.recommendations_received
        )
        if not recommendations:
            return "***No recommendations to show.***"

        dots_needed = False
        if peek_:
            dots_needed = len(recommendations) > 5
            recommendations = recommendations[:5]
        else:
            recommendations = user.paged_list_of(recommendations)

        return "\n".join(
            ("- " if peek_ else f"{user.page_prefix(i+1)}{NUM_EMOJI[i]} ")
            + (
                f"***{self.users[rec.person].name}*** "
                + (
                    f"to *{self.users[rec.receiver].name}*"
                    if sent
                    else f"by *{self.users[rec.sender].name}*"
                )
                + f" ({peek(rec.message)})"
            )
            + ("\n**...**" if dots_needed else "")
            for i, rec in enumerate(recommendations)
            if isinstance(rec, Recommendation)
        )

    def get_name_of(self, user: User | None) -> str:
        return user.name if user else "(no user selected)"

    def selected_user_profile(self, user: User) -> str:
        if not user.selected_user:
            return ""
        return user.selected_user.replace_placeholders(
            PROFILE(name=self.get_name_of(user.selected_user) + "'s")
        )

    async def send_succesful_prop_change(
        self, user: User, changed_from: str, changed_to: str, msg: DcMessage
    ) -> None:
        await msg.add_reaction("✅")
        user.remove_screens_until_stop()
        user.replace.update(
            {
                "<changed_prop>": changed_from,
                "<new_value>": "'*" + peek(changed_to.replace("*", r"\*")) + "*'",
                "<plus_info>": user.additional_info_with_side_effects(),
            }
        )
        await self.send_screen(ScreenId.SUCCESSFUL_PROP_CHANGE, user)
        user.change = None
        user.save()
