from browser_use_recorder.logging_config import setup_logging

setup_logging()

from browser_use_recorder.agent.prompts import SystemPrompt as SystemPrompt
from browser_use_recorder.agent.service import Agent as Agent
from browser_use_recorder.agent.views import ActionModel as ActionModel
from browser_use_recorder.agent.views import ActionResult as ActionResult
from browser_use_recorder.agent.views import AgentHistoryList as AgentHistoryList
from browser_use_recorder.browser.browser import Browser as Browser
from browser_use_recorder.browser.browser import BrowserConfig as BrowserConfig
from browser_use_recorder.browser.context import BrowserContextConfig
from browser_use_recorder.controller.service import Controller as Controller
from browser_use_recorder.dom.service import DomService as DomService

__all__ = [
	'Agent',
	'Browser',
	'BrowserConfig',
	'Controller',
	'DomService',
	'SystemPrompt',
	'ActionResult',
	'ActionModel',
	'AgentHistoryList',
	'BrowserContextConfig',
]
