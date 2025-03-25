import click
from auledft.backend.dft_runner import run_dft

@click.command()
@click.argument("input_file")
@click.option("--software", type=click.Choice(["vasp", "qe"]), required=True)
@click.option("--hpc", is_flag=True, help="Run on HPC")
def cli(input_file, software, hpc):
    """Run DFT on a specified input file."""
    result = run_dft(input_file, software, hpc)
    print(result)

if __name__ == "__main__":
    cli()
