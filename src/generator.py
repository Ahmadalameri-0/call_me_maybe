import numpy as np
from llm_sdk import Small_LLM_Model
from src.models import FunctionDefinition

class ConstrainedGenerator:
    def __init__(self, model: Small_LLM_Model):
        self.model = model

        def generate_function_call(
                self, prompt: str, func_def: FunctionDefinition,
                max_tokens: int = 50
            ) -> str:
            input_tokens = self.model.encode(prompt)

            for _ in range(max_tokens):
                logits = self.model.get_logits_from_input_ids(input_tokens)
                filtered_logits = self.apply_json_mask(
                    logits, func_def, input_tokens
                )
                next_token = int(np.argmax(filtered_logits))
                input_tokens.append(next_token)

                if next_token == self.model.eos_token_id:
                    break

            return self.model.decode(input_tokens)

        def apply_json_mask(
                self, logits: np.ndarray, func_def: FunctionDefinition,
                current_tokens: list
            ) -> np.ndarray:
            """
            This method is the heart of the project!
            For now, we'll restore the probabilities as they are,
            In the next step, we'll modify it to assign '-inf'
            to any token that breaks the JSON structure.
            """
            return logits
