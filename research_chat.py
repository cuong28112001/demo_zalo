# pip install underthesea

from underthesea import word_tokenize, pos_tag, ner

# Câu cần xử lý

tokens_text = word_tokenize(sentence, format="text")
tokens_list = word_tokenize(sentence)
print("text:", tokens_text)
print("list:", tokens_list)

pos_tags = pos_tag(sentence)
print("tag:", pos_tags)

ner_tags = ner(sentence)
print("Kết quả:", ner_tags)