# توثيق مشروع Call Me Maybe ورحلة تعلم LLMs

يحتوي هذا الملف على ملخص مرتب لجميع الخطوات والأكواد والنقاشات التي تمت لبناء مشروع Function Calling باستخدام `uv` ونماذج اللغة الكبيرة (LLMs)، بالإضافة إلى خريطة التعلم الذاتي.

---

## 1. هندسة المشروع وإدارة الموارد (goinfre)
نظراً لقيود مساحة التخزين في مدرسة 42 وحجم النماذج الكبير، تم الاعتماد على مجلد `goinfre` لتخزين بيئة العمل (Virtual Environment) وملفات التخزين المؤقت (Cache) الخاصة بأوزان النموذج.

**القيود الصارمة للمشروع:**
*   ممنوع استخدام `pytorch` أو `transformers` في كود المشروع المخصص (مجلد `src`).
*   المكتبات المسموحة فقط هي `pydantic` و `numpy`.
*   يجب عزل حزمة `llm_sdk` (المقدمة من المدرسة والتي تحتوي على الاعتماديات الممنوعة) كحزمة محلية (Local Dependency).

---

## 2. إعدادات البيئة (Environment Setup)

### ملف `pyproject.toml` (في المسار الجذري)
تم إنشاء هذا الملف ليتوافق مع شروط المشروع ويحتوي فقط على الحزم المسموحة، مع ربط حزمة `llm_sdk` محلياً:

```toml
[project]
name = "call-me-maybe"
version = "0.1.0"
description = "42 Function Calling LLM"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "numpy",
    "pydantic"
]

[dependency-groups]
dev = [
    "flake8",
    "mypy"
]
```

### ملف `Makefile` (لأتمتة الأوامر والمسارات)
لضمان توجه كل التحميلات إلى `goinfre` بشكل آلي، تم بناء هذا الملف:

```makefile
export

UV_PROJECT_ENVIRONMENT=/goinfre/$(USER)/call_me_venv
UV_CACHE_DIR=/goinfre/$(USER)/uv_cache
HF_HOME=/goinfre/$(USER)/hf_cache
UV_LINK_MODE=copy

PYTHON = python3

all: run

setup:
	uv add pydantic numpy ./llm_sdk 
	uv add --dev flake8 mypy
	@echo "Creating symlink for VS Code..."
	@ln -sfn $(UV_PROJECT_ENVIRONMENT) .venv

run:
	uv run $(PYTHON) -m src

install:
	uv sync

debug:
	uv run $(PYTHON) -m pdb -m src

clean:
	rm -rf __pycache__ .mypy_cache .venv
	rm -rf $(UV_PROJECT_ENVIRONMENT)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint-strict:
	uv run flake8 src
	uv run mypy src --strict

.PHONY: all run install debug lint clean setup
```

---

## 3. الأكواد الأساسية (Core Code)

### ملف `src/models.py`
يحتوي على نماذج `Pydantic` للتحقق من صحة البيانات (Data Validation):

```python
from pydantic import BaseModel
from typing import Any, Dict, List

class FunctionProperty(BaseModel):
    type: str
    description: str | None = None

class FunctionParameters(BaseModel):
    type: str
    properties: Dict[str, FunctionProperty]
    required: List[str]

class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters
    returns: Dict[str, str] | None = None

class PromptTest(BaseModel):
    prompt: str

class FunctionCallResult(BaseModel):
    prompt: str
    name: str
    parameters: Dict[str, Any]
```

### ملف `src/__main__.py`
نقطة الدخول الرئيسية لاختبار تحميل النموذج وقراءة الملفات:

```python
import argparse
from llm_sdk import Small_LLM_Model
from src.parser import load_prompts

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--functions_definition", type=str, default="data/input/functions_definition.json")
    parser.add_argument("--input", type=str, default="data/input/function_calling_tests.json")
    parser.add_argument("--output", type=str, default="data/output/function_calling_results.json")
    args = parser.parse_args()
    
    print(f"📂 Loading prompts from: {args.input}")
    prompts = load_prompts(args.input)
    
    if prompts:
        print(f"✅ Loaded {len(prompts)} prompts. First: '{prompts[0].prompt}'")
        
    print("\n🧠 Loading LLM Model (Qwen)...")
    llm = Small_LLM_Model()
    print(f"✅ Model loaded successfully from goinfre!")
    print(f"📖 Vocab path: {llm.get_path_to_vocab_file()}")

if __name__ == "__main__":
    main()
```

---

## 4. خريطة تعلم نماذج اللغة الكبيرة (LLMs Roadmap)

تم ترتيب مسار التعلم ليغطي الأساسيات الرياضية وصولاً إلى التطبيقات المتقدمة:

1. **أساسيات التعلم العميق (Deep Learning Foundations):**
   * Neural Networks (الشبكات العصبية).
   * Forward and Backward Propagation.
   * PyTorch Framework.
2. **معالجة اللغات الطبيعية (Traditional NLP):**
   * أساسيات NLP.
   * Word Embeddings & Word2Vec.
   * Tokenization.
3. **ثورة النماذج اللغوية (Transformers & Attention):**
   * Transformers architecture (الصورة الكبيرة).
   * Self-Attention mechanism (السر الرياضي لربط الكلمات).
   * Encoder vs Decoder models (مثل Qwen الذي يعتبر Decoder-only).
4. **هندسة واستنتاج النماذج (LLM Inference & Engineering):**
   * دورة حياة توليد النص في LLMs.
   * Text Generation and Logits (أساس خوارزمية Constrained Decoding).
   * Temperature and Top-P sampling.
   * Function Calling in LLMs.
5. **التطبيقات المتقدمة (Advanced LLM Ops):**
   * RAG (Retrieval-Augmented Generation).
   * Fine-tuning LLMs.
   * Vector Databases.

**المصادر الموصى بها:**
*   [Machine Learning & LLMs Full Course 2025 (Arabic) - AI Plus / Eng. Mohamed Elshamy](https://www.youtube.com/watch?v=ybRDXSbSW2s&list=PLZ42ZUInDWC7lCjsGUSd8RItbCZ6KESG9)
*   قناة هشام عاصم (Hesham Asem) على يوتيوب للتعمق في الـ NLP.

---

## 5. مفاهيم برمجية وهندسية تم شرحها

### لماذا نستخدم `self.eta = eta` في بايثون الكلاسات؟
لتحويل القيم من **متغيرات محلية مؤقتة (Local Variables)** (تنتهي بانتهاء الدالة `__init__`) إلى **خصائص دائمة (Instance Attributes)** ترتبط بالكائن نفسه، مما يسمح لبقية الدوال (مثل `fit` و `predict`) بالوصول إليها لاحقاً.

### شرح أمر `ln -sfn $(UV_PROJECT_ENVIRONMENT) .venv`
*   `ln`: لإنشاء الروابط (Links).
*   `-s`: (Symbolic) لإنشاء رابط رمزي (اختصار) لا يأخذ مساحة.
*   `-f`: (Force) لاستبدال أي رابط قديم موجود مسبقاً بنفس الاسم.
*   `-n`: (No-dereference) يمنع إنشاء الرابط داخل المجلد الهدف بالخطأ في حال تكرار تنفيذ الأمر، ويحدث الرابط نفسه مباشرة.