from my_utils import Tokenizer
from gen_text import GenerateText
def main():
    tokenizer = Tokenizer("gpt-4")
    gentxt = GenerateText(tokenizer=tokenizer)
    prompt = "The quick brown fox jumps over the lazy dog"
    generated_text = gentxt.generate_text(prompt)
    print(generated_text)

