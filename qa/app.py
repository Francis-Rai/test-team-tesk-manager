import argparse
import subprocess
import pytest
import sys
import os
import shutil
from behave.__main__ import main as behave_main


TEST_PATHS = {"api": "api", "bdd": "bdd/features", "ui": "ui/features"}

COMMANDS = {
    "api": "{test_path} --alluredir={results} --allure-no-capture {args}",
    "bdd": "{test_path} -f allure_behave.formatter:AllureFormatter --outfile={results} {args}",
    "ui": "{test_path} -f allure_behave.formatter:AllureFormatter --outfile={results} {args}",
}

ALLURE_RESULTS = "allure-results"
ALLURE_REPORT = "allure-report"


def clean_folder(folder):
    if os.path.exists(folder):
        print(f"Cleaning folder: {folder}")
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)

def run_command(command, test_type="", ignore_failures=False):
    print(f"Running {test_type} tests with command: {command}\n")

    try:
        if test_type == "api":
            # Split the command into pytest arguments
            # Remove the "pytest" word from template since we'll call pytest.main
            pytest_args = command.split()
            exit_code = pytest.main(pytest_args)
        elif test_type in ["bdd", "ui"]:
            behave_args = command.split()
            exit_code = behave_main(behave_args)
        else:
            result = subprocess.run(
                command,
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            print(result.stdout)

            exit_code = result.returncode

        if exit_code != 0:
            if ignore_failures:
                print(f"Warning: {test_type} tests exited with code {exit_code}, continuing...")
            else:
                print(f"Error: {test_type} tests failed with code {exit_code}")
                sys.exit(exit_code)

    except Exception as e:
        if ignore_failures:
            print(f"Warning: exception running {test_type} tests: {e}")
        else:
            print(f"Error: exception running {test_type} tests: {e}")
            raise


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
        nargs=argparse.REMAINDER,
        default="",
        help="Extra arguments to append to test runner",
    )

    args = parser.parse_args()

    clean_folder(args.output)

    for ttype in args.test_types:
        command = COMMANDS[ttype].format(
            test_path=f"qa/tests/{TEST_PATHS[ttype]}",
            results=args.output,
            args=" ".join(args.additional_args or []),
        )
        run_command(command, test_type=ttype, ignore_failures=True)
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
