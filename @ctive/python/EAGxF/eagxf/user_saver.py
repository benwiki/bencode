import json

from eagxf.date import Date
from eagxf.platform_user import PlatformUser
from eagxf.status import Status


class UserSaver:
    @staticmethod
    def dumps(user: PlatformUser):
        return json.dumps(
            {
                "id": user.id,
                "date_joined": str(user.date_joined),
                "name": user.name,
                "title": user.title,
                "location": user.location,
                "languages": user.languages,
                "questions": user.questions,
                "keywords": user.keywords,
                "status": user.status.value,
                "best_match_prio_order": user.best_match_prio_order,
            }
        )

    @staticmethod
    def load(user_data: dict):
        d, m, y = map(int, user_data["date_joined"].split("."))
        return PlatformUser(
            id=user_data["id"],
            date_joined=Date(day=d, month=m, year=y),
            name=user_data["name"],
            title=user_data["title"],
            location=user_data["location"],
            languages=user_data["languages"],
            questions=user_data["questions"],
            keywords=user_data["keywords"],
            status=Status(user_data["status"]),
            best_match_prio_order=user_data["best_match_prio_order"],
            search_filter=PlatformUser(
                questions={"need_help": "?", "can_help": "?"}, status=Status.ANY
            ),
        )
