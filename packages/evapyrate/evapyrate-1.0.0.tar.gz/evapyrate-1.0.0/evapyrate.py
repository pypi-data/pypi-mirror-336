"""Evapyrate - Encode text into zero width characters."""

_map = {"0": "\u200B", "1": "\u200C"}
_r_map = {"\u200B": "0", "\u200C": "1"}
_delim = "\u200D"

def evaporate(text: str) -> str:
    """Evaporate text into an evapyrated string."""
    segments = []
    for char in text:
        current = ""
        for bit in format(ord(char), "b"):
            current += _map[bit]
        segments.append(current)
    return _delim.join(segments)


def condense(text: str) -> str:
    """Condense evapyrated text back into its original form."""
    ret = ""
    if any(x not in ("\u200B", "\u200C", "\u200D") for x in text):
        raise ValueError("Invalid text to condense.")
    for segment in text.split(_delim):
        current = ""
        for char in segment:
            current += _r_map[char]
        ret += chr(int(current, 2))
    return ret

def main():
    import argparse
    import sys
    try:
        import pyperclip
    except ImportError: # support py3.5
        pyperclip = None

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    evaporate_parser = subparsers.add_parser("eva", help=evaporate.__doc__)
    evaporate_parser.add_argument("text", type=str, help="Text to evaporate", nargs="+")
    evaporate_parser.add_argument("-c", "--copy", action="store_true", help="Copy output to clipboard")

    condense_parser = subparsers.add_parser("con", help=condense.__doc__)
    condense_parser.add_argument("text", type=str, help="Text to condense")

    args = parser.parse_args()
    arg = " ".join(args.text) if args.command == "eva" else args.text

    if args.command == "con":
        try:
            result = condense(arg)
            print("Condensed:", result)
        except ValueError as e:
            print("Error:", e)
            sys.exit(2)
    elif args.command == "eva":
        result = evaporate(arg)
        print("Evaporated: [{result}]".format(result=result))
        if args.copy:
            if pyperclip:
                pyperclip.copy(result)
                print("Copied to clipboard!")
            else:
                print("Tried to copy to clipboard, but pyperclip library is not installed.")
    else:
        return parser.print_help()

    sys.exit(0)



if __name__ == "__main__":
    main()
