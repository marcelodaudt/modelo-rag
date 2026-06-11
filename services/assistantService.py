from services.authenticationService import authentication_openai
import json

clientOpenAI = authentication_openai()

def assistant_question(question: str, context_block: str):
    
    try:
        # 1. PROMPT Final: monta o Prompt (estruturado) para enviar à LLM gerar a resposta
        prompt_messages = [
            {
                "role": "system",
                "content": """You are an IT support specialist.

STRICT RULES:
- You MUST answer ONLY using the provided contexts
- If the contexts are empty, incomplete, or irrelevant, you MUST respond:
  "I don't have enough information to answer this question based on the provided context."
- DO NOT use prior knowledge
- DO NOT guess
- DO NOT infer beyond the context

Be precise and technical when answering.
Answering aways in Portuguese-BR.
"""
            },
            {
                "role": "user",
                "content": f"""
Question:
{question}

Contexts:
{context_block if context_block else "NO_CONTEXT_AVAILABLE"}

Answer:
"""
            }
        ]

        # Debug
        print("\n--- CONTEXT_BLOCK ---")
        print(context_block)
        print("----------------------\n")

        print("\n--- PROMPT ENVIADO ---")
        print(prompt_messages)
        print("----------------------\n")

        if not context_block.strip():
            return {
                "answer": "Não encontrei informações suficientes na Base de Conhecimento para responder."
            }

        response = clientOpenAI.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt_messages,
            temperature=0.1
        )

        return response.choices[0].message.content
    
    except Exception as e:
        return {"message": str(e)}
