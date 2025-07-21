#!/usr/bin/env python3
"""
Simple Asset Classifier - Script minimale senza interfaccia
Utilizzo: python main.py input.json
"""

import json
import sys
from asset_classifier_final import AssetClassifier


def extract_assets(json_result):
    """Estrae asset e valuations/percentuali dal risultato JSON"""
    try:
        # Se è una stringa, parsala come JSON
        if isinstance(json_result, str):
            data = json.loads(json_result)
        else:
            data = json_result
        
        # Estrai asset e valuations
        assets = []
        valuations = []
        
        for asset in data["assets"]:
            for asset_name, valuation in asset.items():
                assets.append(asset_name)
                
                # Controlla se la valuation è una percentuale
                if isinstance(valuation, str) and valuation and '%' in valuation:
                    # Estrai il numero dalla percentuale (gestisce sia virgola che punto)
                    try:
                        # Rimuovi % e spazi, sostituisci virgola con punto
                        clean_percentage = valuation.replace('%', '').strip().replace(',', '.')
                        percentage_value = float(clean_percentage) / 100
                        valuations.append(percentage_value)
                        print(f"DEBUG: {asset_name} -> {valuation} -> {percentage_value}")  # Debug
                    except ValueError:
                        valuations.append(None)
                        print(f"DEBUG: Errore conversione {asset_name}: {valuation}")
                else:
                    valuations.append(valuation)
        
        return assets, valuations
    except Exception as e:
        print(f"Errore in extract_assets: {e}")
        return [], []


def Classificationator(json_data):
    """Funzione principale che accetta dati JSON come parametro"""
    try:
        # Estrai gli asset usando la funzione dedicata
        assets, valuations = extract_assets(json_data)
        
        if not assets:
            print("Nessun asset trovato nei dati")
            return []
        
        # Inizializza il classificatore
        classifier = AssetClassifier()
        
        # Classifica ogni asset
        results = []
        for i, asset in enumerate(assets):
            result = classifier.classify_asset(str(asset))
            result.weight = valuations[i] if i < len(valuations) else None
            results.append(result)
        results = weight_calculator(results)
        # Prepara i risultati
        output_data = [{
            'original_value': r.original_value,
            'asset_type': r.asset_type.value,
            'isin': r.isin,
            'ticker': r.ticker,
            'weight': r.weight,
            'error_message': r.error_message
        } for r in results]
        
        return output_data
        
    except Exception as e:
        print(f"Errore: {e}")
        return []

def weight_calculator(results):
    """Calcola il peso di ogni asset in base al tipo"""
    # Controlla se ci sono già percentuali definite (da OCR)
    has_percentages = any(r.weight is not None and 0 <= r.weight <= 1 for r in results)
    
    if has_percentages:
        # Se ci sono percentuali dall'OCR, usale direttamente
        for result in results:
            if result.weight is None:
                result.weight = 0.0  # Assegna 0 se manca
            # Arrotonda a 2 decimali
            result.weight = round(result.weight, 3)
        return results
    
    # Altrimenti usa la logica originale
    has_zero_or_none = any(r.weight is None or r.weight == 0 for r in results)
    if has_zero_or_none:
        # Se anche solo un peso è zero o None, dividi tutto in parti uguali
        equal_weight = round(1.0 / len(results), 3)
        for result in results:
            result.weight = equal_weight
        return results
    else:
        # Altrimenti normalizza i pesi esistenti
        total_weight = sum(r.weight for r in results)
        if total_weight > 0:
            for result in results:
                result.weight = round(result.weight / total_weight, 2)
    return results

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

