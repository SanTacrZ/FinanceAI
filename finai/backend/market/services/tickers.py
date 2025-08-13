COLCAP_TICKERS = [
	# Nota: Símbolos de ejemplo de empresas colombianas en Yahoo Finance en formato .CL o .CO
	{'symbol': 'ECO.CN', 'name': 'Ecopetrol S.A. (proxy)'} ,
	{'symbol': 'BCOLOMBIA.CN', 'name': 'Bancolombia S.A. (proxy)'},
	{'symbol': 'ISA.CN', 'name': 'Interconexion Electrica (proxy)'},
	{'symbol': 'GRUPOARG.CN', 'name': 'Grupo Argos (proxy)'},
	{'symbol': 'GRUPOAVAL.CN', 'name': 'Grupo Aval (proxy)'}
]

# En producción, reemplazar por símbolos exactos de Yahoo Finance para Colombia (ej. *.CL / *.CO).

def list_supported_tickers():
	return COLCAP_TICKERS