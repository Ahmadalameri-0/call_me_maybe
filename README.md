*This activity has been created as part of
the 42 curriculum by abani-am*

---
## 📝 Description

**Call Me Maybe** introduces **function calling** in LLMs through **constrained decoding**. The program takes natural-language prompts and, using a small local LLM (Qwen3-0.6B), selects the right function and extracts its arguments from dynamically provided function definitions.

Constrained decoding guarantees that the output is always **valid JSON that matches the schema**. Choosing the correct function and values still depends on the model.

## 📖 Instructions

**Requirements:** Python 3.10+, [uv](https://docs.astral.sh/uv/).

```bash
make install   # create the uv environment and install dependencies
make run       # run with the default paths
make debug     # run under pdb
make lint      # flake8 + mypy
make clean     # remove caches and build artifacts
```

`make setup` is an alias of `make install` that also links the cache to `goinfre`.

Custom paths:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

## 🧠 Algorithm Explanation

The LLM never writes free text. The schema fixes the output skeleton, and the LLM only fills the variable parts:

1. **Forced segments:** constant text such as `{"name": "` is encoded and appended to the input ids directly, with no LLM call.
2. **Function name:** at each step the SDK returns the logits. Every token that would not keep the text a prefix of a valid function name gets `-inf` (masking), then the best remaining token is chosen (greedy argmax). If only one option remains, it is completed directly.
3. **Parameters:** they are generated in the schema's order, so no key can be missing, duplicated or invented. Each value is constrained by its type:
   - `number` / `integer`: only digit, sign and dot tokens that keep a valid number. The terminator (`,` or `}`) is allowed only when the number is complete.
   - `string`: any token without `"` or newline. The closing quote ends it, and a token limit prevents endless output.
   - `boolean`: a choice between `true` and `false`.
4. **Output:** the result is validated with Pydantic and written with `json.dumps`, so escaping is always correct.

The vocabulary file is loaded once and each token is converted to readable text (byte-level BPE mapping), so the allowed-token sets are built without decoding 150k tokens at every step.

## 🛠️ Design Decisions

- **Pydantic** for all models and input validation.
- **Forced segments** reduce LLM calls, which improves speed and correctness.
- **Greedy decoding** gives deterministic, reproducible results.
- **Generic by design:** no function names or prompts are hardcoded. The system prompt and the constraints are built from the definitions file.
- **Public SDK API only** (logits, encode, vocabulary path).
- A failure in one prompt is reported and does not stop the others. Missing or malformed files produce a clear error message.

## 📊 Performance Analysis

| Metric | Result |
|---|---|
| Function selection accuracy | [..]% |
| Argument extraction accuracy | [..]% |
| Valid JSON / schema compliance | 100% |
|


**Reliability:** the structure is guaranteed by the decoder and does not depend on model quality. The correctness of the chosen function and values does.

##  Challenges Faced

- **Byte-level BPE vocabulary:** mapping tokens back to readable text. Solved with the reversed GPT-2 `bytes_to_unicode` table.
- **Tokenization boundaries:** encoding text in separate pieces can differ slightly from encoding it whole. [Describe your finding.]
- **Strings that never close:** solved with a token limit.
- **Speed:** solved with forced segments and single-option shortcuts.

##  Testing Strategy

- Pytest with a fake LLM (random logits) to prove the output is always valid, whatever the model does.
- Edge cases: missing, empty and malformed files; empty function list; functions without parameters; overlapping names (`add` / `add_numbers`); negative and decimal numbers; empty strings; quotes, backslashes and Unicode.
- Static checks: `flake8` and `mypy`.

##  Example Usage

```bash
make run
```

Prompt: `[your real prompt]`

```json
{
  "prompt": "[your real prompt]",
  "name": "[function]",
  "parameters": { "[arg]": "[value]" }
}
```

## 📚 Resources
- Project specification (42 subject).
- [Qwen3-0.6B model card](https://huggingface.co/Qwen/Qwen3-0.6B)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [uv documentation](https://docs.astral.sh/uv/)

- [Introduction to Large Language Models (Arabic) - Microsoft Learn](https://learn.microsoft.com/ar-sa/training/modules/introduction-large-language-models/) — Completed this beginner-friendly introduction to LLMs.

- [Neural Networks Explained - Youtube](https://www.youtube.com/watch?v=agqr4yM3Aw0&list=PLDF6ATOtPK9d1mNcJHPI0mPZUU46cvZxi) — An introduction to Neural Networks, including CNNs, RNNs, LSTMs, and Generative Adversarial Networks (GANs).

- [Machine Learning & LLMs Full Course - AI Plus / Eng. Mohamed Elshamy](https://www.youtube.com/watch?v=ybRDXSbSW2s&list=PLZ42ZUInDWC7lCjsGUSd8RItbCZ6KESG9) — Complete this comprehensive course covering theoretical foundations of Deep Learning, PyTorch, Transformers architecture, and LLM fine-tuning.

- [Tokenization ](https://youtube.com/playlist?list=PLdO1rjk2BayU&si=UzXgFVl3oRlY1P5P) — An explanation of Byte Pair Encoding (BPE) Tokenization and how LLMs split text into tokens.

## AI Usage

