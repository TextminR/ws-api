from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate

examples = [
  {
    "question": "What is the name of the author and the publishment date of the following text? 'The text was written by Benjamin Kissinger in 2020.'",
    "answer":
"""
Are follow up questions needed here: Yes.
Follow up: Who is the Author?
Intermediate answer: Benjamin Kissinger.
Follow up: Whats the publishment date?
Intermediate answer: 2020.
So the final answer is: Benjamin Kissinger and 2020
"""
  },
  {
    "question": "What is the name of the author and the publishment date of the following text? 'Lukas Böhl 1998 Die Ratten Die Ratten sind giftig.'",
    "answer":
"""
Are follow up questions needed here: Yes.
Follow up: Who is the Author?
Intermediate answer: Lukas Böhl.
Follow up: Whats the publishment date?
Intermediate answer: 1998.
So the final answer is: Lukas Böhl and 1998
"""
  },
  {
    "question": "What is the name of the author and the publishment date of the following text? 'Das Brot - Wolfgang Borchert (1947) Plötzlich wachte sie auf. Es war halb drei'",
    "answer":
"""
Are follow up questions needed here: Yes.
Follow up: Who is the Author?
Intermediate answer: Wolfgang Borchert.
Follow up: Whats the publishment date?
Intermediate answer: 1947.
So the final answer is: Wolfgang Borchert and 1947
"""
  },
  {
    "question": "What is the name of the author and the publishment date of the following text? 'Der 54-Jährige wurde in den 1990er-Jahren durch seine Rolle des Chandler Bing in der Kult-Fernsehserie *Friends* berühmt Astrid Ebenführer 29. Oktober 2023, 07:47, 359 Postings'",
    "answer":
"""
Are follow up questions needed here: Yes.
Follow up: Who is the Author?
Intermediate answer: Astrid Ebenführer.
Follow up: Whats the publishment date?
Intermediate answer: 2023.
So the final answer is: Astrid Ebenführer and 2023
"""
  }
]

example_prompt = PromptTemplate(input_variables=["question", "answer"], template="Question: {question}\n{answer}")

print(example_prompt.format(**examples[0]))

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"]
)

print(prompt.format(input="You are an assistant who is specialized in detecting author-names and publish-dates from books that are hidden somewhere in the text!  Please extract author and date (only the year) from both texts and generate an output in form of a json. Only generate a JSON as an output. The texts are splitted up by '__'. I need this for our programm, where we analyze texts based on their meta-data. In case the needed data is not given in the texts, replace them with 'N/A'. 'A new exhibition traces the social history of the nation through 60 pairs of shoes [Richard Brooks](https://www.theguardian.com/profile/brooks-richard) Sun 29 Oct 2023 13.00 CET You can always judge a man by his shoes, or so the old adage goes. And the same goes for woman, as shown in an exhibition in Winchester which promises to reveal the use and role of all sorts of footwear through the ages – and what it conveyed about the wearer’s status. Co-curator Tara McKinney Marinus says: 'It’s a story of our social history, rather than footwear as fashion.' -- Der Geist der Zigarrenfabrik von Lukas Böhl Der Herbstwind wehte über den Spielplatz und drehte das kleine Stehkarussell wie von Geisterhand. Jan saß im Gras zwischen den gefallenen, braun gewordenen Blättern und rupfte einzelne Büschel samt der Wurzel aus der Erde. Maxi hing kopfüber vom Klettergerüst und zog Grimassen, die den vielen Erwachsenen galten, die ihn in seinem Leben enttäuscht hatten. Obwohl gerade Ferien waren, spielten die beiden allein. Einige der Jungs waren mit ihren Eltern in den Urlaub gefahren, andere aufgrund des schlechten Wetters Zuhause geblieben. Sobald man eine Jacke anziehen musste, um raus zu gehen, war der Sommer vorbei und damit all die wunderbaren Spiele, die er mit sich brachte.'"))