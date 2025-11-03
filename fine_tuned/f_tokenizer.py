from transformers import AutoTokenizer


class FinetuneTokenizer:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        if self.tokenizer.pad_token is None:
            self.tokenizer.add_special_tokens({"pad_token": "<|PAD|>"})
            self.tokenizer.pad_token_id = self.tokenizer.convert_tokens_to_ids(
                "<|PAD|>"
            )

        self.tokenizer.padding_left = "left"

    def get_tokenizer(self):
        return self.tokenizer
