import traceback
import random
from datetime import datetime
from typing import List, Dict, Optional, AsyncGenerator
from anthropic import AnthropicBedrock
import tiktoken
import boto3
from hwhkit.utils import logger
from hwhkit.llm.models import ModelStrategy, LanguageModelProperty


class BedrockStrategy(ModelStrategy):
    _sts_cache_duration = 36000  # STS 临时凭证有效期 (秒)
    _client_refresh_interval = 7200  # 客户端池刷新间隔 (秒)

    def get_name(self) -> str:
        return "bedrock"

    def base_url(self) -> str | None:
        return None

    def __init__(self, keys: Dict[str, str], model_property: LanguageModelProperty):
        self._keys = keys  # 区域列表，格式: {"us-west-2": "", "us-east-1": ""}
        self._property = model_property
        self._client_pool = []
        self._last_refresh = datetime.min
        self._refresh_clients()

    def _refresh_clients(self) -> None:
        """通过STS获取临时凭证并初始化客户端池"""
        if (datetime.now() - self._last_refresh).seconds < self._client_refresh_interval:
            return

        try:

            self._client_pool = []
            for key_id, access_key in self._keys.items():
                sts_client = boto3.client("sts", aws_access_key_id=key_id, aws_secret_access_key=access_key)
                credentials = sts_client.get_session_token(DurationSeconds=self._sts_cache_duration)['Credentials']

                region = "us-west-2"
                self._client_pool.append({
                    "name": region,
                    "client": AnthropicBedrock(
                        aws_access_key=credentials['AccessKeyId'],
                        aws_secret_key=credentials['SecretAccessKey'],
                        aws_session_token=credentials['SessionToken'],
                        aws_region=region
                    )
                })
            self._last_refresh = datetime.now()
        except Exception as e:
            logger.error(f"Failed to refresh Bedrock clients: {traceback.format_exc()}")
            raise

    def _get_client(self) -> Dict[str, AnthropicBedrock]:
        """随机获取一个可用客户端"""
        if not self._client_pool:
            self._refresh_clients()
            if not self._client_pool:
                raise Exception("No Bedrock client available")
        return random.choice(self._client_pool)

    def _calculate_token_count(self, text: str) -> int:
        return len(tiktoken.get_encoding("cl100k_base").encode(text))

    def _resize_messages(self, messages: List[Dict]) -> List[Dict]:
        if not messages:
            return []

        total_tokens = sum(self._calculate_token_count(m["content"]) for m in messages)
        max_tokens = self._property.max_input_token - 500  # 保留缓冲

        while total_tokens > max_tokens and len(messages) > 1:
            removed = messages.pop(0)
            total_tokens -= self._calculate_token_count(removed["content"])
        return messages

    async def gen_messages(
        self,
        question: str,
        system_prompt: Optional[str] = None,
        history_messages: Optional[List[Dict]] = None
    ) -> List[Dict[str, str]]:
        messages = []
        if system_prompt:
            messages.append({"system": system_prompt})
        if history_messages:
            messages.extend(history_messages)
        if question:
            messages.append({"role": "user", "content": question})
        return self._resize_messages(messages)

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        client = self._get_client()
        system_prompt = ""
        new_messages = []
        for one in messages:
            content = one.get("system")
            if content:
                system_prompt = content
            else:
                new_messages.append(one)
        try:
            response = client["client"].messages.create(
                model=self._property.name,
                messages=messages,
                system=system_prompt,
                max_tokens=self._property.max_output_token,
                temperature=self._property.temperature,
                top_p=self._property.top_p,
                top_k=self._property.top_k
            )
            return response.content[0].text
        except Exception as e:
            logger.error(
                f"Bedrock生成错误\n模型: {self._property.name}"
                f"\n区域: {client['name']}\n错误: {traceback.format_exc()}"
            )
            raise

    async def chat_stream(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        client = self._get_client()

        system_prompt = ""
        new_messages = []
        for one in messages:
            content = one.get("system")
            if content:
                system_prompt = content
            else:
                new_messages.append(one)

        try:
            stream = client["client"].messages.create(
                model=self._property.name,
                messages=new_messages,
                max_tokens=self._property.max_output_token,
                temperature=self._property.temperature,
                top_p=self._property.top_p,
                top_k=self._property.top_k,
                system=system_prompt,
                stream=True
            )
            for event in stream:
                if event.type == "content_block_delta":
                    yield event.delta.text
        except Exception as e:
            logger.error(
                f"Bedrock流式生成错误\n模型: {self._property.name}"
                f"\n区域: {client['name']}\n错误: {traceback.format_exc()}"
            )
            raise