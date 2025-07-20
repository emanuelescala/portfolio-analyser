"""
Asset Classifier - Modulo ottimizzato per la classificazione di asset finanziari
Supporta ISIN, Ticker e Nomi/Nomi abbreviati
"""

import json
import re
import logging
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AssetType(Enum):
    """Enumerazione per i tipi di asset"""
    ISIN = "ISIN"
    TICKER = "TICKER"
    NAME = "NAME"
    UNKNOWN = "UNKNOWN"


@dataclass
class ClassificationResult:
    """Risultato della classificazione di un asset"""
    original_value: str
    asset_type: AssetType
    isin: Optional[str] = None
    ticker: Optional[str] = None
    error_message: Optional[str] = None


class AssetClassifier:
    """Classe principale per la classificazione degli asset"""
    
    # Codici paese ISIN più comuni
    COUNTRY_CODES = {
        'US', 'GB', 'DE', 'FR', 'JP', 'CA', 'AU', 'CH', 'NL', 'IT', 
        'ES', 'SE', 'NO', 'DK', 'FI', 'BE', 'AT', 'IE', 'LU', 'HK',
        'SG', 'KR', 'IN', 'BR', 'MX', 'CN', 'RU', 'ZA', 'IL', 'TW'
    }
    
    # Pattern ticker comuni
    TICKER_PATTERNS = [
        r'^[A-Z]{1,6}$',           # Ticker US standard
        r'^[A-Z0-9]{1,6}\.[A-Z]{1,3}$',  # Con exchange (.L, .PA, .MI, etc.)
    ]
    
    def __init__(self):
        pass
    
    def is_isin(self, text: str) -> bool:
        """Verifica se è un ISIN valido"""
        if not isinstance(text, str):
            return False
        
        cleaned = text.strip().upper()
        
        # Formato rigoroso: esattamente 12 caratteri, no spazi
        if len(cleaned) != 12 or ' ' in cleaned:
            return False
        
        # Pattern: 2 lettere + 9 alfanumerici + 1 cifra
        if not re.match(r'^[A-Z]{2}[A-Z0-9]{9}[0-9]$', cleaned):
            return False
        
        # Codice paese valido
        return cleaned[:2] in self.COUNTRY_CODES
    
    def is_ticker(self, text: str) -> bool:
        """Verifica se è un ticker valido"""
        if not isinstance(text, str) or not text.strip():
            return False
        
        text_upper = text.strip().upper()
        
        # Verifica pattern ticker
        for pattern in self.TICKER_PATTERNS:
            if re.match(pattern, text_upper):
                return True
        
        return False
    
    def is_name(self, text: str) -> bool:
        """Verifica se è un nome di azienda"""
        if not isinstance(text, str) or not text.strip():
            return False
        
        cleaned = text.strip()
        
        # Non è un ISIN
        if self.is_isin(cleaned):
            return False
        
        # Contiene spazi o indicatori aziendali
        if (' ' in cleaned or 
            any(indicator in cleaned for indicator in ['.', '&', '-', 'Inc', 'Corp', 'Ltd', 'SpA', 'AG', 'SA'])):
            return True
        
    
    def get_isin_from_ticker(self, ticker: str) -> Optional[str]:
        """
        Ottiene ISIN da ticker (versione semplificata)
        Per ora restituisce None - da implementare con API esterne se necessario
        """
        logger.debug(f"Ricerca ISIN per ticker {ticker} - Non implementato")
        return None
    
    def get_isin_from_name(self, name: str) -> Optional[str]:
        """
        Ottiene ISIN da nome (placeholder)
        """
        logger.debug(f"Ricerca ISIN per nome '{name}' - Da implementare")
        return None
    
    def classify_asset(self, asset_value: str) -> ClassificationResult:
        """Classifica un singolo asset (ottimizzato)"""
        try:
            if not isinstance(asset_value, str) or not asset_value.strip():
                return ClassificationResult(
                    original_value=asset_value,
                    asset_type=AssetType.UNKNOWN,
                    error_message="Valore vuoto o non valido"
                )
            
            cleaned = asset_value.strip()
            
            # Classificazione veloce in ordine di priorità
            if self.is_isin(cleaned):
                return ClassificationResult(
                    original_value=asset_value,
                    asset_type=AssetType.ISIN,
                    isin=cleaned.upper()
                )
            
            if self.is_ticker(cleaned):
                isin = self.get_isin_from_ticker(cleaned)
                return ClassificationResult(
                    original_value=asset_value,
                    asset_type=AssetType.TICKER,
                    ticker=cleaned.upper(),
                    isin=isin
                )
            
            if self.is_name(cleaned):
                isin = self.get_isin_from_name(cleaned)
                return ClassificationResult(
                    original_value=asset_value,
                    asset_type=AssetType.NAME,
                    isin=isin
                )
            
            return ClassificationResult(
                original_value=asset_value,
                asset_type=AssetType.UNKNOWN,
                error_message="Tipo di asset non riconosciuto"
            )
            
        except Exception as e:
            logger.error(f"Errore nella classificazione di {asset_value}: {e}")
            return ClassificationResult(
                original_value=asset_value,
                asset_type=AssetType.UNKNOWN,
                error_message=f"Errore interno: {str(e)}"
            )
    
    def process_json_file(self, file_path: str) -> List[ClassificationResult]:
        """Processa un file JSON (ottimizzato)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Estrazione asset semplificata
            if isinstance(data, list):
                assets = data
            elif isinstance(data, dict):
                # Cerca chiavi comuni
                for key in ['assets', 'symbols', 'tickers', 'securities']:
                    if key in data:
                        assets = data[key] if isinstance(data[key], list) else [data[key]]
                        break
                else:
                    assets = list(data.values())
            else:
                assets = [str(data)]
            
            # Processa rapidamente ogni asset
            results = []
            for asset in assets:
                if isinstance(asset, str):
                    results.append(self.classify_asset(asset))
                elif isinstance(asset, dict):
                    # Cerca campo principale
                    for key in ['symbol', 'ticker', 'isin', 'name', 'code']:
                        if key in asset:
                            results.append(self.classify_asset(str(asset[key])))
                            break
                else:
                    results.append(self.classify_asset(str(asset)))
            
            logger.info(f"Processati {len(results)} asset da {file_path}")
            return results
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Errore nel file {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Errore generico: {e}")
            raise
    
    def save_results(self, results: List[ClassificationResult], output_path: str) -> None:
        """Salva risultati in JSON (ottimizzato)"""
        try:
            output_data = [{
                'original_value': r.original_value,
                'asset_type': r.asset_type.value,
                'isin': r.isin,
                'ticker': r.ticker,
                'error_message': r.error_message
            } for r in results]
            
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(output_data, file, indent=2, ensure_ascii=False)
            
            logger.info(f"Risultati salvati in: {output_path}")
            
        except Exception as e:
            logger.error(f"Errore nel salvataggio: {e}")
            raise
