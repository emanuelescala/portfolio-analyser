# Portfolio Analyzer 2.0

Un analyzer di immagini di portfolio usando OpenRouter AI per l'analisi OCR e di contenuto.

## Setup

### 1. Clona il repository
```bash
git clone <your-repo-url>
cd open_route
```

### 2. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 3. Configura l'API Key

#### Opzione A: File .env (Raccomandato)
```bash
cp .env.example .env
```
Modifica `.env` e inserisci la tua API key:
```
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

#### Opzione B: Variabile d'ambiente
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-api-key-here"
```

#### Opzione C: Parametro da linea di comando
```bash
python main.py --api-key "sk-or-v1-your-api-key-here" --input-image "image.png"
```

### 4. Ottieni una API Key da OpenRouter

1. Vai su [OpenRouter.ai](https://openrouter.ai)
2. Registrati o fai login
3. Vai nella sezione API Keys
4. Crea una nuova API key
5. Copiala nel file `.env`

## Utilizzo

### Comando Base
```bash
python main.py --input-image "path/to/your/image.png"
```

### Con Parametri Personalizzati
```bash
# Modello diverso
python main.py --input-image "image.png" --model "anthropic/claude-3.5-sonnet"

# Temperatura personalizzata
python main.py --input-image "image.png" --temperature 0.3

# Combinazione
python main.py --input-image "image.png" --model "openai/gpt-4o" --temperature 0.1
```

## Modelli Supportati

OpenRouter supporta molti modelli, alcuni gratuiti:

### Gratuiti
- `mistralai/mistral-small-3.1-24b-instruct:free`
- `meta-llama/llama-3.2-11b-vision-instruct:free`
- `google/gemma-2-9b-it:free`

### A Pagamento (migliore qualità)
- `openai/gpt-4o`
- `anthropic/claude-3.5-sonnet`
- `google/gemini-pro-vision`

## Struttura del Progetto

```
.
├── main.py              # Script principale
├── ocr.py              # Logica OCR e AI
├── .env.example        # Template configurazione
├── .env                # Configurazione locale (non committato)
├── .gitignore          # File da ignorare in Git
├── pyproject.toml      # Dipendenze del progetto
└── README.md           # Questa documentazione
```

## Contribuire

1. Fork del repository
2. Crea un branch per la tua feature
3. Commit delle modifiche
4. Push del branch
5. Apri una Pull Request

## Sicurezza

⚠️ **IMPORTANTE**: Non committare mai file `.env` o API keys nel repository!

- Il file `.env` è in `.gitignore`
- Usa sempre `.env.example` per mostrare la struttura
- Se accidentalmente committi un'API key, revocala immediatamente e creane una nuova

## Licenza

MIT License
