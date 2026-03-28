import argparse
import subprocess
import sys
import os
import shutil


TEST_PATHS = {"api": "api", "bdd": "bdd/features"}

COMMANDS = {
    "api": "pytest {test_path} --alluredir={results} --allure-no-capture {args}",
    "bdd": "behave {test_path} -f allure_behave.formatter:AllureFormatter --outfile={results} {args}",
}

ALLURE_RESULTS = "allure-results"
ALLURE_REPORT = "allure-report"


def clean_folder(folder):
    if os.path.exists(folder):
        print(f"Cleaning folder: {folder}")
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)

def run_command(command, ignore_failures):
    """Run a shell command and stream output."""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    # Stream output live
    for line in process.stdout:
        print(line.decode(), end="")
    process.wait()

    if process.returncode != 0:
        if ignore_failures:
            print(f"Warning: command exited with code {process.returncode}, continuing...")
        else:
            print(f"Error: command failed with code {process.returncode}")
            sys.exit(process.returncode)

def main():
    parser = argparse.ArgumentParser(description="Run Automated Tests")

    parser.add_argument(
        "--test-types",
        type=str,
        nargs='+',  # One or more values
        choices=["ui", "api", "bdd"],
        required=True,
        help="Type of test to run (ui, api, bdd)",
    )

    parser.add_argument(
        "--output",
        default=ALLURE_RESULTS,
        help="Output folder for Allure results",
    )

    parser.add_argument(
        "--history-limit",
        default=5,
        help="Maximum number of history tests",
    )

    parser.add_argument(
        "--port",
        default="8081",
        help="Port to serve allure report",
    )

    parser.add_argument(
        "--serve", action="store_true", help="Serve Allure report after run"
    )

    parser.add_argument(
        "--additional-args",
        type=str,
        default="",
        help="Extra arguments to append to test runner",
    )

    args = parser.parse_args()

    clean_folder(args.output)

    for ttype in args.test_types:
        command = COMMANDS[ttype].format(
            test_path=f"qa/tests/{TEST_PATHS[ttype]}",
            results=args.output,
            args=args.additional_args,
        )
        run_command(command, ignore_failures=True)
    clean_folder(ALLURE_REPORT)
    run_command(
        f"allure generate {args.output} -o {ALLURE_REPORT} --history-limit={args.history_limit}",
        ignore_failures=False,
    )

    if args.serve:
        run_command(
            f"allure serve {ALLURE_REPORT} --port {args.port}", ignore_failures=False
        )

if __name__ == "__main__":
    main()
