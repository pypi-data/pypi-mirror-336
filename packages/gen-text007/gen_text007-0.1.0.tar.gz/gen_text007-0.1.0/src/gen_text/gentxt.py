
class GenerateText():
    def __init__(self, model=None, tokenizer=None, max_length=50):
        self.model = model
        self.tokenizer = tokenizer
        self.max_length = max_length

    def generate_text(self, prompt):
        input_ids = self.tokenizer.tokenize(prompt)
        if(self.model is not None):
            input_ids = input_ids.to(self.model.device)

        if(self.model is None):
            output = self.tokenizer.tokenize(prompt +" -- sample text generated as model is not available")
            return self.tokenizer.detokenize(output)

        for _ in range(max_length):
            logits = model(input_ids)
            logits = logits[0, -1, :]
            predicted_id = torch.argmax(logits).unsqueeze(0)
            input_ids = torch.cat([input_ids, predicted_id], dim=-1)

        return self.tokenizer.detokenize(input_ids)