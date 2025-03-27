import traceback
from typing import Callable, Any, TypeVar

from openai import AsyncOpenAI, NotGiven, NOT_GIVEN

from toolbox51 import logger




TYPE_JSON = {"type": "json_object"}


T = TypeVar("T")

def fake_resolve_func(resp: str) -> str:
    return resp

async def achat(
    prompt: str,
    *,
    url: str, name: str,
    api_key: str = "your-api-key",
    
    system_prompt: str = "You are a good assistant.",
    history: list[tuple[str, str]]|None = None,
    
    max_retries: int = 3,
    resolve_func: Callable[[str], T] = fake_resolve_func,  # 解析函数，用于验证、格式化生成结果。
    
    temperature: float|NotGiven = NOT_GIVEN,
    top_p: float|NotGiven = NOT_GIVEN,
    response_format: Any|NotGiven = NOT_GIVEN,
    timeout: float|NotGiven = NOT_GIVEN,
    max_tokens: int|NotGiven = NOT_GIVEN,
) -> T|None:
    try:
        async with AsyncOpenAI(api_key=api_key, base_url=url) as async_client:
            for i in range(max_retries + 1):
                if(i > 0):
                    logger.info(f"retry: {i}")
                try:
                    messages = []
                    if system_prompt:
                        messages.append({"role": "system", "content": system_prompt})
                    if history:
                        for h in history:
                            messages.append({"role": "user", "content": h[0]})
                            messages.append({"role": "assistant", "content": h[1]})
                    messages.append({"role": "user", "content": prompt})
                    response = await async_client.chat.completions.create(
                        model = name,
                        messages = messages,
                        temperature = temperature,
                        top_p = top_p,
                        response_format = response_format,
                        timeout = timeout,
                        max_tokens = max_tokens,
                    )
                    resp = response.choices[0].message.content
                    logger.debug(resp)
                    if not resp:
                        logger.warning(f"大模型生成结果为空: {response}")
                        continue
                    if not (resp := resolve_func(resp)):
                        logger.warning(f"大模型生成结果解析失败: {response}")
                        continue
                    return resp
                except Exception:
                    logger.warning(f"大模型生成出错, {url=}, {name=}")
                    traceback.print_exc()
            logger.warning("大模型生成失败，请检查模型是否正常运行")
            return None
    except Exception:
        logger.warning(f"无法连接到大模型, {url=}, {name=}")
        traceback.print_exc()
        return None


class AsyncChat:
    url: str
    name: str
    
    system_prompt: str
    api_key: str
    
    max_retries: int
    resolve_func: Callable
    
    temperature: float|NotGiven
    top_p: float|NotGiven
    response_format: Any|NotGiven
    timeout: float|NotGiven
    max_tokens: int|NotGiven
    
    def __init__(
        self,
        url: str, name: str,
        *,
        api_key: str = "your-api-key",
        system_prompt: str = "You are a good assistant.",
        
        max_retries: int = 3,
        resolve_func: Callable[[str], T] = fake_resolve_func,  # 解析函数，用于验证、格式化生成结果。
        
        temperature: float|NotGiven = NOT_GIVEN,
        top_p: float|NotGiven = NOT_GIVEN,
        response_format: Any|NotGiven = NOT_GIVEN,
        timeout: float|NotGiven = NOT_GIVEN,
        max_tokens: int|NotGiven = NOT_GIVEN,
    ):
        self.url = url
        self.name = name
        
        self.system_prompt = system_prompt
        self.api_key = api_key
        
        self.max_retries = max_retries
        self.resolve_func = resolve_func
        
        self.temperature = temperature
        self.top_p = top_p
        self.response_format = response_format
        self.timeout = timeout
        self.max_tokens = max_tokens
        
    async def __call__(
        self,
        prompt: str,
        *,
        url: str|NotGiven = NOT_GIVEN, name: str|NotGiven = NOT_GIVEN,
        api_key: str|NotGiven = NOT_GIVEN,
        
        system_prompt: str|NotGiven = NOT_GIVEN,
        history: list[tuple[str, str]]|None = None,
        
        max_retries: int|NotGiven = NOT_GIVEN,
        resolve_func: Callable[[str], T]|NotGiven = NOT_GIVEN,  # 解析函数，用于验证、格式化生成结果。
        
        temperature: float|NotGiven = NOT_GIVEN,
        top_p: float|NotGiven = NOT_GIVEN,
        response_format: Any|NotGiven = NOT_GIVEN,
        timeout: float|NotGiven = NOT_GIVEN,
        max_tokens: int|NotGiven = NOT_GIVEN,
    ) -> T|None:
        return await achat(
            prompt,
            url = url or self.url,
            name = name or self.name,
            api_key = api_key or self.api_key,
            
            system_prompt = system_prompt or self.system_prompt,
            history = history,
            
            max_retries = max_retries or self.max_retries,
            resolve_func = resolve_func or self.resolve_func,
            
            temperature = temperature or self.temperature,
            top_p = top_p or self.top_p,
            response_format = response_format or self.response_format,
            timeout = timeout or self.timeout,
            max_tokens = max_tokens or self.max_tokens,
        )