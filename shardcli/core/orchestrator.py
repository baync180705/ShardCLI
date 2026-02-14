from shardcli.config import Settings
from shardcli.core.environment import Environment
from shardcli.core.models import ShardResponse
from shardcli.engine import RiskEngine, RiskReport, SecurityPolicy
from shardcli.llm import PromptBuilder, GroqLLMClient, StructuredOutputEnforcer, CommandGenerationResult


class ShardOrchestrator:
    """
    Coordinates all core subsystems:
    - Environment detection
    - Prompt construction
    - LLM invocation
    - Risk analysis

    This class contains NO UI or execution logic.
    """

    def __init__(self, policy: SecurityPolicy):
        self.policy = policy
        self.settings = Settings()

    def process_request(self, user_prompt: str) -> ShardResponse:
        """
        Main entrypoint for processing a user instruction.
        """

        environment = self._detect_environment()
        system_prompt = self._build_system_prompt(environment)
        llm_client = self._initialize_llm(system_prompt)

        command_result = self._generate_command(llm_client, user_prompt)
        risk_report = self._evaluate_risk(command_result.command)

        return ShardResponse(
            command=command_result.command,
            explanation=command_result.explanation,
            risk_report=risk_report
        )

    def _detect_environment(self) -> Environment:
        return Environment()

    def _build_system_prompt(self, environment: Environment) -> str:
        prompt_builder = PromptBuilder(environment)
        return prompt_builder.build_system_prompt()

    def _initialize_llm(self, system_prompt: str) -> GroqLLMClient:
        structured_output = StructuredOutputEnforcer(CommandGenerationResult)

        return GroqLLMClient(
            system_prompt=system_prompt,
            model=self.settings.model_name,
            temperature=self.settings.temperature,
            top_p=self.settings.top_p,
            api_key=self.settings.groq_api_key,
            structured_output_enforcer=structured_output
        )

    def _generate_command(self, llm_client: GroqLLMClient, user_prompt: str) -> CommandGenerationResult:
        return llm_client.generate(user_prompt)

    def _evaluate_risk(self, command: str) -> RiskReport:
        risk_engine = RiskEngine(self.policy)
        return risk_engine.analyze(command)
