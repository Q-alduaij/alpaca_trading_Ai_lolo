import httpx
from typing import Dict, Any
from src.config import SETTINGS

# Unified wrapper so strategies can call `call_llm(prompt, role="...")`
async def call_llm(prompt: str, agent_role: str) -> Dict[str, Any]:
    if SETTINGS.llm_mode == "ollama":
        # Native Ollama chat API
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{SETTINGS.ollama_base_url}/api/chat",
                json={
                    "model": SETTINGS.ollama_model,
                    "messages": [
                        {"role": "system", "content": f"You are {agent_role}."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                }
            )
            resp.raise_for_status()
            data = resp.json()
            return {"text": data.get("message", {}).get("content", "")}

    # OpenAI-compatible (LM Studio etc.) — just swap base_url
    headers = {"Authorization": f"Bearer {SETTINGS.llm_api_key}"}
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{SETTINGS.llm_base_url}/chat/completions",
            headers=headers,
            json={
                "model": "local-model",
                "messages": [
                    {"role": "system", "content": f"You are {agent_role}."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            }
        )
        resp.raise_for_status()
        data = resp.json()
        return {"text": data["choices"][0]["message"]["content"]}
