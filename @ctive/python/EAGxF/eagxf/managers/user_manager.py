import os
from typing import Callable, Iterator

from eagxf.status import Status
from eagxf.typedefs import DcClient, DcUser
from eagxf.user import User
from eagxf.users_path import USERS_PATH


class UserManager:
    def __init__(self, client: DcClient) -> None:
        self.client = client
        self.users: dict[int, User] = self.load_users()
        self.prio_functions: list[Callable[[User, User], int | Status]] = [
            lambda u1, u2: u1.get_language_score(u2),
            lambda u1, u2: u1.get_question_score(u2),
            lambda u1, u2: u1.get_keywords_score(u2),
            lambda u1, u2: u1.get_location_distance(u2),
            lambda u1, u2: u1.get_status(u2),
            lambda u1, u2: u1.get_job_score(u2),
            lambda u1, u2: u1.get_company_score(u2),
        ]

    def load_users(self) -> dict[int, User]:
        return {
            int(id_str): User.load_by_id(id_str)
            for filename in os.listdir(USERS_PATH)
            if (id_str := self.valid_file_name(filename))
        }

    def valid_file_name(self, name: str) -> str:
        if name.endswith(".json") and (id_str := name[:-5]).isdecimal():
            return id_str
        return ""

    def register_user(self, dc_user: DcUser) -> User:
        user = self.users[dc_user.id] = User.from_dc_user(dc_user)
        user.save()
        return user

    def get_user(self, user_id: int) -> DcUser | None:
        return self.client.get_user(user_id)

    async def fetch_user(self, user_id: int) -> DcUser:
        return await self.client.fetch_user(user_id)

    async def stop(self) -> None:
        for user in self.users.values():
            await user.delete_message(spacer_too=True)
        await self.client.close()

    def search_users_for(self, user_searching: User) -> list[int]:
        return [
            user.id
            for user in self.users.values()
            if user.is_selected_by(user_searching)
        ]

    def search_best_matches_for(self, user: User) -> list[int]:
        matches_list = sorted(
            filter(
                lambda u: u.id != user.id and u.status != Status.INVISIBLE,
                self.users.values(),
            ),
            key=lambda u: self.get_priority(user, u),
            reverse=True,
        )
        return [u.id for u in matches_list]

    def get_priority(self, user: User, u: User) -> tuple:
        """This function takes into account the best match priority order of the user"""
        return tuple(
            self.prio_functions[i](user, u) for i in user.best_match_prio_order
        )

    def get_results_for(self, user: User) -> Iterator[User]:
        return self.users_by_ids(user.paged_list_of_results())

    def users_by_ids(self, user_ids: list[int]) -> Iterator[User]:
        return map(lambda x: self.users[x], user_ids)
