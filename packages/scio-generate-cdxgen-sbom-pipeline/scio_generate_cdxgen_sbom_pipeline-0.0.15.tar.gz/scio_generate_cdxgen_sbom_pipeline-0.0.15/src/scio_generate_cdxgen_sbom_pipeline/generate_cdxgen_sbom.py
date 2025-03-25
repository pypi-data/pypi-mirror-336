import logging
import os
import re
import subprocess
import traceback
from pathlib import Path

from django.conf import settings

from scanpipe.pipelines import Pipeline
from scanpipe.pipes.input import copy_inputs

logger = logging.getLogger("scanpipe.pipes")
NPM_CONFIG_PREFIX = "/opt/scancodeio/etc/thirdparty/node_modules"
CDXGEN_BIN = "/opt/scancodeio/etc/thirdparty/node_modules/.bin/cdxgen"
ENV = {
    "PATH": os.environ["PATH"],
    "HOME": os.environ["HOME"],
    "GOPRIVATE": settings.GO_PRIVATE,
    "CDXGEN_DEBUG_MODE": "debug",
    "NPM_CONFIG_PREFIX": NPM_CONFIG_PREFIX,
    "CDXGEN_PLUGINS_DIR": NPM_CONFIG_PREFIX + "/@cyclonedx/cdxgen-plugins-bin/plugins/",
    "MVN_CMD": "/root/.sdkman/candidates/maven/3.9.8/bin/mvn",
    "JAVA_HOME": "/root/.sdkman/candidates/java/current",
}


def get_java_version_from_gradle(project_dir: Path):
    if not os.path.exists(f"{project_dir}/gradlew"):
        return None

    try:
        properties = subprocess_run(
            ["./gradlew", "properties", "-q", "--no-daemon", "--console=plain"],
            cwd=project_dir,
        ).stdout
    except Exception:
        return
    for property in properties.split("\n"):
        key, _, value = property.partition(": ")
        if key == "sourceCompatibility":
            return value


def get_base_image(dockerfile: Path):
    with open(dockerfile) as df:
        lines = df.readlines()
        for line in lines:
            if line.startswith("FROM"):
                _, _, base_image = line.partition("FROM")
                return base_image.strip()


def guess_java_version_by_base_image(base_image: str):
    match = re.search("(jre|jdk).*?([0-9]+)", base_image)
    if not match:
        return None
    version = match.group(2)
    return version


def get_java_version_by_base_image(base_image: str):
    base_image, _, _ = base_image.partition(":")
    version = settings.BASE_IMAGE_JAVA_VERSION_MAPPING.get(base_image)
    if not version:
        version = guess_java_version_by_base_image(base_image)
        if version:
            logger.warning(
                f"Guessing java version: {version} from base image: {base_image}"
            )
    if not version:
        return None
    return version


def get_java_env(base_image, repo_dir):
    java_version = None
    if base_image:
        java_version = get_java_version_by_base_image(base_image)

    if not java_version:
        java_version = get_java_version_from_gradle(repo_dir)

    if java_version:
        java_env = {
            "JAVA_HOME": settings.JAVA_HOME[java_version],
            "PATH": f"{os.environ['PATH']}:{settings.JAVA_HOME[java_version]}/bin",
        }
        logger.info(f"Detected java: {java_version}")
        return java_env

    return {}


def get_env(repo_dir):
    logger.info("[*] Trying to set proper environemnt")
    base_image = None
    try:
        base_image = get_base_image(repo_dir / "Dockerfile")
    except FileNotFoundError:
        with open("no-dockerfile", "a") as f:
            f.write(f"No docker image for: {repo_dir}\n")

    ENV.update(get_java_env(base_image=base_image, repo_dir=repo_dir))
    ENV.update({"PIP_CONFIG_FILE": str(repo_dir / "pip.conf")})
    return ENV


def subprocess_run(args, **kwargs):
    logger.info(f"[+] Executing sub_process: {args}")
    try:
        stats = subprocess.run(
            args=args,
            shell=False,
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
            **kwargs,
        )
        if stats.stderr:
            logger.debug(f"[+] Got Error from subprocess: {stats.stderr}")
        logger.info(f"[+] Got Out from subprocess: {stats.stdout}")
        return stats
    except subprocess.CalledProcessError as e:
        print("Error occurred while executing the subprocess command:")
        traceback.print_exc()
        print(f"Command: {e.cmd}")
        print(f"Return Code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error Output: {e.stderr}")
        return e


class GenerateCdxgenSbom(Pipeline):
    """
    Generate CycloneDX Software Bill of Materials (SBOM) using cdxgen
    """
    is_zip = False
    repo_dir = ""
    
    @classmethod
    def steps(cls):
        return (
            cls.clear_output,
            cls.copy_inputs_to_codebase_directory,
            cls.extract_archives,
            cls.run_cdxgen_scan,
            cls.move_sbom_to_input,
            cls.clear_repo,
            cls.call_load_sbom,
        )

    def clear_output(self):
        """
        Remove the output directory if it exists
        """
        logger.info("[*] Running clear_output")
        if self.project.output_path.exists():
            subprocess_run(["rm", "-rf", self.project.output_path])
        self.project.output_path.mkdir(parents=True, exist_ok=True)
        
    def copy_inputs_to_codebase_directory(self):
        """
        Copy input files to the project's codebase/ directory.
        The code can also be copied there prior to running the Pipeline.
        """
        if self.project.input_sources[0]["filename"].endswith(".zip"):
            self.is_zip = True
        copy_inputs(self.project.inputs("*"), self.project.codebase_path)

    def run_cdxgen_scan(self):
        """
        Return generated cdx filename after scanning given repo_dir
        """
        
        logger.info("[*] Running run_cdxgen_scan")
        output_filename = "output.cdx.json"
        repo_name = self.project.input_sources[0]["filename"].replace(".zip", "")
        self.repo_dir = self.project.codebase_path / repo_name
        if self.is_zip:
            extracted_folder = self.project.codebase_path / Path(str(self.project.input_sources[0]["filename"])+"-extract")
            self.repo_dir = self.project.codebase_path / extracted_folder / repo_name
            logger.info(f"[*] CWD in use: {self.repo_dir}")
        command = [
            CDXGEN_BIN,
            self.repo_dir,
            "--spec-version",
            "1.4",
            "-o",
            output_filename,
        ]
        env = get_env(self.repo_dir)
        subprocess_run(command, env=env, cwd=self.project.output_path)

    def move_sbom_to_input(self):
        """
        Move the generated sbom to the input directory
        """
        logger.info("[*] Running move_sbom_to_input")
        output_filename = "output.cdx.json"
        output_path = self.project.output_path / output_filename
        input_path = self.project.input_path / output_filename
        output_path.rename(input_path)

    def clear_repo(self):
        """
        Remove the repository after the sbom is generated
        """
        logger.info(f"[*] Running clear_repo on {self.repo_dir}")
        if self.repo_dir.exists():
            subprocess_run(["rm", "-rf", str(self.repo_dir)])
    
    def call_load_sbom(self):
        """
        Call the load sbom pipeline
        """
        logger.info("[*] Running call_load_sbom")
        self.project.add_pipeline("load_sbom")
