from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WebScrapingRequestSerializer, WebScrapingResponseSerializer
from .services import WebScrapingService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class WebScrapingView(APIView):
    """
    API endpoint for scraping websites and answering questions using LLM.
    """
    
    @swagger_auto_schema(
        request_body=WebScrapingRequestSerializer,
        responses={
            200: WebScrapingResponseSerializer,
            400: "Bad Request",
            500: "Internal Server Error"
        },
        operation_description="Scrape the provided website URL and answer the question using an LLM."
    )
    def post(self, request, format=None):
        """
        Scrape a website and answer a question using LLM.
        """
        serializer = WebScrapingRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                url = serializer.validated_data['url']
                question = serializer.validated_data['question']
                
                result = WebScrapingService.scrape_and_answer(url, question)
                
                response_serializer = WebScrapingResponseSerializer(data=result)
                if response_serializer.is_valid():
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            except Exception as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)