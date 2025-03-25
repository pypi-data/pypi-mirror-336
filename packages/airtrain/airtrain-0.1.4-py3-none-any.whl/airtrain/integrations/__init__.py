"""Airtrain integrations package"""

# Credentials imports
from .openai.credentials import OpenAICredentials
from .aws.credentials import AWSCredentials
from .google.credentials import GoogleCloudCredentials
from .anthropic.credentials import AnthropicCredentials
from .groq.credentials import GroqCredentials
from .together.credentials import TogetherAICredentials
from .ollama.credentials import OllamaCredentials
from .sambanova.credentials import SambanovaCredentials
from .cerebras.credentials import CerebrasCredentials
from .perplexity.credentials import PerplexityCredentials

# Skills imports
from .openai.skills import OpenAIChatSkill, OpenAIParserSkill
from .anthropic.skills import AnthropicChatSkill
from .aws.skills import AWSBedrockSkill
from .google.skills import GoogleChatSkill
from .groq.skills import GroqChatSkill
from .together.skills import TogetherAIChatSkill
from .ollama.skills import OllamaChatSkill
from .sambanova.skills import SambanovaChatSkill
from .cerebras.skills import CerebrasChatSkill
from .perplexity.skills import PerplexityChatSkill, PerplexityStreamingChatSkill

# Model configurations
from .openai.models_config import OPENAI_MODELS, OpenAIModelConfig
from .anthropic.models_config import ANTHROPIC_MODELS, AnthropicModelConfig
from .perplexity.models_config import PERPLEXITY_MODELS_CONFIG

# Combined modules
from .combined.list_models_factory import (
    ListModelsSkillFactory,
    GenericListModelsInput,
    GenericListModelsOutput,
)

__all__ = [
    # Credentials
    "OpenAICredentials",
    "AWSCredentials",
    "GoogleCloudCredentials",
    "AnthropicCredentials",
    "GroqCredentials",
    "TogetherAICredentials",
    "OllamaCredentials",
    "SambanovaCredentials",
    "CerebrasCredentials",
    "PerplexityCredentials",
    # Skills
    "OpenAIChatSkill",
    "OpenAIParserSkill",
    "AnthropicChatSkill",
    "AWSBedrockSkill",
    "GoogleChatSkill",
    "GroqChatSkill",
    "TogetherAIChatSkill",
    "OllamaChatSkill",
    "SambanovaChatSkill",
    "CerebrasChatSkill",
    "PerplexityChatSkill",
    "PerplexityStreamingChatSkill",
    # Model configurations
    "OPENAI_MODELS",
    "OpenAIModelConfig",
    "ANTHROPIC_MODELS",
    "AnthropicModelConfig",
    "PERPLEXITY_MODELS_CONFIG",
    # Combined modules
    "ListModelsSkillFactory",
    "GenericListModelsInput",
    "GenericListModelsOutput",
]
