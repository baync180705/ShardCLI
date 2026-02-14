import typer
from rich.console import Console
from rich.panel import Panel

from shardcli.core import ShardOrchestrator, CommandExecutor
from shardcli.engine import DefaultPolicy, StrictPolicy, RelaxedPolicy, RiskLevel

class ShardCLI:
    def __init__(self):
        self.console = Console()
        self.app = typer.Typer(help="Shard — AI-powered terminal assistant")

        # Register command
        self.app.command()(self.run)

    def run(
        self,
        prompt: str = typer.Argument(None, help="Natural language instruction"),
        policy: str = typer.Option(
            "default",
            "--policy",
            "-p",
            help="Policy level: strict | default | relaxed"
        ),
        explain: bool = typer.Option(
            False,
            "--explain",
            "-e",
            help="Show command explanation"
        )
    ):
        active_policy = self._resolve_policy(policy)
        orchestrator = ShardOrchestrator(active_policy)
        executor = CommandExecutor()

        if prompt:
            self._handle_prompt(prompt, orchestrator, executor, explain)
        else:
            self._interactive_session(orchestrator, executor, explain)


    def _resolve_policy(self, policy_name: str):
        if policy_name == "strict":
            return StrictPolicy()
        elif policy_name == "relaxed":
            return RelaxedPolicy()
        return DefaultPolicy()

    def _handle_prompt(self, prompt, orchestrator, executor, explain):
        response = orchestrator.process_request(prompt)

        if response.command is None:
            self.console.print(
                Panel(response.explanation, title="Error", style="red")
            )
            return
        
        if response.note:
            self.console.print(f"[dim]Note: {response.note}[/dim]")
        self.console.print(
            Panel(response.command, title="Generated Command", style="cyan")
        )

        if explain:
            self.console.print(f"[bold]Explanation:[/bold] {response.explanation}")

        risk_report = response.risk_report

        if risk_report.level == RiskLevel.BLOCK:
            self.console.print(f"[bold red]BLOCKED:[/bold red] {risk_report.reason}")
            return

        if risk_report.level == RiskLevel.WARN:
            self.console.print(f"[bold yellow]WARNING:[/bold yellow] {risk_report.reason}")

        confirm = typer.confirm("Execute this command?")
        if not confirm:
            return

        execution_result = executor.execute(response.command)

        if execution_result.success:
            self.console.print(execution_result.stdout)
        else:
            self.console.print(f"[red]{execution_result.stderr}[/red]")

    def _interactive_session(self, orchestrator, executor, explain):
        self.console.print("[bold green]Shard Interactive Mode[/bold green]")
        self.console.print("Type 'exit' to quit.\n")

        while True:
            user_input = self.console.input("[bold cyan]>> [/bold cyan]")

            if user_input.lower() in {"exit", "quit"}:
                break

            self._handle_prompt(user_input, orchestrator, executor, explain)
