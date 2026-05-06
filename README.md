# Modelo RAG

**R.A.G.** (Retrieval Augmented Generation)

Este projeto foi desenvolvido como parte dos requisitos para obtenção do título de **Especialista em Engenharia de Software**, realizado na **Escola Superior de Agricultura "Luiz de Queiroz", Universidade de São Paulo** - Esalq/USP, e procurou estudar e desenvolver uma aplicação em **Python** e **FastAPI** para automatizar a criação e manutenção de uma **Base de Conhecimento** a partir de um sistema de Help Desk (chamados técnicos).

O modelo de Geração Aumentada por Recuperação [RAG], do inglês “*Retrieval-Augmented Generation*”, busca reaproveitar os LLMs para criar aplicações voltadas a domínios específicos sem a necessidade de retreinamento ou ajuste fino ("*fine-tuning*"). A abordagem de RAG faz referência a informações proprietárias e contextualmente relevantes, recuperadas de uma base de conhecimento da própria instituição, para enriquecer as respostas geradas pelo modelo.

## Diretórios

[api/](modelo-rag/api/)

* Definição dos *endpoints* da aplicação.

[services/](modelo-rag/services/)

* Definição dos serviços da aplicação. Contém código para:
  * serviço de Assistente Inteligente com geração de "*prompt*";
  * serviço para autenticação no **Pinecone** e na **OpenAI**;
  * serviço para geração de *embeddings*;
  * serviço de criação de índices no **Pinecone**;
  * serviço para extrair texto de arquivos TXT/PDF e geração de "*chunk*";
  * serviço para inserir documentos no banco vetorial.

[notebooks/](modelo-rag/notebooks/)

* Contém os *notebooks* Python para:
  * análise dos dados extraidos do banco de dados do sistema de Help Desk em produção;
  * **RAGAS** - *framework* para realização de testes com o Modelo RAG.

## Features:

- **Python** (programming language)
- **Pinecone** (vector database)
- **OpenAI** (embedding and responses)

---

## CRIAR E ATIVAR O AMBIENTE PYTHON
```bash
python -m venv venv
source venv/bin/activate
```

## EXECUTAR O REQUIRIMENTS
```bash
pip install -r requirements.txt
```