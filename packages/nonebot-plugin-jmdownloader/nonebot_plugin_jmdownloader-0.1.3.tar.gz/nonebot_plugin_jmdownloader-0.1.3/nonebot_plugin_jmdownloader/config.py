from pathlib import Path

from nonebot import get_plugin_config, require
from pydantic import BaseModel, Field

require("nonebot_plugin_localstore")

from nonebot_plugin_localstore import get_plugin_cache_dir


class Config(BaseModel):
    jmcomic_log: bool = Field(default=False, description="是否启用JMComic API日志")
    jmcomic_proxies: str = Field(default="system", description="代理配置")
    jmcomic_thread_count: int = Field(default=10, description="下载线程数量")
    jmcomic_username: str = Field(description="JM登录用户名")
    jmcomic_password: str = Field(description="JM登录密码")
    jmcomic_allow_groups: bool = Field(default=False, description="是否默认启用所有群")
    jmcomic_user_limits: int = Field(default=5, description="每位用户的每周下载限制次数")

plugin_config = get_plugin_config(Config)

plugin_cache_dir: Path = get_plugin_cache_dir()
cache_dir = plugin_cache_dir.as_posix()


config_data = f"""
log: {plugin_config.jmcomic_log}

client:
  impl: api
  retry_times: 1
  postman:
    meta_data:
      proxies: {plugin_config.jmcomic_proxies}

download:
  image:
    suffix: .jpg
  threading:
    image: {plugin_config.jmcomic_thread_count}

dir_rule:
  base_dir: {cache_dir}
  rule: Bd_Pid

plugins:
  after_init:
    - plugin: login
      kwargs:
        username: {plugin_config.jmcomic_username}
        password: {plugin_config.jmcomic_password}

  after_photo:
    - plugin: img2pdf
      kwargs:
        pdf_dir: {cache_dir}
        filename_rule: Pid
"""

