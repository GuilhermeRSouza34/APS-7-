# Sistema de Cálculo Emergético (SCALE)

Este é um sistema para cálculo de emergia baseado em Inventários do Ciclo de Vida (LCI), desenvolvido como projeto acadêmico para a disciplina de Engenharia de Software.

## Funcionalidades

- Importação e manipulação de dados LCI (CSV/Excel)
- Cálculos emergéticos baseados em álgebra emergética
- Interface gráfica amigável
- Geração de relatórios em PDF/CSV
- Visualização de fluxos de emergia

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Estrutura do Projeto

```
scale/
├── data/               # Dados de exemplo e arquivos LCI
├── src/               # Código fonte
│   ├── core/         # Lógica de negócio
│   ├── gui/          # Interface gráfica
│   ├── utils/        # Utilitários
│   └── tests/        # Testes unitários
├── docs/             # Documentação
└── reports/          # Relatórios gerados
```

## Uso

Execute o programa principal:
```bash
python src/main.py
```

## Desenvolvimento

- Padrão de projeto: MVC
- Testes: pytest
- Controle de versão: Git

## Licença

Este projeto é parte de um trabalho acadêmico e está sob a licença MIT. 