"""
CTD Data Preparation Tool

Created by: Deepak Kumar Sachan

This tool downloads and processes CTD data on chemicals, diseases,
phenotypes, and genes.
"""

import logging
import os
import shutil
import sys
from pathlib import Path

import pandas as pd
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# ---------------------------- Logging Setup ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("CTD_Pipeline")
console = Console()

# ---------------------------- Rich UI Functions ----------------------------


def show_intro():
    """Display a welcome message using Rich."""
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


def list_txt_files_in_directory(directory, extension=".txt"):
    """List all .txt files in the given directory."""
    return [
        f.name
        for f in Path(directory).iterdir()
        if f.is_file() and f.suffix == extension
    ]


def get_valid_file_name():
    """Prompt the user to select a valid input file from available .txt files."""
    files = list_txt_files_in_directory(Path.cwd(), extension=".txt")
    console.print("[bold green]Available .txt files:[/bold green]")
    for file in files:
        console.print(file)
    while True:
        input_file = input("Please enter the input file name (with extension): ")
        if input_file in files:
            return input_file
        else:
            console.print(
                f"[bold red]File '{input_file}' not found. Please try again.[/bold red]"
            )


# ---------------------------- Helper Functions ----------------------------


def dataframe_summary(df):
    """Print summary statistics for each column in the DataFrame."""
    for column in df.columns:
        print(f"\nColumn: {column}")
        print(f"Number of unique values: {df[column].nunique()}")
        print(f"Number of missing values: {df[column].isna().sum()}")


def ltof(my_list, file_name):
    """Save a list to a text file."""
    with open(file_name, "w") as file:
        for item in my_list:
            file.write(f"{item}\n")
    logging.info(f"List saved to '{file_name}'")


def aggregate_dataframe(df, group_columns, aggregate_column):
    """
    Group the DataFrame by the given columns and aggregate unique values
    from the specified column.
    """

    def join_unique_strings(series):
        return ", ".join(series.dropna().unique())

    aggregated_df = (
        df.groupby(group_columns)[aggregate_column]
        .agg(join_unique_strings)
        .reset_index()
    )
    # Remove duplicated header row if present
    if (aggregated_df.iloc[0] == aggregated_df.columns).all():
        aggregated_df = aggregated_df.iloc[1:]
    return aggregated_df


def colname(df):
    """Print the column names of the DataFrame."""
    for col in df.columns:
        print(col)


def exportcsv(inputDf, outputFileName):
    """Export the DataFrame to a CSV file."""
    file_name = f"{outputFileName}.csv"
    inputDf.to_csv(file_name, index=False)
    logging.info(f"File saved: {file_name}")


def filter_and_save_dataframe(df, column, value, output_filename):
    """
    Filter the DataFrame based on a given column value and save the filtered DataFrame.
    """
    filtered_df = df[df[column].isin([value])]
    exportcsv(filtered_df, output_filename)


def extract_unique_and_save(df, column, output_filename):
    """
    Extract unique values from a DataFrame column, display the count,
    and save them to a text file.
    """
    unique_values = df[column].unique()
    print(f"\nUnique {column} Count: {len(unique_values)}")
    ltof(unique_values, output_filename)


def read_txt_file_to_list(filename):
    """
    Read a text file and return a list of lines with whitespace stripped.
    """
    try:
        with open(filename, "r") as file:
            lines = [line.strip() for line in file]
        return lines
    except FileNotFoundError:
        logging.error(f"File '{filename}' not found.")
        return []
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return []


def ctd_download(
    input_type, input_terms, report, format, file_base_name, ontology_association=None
):
    """
    Download files from CTD Batch Query for a list of input terms.
    """
    MAX_TERMS = 500  # Maximum terms per request
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
        logging.info(f"Downloading chunk {i + 1} of {total_chunks}...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_name, "wb") as f:
                for chunk_data in response.iter_content(chunk_size=100 * 1024 * 1024):
                    f.write(chunk_data)
            logging.info(f"Chunk {i + 1} downloaded successfully: {file_name}")
        else:
            logging.error(
                f"Failed to download chunk {i + 1}. Status code: {response.status_code}"
            )
            break

    logging.info(f"All chunks downloaded and stored in folder: {folder_name}")

    if os.path.exists(folder_name):
        with open(combined_file_name, "wb") as combined_file:
            for i in range(1, total_chunks + 1):
                chunk_file_name = os.path.join(folder_name, f"{file_base_name}_{i}.csv")
                with open(chunk_file_name, "rb") as chunk_file:
                    combined_file.write(chunk_file.read())
        logging.info(f"Combined all chunks into: {combined_file_name}")
    else:
        logging.error("No chunks were downloaded, so no combined file created.")


def find_common_genes(row):
    """
    For a given DataFrame row, find common genes between ChemicalGeneSymbol and DiseaseGeneSymbol.
    """
    chemical_genes = (
        str(row["ChemicalGeneSymbol"]).split(",")
        if pd.notna(row["ChemicalGeneSymbol"])
        else []
    )
    disease_genes = (
        str(row["DiseaseGeneSymbol"]).split(",")
        if pd.notna(row["DiseaseGeneSymbol"])
        else []
    )
    common = set(chemical_genes).intersection(disease_genes)
    return ", ".join(common) if common else pd.NA


# ---------------------------- Pipeline Function ----------------------------


def run_ctd_pipeline(chemical_file):
    """
    Run the CTD data preparation pipeline using the chemical names provided in the input file.
    """
    # Step 1: Read the chemical list from the selected file.
    chemical_list = read_txt_file_to_list(chemical_file)
    logging.info(f"Chemicals present for analysis: {len(chemical_list)}")

    # Step 2: Download chemical-disease associations.
    ctd_download(
        "chem", chemical_list, "diseases_curated", "csv", "raw_chemical_disease"
    )

    # Step 3: Process the downloaded chemical-disease file.
    df_raw_chemical_disease = pd.read_csv("raw_chemical_disease.csv")
    logging.info(
        f"Unique DiseaseID Count: {len(df_raw_chemical_disease['DiseaseID'].unique())}"
    )
    logging.info(
        f"Unique CasRN Count: {len(df_raw_chemical_disease['CasRN'].unique())}"
    )

    # Step 4: Filter associations with marker/mechanism as DirectEvidence.
    filter_and_save_dataframe(
        df_raw_chemical_disease,
        "DirectEvidence",
        "marker/mechanism",
        "chemical_disease",
    )
    df_chemical_disease = pd.read_csv("chemical_disease.csv")
    logging.info(f"Shape of chemical_disease.csv: {df_chemical_disease.shape}")

    # Step 5: Aggregate chemical-disease associations.
    aggregated_chemical_disease = aggregate_dataframe(
        df_chemical_disease,
        ["# Input", "ChemicalName", "ChemicalID", "CasRN"],
        "DiseaseID",
    )
    aggregated_chemical_disease.to_csv("aggregated_chemical_disease.csv", index=False)
    logging.info(
        f"Shape of aggregated_chemical_disease.csv: {aggregated_chemical_disease.shape}"
    )

    # Step 6: Extract unique disease and chemical IDs.
    extract_unique_and_save(
        df_chemical_disease, "DiseaseID", "diseases_chemical_disease.txt"
    )
    extract_unique_and_save(
        df_chemical_disease, "CasRN", "chemicals_chemical_disease.txt"
    )
    disease_list = read_txt_file_to_list("diseases_chemical_disease.txt")
    chemical_list = read_txt_file_to_list("chemicals_chemical_disease.txt")

    # Step 7: Download additional CTD reports.
    ctd_download(
        "chem", chemical_list, "phenotypes_curated", "csv", "chemical_phenotype"
    )
    ctd_download("chem", chemical_list, "genes_curated", "csv", "chemical_gene")
    ctd_download("disease", disease_list, "genes_curated", "csv", "disease_gene")

    # Step 8: Load and aggregate phenotype and gene data.
    df_chemical_phenotype = pd.read_csv("chemical_phenotype.csv", dtype=str)
    df_chemical_gene = pd.read_csv("chemical_gene.csv", dtype=str)
    df_disease_gene = pd.read_csv("disease_gene.csv", dtype=str)
    logging.info("Additional DataFrames loaded.")
    logging.info(f"Shape of chemical_phenotype.csv: {df_chemical_phenotype.shape}")
    logging.info(f"Shape of chemical_gene.csv: {df_chemical_gene.shape}")
    logging.info(f"Shape of disease_gene.csv: {df_disease_gene.shape}")

    aggregated_chemical_phenotype = aggregate_dataframe(
        df_chemical_phenotype,
        ["# Input", "ChemicalName", "ChemicalID", "CasRN"],
        "PhenotypeID",
    )
    aggregated_chemical_phenotype.to_csv(
        "aggregated_chemical_phenotype.csv", index=False
    )
    aggregated_chemical_gene = aggregate_dataframe(
        df_chemical_gene,
        ["# Input", "ChemicalName", "ChemicalId", "CasRN"],
        "GeneSymbol",
    )
    aggregated_chemical_gene.to_csv("aggregated_chemical_gene.csv", index=False)
    aggregated_disease_gene = aggregate_dataframe(
        df_disease_gene, ["# Input", "DiseaseName", "DiseaseID"], "GeneSymbol"
    )
    aggregated_disease_gene.to_csv("aggregated_disease_gene.csv", index=False)

    # Rename column for consistency.
    aggregated_chemical_gene.rename(columns={"ChemicalId": "ChemicalID"}, inplace=True)
    logging.info(
        f"Columns in aggregated_chemical_gene: {aggregated_chemical_gene.columns}"
    )

    # Step 9: Merge data to combine chemical-disease, phenotype, and gene info.
    merged_cd_pheno = pd.merge(
        df_chemical_disease,
        aggregated_chemical_phenotype[
            ["# Input", "ChemicalName", "ChemicalID", "CasRN", "PhenotypeID"]
        ],
        on=["# Input", "ChemicalName", "ChemicalID", "CasRN"],
        how="left",
    )
    merged_cd_pheno_gene = pd.merge(
        merged_cd_pheno,
        aggregated_chemical_gene[
            ["# Input", "ChemicalName", "ChemicalID", "CasRN", "GeneSymbol"]
        ],
        on=["# Input", "ChemicalName", "ChemicalID", "CasRN"],
        how="left",
    )
    merged_cd_pheno_gene.rename(
        columns={"GeneSymbol": "ChemicalGeneSymbol"}, inplace=True
    )
    exportcsv(merged_cd_pheno_gene, "chemical_phenotype_gene_disease")

    # Step 10: Merge disease gene data and compute common genes.
    df_cp = pd.read_csv("chemical_phenotype_gene_disease.csv")
    df_ag = pd.read_csv("aggregated_disease_gene.csv")
    df_ag.rename(columns={"GeneSymbol": "DiseaseGeneSymbol"}, inplace=True)
    merged_final = pd.merge(
        df_cp,
        df_ag[["DiseaseID", "DiseaseGeneSymbol"]],
        on=["DiseaseID"],
        how="left",
    )
    logging.info(f"Shape after merging disease genes: {merged_final.shape}")
    merged_final["common_gene_chemical_disease"] = merged_final.apply(
        find_common_genes, axis=1
    )
    exportcsv(merged_final, "cd_common_gene")

    # Step 11: Extract unique common genes and download gene ontology data.
    extract_unique_and_save(
        pd.read_csv("cd_common_gene.csv"),
        "common_gene_chemical_disease",
        "cd_common_gene_list.txt",
    )
    unique_genes = set()
    with open("cd_common_gene_list.txt", "r") as file:
        for line in file:
            for value in line.strip().split(","):
                if value.strip().lower() != "nan":
                    unique_genes.add(value.strip())
    with open("set_cd_common_gene_list.txt", "w") as file:
        for value in sorted(unique_genes):
            file.write(value + "\n")
    logging.info("Unique common genes saved in set_cd_common_gene_list.txt")
    set_cd_common_gene_list = read_txt_file_to_list("set_cd_common_gene_list.txt")
    ctd_download(
        "gene",
        set_cd_common_gene_list,
        "go",
        "csv",
        "raw_disease_gene_ontology",
        ontology_association="go_bp",
    )

    # Step 12: Process gene ontology data.
    df_raw_go = pd.read_csv("raw_disease_gene_ontology.csv", dtype=str)
    aggregated_go = aggregate_dataframe(
        df_raw_go, ["# Input", "GeneSymbol"], "GoTermID"
    )
    aggregated_go.to_csv("aggregated_disease_gene.csv", index=False)
    df_aggregated_go = pd.read_csv("aggregated_disease_gene.csv")
    logging.info("Aggregated gene ontology data loaded.")
    gene_go_dict = (
        df_aggregated_go.groupby("GeneSymbol")["GoTermID"].apply(list).to_dict()
    )

    # Merge gene ontology into common gene file.
    df_cd_common = pd.read_csv("cd_common_gene.csv")
    df_cd_common["disease_gene_ontology"] = pd.NA
    for index, row in df_cd_common.iterrows():
        if pd.notna(row["common_gene_chemical_disease"]):
            genes = row["common_gene_chemical_disease"].split(",")
            go_terms = set()
            for gene in genes:
                gene = gene.strip()
                if gene in gene_go_dict:
                    go_terms.update(gene_go_dict[gene])
            df_cd_common.at[index, "disease_gene_ontology"] = (
                ", ".join(go_terms) if go_terms else pd.NA
            )
    df_cd_common.to_csv("finaldf.csv", index=False)

    # Step 13: Compute common ontology between phenotype IDs and gene ontology.
    final_df = pd.read_csv("finaldf.csv")
    final_df["common_ontology"] = pd.NA
    for index, row in final_df.iterrows():
        phenotype_ids = (
            str(row["PhenotypeID"]).split(",") if pd.notna(row["PhenotypeID"]) else []
        )
        disease_ontologies = (
            str(row["disease_gene_ontology"]).split(",")
            if pd.notna(row["disease_gene_ontology"])
            else []
        )
        common = list(set(phenotype_ids) & set(disease_ontologies))
        final_df.at[index, "common_ontology"] = ", ".join(common) if common else pd.NA
    final_df.to_csv("complete.csv", index=False)
    logging.info("Final DataFrame saved as complete.csv")
    dataframe_summary(final_df)

    # ---------------------------- Main ----------------------------

    def build_aop_data():
        show_intro()
        chemical_file = get_valid_file_name()
        console.print(f"[bold green]Selected file: {chemical_file}[/bold green]")
        try:
            run_ctd_pipeline(chemical_file)
            console.print(
                "[bold green]CTD data preparation pipeline completed successfully.[/bold green]"
            )
            logging.info("CTD data preparation pipeline completed successfully.")
        except Exception as e:
            logging.exception("An error occurred during the CTD pipeline execution.")


if __name__ == "__main__":
    build_aop_data()
