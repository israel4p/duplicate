# Makefile
.PHONY: install format lint test sec build

install:
	@echo "\e[33m\n* Instalando dependências...\e[m"
	@poetry install

format:
	@echo "\e[33m\n* Formatando código...\e[m"
	@blue .
	@echo "\e[33m\n* Formatando imports...\e[m"
	@isort .

lint:
	@echo "\e[33m\n* Checando formatação...\e[m"
	@blue . --check
	@echo "\e[33m\n* Checando imports...\e[m"
	@isort . --check
	@echo "\e[33m\n* Checando qualidade do código...\e[m"
	@prospector --with-tool pep257 --doc-warning

test:
	@echo "\e[33m\n* Executando testes...\e[m"
	@pytest -v

sec:
	@echo "\e[33m\n* Checando segurança dos modulos...\e[m"
	@pip-audit

build:
	@echo "\e[33m\n* Criando executável...\e[m"
	@pyinstaller --onefile --noconsole --clean src/main.py
	@echo "\e[33m\n* Limpando arquivos de buld...\e[m"
	@rm -rf main.spec build
