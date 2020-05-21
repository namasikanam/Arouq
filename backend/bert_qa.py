import torch
from transformers import BertTokenizer, BertForQuestionAnswering

tokenizer = BertTokenizer.from_pretrained('../dataset/bert-base-squad2')
model = BertForQuestionAnswering.from_pretrained('../dataset/bert-base-squad2')

print("Bert init end!")

def bert_QA(question, answer_text):
    input_ids = tokenizer.encode(question, answer_text)
    sep_index = input_ids.index(tokenizer.sep_token_id)
    num_seg_a = sep_index + 1
    num_seg_b = len(input_ids) - num_seg_a
    segment_ids = [0] * num_seg_a + [1] * num_seg_b
    start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids = torch.tensor([segment_ids]))
    print(start_scores, end_scores)
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    if answer_start >= answer_end or answer_start <= num_seg_a:
        return None
    answer = tokens[answer_start]
    for i in range(answer_start + 1, answer_end + 1):
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        else:
            answer += ' ' + tokens[i]
    return answer

if __name__ == '__main__':
    question = "Where is China"
    answer_text = "China (Chinese: 中国; pinyin: Zhōngguó), officially the People's Republic of China is a country in East Asia"
    print(bert_QA(question, answer_text))

    question = "What is China?"
    print(bert_QA(question, answer_text))