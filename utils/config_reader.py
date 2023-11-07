import os


def clean_line(line: str):
    return line.strip().strip("\n").strip()


def read_bool(value: str):
    if value == "true":
        return str(True)
    if value == "false":
        return str(False)

    return None


def read_int(value: str):
    try:
        return int(value)
    except Exception:
        return None


def parse_value(value: str):
    bool_value = read_bool(value)
    int_value = read_int(value)

    if bool_value is not None:
        return bool_value

    # if int_value is not None:
    #     return int_value

    return value


def read_config(config_file: str):
    config = {}
    try:
        with open(f"{config_file}.txt", "r") as f:
            for line in f.readlines():
                line = clean_line(line)
                split_line = line.split("=")
                variable = clean_line(split_line[0])
                value = clean_line(split_line[1])

                print(f"Setting: {variable} = {parse_value(value)}")
                config[variable] = parse_value(value)

    except Exception:
        pass
        # return config

    return config


def load_config(config_file: str):
    print("LOADING CONFIG")
    config_dict = read_config(config_file)

    for key in config_dict.keys():
        os.environ[key] = config_dict.get(key)
