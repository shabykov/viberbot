import json


def read(filename):
    fd = open(filename, mode='r')
    for log in fd:
        yield log
    fd.close()


def parse(log):
    parsed = []
    for line in log:
        if 'Event: b' in line:
            parsed.append(json.loads(line.split('Event: b')[-1].replace("'", '')))
    return parsed


def save(parsed):
    with open('data.json', 'w') as outfile:
        json.dump(parsed, outfile)


if __name__ == "__main__":
    log = read('dump.log')
    parsed = parse(log)
    if parsed is not None:
        save(parsed)
