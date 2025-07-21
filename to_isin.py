#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: primo_investing.py
Descrizione: data una stringa 'nome', cerca su Google 'nome investing.com'
             e stampa il primo risultato.
Dipendenze: pip install googlesearch-python
"""

import sys
from googlesearch import search
import re
from urllib.parse import urlparse



def primo_risultato_investing(query: str) -> tuple[str, str,str] | None:
    """
    Esegue una ricerca Google per 'query investing.com' e ritorna
    una tupla (URL, ISIN) del primo risultato. Se non ne trova, restituisce None.
    """
    full_query = f' "isin" {query} inurl:investing.com'
    try:
        # Usa la funzione search avanzata per ottenere anche le descrizioni
        from googlesearch import search
        results = search(full_query, advanced=True)
        
        for result in results:
            url = result.url
            categoria = estrai_categoria_da_url(url)
            description = result.description
            
            # Cerca il pattern ISIN nella descrizione
            if description:
                isin_match = re.search(r'ISIN:\s*([A-Z]{2}[A-Z0-9]{10})', description)
                if isin_match:
                    isin_code = isin_match.group(1)
                    return url, isin_code, categoria
                
                # Pattern alternativo per ISIN
                isin_match_alt = re.search(r'([A-Z]{2}[A-Z0-9]{10})', description)
                if isin_match_alt:
                    isin_code = isin_match_alt.group(1)
                    return isin_code, categoria
            
            # Se non trova ISIN nella descrizione, ritorna comunque l'URL
            return None
            
    except Exception as e:
        print(f"[Errore] durante la ricerca: {e}", file=sys.stderr)
    return None

def estrai_categoria_da_url(url: str) -> str | None:
    """
    Estrae la categoria dall'URL di investing.com.
    Ad esempio: da 'https://www.investing.com/etfs/vanguard-ftse...' estrae 'etfs'
    """
    try:
        parsed_url = urlparse(url)
        # Divide il path per '/' e prende il primo elemento non vuoto
        path_parts = [part for part in parsed_url.path.split('/') if part]
        if path_parts:
            if path_parts[0] == 'etfs':
                return 'etf'
            elif path_parts[0] == 'equities':
                return 'equity'
            elif path_parts[0] == 'rates-bonds':
                return 'bond'
            elif path_parts[0] == 'commodities':
                return 'commodity'
            else :
                return path_parts[0]
    except Exception as e:
        print(f"[Errore] nell'estrazione della categoria: {e}", file=sys.stderr)
    return None

def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} \"nome da cercare\"", file=sys.stderr)
        sys.exit(1)

    nome = sys.argv[1].strip()
    risultato = primo_risultato_investing(nome)
    if risultato:
        isin, categoria = risultato
        print(f"Categoria: {categoria}")
        if isin:
            print(f"ISIN: {isin}")
        else:
            print("ISIN: Non trovato nella descrizione")
    else:
        print("Nessun risultato trovato.", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()

