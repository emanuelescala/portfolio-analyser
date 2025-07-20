from argparse import ArgumentParser
import json

from ocr import OcrChain
from test import Classificationator

"""source $(poetry env info --path)/bin/activate"""
def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        default="mistralai/mistral-small-3.1-24b-instruct:free",
        help="The model to use for the chat.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default="",
        help="OpenRouter API key (or set OPENROUTER_API_KEY environment variable).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="The temperature to use for the chat.",
    )
    parser.add_argument(
        "--input-image",
        type=str,
        required=True,
        help="The image to perform OCR on.",
    )
    args = parser.parse_args()
    
    try:
        ocr_chain = OcrChain(
            model=args.model,
            api_key=args.api_key,
            temperature=args.temperature,
        )
        result = ocr_chain.invoke(args.input_image)

        print("OCR result:", result)
        
        # Converti il risultato JSON in un oggetto Python
        if isinstance(result, str):
            json_data = json.loads(result)
        else:
            json_data = result
        
        result2 = Classificationator(json_data)
        
        print("Classification result:", result2)
        
    except json.JSONDecodeError as e:
        print(f"Errore nel parsing JSON: {e}")
    except Exception as e:
        print(f"Errore generale: {e}")

if __name__ == "__main__":
    main()
