alphabet = ["X", "#"]
transitions = {
    "X": "X"}

input_str = "XXXXXXXXXX#"


def main():
    output = input_str
    while not output.startswith("#"):
        first = output[0]
        output = output[2:] + transitions[first]

    print(output)


if __name__ == '__main__':
    main()
