import logging
import os
import shutil
from pathlib import Path

import pandas as pd
import requests
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer()
logger = logging.getLogger("CTD_Pipeline")
console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def show_intro():
    console.clear()
    text = Text()
    text.append("CTD Data Preparation Tool\n\n", style="bold cyan")
    text.append("Created by: Deepak Kumar Sachan\n", style="bold white")
    text.append(
        "This tool downloads and processes CTD data on chemicals, diseases,\n",
        style="bold green",
    )
    text.append("phenotypes, and genes.\n", style="bold green")
    panel = Panel(
        text, title="Welcome", title_align="left", border_style="bright_yellow"
    )
    console.print(panel)


def read_txt_file_to_list(filename):
    try:
        with open(filename, "r") as file:
            lines = [line.strip() for line in file]
        return lines
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        return []
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return []


def exportcsv(inputDf, outputFileName):
    file_name = f"{outputFileName}.csv"
    inputDf.to_csv(file_name, index=False)
    logger.info(f"File saved: {file_name}")


def aggregate_dataframe(df, group_columns, aggregate_column):
    def join_unique_strings(series):
        return ", ".join(series.dropna().unique())

    aggregated_df = (
        df.groupby(group_columns)[aggregate_column]
        .agg(join_unique_strings)
        .reset_index()
    )
    if (aggregated_df.iloc[0] == aggregated_df.columns).all():
        aggregated_df = aggregated_df.iloc[1:]
    return aggregated_df


def extract_unique_and_save(df, column, output_filename):
    unique_values = df[column].unique()
    with open(output_filename, "w") as file:
        for item in unique_values:
            file.write(f"{item}\n")
    logger.info(f"Unique values saved to '{output_filename}'")


def ctd_download(
    input_type, input_terms, report, format, file_base_name, ontology_association=None
):
    MAX_TERMS = 500
    total_chunks = (len(input_terms) - 1) // MAX_TERMS + 1
    folder_name = f"{file_base_name}_files"
    combined_file_name = f"{file_base_name}.{format}"

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    os.makedirs(folder_name)

    for i, start in enumerate(range(0, len(input_terms), MAX_TERMS)):
        chunk = input_terms[start : start + MAX_TERMS]
        input_terms_str = "|".join(chunk)
        url = (
            f"https://ctdbase.org/tools/batchQuery.go?inputType={input_type}"
            f"&inputTerms={input_terms_str}&report={report}&format={format}"
            f"&ontology={ontology_association}&inputTermSearchType=directAssociations"
        )
        file_name = os.path.join(folder_name, f"{file_base_name}_{i + 1}.csv")
        logger.info(f"Downloading chunk {i + 1} of {total_chunks}...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_name, "wb") as f:
                for chunk_data in response.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk_data)
            logger.info(f"Chunk {i + 1} downloaded successfully: {file_name}")
        else:
            logger.error(
                f"Failed to download chunk {i + 1}. Status code: {response.status_code}"
            )
            break

    if os.path.exists(folder_name):
        with open(combined_file_name, "wb") as combined_file:
            for i in range(1, total_chunks + 1):
                chunk_file_name = os.path.join(folder_name, f"{file_base_name}_{i}.csv")
                with open(chunk_file_name, "rb") as chunk_file:
                    combined_file.write(chunk_file.read())
        logger.info(f"Combined all chunks into: {combined_file_name}")
    else:
        logger.error("No chunks were downloaded, so no combined file created.")


@app.command()
def run(
    chemical_file: str = typer.Argument(..., help="Input .txt file with chemical names")
):
    """Run the CTD data preparation pipeline."""
    show_intro()
    chemical_list = read_txt_file_to_list(chemical_file)
    logger.info(f"Chemicals present for analysis: {len(chemical_list)}")

    ctd_download(
        "chem", chemical_list, "diseases_curated", "csv", "raw_chemical_disease"
    )
    df_raw = pd.read_csv("raw_chemical_disease.csv")
    df_filtered = df_raw[df_raw["DirectEvidence"] == "marker/mechanism"]
    exportcsv(df_filtered, "chemical_disease")

    agg_df = aggregate_dataframe(
        df_filtered, ["# Input", "ChemicalName", "ChemicalID", "CasRN"], "DiseaseID"
    )
    exportcsv(agg_df, "aggregated_chemical_disease")

    extract_unique_and_save(df_filtered, "DiseaseID", "diseases_chemical_disease.txt")
    extract_unique_and_save(df_filtered, "CasRN", "chemicals_chemical_disease.txt")

    disease_list = read_txt_file_to_list("diseases_chemical_disease.txt")
    chem_list = read_txt_file_to_list("chemicals_chemical_disease.txt")
    ctd_download("chem", chem_list, "phenotypes_curated", "csv", "chemical_phenotype")
    ctd_download("chem", chem_list, "genes_curated", "csv", "chemical_gene")
    ctd_download("disease", disease_list, "genes_curated", "csv", "disease_gene")

    console.print(
        "[bold green]CTD data preparation pipeline completed successfully.[/bold green]"
    )


if __name__ == "__main__":
    app()
