"""Runtime configuration for Sentinel Coder agent."""

import json
from dataclasses import dataclass, field
from pathlib import Path


def _load_preferred_model() -> str:
    """Load preferred model from ~/.sentinel/configuration.json (or legacy ~/.hive/)."""
    for config_path in [
        Path.home() / ".sentinel" / "configuration.json",
        Path.home() / ".hive" / "configuration.json",
    ]:
        if config_path.exists():
            try:
                with open(config_path, encoding="utf-8") as f:
                    config = json.load(f)
                llm = config.get("llm", {})
                if llm.get("provider") and llm.get("model"):
                    return f"{llm['provider']}/{llm['model']}"
            except Exception:
                pass
    # Default to Airia Pro for orchestration
    return "airia/airia-pro"


@dataclass
class RuntimeConfig:
    model: str = field(default_factory=_load_preferred_model)
    temperature: float = 0.7
    max_tokens: int = 8000
    api_key: str | None = None
    api_base: str | None = None


default_config = RuntimeConfig()


@dataclass
class AgentMetadata:
    name: str = "Sentinel Coder"
    version: str = "1.0.0"
    description: str = (
        "Native coding agent powered by Airia Pro that builds production-ready "
        "Sentinel compliance agent packages from natural language specifications. Produces "
        "complete Python packages with goals, nodes, edges, system prompts, "
        "MCP configuration, and tests. Worker nodes use Airia Fast for cost efficiency."
    )
    intro_message: str = (
        "I'm Sentinel Coder — I build compliance agents powered by Airia. Describe "
        "what kind of compliance agent you want to create and I'll design, implement, and "
        "validate it for you."
    )


metadata = AgentMetadata()
