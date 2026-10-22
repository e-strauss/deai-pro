"""Simple sequential reference runner; scheduling optimizations are the exercise."""

import json
from pathlib import Path
import subprocess
import sys
from time import perf_counter


def main():
    root = Path(__file__).resolve().parent
    output_dir = Path("results")
    manifest = json.loads((root / "trajectory.json").read_text())
    results = []
    for step in manifest["steps"]:
        print(f"Step {step['step']}: {step['name']}", flush=True)
        for candidate in step["pipelines"]:
            pipeline_id = Path(candidate["file"]).stem
            started = perf_counter()
            score = None
            with subprocess.Popen(
                [sys.executable, str(root / candidate["file"])],
                stdout=subprocess.PIPE, text=True,
            ) as process:
                for line in process.stdout:
                    print(line, end="", flush=True)
                    if line.startswith("Final Validation Score: "):
                        score = float(line.split(":", 1)[1])
                returncode = process.wait()
                if returncode:
                    raise subprocess.CalledProcessError(returncode, process.args)
            if score is None:
                raise RuntimeError(f"{pipeline_id} did not report a final validation score")
            results.append({"pipeline_id": pipeline_id,
                            "cv_accuracy": score,
                            "seconds": perf_counter() - started})
    # Stable display order for ties; equal scores still share rank.
    print("-"*60)
    results.sort(key=lambda result: -result["cv_accuracy"])
    previous_score, rank = None, 0
    for position, result in enumerate(results, start=1):
        if result["cv_accuracy"] != previous_score:
            rank = position
        result["rank"] = rank
        previous_score = result["cv_accuracy"]
        print(f"{rank:2d}  {result['pipeline_id']}  {result['cv_accuracy']:.6f}")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
