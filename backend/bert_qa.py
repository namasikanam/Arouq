import torch
from transformers import BertTokenizer, BertForQuestionAnswering, BasicTokenizer
import wikipediaapi
from nltk.tokenize import sent_tokenize
from utils import remove_stopwords
import math

print("[Bert]")
tokenizer = BertTokenizer.from_pretrained('../dataset/bert-base-squad2')
basicTokenizer = BasicTokenizer()
model = BertForQuestionAnswering.from_pretrained('../dataset/bert-base-squad2')
model = model.cuda()
print("[Bert] Init End!")

print("[Wiki]")
wiki = wikipediaapi.Wikipedia('en')
print("[Wiki] Init End")


def bert(question, answer_text):
    for i in range(len(answer_text)):
        tokens = tokenizer.encode(question, ' '.join(answer_text[:i+1]))
        if len(tokens) < 512:
            input_ids = tokens
        else:
            break
    sep_index = input_ids.index(tokenizer.sep_token_id)
    num_seg_a = sep_index + 1
    num_seg_b = len(input_ids) - num_seg_a
    segment_ids = [0] * num_seg_a + [1] * num_seg_b
    start_scores, end_scores = model(torch.tensor([input_ids]).cuda(), token_type_ids = torch.tensor([segment_ids]).cuda())
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    if answer_start > answer_end or answer_start <= num_seg_a:
        return None, -1

    answer = tokens[answer_start]
    for i in range(answer_start + 1, answer_end + 1):
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        else:
            answer += ' ' + tokens[i]
    return answer, torch.max(start_scores) + torch.max(end_scores)


def get_keywords(question):
    tokens = basicTokenizer.tokenize(question)
    return remove_stopwords(tokens)


def wiki_sentence(word):
    page = wiki.page(word).text
    page = page.replace('.\n', '. ')
    page = page.replace('\n', '. ')
    return sent_tokenize(page)


def bert_QA(question):
    print("[QA] ", question)
    keywords = get_keywords(question)
    print("[Keywords]", keywords)
    max_score = -2
    best_answer = None 
    keyword = None
    for word in keywords:
        print("[QA] word: ", word)
        sents = wiki_sentence(word)
        if len(sents) == 0:
            continue
        idf = {}
        for word in keywords:
            idf[word] = 2
        for sent in sents:
            for word in keywords:
                if sent.find(word) != -1:
                    idf[word] += 1
        for w in idf:
            idf[w] = 1/math.log(idf[w]) + 1
        print("  [IDF] ", idf)
        candidates = [(10000.0, 0)]
        for idx, sent in enumerate(sents):
            score = 0
            is_key = False
            for w in keywords:
                if sent.find(w) != -1:
                    score += idf[word]
                    if w != word:
                        is_key = True
            if score > 0 and idx > 0 and is_key:
                candidates.append((score, idx))
        candidates.sort()
        candidates.reverse()
        candidates = candidates[:min(len(candidates), 10)]
        print("  [Candidates] ", candidates)
        for _, pos in candidates:
            ans, score = bert(question, sents[pos:])
            print("  [Bert] Answer at {}: {} {}".format(pos, ans, score))
            if score > max_score and ans is not None:
                best_answer = ans
                max_score = score
                keyword = ans
    print("[QA] answer = {}, score = {}".format(best_answer, max_score))
    return best_answer, max_score, keyword


if __name__ == '__main__':
    print(bert_QA('What is the climate of China?')) # agriculturally suitable
    print(bert_QA('what is the earliest form of football?'))
