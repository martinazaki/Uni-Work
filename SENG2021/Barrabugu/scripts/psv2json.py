import csv
import json

enrolments = []

with open("db/enrolments.psv", "r") as psvfile, open(
    "db/enrolments.json", "w"
) as jsonfile:
    reader = csv.reader(psvfile, delimiter="|")

    # Course|zID|Name|Degree Number|Program|Wam|Term|DoB|Gender
    for row in reader:
        for i, element in enumerate(row):
            row[i] = element.strip()

        duplicate = False
        for enrolment in enrolments:
            if row[1] == enrolment["zID"]:
                duplicate = True
                # print(list(enrolment.values()), "\n", row, "\n", sep="")

        if duplicate:
            continue

        enrolments.append(
            {
                "course": row[0],
                "zID": row[1],
                "Name": row[2],
                "Degree Number": row[3],
                "Program": row[4],
                "WAM": row[5],
                "Term": row[6],
                "DoB": row[7],
                "Gender": row[8],
            }
        )

    json.dump(enrolments, jsonfile)
