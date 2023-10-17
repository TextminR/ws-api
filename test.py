from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)
example = "Jannik Sinner stammt aus Lichtenwörth und begann im Alter von sechs Jahren mit dem Tennisspielen."

ner_results = nlp(example)
print(ner_results)