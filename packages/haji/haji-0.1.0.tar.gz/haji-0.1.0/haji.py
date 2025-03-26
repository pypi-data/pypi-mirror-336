import click
import requests
import asyncio
from g4f.client import Client


@click.command()
@click.argument("url")
@click.pass_context
def haji(ctx, url):
    """A simple CLI tool that takes a URL as input and fetches its content."""
    asyncio.run(haji_async(url))  # Run the async function properly


async def haji_async(url):
    """Asynchronous function that performs the operations."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            operations = {
                "c": "Comment Only",
                "r": "Comment with Relevancy",
            }
            # Show choices with title
            click.echo("Available operations:")
            for key, value in operations.items():
                click.echo(f"{key}: {value}")
            operation = click.prompt(
                "Choose an operation",
                type=click.Choice(operations.keys()),
                show_choices=True,
            )
            if operation not in operations.keys():
                click.echo("Invalid operation selected.")
                return
            client = Client()
            site_text = response.text
            prompt = f"Write a comment according to the context to website text. Here is the html website text with all other comments and context: \n{site_text}"
            if operation == "r":
                keyword = click.prompt("Enter your keyword", type=str)
                prompt = f"Write a comment according to the context to website text making relevancy to this keyword: '{keyword}'. Here is the website text with all other comments and context: \n{site_text}"

            click.echo(f"Writing comment...")
            message = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            # Print response
            click.echo(message.choices[0].message.content)

        else:
            click.echo(f"Failed to fetch URL: {url} (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching URL: {e}")


if __name__ == "__main__":
    haji()  # Click runs this function, and it will call `asyncio.run()`
