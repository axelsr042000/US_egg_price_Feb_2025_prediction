from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
import torch.nn.functional as F


MODEL = "cardiffnlp/twitter-roberta-base-sentiment" # cardiffnlp folder not in GitHub version.
ROBERTA_SUPPORTED_LANGUAGES = ["ar", "en", "fr", "de", "hi", "it", "es", "pt"]

model = AutoModelForSequenceClassification.from_pretrained(MODEL)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
config.id2label = {0: "negative", 1: "neutral", 2: "positive"}

#/ save the model locally
model.save_pretrained(MODEL)
tokenizer.save_pretrained(MODEL)



# Preprocess the text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = "@user" if t.startswith("@") and len(t) > 1 else t
        t = "http" if t.startswith("http") else t
        new_text.append(t)
    return " ".join(new_text)



# def predict_sentiment(text: str) -> str:
#     processed_text = preprocess(text)
#     encoded_input = tokenizer(processed_text, return_tensors="pt")
#     output = model(**encoded_input)
#     index_of_sentiment = output.logits.argmax().item()
#     sentiment = config.id2label[index_of_sentiment]
#     return sentiment



def predict_sentiment(text: str) -> (str, float):
    processed_text = preprocess(text)
    encoded_input = tokenizer(processed_text, return_tensors="pt")
    output = model(**encoded_input)
    logits = output.logits
    probabilities = F.softmax(logits, dim=1).squeeze().tolist()
    index_of_sentiment = logits.argmax().item()
    sentiment = config.id2label[index_of_sentiment]
    
    # Get the probability of the predicted sentiment
    sentiment_probability = probabilities[index_of_sentiment]
    
    return sentiment, sentiment_probability



#text = "el presidente es un corrupto https://youtube.com"
# print(predict_sentiment(text_2))