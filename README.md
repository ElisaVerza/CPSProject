# CPSProject - Operation P.A.N.D.A.S.
##### Libreria Worldbank per il corso Complementi di Probabilità e Statistica
__________
Home del Package su TestPyPI: 

[https://test.pypi.org/project/opandasWorldBank/](https://test.pypi.org/project/opandasWorldBank/)
___________
## Manuale d'installazione
1. Installare i package `requests`, `matplotlib` e `pandas`

    
    python3 -m pip install requests matplotlib pandas --upgrade
2. Installare il package del progetto da testPyPI:
    

    python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps opandas_wb
Importare i package da utilizzare. L'utente dovrebbe usare solamente 
i metodi all'interno del package `api`:

    from opandas_wb.api import fetch, plots # metodi per ottenere dati da WB e graficarli

Per degli esempi di utilizzo vedere i [tests](tests/api_test.py) e la relazione [case_study.ipynb](Relazione_CaseStudy.ipynb). 
Per il manuale d'uso delle funzioni, aprire su un browser [docs/src/opandas/index.html](docs/src/opandas/index.html)