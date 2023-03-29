import dataclasses
import json
from itertools import groupby


@dataclasses.dataclass(frozen=True, eq=True)
class MeasureEntry:
    boy: str
    length: int
    date: str


def read_dump(path):
    with open(path, mode="r", encoding="utf-8") as fin:
        return json.loads(fin.read())


def filter_message(message):
    return message["type"] == "message" and message.get("via_bot", "").startswith("@rus_") \
           and len(message.get("text", [])) == 3 and message["text"][0].startswith("My ")


def payload_to_me_mapper(message):
    return MeasureEntry(
        message.get("from", "unknown"),
        int(message.get("text")[1]["text"][:-2]),
        message.get("date").split("T")[0]
    )


def main():
    r_json = read_dump("../result.json")
    measures = set(map(payload_to_me_mapper, filter(filter_message, r_json.get("messages", []))))
    dates = list(sorted(set(map(lambda x: x.date, measures))))
    print(len(measures), len(dates))
    r_grouped = groupby(sorted(measures, key=lambda x: x.date), lambda x: x.date)
    counter = 0
    for k, v in r_grouped:
        l = list(v)
        print(l)
        counter += 1 if sum(map(lambda x: x.length, l)) >= 100 else 0

    print(counter)


if __name__ == "__main__":
    main()
