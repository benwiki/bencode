import json

from eagxf.constants import QUESTION_NAMES, VISIBLE_SIMPLE_USER_PROPS
from eagxf.date import Date
from eagxf.platform_user import PlatformUser
from eagxf.status import Status


class UserManager:
    @staticmethod
    def dumps(user: PlatformUser):
        return json.dumps(
            {
                "id": user.id,
                "date_joined": str(user.date_joined),
                "questions": user.questions,
                "status": user.status.value,
                "best_match_prio_order": user.best_match_prio_order,
                "interests": user.interests,
                **{
                    attr: getattr(user, attr)
                    for attr in VISIBLE_SIMPLE_USER_PROPS
                },
            },
            indent=4,
        )

    @staticmethod
    def load(user_data: dict):
        d, m, y = map(int, user_data["date_joined"].split("."))
        return PlatformUser(
            id=user_data["id"],
            date_joined=Date(day=d, month=m, year=y),
            questions=user_data["questions"],
            status=Status(user_data["status"]),
            best_match_prio_order=user_data["best_match_prio_order"],
            interests=user_data["interests"],
            search_filter=PlatformUser(
                questions={q: "?" for q in QUESTION_NAMES}, status=Status.ANY
            ),
            **{
                attr: user_data[attr]
                for attr in VISIBLE_SIMPLE_USER_PROPS
            },
        )
