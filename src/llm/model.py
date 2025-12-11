from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


def load_model():
    """
    Carrega o tokenizer e o modelo LLM localmente.
    O modelo é carregado apenas uma vez.
    """
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",  
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )

    model.eval()
    return tokenizer, model