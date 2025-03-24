# toxichempy/_env_check.py

import os
import sys
import warnings


def check_environment():
    required_python = (3, 12)
    current_python = sys.version_info[:2]
    in_conda = "CONDA_PREFIX" in os.environ
    suppress = os.getenv("TOXICHEMPY_SUPPRESS_ENV_WARNING")

    if suppress:
        return  # Advanced user opt-out

    warning_needed = False
    msg = ["\n⚠️  Environment Warning for `toxichempy`:"]

    if not in_conda:
        msg.append("❌ You are not in a Conda environment.")
        warning_needed = True

    if current_python != required_python:
        msg.append(
            f"❌ You are using Python {current_python[0]}.{current_python[1]} — expected Python 3.12."
        )
        warning_needed = True

    if warning_needed:
        msg += [
            "",
            "✅ Recommended setup:",
            "   conda create -n toxichempy-env -c conda-forge python=3.12 rdkit openbabel python-dotenv pip",
            "   conda activate toxichempy-env",
            "   pip install toxichempy",
            "",
            "📘 Docs: https://toxichempy.readthedocs.io/en/latest/installation/",
            "💡 Suppress this warning with:",
            "   export TOXICHEMPY_SUPPRESS_ENV_WARNING=1",
        ]
        warnings.warn("\n".join(msg), category=UserWarning)
