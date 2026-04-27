Write-Host "--- 1. Organizando Imports (isort) ---" -ForegroundColor Cyan
isort .

Write-Host "--- 2. Formatando Código (black) ---" -ForegroundColor Cyan
black .

Write-Host "--- 3. Verificando Estilo (flake8) ---" -ForegroundColor Cyan
flake8 .

Write-Host "--- 4. Validando Contratos e Tipos (mypy) ---" -ForegroundColor Cyan
mypy api infra tests main.py --explicit-package-bases

Write-Host "--- 5. Avaliando Qualidade e Nota (pylint) ---" -ForegroundColor Cyan
pylint api infra main.py

Write-Host "--- 6. Executando Testes e Cobertura (pytest) ---" -ForegroundColor Cyan
python -m pytest --cov
