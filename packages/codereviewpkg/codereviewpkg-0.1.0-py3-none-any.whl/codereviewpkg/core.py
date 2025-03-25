"""
Core functionality for code review and analysis.
"""

import os
from typing import Dict, List, Optional, Union
import pylint.lint
import black
import bandit.core.manager
import bandit.core.config
import radon.complexity as radon_complexity
import pydocstyle


class CodeReviewer:
    """Main class for code review functionality."""

    def __init__(self):
        """Initialize the CodeReviewer."""
        self.black_mode = black.FileMode()

    def review_file(self, file_path: str) -> Dict:
        """
        Review a single Python file.

        Args:
            file_path: Path to the Python file to review

        Returns:
            Dict containing review results
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        results = {
            "file_path": file_path,
            "style_check": self._check_style(file_path),
            "security_check": self._check_security(file_path),
            "complexity": self._check_complexity(file_path),
            "documentation": self._check_documentation(file_path),
        }

        return results

    def review_directory(self, directory_path: str) -> List[Dict]:
        """
        Review all Python files in a directory.

        Args:
            directory_path: Path to the directory to review

        Returns:
            List of review results for each Python file
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        results = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    results.append(self.review_file(file_path))

        return results

    def _check_style(self, file_path: str) -> Dict:
        """Check code style using pylint and black."""
        # Run pylint
        pylint_output = pylint.lint.Run([file_path], exit=False)
        pylint_score = pylint_output.linter.stats.global_note

        # Check black formatting
        try:
            with open(file_path, "r") as f:
                content = f.read()
            black.format_str(content, mode=self.black_mode)
            black_formatted = True
        except Exception:
            black_formatted = False

        return {
            "pylint_score": pylint_score,
            "black_formatted": black_formatted,
        }

    def _check_security(self, file_path: str) -> List[Dict]:
        """Check for security vulnerabilities using bandit."""
        b_mgr = bandit.core.manager.BanditManager(
            bandit.core.config.BanditConfig(), [file_path]
        )
        b_mgr.run_tests()
        return [
            {"line": issue.lineno, "message": issue.text}
            for issue in b_mgr.get_issue_list()
        ]

    def _check_complexity(self, file_path: str) -> List[Dict]:
        """Check code complexity using radon."""
        with open(file_path, "r") as f:
            content = f.read()
        results = radon_complexity.cc_visit(content)
        return [
            {"line": item.lineno, "complexity": item.complexity} for item in results
        ]

    def _check_documentation(self, file_path: str) -> List[Dict]:
        """Check documentation using pydocstyle."""
        results = pydocstyle.check([file_path])
        return [{"line": error.line, "message": error.message} for error in results]
