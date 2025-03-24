import csv
import glob
import logging
import os
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.DataStructs import TanimotoSimilarity
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from tqdm import tqdm

# Initialize console
console = Console()
# Load environment variables
load_dotenv()

# Constants
BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/assay/pcget.cgi?query=download&record_type=datatable&actvty=all&response_type=save&aid={}"
REQUIRED_COLUMNS = [
    "PUBCHEM_CID",
    "PUBCHEM_EXT_DATASOURCE_SMILES",
    "PUBCHEM_ACTIVITY_OUTCOME",
]
RETRIES = 3
TIMEOUT = 10
LOG_FILE = "tox_assay.log"
DEBUG = False


# Setup logging
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


# Introduction message
def show_intro():
    console.clear()
    text = Text()
    text.append("Bioassay Data Preparation Tool form ML model\n\n", style="bold cyan")
    text.append("Created by: Deepak Kumar Sachan\n", style="bold white")
    text.append("Supervisor: Dr. R. Parthasarathi\n", style="bold white")
    text.append(
        "Institution: CSIR - Indian Institute of Toxicology Research\n",
        style="bold white",
    )
    text.append(
        "\nThis tool will collect bioassay data and prepare it for machine learning model development.\n",
        style="bold green",
    )
    text.append(
        "\nPlease create a file named 'AssayDictionary.csv' containing your data IDs, followed by a list of bioassays in each row.(eg. <id>,<bioassay id 1>,<bioassay is 2>...\n",
        style="bold red",
    )

    panel = Panel(
        text, title="Welcome", title_align="left", border_style="bright_yellow"
    )
    console.print(panel)


def read_assay_dictionary(file_name):
    file_path = Path.cwd() / file_name
    dict_of_lists = {}
    try:
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                key = row[0]
                values = row[1:]
                dict_of_lists[key] = values
        logger.info(f"Successfully read assay dictionary from {file_name}")
    except Exception as e:
        logger.error(f"Failed to read assay dictionary from {file_name}: {e}")
    return dict_of_lists


def fetch_assay_data(aid, output_file):
    for attempt in range(RETRIES):
        try:
            response = requests.get(BASE_URL.format(aid), timeout=TIMEOUT)
            if response.status_code == 200:
                with open(output_file, "w") as file:
                    file.write(response.text)
                logger.info(f"Assay data for AID {aid} saved to {output_file}")
                return True
            else:
                logger.warning(
                    f"Failed to retrieve assay data for AID {
                        aid}. Status code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt + 1} for AID {aid} failed with error: {e}")
            time.sleep(2)
    return False


def fetch_multiple_assays(aid_list, root_dir):
    for aid in aid_list:
        try:
            assay_output_dir = Path(root_dir) / f"AID_{aid}"
            if assay_output_dir.exists():
                shutil.rmtree(assay_output_dir)
            assay_output_dir.mkdir(parents=True)
            output_file = assay_output_dir / f"rawdata_{aid}.csv"
            if fetch_assay_data(aid, output_file):
                logger.info(f"Successfully fetched data for AID {aid}")
            else:
                logger.warning(
                    f"Failed to fetch data for AID {
                        aid} after multiple attempts"
                )
        except Exception as e:
            logger.error(f"Error fetching multiple assays for AID {aid}: {e}")
        time.sleep(0.2)


def get_standardize_smiles(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            return rdMolStandardize.StandardizeSmiles(
                Chem.MolToSmiles(mol, isomericSmiles=False)
            )
    except Exception as e:
        logger.error(f"Error standardizing SMILES {smiles}: {e}")
    return None


def compare_smiles(smiles, standardized_smiles):
    return smiles != standardized_smiles


def process_assay_data(aid, file_path, output_dir):
    try:
        df = pd.read_csv(file_path, low_memory=False)
        if all(col in df.columns for col in REQUIRED_COLUMNS):
            df = df[REQUIRED_COLUMNS].dropna()
            df["PUBCHEM_CID"] = df["PUBCHEM_CID"].astype(int)

            failed_standardizations = []

            def try_standardize(row):
                smiles = row["PUBCHEM_EXT_DATASOURCE_SMILES"]
                pubchem_cid = row["PUBCHEM_CID"]
                standardized_smiles = get_standardize_smiles(smiles)
                if standardized_smiles is None:
                    failed_standardizations.append(pubchem_cid)
                return standardized_smiles

            df["STANDARDIZED_SMILES"] = df.apply(try_standardize, axis=1)

            failed_file = Path(output_dir) / f"failed_standardize_smiles_{aid}.txt"
            with failed_file.open("w") as f:
                for cid in failed_standardizations:
                    f.write(f"{cid}\n")
            logger.info(f"Failed standardizations for AID {aid} saved to {failed_file}")

            df.dropna(subset=["STANDARDIZED_SMILES"], inplace=True)
            df["IS_STANDARDIZED"] = df.apply(
                lambda row: compare_smiles(
                    row["PUBCHEM_EXT_DATASOURCE_SMILES"], row["STANDARDIZED_SMILES"]
                ),
                axis=1,
            )

            df = df[["PUBCHEM_CID", "STANDARDIZED_SMILES", "PUBCHEM_ACTIVITY_OUTCOME"]]
            df = df[df["PUBCHEM_ACTIVITY_OUTCOME"].isin(["Active", "Inactive"])]

            output_file = Path(output_dir) / f"cleaned_data_{aid}.csv"
            df.to_csv(output_file, index=False)
            logger.info(f"Processed data for AID {aid} saved to {output_file}")
        else:
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            logger.warning(f"Missing columns in AID {aid} data: {missing_cols}")
    except Exception as e:
        logger.error(f"Error processing assay data for AID {aid}: {e}")


def fetch_and_process_assays(dict_of_lists):
    for root_dir, aid_list in dict_of_lists.items():
        Path(root_dir).mkdir(parents=True, exist_ok=True)
        fetch_multiple_assays(aid_list, root_dir)
        for aid in aid_list:
            try:
                assay_output_dir = Path(root_dir) / f"AID_{aid}"
                process_assay_data(
                    aid,
                    assay_output_dir / f"rawdata_{aid}.csv",
                    assay_output_dir,
                )
            except Exception as e:
                logger.error(f"Error processing assays for AID {aid}: {e}")


def get_cleaned_data(aid, root_dir):
    file_path = Path(root_dir) / f"AID_{aid}" / f"cleaned_data_{aid}.csv"
    if file_path.exists():
        return pd.read_csv(file_path)
    else:
        logger.error(f"File not found: {file_path}")
        return None


def process_assay(aid, root_dir):
    try:
        df = get_cleaned_data(aid, root_dir)
        if df is None:
            return

        logger.info(f"AID {aid}: Total rows = {df.shape[0]}")

        df["PUBCHEM_CID"] = df["PUBCHEM_CID"].astype(int)
        df["Molecule"] = df["STANDARDIZED_SMILES"].apply(Chem.MolFromSmiles)
        df["Fingerprint"] = df["Molecule"].apply(
            lambda mol: (
                AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
                if mol is not None
                else None
            )
        )

        df = df.dropna(subset=["Molecule", "Fingerprint"])
        active_df = df[df["PUBCHEM_ACTIVITY_OUTCOME"] == "Active"]
        inactive_df = df[df["PUBCHEM_ACTIVITY_OUTCOME"] == "Inactive"]

        logger.info(f"AID {aid}: Active compounds count = {active_df.shape[0]}")
        logger.info(f"AID {aid}: Inactive compounds count = {inactive_df.shape[0]}")

        results = []
        not_selected_active = []
        not_selected_inactive = inactive_df.copy()
        used_inactive_indices = set()

        for idx, active_row in active_df.iterrows():
            active_fp = active_row["Fingerprint"]
            similarities = inactive_df["Fingerprint"].apply(
                lambda x: TanimotoSimilarity(active_fp, x)
            )

            similarities = similarities[~similarities.index.isin(used_inactive_indices)]

            if not similarities.empty and similarities.max() > 0:
                most_similar_idx = similarities.idxmax()
                most_similar_inactive = inactive_df.loc[most_similar_idx]
                used_inactive_indices.add(most_similar_idx)

                results.append(
                    {
                        "Active_PUBCHEM_CID": active_row["PUBCHEM_CID"],
                        "Active_SMILES": active_row["STANDARDIZED_SMILES"],
                        "Active_PUBCHEM_ACTIVITY_OUTCOME": active_row[
                            "PUBCHEM_ACTIVITY_OUTCOME"
                        ],
                        "Inactive_PUBCHEM_CID": most_similar_inactive["PUBCHEM_CID"],
                        "Inactive_SMILES": most_similar_inactive["STANDARDIZED_SMILES"],
                        "Inactive_PUBCHEM_ACTIVITY_OUTCOME": most_similar_inactive[
                            "PUBCHEM_ACTIVITY_OUTCOME"
                        ],
                        "Similarity": similarities[most_similar_idx],
                    }
                )

                not_selected_inactive = not_selected_inactive.drop(most_similar_idx)
            else:
                results.append(
                    {
                        "Active_PUBCHEM_CID": active_row["PUBCHEM_CID"],
                        "Active_SMILES": active_row["STANDARDIZED_SMILES"],
                        "Active_PUBCHEM_ACTIVITY_OUTCOME": active_row[
                            "PUBCHEM_ACTIVITY_OUTCOME"
                        ],
                        "Inactive_PUBCHEM_CID": None,
                        "Inactive_SMILES": None,
                        "Inactive_PUBCHEM_ACTIVITY_OUTCOME": None,
                        "Similarity": None,
                    }
                )
                not_selected_active.append(
                    {
                        "PUBCHEM_CID": active_row["PUBCHEM_CID"],
                        "STANDARDIZED_SMILES": active_row["STANDARDIZED_SMILES"],
                        "PUBCHEM_ACTIVITY_OUTCOME": active_row[
                            "PUBCHEM_ACTIVITY_OUTCOME"
                        ],
                    }
                )

        results_df = pd.DataFrame(results)
        not_selected_active_df = pd.DataFrame(not_selected_active)
        not_selected_inactive_df = not_selected_inactive

        results_df["Inactive_PUBCHEM_CID"] = results_df["Inactive_PUBCHEM_CID"].astype(
            pd.Int64Dtype()
        )

        final_results_df = pd.concat(
            [
                results_df[
                    [
                        "Active_PUBCHEM_CID",
                        "Active_SMILES",
                        "Active_PUBCHEM_ACTIVITY_OUTCOME",
                    ]
                ].rename(
                    columns={
                        "Active_PUBCHEM_CID": "PUBCHEM_CID",
                        "Active_SMILES": "STANDARDIZED_SMILES",
                        "Active_PUBCHEM_ACTIVITY_OUTCOME": "PUBCHEM_ACTIVITY_OUTCOME",
                    }
                ),
                results_df[
                    [
                        "Inactive_PUBCHEM_CID",
                        "Inactive_SMILES",
                        "Inactive_PUBCHEM_ACTIVITY_OUTCOME",
                    ]
                ]
                .dropna()
                .rename(
                    columns={
                        "Inactive_PUBCHEM_CID": "PUBCHEM_CID",
                        "Inactive_SMILES": "STANDARDIZED_SMILES",
                        "Inactive_PUBCHEM_ACTIVITY_OUTCOME": "PUBCHEM_ACTIVITY_OUTCOME",
                    }
                ),
            ]
        )

        final_results_df = final_results_df.drop_duplicates().reset_index(drop=True)

        assay_output_dir = Path(root_dir) / f"AID_{aid}"
        assay_output_dir.mkdir(parents=True, exist_ok=True)

        results_df.to_csv(
            assay_output_dir / f"most_similar_inactive_compounds_{aid}.csv",
            index=False,
        )
        not_selected_active_df.to_csv(
            assay_output_dir / f"not_selected_active_compounds_{aid}.csv",
            index=False,
        )
        not_selected_inactive_df.to_csv(
            assay_output_dir / f"not_selected_inactive_compounds_{aid}.csv",
            index=False,
        )
        final_results_df.to_csv(
            assay_output_dir / f"SmilesForMl_{aid}.csv", index=False
        )
    except Exception as e:
        logger.error(f"Error processing assay for AID {aid}: {e}")


def process_all_assays(dict_of_lists):
    for root_dir, aid_list in dict_of_lists.items():
        Path(root_dir).mkdir(parents=True, exist_ok=True)
        for aid in aid_list:
            try:
                process_assay(aid, root_dir)
            except Exception as e:
                logger.error(f"Error processing all assays for AID {aid}: {e}")


def get_mol_descriptors(smiles, missing_val=None):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        try:
            descriptors = {desc[0]: desc[1](mol) for desc in Descriptors._descList}
            return descriptors
        except Exception as e:
            logger.error(
                f"Error calculating descriptors for SMILES: {
                    smiles}, Error: {e}"
            )
            return {desc[0]: missing_val for desc in Descriptors._descList}
    else:
        logger.warning(f"Invalid SMILES: {smiles}")
        return {desc[0]: missing_val for desc in Descriptors._descList}


def process_aid_descriptors(aid, root_dir):
    try:
        df = get_cleaned_data(aid, root_dir)
        if df is None:
            return

        logger.info(f"Processing AID {aid} in {root_dir} with {len(df)} records.")

        descriptor_dicts = []
        failed_indices = []

        for idx, smiles in tqdm(enumerate(df["STANDARDIZED_SMILES"]), total=len(df)):
            descriptors = get_mol_descriptors(smiles)
            descriptor_dicts.append(descriptors)
            if all(val is None for val in descriptors.values()):
                failed_indices.append(idx)

        descriptors_df = pd.DataFrame(descriptor_dicts)
        descriptors_df.index = df.index
        df_with_descriptors = pd.concat([df, descriptors_df], axis=1)

        output_file = Path(root_dir) / f"AID_{aid}" / f"raw_descriptors_{aid}.csv"
        df_with_descriptors.to_csv(output_file, index=False)
        logger.info(f"Descriptors saved to {output_file}")

        if failed_indices:
            failed_df = df.iloc[failed_indices]
            failed_file = (
                Path(root_dir) / f"AID_{aid}" / f"raw_failed_descriptors_{aid}.csv"
            )
            failed_df.to_csv(failed_file, index=False)
            logger.info(f"Failed descriptors saved to {failed_file}")
    except Exception as e:
        logger.error(f"Error processing descriptors for AID {aid}: {e}")


def process_all_aids_descriptors(dict_of_lists):
    for root_dir, aid_list in dict_of_lists.items():
        Path(root_dir).mkdir(parents=True, exist_ok=True)
        for aid in aid_list:
            try:
                process_aid_descriptors(aid, root_dir)
            except Exception as e:
                logger.error(f"Error processing all descriptors for AID {aid}: {e}")


def calculate_fingerprint(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        fingerprint = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
        return fingerprint.ToBitString()
    else:
        return None


def process_aid_fingerprints(aid, root_dir):
    try:
        df = get_cleaned_data(aid, root_dir)
        if df is None:
            return

        logger.info(f"Processing AID {aid} with {len(df)} records.")

        fingerprint_list = []
        failed_indices = []

        for idx, smiles in tqdm(enumerate(df["STANDARDIZED_SMILES"]), total=len(df)):
            fingerprint = calculate_fingerprint(smiles)
            fingerprint_list.append(fingerprint)
            if fingerprint is None:
                failed_indices.append(idx)

        fingerprints_df = pd.DataFrame(fingerprint_list, columns=["MorganFingerprint"])
        fingerprints_df.index = df.index
        df_with_fingerprints = pd.concat([df, fingerprints_df], axis=1)

        output_file = (
            Path(root_dir) / f"AID_{aid}" / f"raw_morgan_fingerprints_{aid}.csv"
        )
        df_with_fingerprints.to_csv(output_file, index=False)
        logger.info(f"Morgan fingerprints saved to {output_file}")

        if failed_indices:
            failed_df = df.iloc[failed_indices]
            failed_file = (
                Path(root_dir) / f"AID_{aid}" / f"failed_morgan_fingerprints_{aid}.csv"
            )
            failed_df.to_csv(failed_file, index=False)
            logger.info(f"Failed fingerprints saved to {failed_file}")
    except Exception as e:
        logger.error(f"Error processing fingerprints for AID {aid}: {e}")


def process_all_aids_fingerprints(dict_of_lists):
    for root_dir, aid_list in dict_of_lists.items():
        Path(root_dir).mkdir(parents=True, exist_ok=True)
        for aid in aid_list:
            try:
                process_aid_fingerprints(aid, root_dir)
            except Exception as e:
                logger.error(f"Error processing all fingerprints for AID {aid}: {e}")


def merge_smiles_files(dict_of_lists):
    for root_dir, aid_list in dict_of_lists.items():
        Path(root_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Merging files for {root_dir}")
        all_files = []
        for aid in aid_list:
            file_path = Path(root_dir) / f"AID_{aid}" / f"SmilesForMl_{aid}.csv"
            if file_path.exists():
                all_files.append(pd.read_csv(file_path))
            else:
                logger.error(f"File not found: {file_path}")
        if all_files:
            merged_df = pd.concat(all_files, ignore_index=True)
            output_file = Path(root_dir) / f"SmilesForMl_{root_dir}.csv"
            merged_df.to_csv(output_file, index=False)
            logger.info(f"Merged file saved to {output_file}")
        else:
            logger.error(f"No files found for {root_dir}")


def merge_descriptor_files(dict_of_lists):
    for root_dir, aid_list in dict_of_lists.items():
        Path(root_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Merging files for {root_dir}")
        all_files = []
        for aid in aid_list:
            file_path = Path(root_dir) / f"AID_{aid}" / f"raw_descriptors_{aid}.csv"
            if file_path.exists():
                all_files.append(pd.read_csv(file_path))
            else:
                logger.error(f"File not found: {file_path}")
        if all_files:
            merged_df = pd.concat(all_files, ignore_index=True)
            output_file = Path(root_dir) / f"raw_descriptors_{root_dir}.csv"
            merged_df.to_csv(output_file, index=False)
            logger.info(f"Merged file saved to {output_file}")
        else:
            logger.error(f"No files found for {root_dir}")


def copy_and_rename_files(dict_of_lists, file_patterns, timeout_seconds=300):
    start_time = datetime.now()
    ml_data_dir = Path("MlData").resolve()
    ml_data_dir.mkdir(parents=True, exist_ok=True)

    for root_dir, aid_list in dict_of_lists.items():
        for pattern in file_patterns:
            search_pattern = str(Path(root_dir) / pattern.format(root_dir=root_dir))
            files = glob.glob(search_pattern)
            if not files:
                logger.error(f"No files found for pattern: {search_pattern}")
            for file_path in files:
                if (datetime.now() - start_time).seconds > timeout_seconds:
                    logger.error("Process timed out.")
                    return
                try:
                    dest_filename = Path(file_path).name.replace(
                        "raw_descriptors_", "data_"
                    )
                    dest_path = ml_data_dir / dest_filename
                    shutil.copy(file_path, dest_path)
                    logger.info(f"Copied {file_path} to {dest_path}")
                except Exception as e:
                    logger.error(f"Failed to copy {file_path} to {dest_path}: {e}")


def create_comparative_table(directory):
    file_info_list = []

    for filename in Path(directory).iterdir():
        if filename.is_file() and filename.suffix == ".csv":
            df = pd.read_csv(filename)

            # Statistics before removing duplicates
            total_entries_before = len(df)
            active_count_before = df[df["PUBCHEM_ACTIVITY_OUTCOME"] == "Active"].shape[
                0
            ]
            inactive_count_before = df[
                df["PUBCHEM_ACTIVITY_OUTCOME"] == "Inactive"
            ].shape[0]

            # Remove duplicates
            df_no_duplicates = df.drop_duplicates(subset=["PUBCHEM_CID"])
            new_file_path = Path(directory) / f"No_duplicates_{filename.name}"
            df_no_duplicates.to_csv(new_file_path, index=False)
            logger.info(f"File without duplicates saved at {new_file_path}")

            # Statistics after removing duplicates
            total_entries_after = len(df_no_duplicates)
            active_count_after = df_no_duplicates[
                df_no_duplicates["PUBCHEM_ACTIVITY_OUTCOME"] == "Active"
            ].shape[0]
            inactive_count_after = df_no_duplicates[
                df_no_duplicates["PUBCHEM_ACTIVITY_OUTCOME"] == "Inactive"
            ].shape[0]
            duplicate_count = total_entries_before - total_entries_after
            unique_count = df_no_duplicates["PUBCHEM_CID"].nunique()

            file_info = {
                "Filename": filename.name,
                "Total Entries Before": total_entries_before,
                "Active Before": active_count_before,
                "Inactive Before": inactive_count_before,
                "Total Entries After": total_entries_after,
                "Active After": active_count_after,
                "Inactive After": inactive_count_after,
                "Duplicate Count": duplicate_count,
                "Unique Count": unique_count,
            }
            file_info_list.append(file_info)

    df_summary = pd.DataFrame(file_info_list)
    output_csv = Path(directory) / "comparative_table.csv"
    df_summary.to_csv(output_csv, index=False)
    logger.info(f"Comparative table created at {output_csv}")
    return df_summary


# List .csv files in the directory
def list_files_in_directory(directory, extension=".csv"):
    return [
        f.name
        for f in Path(directory).iterdir()
        if f.is_file() and f.suffix == extension
    ]


# Get a valid file name from the user
# Get a valid file name from the user
def get_valid_file_name():
    files = list_files_in_directory(Path.cwd())
    logger.info("Available .csv files:")
    for file in files:
        logger.info(file)
    while True:
        input_file = input("Please enter the input file name (with extension): ")
        if input_file in files:
            return input_file
        else:
            logger.warning(f"File '{input_file}' not found. Please try again.")
            console.print(f"[bold red]File '{input_file}' not found. Please try again.")
            logger.info("Available .csv files:")
            for file in files:
                logger.info(file)


def run_bioassay_data_prep_pipeline():
    show_intro()
    try:
        # Get a valid input file name from the user
        valid_file = get_valid_file_name()
        print(f"Selected file: {valid_file}")

        # Use the valid_file variable
        assay_dict = read_assay_dictionary(valid_file)
        fetch_and_process_assays(assay_dict)
        process_all_assays(assay_dict)
        process_all_aids_descriptors(assay_dict)
        process_all_aids_fingerprints(assay_dict)
        merge_smiles_files(assay_dict)
        merge_descriptor_files(assay_dict)
        file_patterns = ["raw_descriptors_{root_dir}.csv"]
        copy_and_rename_files(assay_dict, file_patterns)
        ml_data_dir = Path("./MlData").resolve()
        create_comparative_table(ml_data_dir)
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    run_bioassay_data_prep_pipeline()
    console.print("Bioassay data preparation pipeline completed successfully.")
    logger.info("Bioassay data preparation pipeline completed successfully.")
