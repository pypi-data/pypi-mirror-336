# CodeReviewPkg

A Python package for automated code review and analysis.

## Installation

```bash
pip install codereviewpkg
```

## Usage

```python
from codereviewpkg import CodeReviewer

# Initialize the code reviewer
reviewer = CodeReviewer()

# Review a file
results = reviewer.review_file("path/to/your/file.py")

# Review a directory
results = reviewer.review_directory("path/to/your/project")
```

## Features

- Code style checking
- Complexity analysis
- Security vulnerability scanning
- Best practices validation
- Documentation checking

## Requirements

- Python 3.7+
- See requirements.txt for package dependencies

## License

MIT License 