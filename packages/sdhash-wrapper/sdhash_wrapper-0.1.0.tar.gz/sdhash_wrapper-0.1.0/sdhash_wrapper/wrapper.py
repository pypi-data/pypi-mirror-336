import subprocess
import os

class SDHash:
    def __init__(self):
        """Use the locally installed sdhash binary."""
        self.sdhash_path = os.path.join(os.path.dirname(__file__), "sdhash")
        if not os.path.exists(self.sdhash_path):
            raise FileNotFoundError("SDhash binary is missing. Reinstall the package.")

    def run(self, args):
        """Run sdhash with given arguments and return output."""
        try:
            result = subprocess.run(
                [self.sdhash_path] + args,
                check=True, capture_output=True, text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"

    def generate(self, file_path):
        """Generate an SDBF hash for a given file."""
        return self.run(["-r", file_path])

    def compare(self, file1, file2):
        """Compare two SDBF hash files."""
        return self.run(["-c", file1, file2])

    def validate(self, sdbf_file):
        """Validate an SDBF file."""
        return self.run(["--validate", sdbf_file])
