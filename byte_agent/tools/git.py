"""Git integration tools."""

import subprocess
import os
from typing import Optional


def run_git(args: str) -> str:
    try:
        result = subprocess.run(
            f"git {args}",
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return result.stdout.strip() or result.stderr.strip() or "OK"
    except Exception as e:
        return f"Git error: {e}"


def git_status() -> str:
    return run_git("status")


def git_commit(message: str) -> str:
    return run_git(f'commit -m "{message}"')


def git_diff() -> str:
    return run_git("diff")


def git_log(limit: int = 10) -> str:
    return run_git(f"log --oneline -{limit}")


def git_add(files: str = ".") -> str:
    return run_git(f"add {files}")


def git_branch(branch_name: str) -> str:
    return run_git(f"checkout -b {branch_name}")
