import os
import sys
from pathlib import Path

from browser_use_recorder.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_openai import ChatOpenAI

from browser_use_recorder import Agent, Controller
from browser_use_recorder.browser.browser import Browser, BrowserConfig
from browser_use_recorder.browser.context import BrowserContext

browser = Browser(
	config=BrowserConfig(
		# NOTE: you need to close your chrome browser - so that this can open your browser in debug mode
		browser_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)


async def main():
	agent = Agent(
		task='In docs.google.com write my Papa a quick letter',
		llm=ChatOpenAI(model='gpt-4o'),
		browser=browser,
	)

	await agent.run()
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
