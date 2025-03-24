import os, asyncio; from anthropic import AsyncAnthropic, HUMAN_PROMPT, AI_PROMPT; async def test(): client = AsyncAnthropic(api_key=os.environ.get('ANTHROPIC_API_KEY')); try: completion = await client.completion(prompt=f"{HUMAN_PROMPT} Hello{AI_PROMPT}", model='claude-2', max_tokens_to_sample=10); print('Success:', completion); except Exception as e: print(f'Error: {type(e).__name__}: {e}'); asyncio.run(test())
