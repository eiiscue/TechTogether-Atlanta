from transformers import pipeline
class Summarize:
    def __init__(self,original_text = ""):
        self.text = original_text
    def summarize(self):
        summarization = pipeline("summarization")
        summary_text = "Summary:" + summarization(self.text)[0]['summary_text']
        return summary_text