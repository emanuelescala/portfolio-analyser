#!/usr/bin/env python3
"""
Simple Asset Classifier - Script minimale senza interfaccia
Utilizzo: python main.py input.json
"""

import json
import sys
from asset_classifier_final import AssetClassifier


def extract_assets(json_result):
    """Estrae solo gli ISIN dal risultato JSON"""
    try:
        # Se è una stringa, parsala come JSON
        if isinstance(json_result, str):
            data = json.loads(json_result)
        else:
            data = json_result
        
        # Estrai le chiavi (ISIN) da ogni asset
        assets = []
        for asset in data["assets"]:
            assets.extend(asset.keys())
        
        return assets
    except:
        return []


def Classificationator(json_data):
    """Funzione principale che accetta dati JSON come parametro"""
    try:
        # Estrai gli asset usando la funzione dedicata
        assets = extract_assets(json_data)
        
        if not assets:
            print("Nessun asset trovato nei dati")
            return []
        
        # Inizializza il classificatore
        classifier = AssetClassifier()
        
        # Classifica ogni asset
        results = []
        for asset in assets:
            result = classifier.classify_asset(str(asset))
            results.append(result)
        
        # Prepara i risultati
        output_data = [{
            'original_value': r.original_value,
            'asset_type': r.asset_type.value,
            'isin': r.isin,
            'ticker': r.ticker,
            'error_message': r.error_message
        } for r in results]
        
        return output_data
        
    except Exception as e:
        print(f"Errore: {e}")
        return []


def main_cli():
    """Funzione per utilizzo da linea di comando"""
    if len(sys.argv) != 2:
        print("Utilizzo: python test.py input.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        # Leggi il file JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Classifica
        results = Classificationator(data)
        
        # Salva i risultati
        output_file = 'results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Classificazione completata. Risultati salvati in {output_file}")
    
    except FileNotFoundError:
        print(f"File non trovato: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Errore: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main_cli()

