from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    figma_api_key: str | None = None
    tavily_api_key: str | None = None
    duckduckgo_api_key: str | None = None
    bfl_api_key: str | None = None

    enable_commond_tools: bool = True
    enable_file_ops_tools: bool = True
    enable_audio_tools: bool = True
    enabel_enhance_tools: bool = True
    tool_home: str = Path("~/.zerolab/mcp-toolbox").expanduser().as_posix()

    @property
    def cache_dir(self) -> str:
        return (Path(self.tool_home) / "cache").expanduser().resolve().absolute().as_posix()

    @property
    def memory_file(self) -> str:
        return (Path(self.tool_home) / "memory.sqlite").expanduser().resolve().absolute().as_posix()


if __name__ == "__main__":
    print(Config())
