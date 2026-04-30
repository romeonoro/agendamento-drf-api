Write-Host "--- 1. Organizando Imports (isort) ---" -ForegroundColor Cyan
isort .

Write-Host "--- 2. Formatando Código (black) ---" -ForegroundColor Cyan
black .

Write-Host "--- 3. Verificando Estilo (flake8) ---" -ForegroundColor Cyan
flake8 application core infra rest_api tests

Write-Host "--- 4. Validando Contratos e Tipos (mypy) ---" -ForegroundColor Cyan
mypy application core infra rest_api tests

Write-Host "--- 5. Avaliando Qualidade e Nota (pylint) ---" -ForegroundColor Cyan
pylint application core infra rest_api

Write-Host "--- 6. Executando Testes e Cobertura (pytest) ---" -ForegroundColor Cyan
python -m pytest --cov
