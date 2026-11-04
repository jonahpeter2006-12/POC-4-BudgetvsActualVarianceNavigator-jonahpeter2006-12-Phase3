
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SCRIPTS = [
    "profile_canonical_data.py",
    "assess_representativeness.py",
    "assess_data_quality.py",
    "assess_analytical_readiness.py"
]

OUTPUTS = [
    ROOT / "data-science/outputs/canonical_profile.json",
    ROOT / "data-science/outputs/representativeness_assessment.json",
    ROOT / "data-science/outputs/quality_assessment.json",
    ROOT / "data-science/outputs/analytical_readiness.json"
]

INPUTS = [
    ROOT / "data/canonical/intelligence_data.csv",
    ROOT / "data/source-sample/source_sample.csv",
    ROOT / "data/manifest.json",
    ROOT / "data/schema.json",
    ROOT / "data/quality/validation_report.json"
]


def file_hash(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)

    return digest.hexdigest()


def input_hashes():
    missing_files = [
        str(path.relative_to(ROOT))
        for path in INPUTS
        if not path.is_file()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Required input files are missing: "
            + ", ".join(missing_files)
        )

    return {
        str(path.relative_to(ROOT)): file_hash(path)
        for path in INPUTS
    }

def run_script(script_name):
    script_path = ROOT / "data-science/scripts" / script_name

    print("\nRunning:", script_name)

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT,
        check=True
    )


def run_pipeline():
    for script_name in SCRIPTS:
        run_script(script_name)


def load_outputs():
    results = {}

    for path in OUTPUTS:
        if not path.exists():
            raise FileNotFoundError(
                f"Required output is missing: {path}"
            )

        with path.open("r", encoding="utf-8") as file:
            results[str(path.relative_to(ROOT))] = json.load(file)

    return results


def main():
    print("Starting reproducibility verification.")

    before_hashes = input_hashes()

    if not before_hashes:
        raise RuntimeError("No input files were available for verification.")

    # First complete run.
    print("\n========== RUN 1 ==========")
    run_pipeline()
    first_results = load_outputs()

    # Second complete run.
    print("\n========== RUN 2 ==========")
    run_pipeline()
    second_results = load_outputs()

    outputs_match = first_results == second_results
    after_hashes = input_hashes()
    inputs_unchanged = before_hashes == after_hashes

    if not outputs_match:
        raise RuntimeError(
            "Reproducibility verification failed: "
            "assessment outputs differ between runs."
        )

    if not inputs_unchanged:
        raise RuntimeError(
            "Reproducibility verification failed: "
            "one or more input files changed."
        )

    # Update the reproducibility evidence in the quality report.
    quality_path = OUTPUTS[2]

    with quality_path.open("r", encoding="utf-8") as file:
        quality = json.load(file)

    reproducibility = quality["dimensions"]["reproducibility"]

    reproducibility["status"] = "passed"
    reproducibility["evidence"].update({
        "verification_method": (
            "Two complete pipeline executions with JSON output comparison."
        ),
        "pipeline_runs_completed": 2,
        "assessment_outputs_compared": len(OUTPUTS),
        "assessment_outputs_match": outputs_match,
        "input_files_unchanged": inputs_unchanged,
        "full_pipeline_reproduction_verified": True
    })

    reproducibility["limitation"] = (
        "Verification confirms repeatable execution against the current "
        "local inputs. It does not establish real-world data accuracy."
    )

    quality_path.write_text(
        json.dumps(quality, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    # Rebuild analytical readiness using the verified quality report.
    run_script("assess_analytical_readiness.py")
    readiness_first = load_outputs()[str(OUTPUTS[3].relative_to(ROOT))]

    run_script("assess_analytical_readiness.py")
    readiness_second = load_outputs()[str(OUTPUTS[3].relative_to(ROOT))]

    if readiness_first != readiness_second:
        raise RuntimeError(
            "Final analytical readiness output is not reproducible."
        )

    print("\n========== VERIFICATION RESULT ==========")
    print("Pipeline runs completed: 2")
    print("Assessment outputs compared:", len(OUTPUTS))
    print("Assessment outputs match:", outputs_match)
    print("Input files unchanged:", inputs_unchanged)
    print("Final analytical readiness stable: True")
    print("Reproducibility status: passed")


if __name__ == "__main__":
    main()
