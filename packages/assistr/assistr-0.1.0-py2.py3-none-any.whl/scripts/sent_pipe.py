
from transformers import pipeline
model = "nlptown/bert-base-multilingual-uncased-sentiment"

# default model
#sentiment_pipeline = pipeline("sentiment-analysis")

model_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

data = ["I love you", "I hate you", "I am you", "You are me"]
output = model_pipeline(data)
print(output)