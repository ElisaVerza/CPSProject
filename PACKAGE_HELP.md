# Creazione del package
1. Aggiunti i file LICENCE (MIT), pyproject.toml, setup.cfg
2. Creata directory src/wb con all'interno \_\_init\_\_.py
3. I file del progetto sono tutti presenti nella cartella del package.
4. `python3 -m build` per impacchettare il package
5. Per fare l'upload:
   - Su TestPyPI (test): `python3 -m twine upload --repository testpypi dist/*`
   - Su PyPI (production): `python3 -m twine upload dist/*`
6. Inserire username: "\_\_token\_\_" e come password il valore del token creato sul sito [Test]PyPI
7. Scaricare il package: 
   - Da TestPyPI: `python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps opandas_wb`
   - Da PyPI: `python3 -m pip install opandas_wb`
# Aggiornamento del package
1. Eliminare la cartella dist
2. Incrementare il campo version in setup.cfg
3. `python3 -m build`
4. Upload:
   - Su TestPyPI:`python3 -m twine upload --repository testpypi dist/*`
   - Su PyPI: `python3 -m twine upload dist/*`
5. Inserire username: "\_\_token\_\_" e il valore del token come password
6. Aggiornare localmente il package:
   - Da TestPyPI: `python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps opandas_wb`
   - Da PyPI: `python3 -m pip install opandas_wb`
# Disinstallazione del package
- Da TestPyPI: python3 -m pip uninstall opandas_wb