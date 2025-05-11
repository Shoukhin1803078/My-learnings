from rest_framework import serializers

class WebScrapingRequestSerializer(serializers.Serializer):
    url = serializers.URLField(help_text="URL of the website to scrape")
    question = serializers.CharField(help_text="Question to answer about the website content")

class WebScrapingResponseSerializer(serializers.Serializer):
    answer = serializers.CharField(help_text="LLM-generated answer to the question")