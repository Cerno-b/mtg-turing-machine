
def encode_2tag_to_utm(alphabet, transitions, input_str):

    letter_encodings = {}

    previous_transition_length = 0
    previous_encoding = 0
    for letter in alphabet:
        letter_encodings[letter] = previous_encoding + previous_transition_length + 1
        if letter != alphabet[-1]:
            transition = transitions[letter]
            previous_encoding = letter_encodings[letter]
            previous_transition_length = len(transition)

    initial_tape = "tt"

    for i, letter in enumerate(reversed(alphabet)):
        if letter != alphabet[-1]:
            transition = transitions[letter]
            transition = reversed(transition)
            transition_list = ["1"*letter_encodings[t] for t in transition]
            transition_encoding = "bb" + "1b".join(transition_list)
            print("transition {i}: encoding: {enc}".format(i=i, enc=transition_encoding))

            initial_tape += transition_encoding

    initial_tape += "bb^"

    input_encoding = ""
    for i, letter in enumerate(input_str):
        string = "1"*letter_encodings[letter]
        print("data {i}: encoding: {enc}".format(i=i, enc=string))
        input_encoding += string + "c"

    initial_tape += input_encoding

    print()
    print("letter encodings:")
    print()
    for letter in alphabet:
        print(letter, "1"*letter_encodings[letter])
    print()
    print("initial tape:", initial_tape)
    print("input:", input_str, "->", input_encoding)

    return initial_tape


def main():
    alphabet = ["X", "#"]
    transitions = {
        "X": "X"}

    input_str = "XXXXXXXXXX#"

    encode_2tag_to_utm(alphabet, transitions, input_str)


if __name__ == '__main__':
    main()

