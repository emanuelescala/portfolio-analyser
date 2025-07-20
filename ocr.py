from typing import Optional, Any
import io
import base64
import json
import re
import os
from dotenv import load_dotenv

from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.utils import Input, Output
from langchain_openai import ChatOpenAI
from PIL import Image

from prompt import create_ocr_prompt

# Load environment variables
load_dotenv()


class OcrChain(Runnable[Input, Output]):
    def __init__(self, model: str, api_key: str, temperature: float):
        # Use provided API key or fall back to environment variable
        openrouter_api_key = api_key if api_key else os.getenv("OPENROUTER_API_KEY")
        
        if not openrouter_api_key:
            raise ValueError("OpenRouter API key is required. Provide it as parameter or set OPENROUTER_API_KEY environment variable.")
        
        self._llm = ChatOpenAI(
            model=model,
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
        )
        self._ocr_prompt = create_ocr_prompt()

    def invoke(self, image_filename: str, config: Optional[RunnableConfig] = None, **kwargs: Any) -> str:
        image_data = self._read_image(image_filename)
        input_data = {"image_data": image_data}
        response = self._create_chain().invoke(input_data, config, **kwargs).content
        return self._extract_json(response)

    def _extract_json(self, response: str) -> str:
        """Extract JSON from response, handling cases where model includes extra text"""
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                # Validate that it's valid JSON
                json.loads(json_match.group())
                return json_match.group()
            except json.JSONDecodeError:
                pass
        
        # If no valid JSON found, return the original response
        return response

    def _create_chain(self) -> Runnable:
        return self._ocr_prompt|self._llm

    def _read_image(self, image_filename: str) -> str:
        file = Image.open(image_filename)
        buf = io.BytesIO()
        file.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
