import click
from .cleaner import find_large_files

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """GitHub Cleaner CLI"""
    if ctx.invoked_subcommand is None:
        click.echo("\nGit Cleaner CLI\n")
        click.echo("Usage: gitrim [COMMAND] [OPTIONS]\n")
        click.echo("Commands:")
        click.echo("  large-files               Detect large files in Git history")
        click.echo("  scan-working-dir          Detect large files in the current working directory")
        click.echo("  remove-large-files        Remove large files from the working directory")
        click.echo("  generate-pre-commit-hook  Generate a pre-commit hook to block large files\n")
        click.echo("Examples:")
        click.echo("  gitrim large-files --threshold 5 --unit MB")
        click.echo("  gitrim scan-working-dir --threshold 500 --unit KB")
        click.echo("  gitrim remove-large-files --threshold 2 --unit MB")
        click.echo("  gitrim generate-pre-commit-hook --threshold 1 --unit MB\n")
        click.echo("For more details on a command, use 'gitrim COMMAND --help'\n")

@cli.command()
@click.option("--threshold", default=10, type=float, help="Size threshold.")
@click.option("--unit", default="MB", type=click.Choice(["KB", "MB", "GB"], case_sensitive=False), help="Unit for threshold (KB, MB, GB)")
def large_files(threshold, unit):
    """Detect large files in Git history"""
    find_large_files(threshold, unit)

@click.command()
@click.option("--threshold", default=10, type=float, help="Size threshold.")
@click.option("--unit", default="MB", type=click.Choice(["KB", "MB", "GB"], case_sensitive=False), help="Unit for threshold (KB, MB, GB)")
def scan_working_dir(threshold, unit):
    """Detect large files in the current working directory (not git history)"""
    from .cleaner import find_large_files_in_dir
    find_large_files_in_dir(threshold, unit)

@click.command()
@click.option("--threshold", default=10, type=float, help="Size threshold.")
@click.option("--unit", default="MB", type=click.Choice(["KB", "MB", "GB"], case_sensitive=False), help="Unit for threshold (KB, MB, GB)")
def generate_pre_commit_hook(threshold, unit):
    """Generate a pre-commit hook to block large files from being committed."""
    from .cleaner import generate_pre_commit_hook
    generate_pre_commit_hook(threshold, unit)

@click.command()
@click.option("--threshold", default=10, type=float, help="Size threshold.")
@click.option("--unit", default="MB", type=click.Choice(["KB", "MB", "GB"], case_sensitive=False), help="Unit for threshold (KB, MB, GB)")
@click.option("--dry-run", is_flag=True, help="Show what would be deleted, but don't delete.")
@click.option("--yes", is_flag=True, help="Delete without confirmation.")
def remove_large_files(threshold, unit, dry_run, yes):
    """Remove large files from the working directory."""
    from .cleaner import remove_large_files_in_dir
    remove_large_files_in_dir(threshold, unit, dry_run, yes)

cli.add_command(scan_working_dir)
cli.add_command(generate_pre_commit_hook)
cli.add_command(remove_large_files)
