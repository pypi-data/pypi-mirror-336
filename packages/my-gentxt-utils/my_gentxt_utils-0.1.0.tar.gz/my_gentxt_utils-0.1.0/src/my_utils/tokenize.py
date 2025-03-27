import tiktoken

class Tokenizer:
    def __init__(self, model_name):
        self.encoding = tiktoken.encoding_for_model(model_name)

    def tokenize(self, text):
        return self.encoding.encode(text)

    def detokenize(self, tokens):
        return self.encoding.decode(tokens)