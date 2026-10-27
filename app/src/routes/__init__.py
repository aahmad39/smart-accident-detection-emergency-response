# Tier 1 & 2: Routes Init
from .web import web_bp
from .api_v1 import api_v1_bp
from .ai_agents_api import ai_agents_bp

__all__ = ["web_bp", "api_v1_bp", "ai_agents_bp"]
