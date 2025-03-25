import typer
import datetime
from .client import SolidTimeClient

app = typer.Typer()

def client():
    try:
        client = SolidTimeClient()
    except Exception as e:
        typer.echo(f"Failed to initialize client: {e}")
        exit()
    return client
CLIENT = client()

@app.command()
def current(description_length: int = typer.Option(20, help="Limit the description length")):
    """Show the current active timer."""
    timer = CLIENT.get_current_timer()

    if not timer:
        typer.echo("No active timer found.")
        return

    description = timer["data"].get("description", "No description")
    start_time = timer["data"].get("start")
    # Get Diff time
    if start_time:
        try:
            start_datetime = datetime.datetime.fromisoformat(start_time)
            current_time = datetime.datetime.now(datetime.timezone.utc)
            time_diff = current_time - start_datetime
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time = f"{hours:02d}:{minutes:02d}"
        except (ValueError, TypeError):
            time = "Unable to calculate duration"
    else:
        time = "No start time available"
    typer.echo(f"{description[:description_length]} - {time}")

@app.command()
def start(
    description: str = typer.Argument(..., help="Description of the time entry"),
    billable: bool = typer.Option(True, help="Whether the time entry is billable"),
    keep: bool = typer.Option(True, help="Whether to keep the active timer or replace it")
):
    """Start a new timer with the given description."""
    # Check if there's an active timer and stop it first
    current_timer = CLIENT.get_current_timer()
    if current_timer:
        if keep:
            typer.echo(f"Keeping current timer: {current_timer['data'].get('description', 'No description')}")
            exit()
        else:
            typer.echo(f"Stopping current timer: {current_timer['data'].get('description', 'No description')}")
            CLIENT.stop_timer(current_timer)
    # Start the new timer
    result = CLIENT.start_timer(description, billable)

    if "error" in result:
        typer.echo(f"Failed to start timer: {result.get('error')}")
        return

    timer = result.get("data")
    typer.echo(f"Timer started: {timer.get('description')}")
    typer.echo(f"Started at: {timer.get('start')}")

@app.command()
def stop():
    """Stop the current active timer."""
    timer = CLIENT.get_current_timer()

    if not timer:
        typer.echo("No active timer found.")
        return

    typer.echo(f"Stopping timer: {timer['data']['description']}")
    result = CLIENT.stop_timer(timer).get("data")
    data = result.get("data")
    typer.echo(f"Timer stopped: {data.get('description')}")
    typer.echo(f"Stopped at: {data.get('end')}")

@app.command()
def members():
    """List all members of the organization."""
    result = CLIENT.list_members()

    if not result:
        typer.echo("No members found.")
        return

    typer.echo("Members:")
    for member in result.get("data"):
        typer.echo(f"- {member["id"]} {member['name']} ({member['email']})")

def main():
    app()

if __name__ == "__main__":
    main()
