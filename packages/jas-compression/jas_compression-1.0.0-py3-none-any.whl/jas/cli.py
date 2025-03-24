import argparse
import logging
from .compressor import write_jas_file
from .decompressor import read_jas_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["compress", "decompress"])
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO, force=True)

    if args.mode == "compress":
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
        write_jas_file(text, args.output)
    elif args.mode == "decompress":
        text = read_jas_file(args.input)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)

if __name__ == "__main__":
    main()