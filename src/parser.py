import json
import sys
from typing import List
from src.models import PromptTest, FunctionDefinition


def load_prompts(file_path: str) -> List[PromptTest]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            prompts = [PromptTest(**item) for item in data]
            return prompts
    except FileNotFoundError:
        print(
            f"Error: The input file '{file_path}' "
            "was not found.", file=sys.stderr
        )
    except json.JSONDecodeError:
        print(
            f"Error: The file '{file_path}' contains invalid JSON.",
            file=sys.stderr
        )
    except Exception as e:
        print(
            f"Unexpected error while reading prompts: {e}",
            file=sys.stderr
        )
    return []


def load_functions(file_path: str) -> List[FunctionDefinition]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            return [FunctionDefinition(**item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

    return []
