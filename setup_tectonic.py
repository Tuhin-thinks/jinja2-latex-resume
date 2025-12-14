import os
import subprocess

IS_UNIX = os.name == "posix"


def check_tectonic_installed():
    try:
        tectonic_path = get_tectonic_exe_path()
        subprocess.run(
            [tectonic_path, "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_tectonic_exe_path():
    if IS_UNIX:
        return "./tectonic"
    else:
        return "tectonic.exe"


def download_tectonic_unix():
    download_command = [
        "curl",
        "--proto",
        "=https",
        "--tlsv1.2",
        "-fsSL",
        "https://drop-sh.fullyjustified.net",
        "|",
        "sh",
    ]
    # this will raise an exception if the command fails
    runner_process = subprocess.run(" ".join(download_command), shell=True, check=True)
    runner_process.check_returncode()
    # Verify installation
    if not check_tectonic_installed():
        # show error message
        _err_msg = (
            (runner_process.stdout.decode() + "\n" + runner_process.stderr.decode())
            if runner_process.stderr
            else "Unknown error"
        )
        print(f"Error: {_err_msg}.", flush=True)
        raise RuntimeError("Tectonic installation failed.")


def download_tectonic_windows():
    command_1 = "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072"
    command_2 = "iex ((New-Object System.Net.WebClient).DownloadString('https://drop-ps1.fullyjustified.net'))"
    full_command = f"{command_1}; {command_2}"
    # this will raise an exception if the command fails
    runner_process = subprocess.run(
        ["powershell", "-Command", full_command],
        check=True,
    )
    runner_process.check_returncode()
    # Verify installation
    if not check_tectonic_installed():
        # show error message
        _err_msg = (
            (runner_process.stdout.decode() + "\n" + runner_process.stderr.decode())
            if runner_process.stderr
            else "Unknown error"
        )
        print(f"Error: {_err_msg}.", flush=True)
        raise RuntimeError("Tectonic installation failed.")


def setup_tectonic():
    if check_tectonic_installed():
        print("Tectonic is already installed.")
        return

    import platform

    system = platform.system()
    try:
        if system == "Windows":
            print("Downloading Tectonic for Windows...")
            download_tectonic_windows()
        else:
            print("Downloading Tectonic for Unix-like OS...")
            download_tectonic_unix()
        print("Tectonic installation completed successfully.")
    except Exception as e:
        print(f"An error occurred during Tectonic installation: {e}")
        raise


if __name__ == "__main__":
    setup_tectonic()
