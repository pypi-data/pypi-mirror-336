import asyncio
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

from ai_migrate.llm_providers import DefaultClient


async def get_pr_details(pr_number: str) -> Dict:
    """Get details about a PR using the GitHub CLI.

    Args:
        pr_number: The PR number to get details for

    Returns:
        A dictionary with PR details
    """
    result = await asyncio.create_subprocess_exec(
        "gh",
        "pr",
        "view",
        pr_number,
        "--json",
        "title,body,files,commits,additions,deletions,changedFiles",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await result.communicate()

    if result.returncode != 0:
        raise Exception(f"Error getting PR details: {stderr.decode()}")

    return json.loads(stdout.decode())


async def get_file_diff(pr_number: str, file_path: str) -> str:
    """Get the diff for a specific file in a PR.

    Args:
        pr_number: The PR number
        file_path: The path to the file

    Returns:
        The diff content as a string
    """
    result = await asyncio.create_subprocess_exec(
        "gh",
        "pr",
        "diff",
        pr_number,
        "--name-only",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await result.communicate()

    if result.returncode != 0:
        raise Exception(f"Error getting PR file list: {stderr.decode()}")

    files = stdout.decode().strip().split("\n")

    if file_path not in files:
        raise ValueError(f"File {file_path} not found in PR {pr_number}")

    result = await asyncio.create_subprocess_exec(
        "gh",
        "pr",
        "diff",
        pr_number,
        file_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await result.communicate()

    if result.returncode != 0:
        raise Exception(f"Error getting file diff: {stderr.decode()}")

    return stdout.decode()


async def get_file_content(pr_number: str, file_path: str, base: bool = False) -> str:
    """Get the content of a file from a PR.

    Args:
        pr_number: The PR number
        file_path: The path to the file
        base: If True, get the base (before) version, otherwise get the head (after) version

    Returns:
        The file content as a string
    """
    # Try multiple approaches to get file content

    # Approach 1: Use gh pr diff to get the file content
    try:
        # This gets the diff which includes both before and after content
        result = await asyncio.create_subprocess_exec(
            "gh",
            "pr",
            "diff",
            pr_number,
            "--patch",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await result.communicate()

        if result.returncode == 0:
            diff_content = stdout.decode()

            # Extract file content from the diff
            file_diffs = diff_content.split("diff --git ")
            for file_diff in file_diffs:
                if f"a/{file_path}" in file_diff or f"b/{file_path}" in file_diff:
                    # Found the right file
                    lines = file_diff.splitlines()
                    content_lines = []
                    in_content = False

                    for line in lines:
                        if line.startswith("+++") and base:
                            in_content = True
                            continue
                        elif line.startswith("---") and not base:
                            in_content = True
                            continue

                        if in_content:
                            if line.startswith("+") and not base:
                                content_lines.append(line[1:])
                            elif line.startswith("-") and base:
                                content_lines.append(line[1:])
                            elif not line.startswith("+") and not line.startswith("-"):
                                content_lines.append(line)

                    if content_lines:
                        return "\n".join(content_lines)
    except Exception as e:
        print(f"Approach 1 failed: {e}")

    # Approach 2: Use GitHub API to get file content
    try:
        # First, get the PR branch information
        result = await asyncio.create_subprocess_exec(
            "gh",
            "pr",
            "view",
            pr_number,
            "--json",
            "baseRefName,headRefName",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await result.communicate()

        if result.returncode == 0:
            branch_data = json.loads(stdout.decode())
            ref = branch_data["baseRefName"] if base else branch_data["headRefName"]

            # Then fetch the file content
            result = await asyncio.create_subprocess_exec(
                "gh",
                "api",
                f"repos/:owner/:repo/contents/{file_path}?ref={ref}",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                content_data = json.loads(stdout.decode())
                import base64

                return base64.b64decode(content_data["content"]).decode("utf-8")
    except Exception as e:
        print(f"Approach 2 failed: {e}")

    # Approach 3: Use a simpler fallback approach
    try:
        # Create a simplified version based on the PR description
        if base:
            return f"// Original content of {file_path}\n// This is a placeholder for demonstration purposes"
        else:
            return f"// Modified content of {file_path}\n// This is a placeholder for demonstration purposes"
    except Exception as e:
        print(f"Approach 3 failed: {e}")

    # If all approaches fail, return a minimal placeholder
    return f"// Content of {file_path} (not available)"


async def generate_system_prompt(pr_details: Dict, description: str) -> str:
    """Generate a system prompt based on PR details and a description.

    Args:
        pr_details: The PR details
        description: A short description of the migration task

    Returns:
        The generated system prompt
    """
    client = DefaultClient()

    system_prompt = """You are an expert at creating system prompts for code migration tasks.
Given information about a pull request that demonstrates a code migration pattern, 
create a clear, concise system prompt that will guide an AI to perform similar migrations on other files."""

    user_prompt = f"""
I need to create a system prompt for a code migration task. Here are the details:

Description: {description}

Pull Request Title: {pr_details["title"]}
Pull Request Description: {pr_details["body"]}

Files Changed: {len(pr_details["files"])}
Total Additions: {pr_details["additions"]}
Total Deletions: {pr_details["deletions"]}

Create a system prompt that clearly explains:
1. The migration goal
2. Key patterns to look for
3. How to transform the code
4. Any important constraints or considerations

The system prompt should be concise but comprehensive, focusing on the patterns demonstrated in the PR.
"""

    return await client.generate_text(system_prompt, user_prompt)


async def extract_example_patterns(
    pr_number: str, pr_details: Dict
) -> List[Tuple[str, str]]:
    """Extract example patterns from a PR.

    Args:
        pr_number: The PR number
        pr_details: The PR details

    Returns:
        A list of (before, after) example pairs
    """
    client = DefaultClient()

    # Get a sample of changed files (max 5 for analysis)
    files_to_analyze = pr_details.get("files", [])
    if not files_to_analyze and "changedFiles" in pr_details:
        # If 'files' is not available, try to get file list using another method
        result = await asyncio.create_subprocess_exec(
            "gh",
            "pr",
            "view",
            pr_number,
            "--json",
            "files",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await result.communicate()

        if result.returncode == 0:
            files_data = json.loads(stdout.decode())
            files_to_analyze = files_data.get("files", [])

    # If still no files, try to get files from diff
    if not files_to_analyze:
        try:
            result = await asyncio.create_subprocess_exec(
                "gh",
                "pr",
                "diff",
                pr_number,
                "--name-only",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                file_paths = stdout.decode().strip().split("\n")
                files_to_analyze = [{"path": path} for path in file_paths]
        except Exception as e:
            print(f"Error getting files from diff: {e}")

    # Limit to 5 files for analysis
    files_to_analyze = files_to_analyze[:5]

    examples = []
    for file_info in files_to_analyze:
        # Skip if we can't determine the file path
        if not isinstance(file_info, dict) or "path" not in file_info:
            continue

        file_path = file_info["path"]

        # Skip if file was added or deleted
        if "status" in file_info and (
            file_info["status"] == "added" or file_info["status"] == "deleted"
        ):
            continue

        try:
            before_content = await get_file_content(pr_number, file_path, base=True)
            after_content = await get_file_content(pr_number, file_path, base=False)

            # Skip if we couldn't get meaningful content
            if "not available" in before_content and "not available" in after_content:
                print(f"Skipping {file_path} - content not available")
                continue

            system_prompt = """You are an expert at identifying code migration patterns.
Given a before and after version of a file, extract the minimal, representative example that 
clearly demonstrates the migration pattern. Focus on the core transformation pattern, not incidental changes."""

            user_prompt = f"""
Analyze these before and after versions of a file and extract a minimal example that demonstrates the key migration pattern:

BEFORE:
```
{before_content}
```

AFTER:
```
{after_content}
```

Extract just the essential parts that show the migration pattern. The example should be as small as possible while still 
demonstrating the pattern clearly. Remove any code that doesn't directly demonstrate the migration pattern.

Respond with two code blocks labeled BEFORE and AFTER containing your minimal examples.
"""

            response = await client.generate_text(system_prompt, user_prompt)

            # Extract the before and after examples from the response
            before_match = re.search(r"BEFORE:\s*```.*?\n(.*?)```", response, re.DOTALL)
            after_match = re.search(r"AFTER:\s*```.*?\n(.*?)```", response, re.DOTALL)

            if before_match and after_match:
                before_example = before_match.group(1).strip()
                after_example = after_match.group(1).strip()
                examples.append((before_example, after_example))
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    # If we couldn't extract any examples, create a simple one based on the PR title and description
    if not examples and pr_details.get("title") and pr_details.get("body"):
        try:
            system_prompt = """You are an expert at creating code examples for migration patterns.
Given a PR title and description, create a minimal example that demonstrates the migration pattern described."""

            user_prompt = f"""
Create a minimal example that demonstrates the migration pattern described in this PR:

Title: {pr_details["title"]}
Description: {pr_details["body"]}

Create two code blocks labeled BEFORE and AFTER that show the migration pattern.
The examples should be minimal but clearly demonstrate the key changes involved in this migration.
"""

            response = await client.generate_text(system_prompt, user_prompt)

            # Extract the before and after examples from the response
            before_match = re.search(r"BEFORE:\s*```.*?\n(.*?)```", response, re.DOTALL)
            after_match = re.search(r"AFTER:\s*```.*?\n(.*?)```", response, re.DOTALL)

            if before_match and after_match:
                before_example = before_match.group(1).strip()
                after_example = after_match.group(1).strip()
                examples.append((before_example, after_example))
        except Exception as e:
            print(f"Error creating example from PR description: {e}")

    return examples


async def save_examples(
    examples: List[Tuple[str, str]], examples_dir: Path, file_extension: str = "java"
):
    """Save example pairs to files.

    Args:
        examples: List of (before, after) example pairs
        examples_dir: Directory to save examples to
        file_extension: File extension to use for examples
    """
    examples_dir.mkdir(parents=True, exist_ok=True)

    for i, (before, after) in enumerate(examples):
        base_name = f"Example{i + 1}"
        before_file = examples_dir / f"{base_name}.old.{file_extension}"
        after_file = examples_dir / f"{base_name}.new.{file_extension}"

        before_file.write_text(before)
        after_file.write_text(after)

    print(f"Saved {len(examples)} example pairs to {examples_dir}")


async def generate_verify_script(
    pr_details: Dict, project_dir: Path, file_extension: str
) -> str:
    """Generate a verification script based on PR details.

    Args:
        pr_details: The PR details
        project_dir: The project directory
        file_extension: The file extension of the migrated files

    Returns:
        The generated verification script
    """
    client = DefaultClient()

    system_prompt = """You are an expert at creating verification scripts for code migration tasks.
Given information about a pull request that demonstrates a code migration pattern, create a Python script
that can verify if a file has been properly migrated according to the pattern."""

    user_prompt = f"""
I need to create a verification script for a code migration task. Here are the details:

Pull Request Title: {pr_details["title"]}
Pull Request Description: {pr_details["body"]}

Files Changed: {len(pr_details["files"])}
File Extension: {file_extension}

Create a Python script that:
1. Takes a file path as input
2. Verifies if the file has been properly migrated according to the pattern
3. Returns a non-zero exit code if verification fails

The script should be saved as verify.py in the project directory and should be runnable as:
python verify.py <file_path>

For pre-verification (to gather information before migration), it should support:
python verify.py --pre <file_path>

Focus on creating a practical verification script that checks for the key aspects of the migration.
"""

    verify_script = await client.generate_text(system_prompt, user_prompt)

    # Extract just the Python code if it's wrapped in a code block
    code_match = re.search(r"```python\n(.*?)```", verify_script, re.DOTALL)
    if code_match:
        verify_script = code_match.group(1)

    return verify_script


async def setup_project_from_pr(
    pr_number: str, project_path: str, description: str, file_extension: str = "java"
) -> None:
    """Set up a migration project based on a PR.

    Args:
        pr_number: The PR number
        project_path: Path where the project should be created
        description: Short description of the migration task
        file_extension: File extension for the migrated files
    """
    project_dir = Path(project_path).expanduser()

    # Create project directory structure
    project_dir.mkdir(parents=True, exist_ok=True)
    examples_dir = project_dir / "examples"
    examples_dir.mkdir(exist_ok=True)
    evals_dir = project_dir / "evals"
    evals_dir.mkdir(exist_ok=True)

    print(f"Created project directory structure at {project_dir}")

    try:
        # Get PR details
        print(f"Fetching PR #{pr_number} details...")
        pr_details = await get_pr_details(pr_number)

        # Generate system prompt
        print("Generating system prompt...")
        system_prompt = await generate_system_prompt(pr_details, description)
        system_prompt_file = project_dir / "system_prompt.md"
        system_prompt_file.write_text(system_prompt)
        print(f"Saved system prompt to {system_prompt_file}")

        # Extract and save example patterns
        print("Extracting example patterns...")
        examples = await extract_example_patterns(pr_number, pr_details)
        if not examples:
            print(
                "Warning: No example patterns were extracted. Creating a simple example..."
            )
            # Create a simple example if none were extracted
            examples = [
                (
                    "// Old version\npublic class Example {\n    // TODO: Add your code here\n}",
                    "// New version\npublic class Example {\n    // TODO: Migrated code here\n}",
                )
            ]
        await save_examples(examples, examples_dir, file_extension)

        # Generate verification script
        print("Generating verification script...")
        verify_script = await generate_verify_script(
            pr_details, project_dir, file_extension
        )
        verify_script_file = project_dir / "verify.py"
        verify_script_file.write_text(verify_script)
        print(f"Saved verification script to {verify_script_file}")

        print(f"Project setup complete at {project_dir}")
    except Exception as e:
        print(f"Error during project setup: {e}")
        # Create minimal files if something went wrong
        from .migrate import SYSTEM_MESSAGE
        from .manifest import SYSTEM_PROMPT_FILE, VERIFY_SCRIPT_FILE

        # Create minimal system prompt
        system_prompt_file = project_dir / SYSTEM_PROMPT_FILE
        if not system_prompt_file.exists():
            system_prompt = f"{SYSTEM_MESSAGE}\n\n# Migration Task\n\n{description}"
            system_prompt_file.write_text(system_prompt)
            print(f"Created minimal system prompt at {system_prompt_file}")

        # Create minimal verify script
        verify_script_file = project_dir / VERIFY_SCRIPT_FILE
        if not verify_script_file.exists():
            verify_script = (
                "import sys\n\n"
                "def main():\n"
                "    # TODO: Implement verification\n"
                '    print(f"Verifying {sys.argv[1]}...")\n'
                "    return 0\n\n"
                'if __name__ == "__main__":\n'
                "    sys.exit(main())\n"
            )
            verify_script_file.write_text(verify_script)
            print(f"Created minimal verification script at {verify_script_file}")

        print(
            "Project setup completed with errors. Some files may need manual editing."
        )
