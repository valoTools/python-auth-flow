import typer
import riot_auth
import asyncio
from typing_extensions import Annotated
from rich import print

app = typer.Typer()

@app.command()
def authorize(
    username: Annotated[str, typer.Option(prompt=True)],
    password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
    ) -> None:
    """Authorize using the given username and password."""

    auth = riot_auth.RiotAuth()

    async def authorize_async():
        is_mfa = await auth.authorize(username, password)
        if is_mfa:
            typer.echo("Two-factor authentication required. Please enter your code:")
            code = typer.prompt("Code") 
            await auth.authorize_mfa(code)

        print("[bold red]Authorization successful![/bold red]:boom: ✅")
        typer.echo(f"Access Token: {auth.access_token}")
        typer.echo(f"Entitlements Token: {auth.entitlements_token}")
        typer.echo(f"User ID: {auth.user_id}")

    asyncio.run(authorize_async())

@app.command()
def reauthorize() -> None:
    """Reauthorize using saved cookies."""

    auth = riot_auth.RiotAuth()

    async def reauthorize_async():
        success = await auth.reauthorize()
        if success:
            typer.echo("Reauthorization successful!")
            typer.echo(f"Access Token: {auth.access_token}")
            typer.echo(f"Entitlements Token: {auth.entitlements_token}")
            typer.echo(f"User ID: {auth.user_id}")
        else:
            typer.echo("Reauthorization failed. Please try authorizing again.")

    asyncio.run(reauthorize_async())

# Optionally add more commands as needed (e.g., get_balance, get_profile, etc.)

if __name__ == "__main__":
    app()
