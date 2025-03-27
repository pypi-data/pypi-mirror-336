from my_utils import Tokenizer, TextDataset, load_data
def main():
    tknzr = Tokenizer("gpt-4")
    data = ["hello world, from transformer", "The quick brown fox jumps over the lazy dog"]
    dataset = TextDataset(data, seq_len=4)
    
    for _ in range(len(dataset)):
        print(dataset[_])

    '''
    print('stride 2')
    dataset = TextDataset(data, seq_len=4, stride=2)

    for _ in range(len(dataset)):
        print(dataset[_])   
    
    data = load_data("/Users/venkatkedar/personal/work/gutenberg/data/.mirror/1/0/0/0/10000/10000-0.txt")
    dataset = TextDataset(data, tokenizer=tknzr, seq_len=4)
    print(len(dataset))
    for _ in range(200):
        print(dataset[_])
    ''' 

