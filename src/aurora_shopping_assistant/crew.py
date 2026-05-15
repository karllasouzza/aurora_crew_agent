import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from aurora_shopping_assistant.tools import (
    ListProductsTool,
    GetProductTool,
    GetOrderStatusTool,
    CreateOrderTool,
)

llm = LLM(
    model="openrouter/inclusionai/ring-2.6-1t:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)


@CrewBase
class AuroraShoppingAssistant():
    """AuroraShoppingAssistant crew - Shopping assistant with research, data processing, validation, and persona layers."""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],  # type: ignore[index]
            verbose=True,
            reasoning=True,
            llm=llm,
        )

    @agent
    def data_processor(self) -> Agent:
        return Agent(
            config=self.agents_config['data_processor'],  # type: ignore[index]
            tools=[ListProductsTool(), GetProductTool(),
                   GetOrderStatusTool(), CreateOrderTool()],
            verbose=True,
            llm=llm,
        )

    @agent
    def logic_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['logic_reviewer'],  # type: ignore[index]
            tools=[ListProductsTool(), GetProductTool(),
                   GetOrderStatusTool(), CreateOrderTool()],
            verbose=True,
            reasoning=True,
            llm=llm,
        )

    @agent
    def aurora(self) -> Agent:
        return Agent(
            config=self.agents_config['aurora'],  # type: ignore[index]
            verbose=True,
            llm=llm,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],  # type: ignore[index]
        )

    @task
    def data_processing_task(self) -> Task:
        return Task(
            # type: ignore[index]
            config=self.tasks_config['data_processing_task'],
            context=[self.research_task()],
        )

    @task
    def logic_review_task(self) -> Task:
        return Task(
            # type: ignore[index]
            config=self.tasks_config['logic_review_task'],
            context=[self.data_processing_task()],
        )

    @task
    def generate_response_task(self) -> Task:
        return Task(
            # type: ignore[index]
            config=self.tasks_config['generate_response_task'],
            context=[self.logic_review_task()],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AuroraShoppingAssistant crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
