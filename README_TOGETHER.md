# Utilizzo con Together.ai

Il progetto è stato aggiornato per utilizzare Together.ai invece di un modello locale Ollama.

## Setup

1. Ottieni una API key da [Together.ai](https://api.together.xyz/)
2. Installa le dipendenze: `poetry install`

## Utilizzo

```bash
python main.py --api-key YOUR_TOGETHER_API_KEY --input-image path/to/your/image.png
```

### Parametri disponibili:

- `--model`: Il modello da utilizzare (default: "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo")
- `--api-key`: La tua API key di Together.ai (richiesta)
- `--temperature`: La temperatura per la generazione (default: 0.0)
- `--input-image`: L'immagine su cui eseguire l'OCR (richiesta)

## Modelli supportati su Together.ai

Alcuni modelli vision disponibili:
- `meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo`
- `meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo`
- `meta-llama/Llama-Vision-Free`

## Esempio completo

```bash
python main.py \
  --model "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo" \
  --api-key "your-api-key-here" \
  --temperature 0.0 \
  --input-image "portfolio_screenshot.png"
```

## Variabili d'ambiente

Puoi anche impostare la API key come variabile d'ambiente:

```bash
export TOGETHER_API_KEY=your-api-key-here
```

E poi modificare il codice per utilizzarla automaticamente se non specificata nei parametri.
