"""
Dumps to stdout based on the data given in stdin (format like enrolments.json)
{
    "details": {
        "<email>": {
            "name": "...",
            "email": "...",
            "description": "...",
        },
        ...
    }
    "teams": {
        "teamname": ['z1', 'z2', 'z3'],
        ...
    },
    "teamless": ['z9', 'z8', 'z7']
}
"""

import sys
import json
import random
import click
from collections import defaultdict


def get_email(zid):
    assert zid[0] != "z"
    return f"z{zid}@unsw.edu.au"


def get_name(fullname):
    """ <lastname>, <firstname> <middle names> to <firstname> <lastname> """
    parts = fullname.split()
    return f"{parts[1]} {parts[0][:-1]}"


def get_details(student_enrolment):
    return {
        "name": get_name(student_enrolment["Name"]),
        "email": get_email(student_enrolment["zID"]),
        "description": student_enrolment["Program"],
    }


@click.command()
@click.option("--seed", "seed", default=1, help="Seed the randomness engine")
@click.option("--teams", "number_of_teams", default=10, help="number of teams")
@click.option(
    "--size",
    "team_size",
    default="5",
    help="team size. Exact number (5) or range (2-5), ends included",
)
@click.option(
    "--teamless",
    "number_of_teamless_students",
    default=10,
    help="number of teamless students",
)
def main(seed, number_of_teams, team_size, number_of_teamless_students):
    """ Generates teams organisation as JSON (to stdout) based on the data fed in stdin """
    enrolments = json.load(sys.stdin)

    if "-" in team_size:
        try:
            team_size_min, team_size_max = [int(n) for n in team_size.split("-")]
        except Exception as e:
            print("invalid size argument. Examples include '5', or '2-6'", sys.stderr)
            raise e

        if team_size_min > team_size_max:
            raise ValueError(
                f"invalid range ({team_size_min}-{team_size_max}). Min should be <= than max"
            )
    else:
        team_size_min = team_size_max = int(team_size)

    if number_of_teamless_students + number_of_teams * team_size_max > len(enrolments):
        print("not enough student to guarantee success in database")
        exit(1)

    rand = random.Random(seed)
    rand.shuffle(enrolments)

    assert len(enrolments) == len(set(student["zID"] for student in enrolments))

    obj = {"details": {}, "teams": {}, "teamless": []}

    head = 0
    for team_number in range(number_of_teams):
        team_size = rand.randint(team_size_min, team_size_max)
        students = enrolments[head : head + team_size]

        obj["teams"][f"team-{team_number}"] = []
        for student in students:
            obj["details"][get_email(student["zID"])] = get_details(student)
            obj["teams"][f"team-{team_number}"].append(get_email(student["zID"]))

        head += team_size

    for student in enrolments[head : head + number_of_teamless_students]:
        obj["teamless"].append(get_email(student["zID"]))
        obj["details"][get_email(student["zID"])] = get_details(student)

    json.dump(obj, sys.stdout, indent=2)

    check_validity(obj)


def check_validity(obj):
    # key matches email
    for email, details in obj["details"].items():
        assert email == details["email"], "key should match the email"

    # unique emails
    assert len(set(obj["details"])) == len(obj["details"]), "emails aren't unique"

    # no student shows up anywhere twice
    students_seen = defaultdict(list)
    for student_email in obj["teamless"]:
        students_seen[student_email].append("teamless")

    for teamname, team in obj["teams"].items():
        for student_email in team:
            students_seen[student_email].append(f"team {teamname}")

    duplicates = {}
    for student_email in students_seen:
        if len(students_seen[student_email]) != 1:
            duplicates[student_email] = students_seen[student_email]

    if len(duplicates) != 0:
        raise ValueError(f"students {duplicates} found multiple times")


if __name__ == "__main__":
    main()
