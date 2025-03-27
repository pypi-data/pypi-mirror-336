from torch.utils.data import Dataset
from my_utils import Tokenizer
import torch

class TextDataset(Dataset):
    def __init__(self, data=[], tokenizer=None, seq_len=50, pad_token_id=-100, stride = 1):
        self.data = data
        self.tokenizer = tokenizer
        token_ids = []
        if(self.tokenizer is None):
            self.tokenizer = Tokenizer("gpt-4")
        self.seq_len = seq_len
        eos_token_id = self.tokenizer.get_encoder().eot_token
        token_ids = [self.tokenizer.tokenize(item) + [eos_token_id] for item in self.data]
        inputs=[]
        targets=[]
        
        ## batch_len is the maximum length of the token_ids but not more than seq_len
        batch_len = max(len(item) for item in token_ids)
        batch_len = min(batch_len, seq_len)

        for i in range(len(token_ids)):
            for j in range(0,len(token_ids[i])-1, stride):
                min_len = min(j+batch_len, len(token_ids[i]))
                min_len_1 = min(j+1+batch_len, len(token_ids[i]))
                inputs.append(token_ids[i][j:min_len])
                targets.append(token_ids[i][j+1:min_len_1])
                if(len(inputs[-1]) < batch_len):
                    inputs[-1].extend([pad_token_id]*(batch_len-len(inputs[-1])))
                if(len(targets[-1]) < batch_len):
                    targets[-1].extend([pad_token_id]*(batch_len-len(targets[-1])))
                  
        self.inputs = inputs
        self.targets = targets
        
    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return self.inputs[idx], self.targets[idx]

