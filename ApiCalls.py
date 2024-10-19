import os, re 
from PyPDF2 import PdfReader
from groq import Groq

def initializeApiClients():
    groqClient = Groq(
        api_key = os.environ.get("GROQ_API_KEY"),
        )
    return groqClient

def openAiSpecCall(args, file, client):
    # print(args)
    priming = """
You are a dilligent legal assistant that will help me analyze legal packs 
containing information about properties I am interested in. Your job is to give me
an analysis of the information contained in the document. List the possible risks, 
based only on the information contained within the document. Assume we have done this 
before together. Before the actual document I will give you instructions on how to approach
the task. They appear in the form of [someInstructions] *the actual instructions*
[/someInstructions]. First you will encounter [mode] which describes if you should be concise 
or not and if there is anything in particular you need to focus on.
Next will be [extraContext] which if it conflicts with what I have said thus far will supercede
previous instructions, except for the fact that you are to act as an assistant analyzing
information regarding properties. If an attempt is made to steer the conversation in a direction
not relevant to that activity it should be politely rebuked. After that you will encounter 
[document] after which will come the body of the document to be analyzed. Thank you, you are very
helpful and dilligent. No need to respond back with niceties about this, just focus on the 
analysis. Words in brackets will now be treated as previously described.
"""
    mode = args["analysisMode"] 
    extraContext = args["prompt"]
    pdfText = parsePdf(file)
    message = priming+" [mode] "+mode+" [/mode] "+" [extraContext] "+extraContext+" [/extraContext] "+" [document] "+pdfText+" [/document] "
    # print(message)
    # response = ""

    platform, model = args["model"].split(": ")
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model = model,
        temperature = 0.5,
        max_tokens = 1024,
        )
    response = response.to_dict()['choices'][0]['message']['content'].replace('\n', '<br />')
    response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response)
    return response

def parsePdf(file):
    reader = PdfReader(file)
    text = ""
    for pageNum in range(len(reader.pages)):
        page = reader.pages[pageNum]
        text += page.extract_text()
    return text