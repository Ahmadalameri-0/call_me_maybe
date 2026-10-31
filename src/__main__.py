import argparse
from llm_sdk import Small_LLM_Model
from src.parser import load_prompts, load_functions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--functions_definition", type=str, default="data/input/functions_definition.json")
    parser.add_argument("--input", type=str, default="data/input/function_calling_tests.json")
    parser.add_argument("--output", type=str, default="data/output/function_calling_results.json")
    args = parser.parse_args()

    print(f"📂 Loading prompts and functions...")
    prompts = load_prompts(args.input)
    functions = load_functions(args.functions_definition)
    
    if prompts and functions:
        print(f"✅ Loaded {len(prompts)} prompts.")
        print(f"✅ Loaded {len(functions)} functions. First function name: '{functions[0].name}'")
        
    print("\n🧠 Loading LLM Model (Qwen)...")
    llm = Small_LLM_Model()
    print(f"✅ Model ready! Vocab path: {llm.get_path_to_vocab_file()}")

if __name__ == "__main__":
    main()
