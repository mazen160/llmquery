import argparse
import os
import sys
import llmquery
from rich.console import Console
from rich.json import JSON
import json

console = Console()

def list_models():
    console.print("[bold cyan]Available models:[/bold cyan]")
    console.print("[bold cyan](OpenAI)[/bold cyan]")
    console.print(f"[bold cyan]OpenAI[/bold cyan] default model: {llmquery.openai.DEFAULT_MODEL}")
    for i in llmquery.openai.ACCEPTED_MODELS:
        console.print(f"[bold cyan]OpenAI[/bold cyan] model: {i}")
    console.print("[bold cyan](Anthropic)[/bold cyan]")
    console.print(f"[bold cyan]Anthropic[/bold cyan] default model: {llmquery.anthropic_claude.DEFAULT_MODEL}")
    for i in llmquery.anthropic_claude.ACCEPTED_MODELS:
        console.print(f"[bold cyan]Anthropic[/bold cyan] model: {i}")
    console.print("[bold cyan](Google Gemini)[/bold cyan]")
    console.print(f"[bold cyan]Google Gemini[/bold cyan] default model: {llmquery.google_gemini.DEFAULT_MODEL}")
    for i in llmquery.google_gemini.ACCEPTED_MODELS:
        console.print(f"[bold cyan]Google Gemini[/bold cyan] model: {i}")
    console.print("[bold cyan](OLLAMA)[/bold cyan]")
    console.print("[bold cyan](AWS Bedrock)[/bold cyan]")
    console.print(f"[bold cyan](AWS Bedrock)[/bold cyan] default model: {llmquery.aws_bedrock.DEFAULT_MODEL}")
    console.print("[bold cyan]AWS Bedrock[/bold cyan]: Run the command 'aws bedrock list-foundation-models' to list available models.")
    for i in llmquery.aws_bedrock.ALLOWED_MODELS:
        console.print(f"[bold cyan]AWS Bedrock[/bold cyan] model: {i}")
        
def display_banner():
    console.print("[bold magenta]Welcome to llmquery CLI![/bold magenta]", justify="left")
    console.print("[green]Scaling GenAI automation 🚀🌐[/green]", justify="left")
    console.print("""[cyan]

██      ██      ███    ███  ██████  ██    ██ ███████ ██████  ██    ██
██      ██      ████  ████ ██    ██ ██    ██ ██      ██   ██  ██  ██
██      ██      ██ ████ ██ ██    ██ ██    ██ █████   ██████    ████
██      ██      ██  ██  ██ ██ ▄▄ ██ ██    ██ ██      ██   ██    ██
███████ ███████ ██      ██  ██████   ██████  ███████ ██   ██    ██
                               ▀▀
https://github.com/mazen160/llmquery | https://mazinahmed.net
    [/cyan]""")


def main():
    display_banner()

    parser = argparse.ArgumentParser(
        description="[bold cyan]A CLI for querying LLMs using YAML templates with llmquery.[/bold cyan]"
    )

    parser.add_argument(
        "--provider",
        type=str,
        choices=llmquery.ACCEPTED_PROVIDERS,
        default=os.getenv("LLMQUERY_PROVIDER"),
        help=f"Specify the LLM provider to use (e.g. {', '.join(llmquery.ACCEPTED_PROVIDERS)}).",
    )

    parser.add_argument(
        "--templates-path",
        type=str,
        help=f"Path to the YAML templates directory defining the query (Default: {llmquery.TEMPLATES_PATH}).",
        default=llmquery.TEMPLATES_PATH
    )

    parser.add_argument(
        "--template-id",
        type=str,
        help="Template ID to use when multiple templates exist in the file.",
    )

    parser.add_argument(
        "--variables",
        type=str,
        help="JSON string of variables to pass to the template.",
    )

    parser.add_argument(
        "--variables-file",
        type=str,
        help="JSON file of variables to pass to the template.",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("LLMQUERY_MODEL"),
        help="The model to use for the query (e.g., gpt-4).",
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=8192,
        help="Maximum number of tokens for the response (default: 8192).",
    )

    parser.add_argument(
        "--max-length",
        type=int,
        default=2048,
        help="Maximum character length for the prompt (default: 2048).",
    )

    parser.add_argument(
        "--api-key",
        type=str,
        help="API key for the selected provider. If not provided, the environment variable for the provider will be used.",
    )

    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models for the selected provider.",
    )

    parser.add_argument(
        "--aws-bedrock-region",
        type=str,
        help="AWS region for Bedrock service.",
        default=llmquery.aws_bedrock.AWS_REGION,
    )

    parser.add_argument(
        "--aws-bedrock-anthropic-version",
        type=str,
        help="Anthropic version for AWS Bedrock Claude models.",
        default=llmquery.aws_bedrock.ANTHROPIC_VERSION,
    )

    args = parser.parse_args()

    if args.list_models:
        list_models()
        sys.exit(0)

    # Validate inputs
    if not args.templates_path:
        console.print("[bold red]Error:[/bold red] You must provide --template-path.", style="red")
        sys.exit(1)

    if not args.provider:
        console.print("[bold red]Error:[/bold red] You must provide --provider.", style="red")
        sys.exit(1)

    # Parse variables
    variables = {}
    if args.variables:
        try:
            variables = json.loads(args.variables)
        except json.JSONDecodeError:
            console.print("[bold red]Error:[/bold red] --variables must be a valid JSON string.", style="red")
            sys.exit(1)
    if args.variables_file:
        try:
            with open(args.variables_file, "r") as f:
                variables = json.loads(f.read())
        except json.JSONDecodeError:
            console.print("[bold red]Error:[/bold red] --variables-file must be a valid JSON file.", style="red")
            sys.exit(1)

    # Initialize LLMQuery
    try:
        console.print("[cyan]Initializing query...[/cyan]")
        query = llmquery.LLMQuery(
            provider=args.provider,
            templates_path=args.templates_path,
            template_id=args.template_id,
            variables=variables,
            openai_api_key=os.getenv("OPENAI_API_KEY") if args.provider == "OPENAI" else args.api_key,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY") if args.provider == "ANTHROPIC" else args.api_key,
            google_gemini_api_key=os.getenv("GOOGLE_GEMINI_API_KEY") if args.provider == "GOOGLE_GEMINI" else args.api_key,
            model=args.model,
            max_tokens=args.max_tokens,
            max_length=args.max_length,
            aws_bedrock_region=args.aws_bedrock_region,
            aws_bedrock_anthropic_version=args.aws_bedrock_anthropic_version,
        )

        response = query.Query()
        console.print("[yellow bold]Data Sent:[/yellow bold]", style="bold yellow")
        console.print(JSON.from_data(response["data"]))
        console.print("[green bold]Response Received:[/green bold]", style="bold green")
        console.print(JSON.from_data(response["response"]))
        try:
            data = json.loads(response["response"])
            console.print("[purple bold]Response JSON (Parsed):[/purple bold]", style="bold purple")
            console.print(JSON.from_data(data))
        except Exception:
            pass

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="red")
        sys.exit(1)

if __name__ == "__main__":
    main()
