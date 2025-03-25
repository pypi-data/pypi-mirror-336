"""
Command-line interface for CodeReviewPkg.
"""

import argparse
import json
from .core import CodeReviewer


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Code review tool for Python files")
    parser.add_argument("path", help="Path to file or directory to review")
    parser.add_argument("--output", "-o", help="Output file for results (JSON format)")

    args = parser.parse_args()

    reviewer = CodeReviewer()

    try:
        if args.path.endswith(".py"):
            results = reviewer.review_file(args.path)
        else:
            results = reviewer.review_directory(args.path)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
        else:
            print(json.dumps(results, indent=2))

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
