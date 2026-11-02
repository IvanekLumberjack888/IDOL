
import subprocess
import os
from datetime import date, datetime, timedelta

# IDOL – 5x7 pixel font
letters = [
    [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "11111",
    ],
    [
        "11110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "11110",
    ],
    [
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
    [
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "11111",
    ],
]

# Combine letters with one column of spacing
rows = []
for y in range(7):
    rows.append("0".join(letter[y] for letter in letters))

# Check Git repository
subprocess.run(
    ["git", "rev-parse", "--is-inside-work-tree"],
    check=True,
    capture_output=True
)

# Use 23 completed weeks, ending on Saturday
today = date.today()
last_saturday = today - timedelta(
    days=(today.weekday() + 2) % 7
)
start = last_saturday - timedelta(weeks=22, days=6)

count = 0

for x in range(23):
    for y in range(7):
        if rows[y][x] == "1":
            commit_date = start + timedelta(days=x * 7 + y)

            timestamp = datetime.combine(
                commit_date,
                datetime.min.time()
            ).replace(hour=12).isoformat()

            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = timestamp
            env["GIT_COMMITTER_DATE"] = timestamp

            subprocess.run(
                [
                    "git", "commit",
                    "--allow-empty",
                    "-m", "IDOL pixel"
                ],
                env=env,
                check=True
            )

            count += 1

print(f"IDOL generated: {count} commits")
print("Push your branch to GitHub to publish.")
