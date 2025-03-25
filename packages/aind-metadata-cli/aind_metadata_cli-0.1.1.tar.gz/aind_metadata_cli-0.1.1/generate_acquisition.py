"""Example file for generating acquisition files."""

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate acquisition files.")
    parser.add_argument("--subject-id", required=True, help="The subject ID for the acquisition.")
    args = parser.parse_args()

    print(f"\n(Generate acquisition): {args.subject_id}")
