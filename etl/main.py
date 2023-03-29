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


name_mapper = read_dump("../config/name_mapper.json")


def filter_message(message):
    return message["type"] == "message" and message.get("via_bot", "").startswith("@rus_") \
           and len(message.get("text", [])) == 3 and message["text"][0].startswith("My ")


def payload_to_me_mapper(message):
    return MeasureEntry(
        name_mapper.get(message.get("from", "unknown"), "unknown"),
        int(message.get("text")[1]["text"][:-2]),
        message.get("date").split("T")[0]
    )


def date_results_mapper(measure_list_iterator):
    measure_list = list(measure_list_iterator)
    sum_ = sum(map(lambda x: x.length, measure_list))
    return {
        "measures": [dataclasses.asdict(x) for x in measure_list],
        "sum": sum_,
        "win": sum_ >= 100
    }


def main():
    r_json = read_dump("../result.json")
    measures = set(map(payload_to_me_mapper, filter(filter_message, r_json.get("messages", []))))
    r_grouped = groupby(sorted(measures, key=lambda x: x.date), lambda x: x.date)

    transformed = {k: date_results_mapper(v) for k, v in r_grouped}

    print(json.dumps(transformed))


if __name__ == "__main__":
    main()
