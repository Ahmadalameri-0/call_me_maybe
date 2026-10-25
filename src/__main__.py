import argparse
from llm_sdk import Small_LLM_Model
from src.parser import load_prompts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--functions_definition',
        type=str, default="data/input/functions_definition.json"
    )
    parser.add_argument(
        "--input", type=str,
        default="data/input/function_calling_tests.json"
    )
    parser.add_argument(
        "--output", type=str,
        default="data/output/function_calling_results.json"
    )
    args = parser.parse_args()

    print(f"📂 Loading prompts from: {args.input}")
    prompts = load_prompts(args.input)

    if prompts:
        print(f"Loaded {len(prompts)} prompts. First: '{prompts[0].prompt}'")

    print("\n🧠 Loading LLM Model (Qwen)...")
    llm = Small_LLM_Model()
    print("✅ Model loaded successfully from goinfre!")
    print(f"📖 Vocab path: {llm.get_path_to_vocab_file()}")


if __name__ == "__main__":
    main()
