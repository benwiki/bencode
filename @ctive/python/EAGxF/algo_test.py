import csv
from pprint import pformat, pprint
from typing import Callable

from eagxf.constants import NOT_ALPHANUMERIC, Q_MAPPING, QUESTION_PROPS
from eagxf.enums.property import Property
from eagxf.questions import Questions
from eagxf.user import User

users: list[User] = []
with open("data.csv", "r", encoding="utf-8") as data:
    reader = csv.reader(data)
    first = True
    for line in reader:
        if first:
            first = False
            continue
        user = User(
            id=int(line[0]),
            company=line[1],
            job=line[2],
            questions=Questions(
                about_me=line[3],
                need_help=line[4],
                can_help=line[5],
            ),
        )
        users.append(user)


def search_best_matches_for(user: User, n: int):
    matches_list = sorted(
        (
            (u.id, get_priority(user, u))
            for u in filter(lambda u: u.id != user.id, users)
        ),
        key=lambda l: l[1],
        reverse=True,
    )
    return matches_list[:n]


def get_priority(u1: User, u2: User) -> tuple:
    """This function takes into account the best match priority order of the user"""
    return tuple(fn(u1, u2) for fn in prio_functions)


def get_score_between(q1: Questions, q2: Questions) -> int:
    with open("stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = set(f.read().splitlines())
    return sum(  # type: ignore
        (  # type: ignore
            (1.0 if q_id2 == Q_MAPPING[q_id1] else 0.5)
            if kw in q2[q_id2].lower()
            else 0.0  # type: ignore
        )
        for q_id1 in QUESTION_PROPS
        if q_id1 != Property.CONCERNS
        for q_id2 in QUESTION_PROPS
        if q_id2 != Property.CONCERNS
        for kw in NOT_ALPHANUMERIC.split(q1[q_id1].lower())
        if kw not in stopwords
    )


def get_kws_with_scores(q1: Questions, q2: Questions) -> dict:
    with open("stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = set(f.read().splitlines())
    return {
        q_id1.to_str: {
            q_id2.to_str: list(
                (
                    kw,
                    ((1.0 if q_id2 == Q_MAPPING[q_id1] else 0.5)),
                )
                for kw in NOT_ALPHANUMERIC.split(q1[q_id1].lower())
                if kw not in stopwords and kw in q2[q_id2].lower()
            )
            for q_id2 in QUESTION_PROPS
            if q_id2 != Property.CONCERNS
        }
        for q_id1 in QUESTION_PROPS
        if q_id1 != Property.CONCERNS
    }


prio_functions: list[Callable[[User, User], int]] = [
    # lambda u1, u2: u1.get_language_score(u2),
    # lambda u1, u2: u1.get_question_score(u2),
    lambda u1, u2: get_score_between(u1.questions, u2.questions),
    # lambda u1, u2: u1.get_keywords_score(u2),
    # lambda u1, u2: u1.get_location_distance(u2),
    # lambda u1, u2: u1.get_status(u2),
    lambda u1, u2: u1.get_job_score(u2),
    lambda u1, u2: u1.get_company_score(u2),
]

first = True
first1 = True
first3 = True
while True:
    print()
    print("Menu. Choose:")
    print("1. Search best matches for users.")
    print("2. Get insight in the score between two users.")
    print("3. Get ranking index of a user compared to another.")
    print("4. Print profile of a user.")
    print("5. Exit.")
    choice = input("Choice: ")
    print()
    if choice == "1":
        how_many_raw = input("How many best matches to show? ")
        if how_many_raw == "done":
            continue
        how_many = int(how_many_raw)
        print("\nOk!\n")
        if first1:
            print("<-- Just write 'done' to exit.")
            input("Press Enter to continue.")
            print()
            first1 = False
        while True:
            user_id_raw = input("Enter user ID: ")
            if user_id_raw == "done":
                break
            user_id = int(user_id_raw)
            user = next(filter(lambda u: u.id == user_id, users), None)  # type: ignore
            if user is None:
                print("User not found.")
            else:
                pprint(search_best_matches_for(user, how_many))
            print()
    elif choice == "2":
        if first:
            print("-----------------------------")
            print(
                "You will give two user IDs, the first one is the seeker, the second one is the target."
            )
            print(
                "The program will count, how many of the seeker's words are in the target's questions,"
            )
            print(
                "not counting the stopwords. You can change the stopwords in the file 'stopwords.txt'."
            )
            print()
            print("Then the program generates a file with the keywords and the scores,")
            print("with this kind of name: 'seeker-id_target-id.txt'.")
            print("The program will also print the total score.")
            print()
            print("<-- Just write 'done' to exit.")
            input("Press Enter to continue.")
            print()
            first = False
        while True:
            user_id1_raw = input("Enter seeker's ID: ")
            if user_id1_raw == "done":
                break
            user_id2_raw = input("Enter target's ID: ")
            if user_id2_raw == "done":
                break
            user_id1 = int(user_id1_raw)
            user_id2 = int(user_id2_raw)
            user1 = next(filter(lambda u: u.id == user_id1, users), None)
            user2 = next(filter(lambda u: u.id == user_id2, users), None)
            if user1 is None or user2 is None:
                print("User not found.")
            else:
                print(
                    "=== Total score:",
                    get_score_between(user1.questions, user2.questions),
                )
                with open(f"{user1.id}_{user2.id}.txt", "w", encoding="utf-8") as f:
                    kws_with_scores = get_kws_with_scores(
                        user1.questions, user2.questions
                    )
                    f.write(pformat(kws_with_scores))
                    f.write(f"\nTotal score: {user1.get_question_score(user2)}")
            print("File generated.")
            print()
    elif choice == "3":
        if first3:
            print("-----------------------------")
            print(
                "First you provide the seeker's ID, then you can give IDs of targets."
            )
            print(
                "The program will print the ranking index of the target compared to the seeker."
            )
            print()
            print("<-- Just write 'done' to exit.")
            input("Press Enter to continue.")
            print()
            first3 = False
        seeker_raw = input("(only once) Enter seeker's ID: ")
        if seeker_raw == "done":
            break
        seeker = int(seeker_raw)
        print("-----------------")
        while True:
            target_raw = input("Enter target's ID: ")
            if target_raw == "done":
                break
            target = int(target_raw)
            user1 = next(filter(lambda u: u.id == seeker, users), None)  # type: ignore
            user2 = next(filter(lambda u: u.id == target, users), None)  # type: ignore
            if user1 is None or user2 is None:
                print("User not found.")
            else:
                best_matches = search_best_matches_for(user1, len(users))
                print(
                    "Ranking on the best match list:",
                    best_matches.index((user2.id, get_priority(user1, user2))) + 1,
                )
            print()
    elif choice == "4":
        user_id = int(input("Enter user ID: "))
        user = next(filter(lambda u: u.id == user_id, users), None)  # type: ignore
        if user is None:
            print("User not found.")
        else:
            pprint(user)
        input("Press Enter to continue.")
    elif choice == "5":
        break
    else:
        print("Invalid choice.")
        input("Press Enter to continue.")
