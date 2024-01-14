from pydantic import json


async def extraction(classifier, texts):
    result = await process_text_list(texts, classifier)
    return result


async def process_ner_output(ner_output):
    # Process NER output and extract author and date with the highest score
    author = None
    date = None

    for entity in ner_output:
        if entity['entity_group'] == 'AUTHOR' and (author is None or entity['score'] > author['score']):
            author = {'author': entity['word'], 'score': entity['score']}

        if entity['entity_group'] == 'DATE' and (date is None or entity['score'] > date['score']):
            date = {'date': entity['word'], 'score': entity['score']}

    return {'author': author['author'] if author else 'N/A', 'date': date['date'] if date else 'N/A'}


# list: simulates the json that we receive from the frontend. In this case, it is highly recommended to use the examples from the test-dataset.
# The model is still not able to handle all the possible inputs, since the training dataset has not been optimized yet. Test dataset can be found in the folder: test.jsonl.
async def process_text_list(text_list, classifier):
    result_list = []
    ner_output_list = []
    for i in range(len(text_list)):
        ner_output_list.append(classifier(text_list[i]))

    for text, ner_output in zip(text_list, ner_output_list):
        processed_result = await process_ner_output(ner_output)
        result_list.append({'text': text, 'response': processed_result})

    return result_list
