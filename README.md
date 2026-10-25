*This activity has been created as part of
the 42 curriculum by abani-am*

---
## 📝 Description
**Call Me Maybe** is a local LLM engineering project focused on implementing **Function Calling** through **Constrained Decoding**.

The goal of this project is to build a robust the system that forces a small, locally-hosted LLM (Qwen) to parse natural language prompts and strictly output correctly formatted and validated JSON arguments that match predefined function schemas, eliminating model hallucinations and ensuring predictable API interactions.

## 🚀 Quick Start
1. **Setup the Environment:**
Initialization the `uv` environment, installs local dependencies, and links the cache to `goinfre`.
``` bash
make setup
```

2. **Run the Model:**
Executes the parser, loads the LLM weights, and processes the input prompts.
``` bash
make run
```


## 📚 Resources
- The official project specification, outlining the requirements and objectives of the project.

- [Introduction to Large Language Models (Arabic) - Microsoft Learn](https://learn.microsoft.com/ar-sa/training/modules/introduction-large-language-models/) — Completed this beginner-friendly introduction to LLMs.

- [Neural Networks Explained - Youtube](https://www.youtube.com/watch?v=agqr4yM3Aw0&list=PLDF6ATOtPK9d1mNcJHPI0mPZUU46cvZxi) — An introduction to Neural Networks, including CNNs, RNNs, LSTMs, and Generative Adversarial Networks (GANs).

- [Machine Learning & LLMs Full Course - AI Plus / Eng. Mohamed Elshamy](https://www.youtube.com/watch?v=ybRDXSbSW2s&list=PLZ42ZUInDWC7lCjsGUSd8RItbCZ6KESG9) — Complete this comprehensive course covering theoretical foundations of Deep Learning, PyTorch, Transformers architecture, and LLM fine-tuning.