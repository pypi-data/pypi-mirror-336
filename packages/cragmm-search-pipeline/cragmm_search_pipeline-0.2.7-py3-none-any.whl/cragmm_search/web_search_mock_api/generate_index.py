#!/usr/bin/env python
"""
Script to generate the web search index from a JSONL file.
"""

import argparse
import os

from api.web_search import index_web_data


def main():
    parser = argparse.ArgumentParser(
        description="Generate web search index from JSONL file"
    )
    parser.add_argument(
        "--input",
        default="corpus",
        help="Path to input corpus folder",
    )
    args = parser.parse_args()

    print(f"Generating index from {args.input} folder...")

    # Create data directory
    os.makedirs("api/web_index", exist_ok=True)

    # Generate index
    collection = index_web_data(args.input, overwrite=True)

    print(f"Index generated successfully with {collection.count()} entries")


if __name__ == "__main__":
    main()
