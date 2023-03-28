import dataclasses
import json


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


if __name__ == "__main__":
    main()
