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
            # Print results in a more readable format
            print(f"\nReviewing: {results['file_path']}")

            print("\nStyle Check:")
            print(f"- Pylint Score: {results['style_check']['pylint_score']:.2f}/10")
            print(f"- Black Formatted: {results['style_check']['black_formatted']}")

            print("\nHigh Complexity Functions:")
            if not results["complexity"]:
                print("- No functions with complexity > 11 found")
            else:
                for item in results["complexity"]:
                    print(f"\nFunction: {item['function']}")
                    print(f"Line: {item['line']}")
                    print(f"Complexity Score: {item['complexity']}")
                    print("Suggested Improvements:")
                    for suggestion in item["suggestions"]:
                        print(f"- {suggestion}")

            print("\nDocumentation Issues:")
            if not results["documentation"]:
                print("- No documentation issues found")
            else:
                for item in results["documentation"]:
                    print(f"- Line {item['line']}: {item['message']}")

            print("\nSecurity Issues:")
            if not results["security_check"]:
                print("- No security issues found")
            else:
                for item in results["security_check"]:
                    print(f"- Line {item['line']}: {item['message']}")

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
