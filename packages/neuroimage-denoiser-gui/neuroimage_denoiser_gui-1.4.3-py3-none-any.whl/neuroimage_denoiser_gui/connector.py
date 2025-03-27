import importlib.util
from tkinter import messagebox
import os
import re
import subprocess
import threading
import pathlib
from typing import IO
import logging
import sys
import importlib
logger = logging.getLogger("Neuroimage_Denoiser_GUI")

from .utils import *
from .config import NDenoiser_Settings as Settings

class Connector:

    thread: threading.Thread | None = None
    currentSubprocess: subprocess.CompletedProcess = None
    _threadStopRequest = False

    def ImportNDenoiser() -> bool:
        logger.info(f"Detected environment used: {os.environ['CONDA_DEFAULT_ENV'] if 'CONDA_DEFAULT_ENV' in os.environ.keys() else ''}")
        if importlib.util.find_spec("neuroimage_denoiser") is None:
            logger.critical(f"Importlib can't find the Neuroimage Denoiser module. Terminating the program")
            messagebox.showerror("Neuroimage Denoiser GUI", "Can't find the Neuroimage Denoiser module. Terminating")
            exit()
        return True
    
    def TestInstallation():
        def _run():
            logger.info("--- Testing installation. This may take some seconds ---")
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(["python", "-c", "import os; print(os.environ['CONDA_DEFAULT_ENV'] if 'CONDA_DEFAULT_ENV' in os.environ.keys() else '')"], env=env, capture_output=True, encoding="utf-8")
            if len(result.stderr) > 0:
                logger.error("Testing the environment threw an error: \n---\n%s\n---" % result.stderr)
                return
            elif (env_import := result.stdout.removesuffix("\n").strip()) == (env_gui := (os.environ['CONDA_DEFAULT_ENV'] if 'CONDA_DEFAULT_ENV' in os.environ.keys() else None)):
                logger.debug(f"The environment ('{env_gui}') is the same")
            else:
                logger.info(f"The environment differs between the GUI ('{env_gui}') and the Denoiser ('{env_import}'). This may be correct depending on your installation")
            
            result = subprocess.run(["python", "-m", "neuroimage_denoiser"], env=env, capture_output=True, encoding="utf-8")
            re1 = re.search(r"(Neuroimage Denoiser)", result.stdout)
            re2 = re.search(r"(positional arguments)", result.stdout)
            if len(result.stderr) > 0:
                logger.error("Trying to import Neuro Image Denoiser threw an error: \n---\n%s\n---" % result.stderr)
                return
            elif not(re1 and re2):
                logger.error("Neuroimage Denoiser was found, but it prompted an unexpected message: \n---\n%s\n---" % result.stdout)
                return
            else:
                logger.info("Neuroimage Denoiser was found and seems to be working")

            logger.info(f"Testing Torch and CUDA")

            result = subprocess.run(["python", "-c", "import torch; print(torch.cuda.is_available())"], env=env, capture_output=True, encoding="utf-8")
            if len(result.stderr) > 0:
                logger.error("Testing for CUDA in torch threw an error: \n---\n%s\n---" % result.stderr)
                return
            elif (rs := result.stdout.removesuffix("\n").strip()) not in ["True", "False"]:
                logger.error("Torch was found, but it prompted an unexpected message: \n---\n%s\n---" % result.stdout)
                return
            elif rs != "True":
                logger.warning(f"Torch is ready, but does not use CUDA. The Denoiser will therefore fall back to CPU. It is not recommended to proceed, as this may increase runtime by magnitudes")

            logger.info("CUDA is ready for use")
            logger.info("--- Finished testing the installation ---") 

        t = threading.Thread(target=_run, daemon=True)
        t.start()

    def CudaFix():
        def _run():
            args = "python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --upgrade"
            logger.info("--- Installing CUDA fix. This may take several minutes. Please wait until you see a success message ---")
            logger.debug(args)
            result = subprocess.run(args.split(" "), env=os.environ.copy(), capture_output=True)
            if len(result.stderr) > 0:
                logger.error("Installing the CUDA fix threw an error: \n---\n%s\n---" % result.stderr.decode('utf-8'))
            logger.debug("Output of the PIP command for installing CUDA fix: \n---\n%s\n---" % result.stdout.decode('utf-8'))
            logger.info("---Finished installing CUDA fix---")

        t = threading.Thread(target=_run, daemon=True)
        t.start()


    def Denoise(fileQueue:FileQueue, outputPath: pathlib.Path, invalidateQueueCallback):
        if outputPath is None or not outputPath.exists() or len(str(outputPath)) <= 3:
            logger.warning("Your output path is invalid")
            return
        if not (model_path := (Settings.app_data_path / "model.pt")).exists() or not model_path.is_file():
            logger.warning(f"You first need to import a model. If you did, check if it is copied into users AppData folder")
            return
        def _run():
            if (fileQueue.PopQueued() is None):
                logger.info("There are no files in the queue")
                return
            logger.info("---Starting Denoising---")
            while (fileQueue.PopQueued() is not None):
                if Connector._threadStopRequest:
                    logger.warning("You aborted denoising")
                    break
                qf = fileQueue.PopQueued()
                qf.status = FileStatus.RUNNING
                logger.info(f"Denoising {qf.filename}")
                invalidateQueueCallback()
                if isinstance(qf, QueuedFile):
                    params = ["python", "-m", "neuroimage_denoiser", "denoise", "--path", '"' + str(qf.path) + '"', "--outputpath", '"' + str(outputPath) + '"', "--modelpath", '"' + str(model_path) + '"']
                elif isinstance(qf, QueuedFolder):
                    params = ["python", "-m", "neuroimage_denoiser", "denoise", "--path", '"' + str(qf.path) + '"', "--outputpath", '"' + str(outputPath) + '"', "--modelpath", '"' + str(model_path)+ '"', "--directory_mode"]
                else:
                    raise RuntimeError("A provided Queued Object has an invalid type")
                logger.debug(f"Running subprocess with the following args: {' '.join(params)}")

                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "utf-8" # Alive progress in Stephans code needs utf-8. By default, python uses the wrong encoding. Setting the encoding in subprocess Popen only enables a conversion afterwards
                Connector.currentSubprocess = subprocess.Popen(params, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", bufsize=-1)
                Connector.currentSubprocess.wait()
                Connector.ND_ProcessOutput(Connector.currentSubprocess.returncode, Connector.currentSubprocess.stdout, Connector.currentSubprocess.stderr, qf)
                logger.info(f"Finished {qf.filename}")
                invalidateQueueCallback()
            logger.info("---Finished Denoising---")
        Connector._threadStopRequest = False
        if Connector.Is_Denoising(): return
        Connector.thread = threading.Thread(target=_run, daemon=True)
        Connector.thread.start()

    def Is_Denoising():
        if Connector.thread is not None and Connector.thread.is_alive():
            return True
        return False
    
    def ND_ProcessOutput(returncode, stdout: IO[str], stderr: IO[str], qf: QueuedObject):
        if stdout is None or stdout == "None":
            qf.status = FileStatus.ERROR
            return
        if stderr is None or stderr == "None":
            qf.status = FileStatus.ERROR
            return
        status = []

        known_error_lines = {"FutureWarning: You are using `torch.load` with `weights_only=False`": "Future Warning on Torch", "torch.load(weights": "Future Warning on Torch"}
        stderr_known_errors = []
        stderr_unknown_lines = []
        while (line := stderr.readline().removesuffix("\n").strip()) != "":
            for error_str,error_name in known_error_lines:
                if error_str in line:
                    stderr_known_errors.append(error_name)
                    break
            else:
                stderr_unknown_lines.append(line)

        for error_name in stderr_known_errors:
            match error_name:
                case "Future Warning on Torch":
                    logger.info(f"Neuroimage Denoiser issued a FutureWarning on torch")
                case _:
                    logger.info(f"There was an exception in the Denoiser output ('{error_name}'), but it is marked as not disturbing")
        if len(stderr_unknown_lines) > 0:
            logger.warning("There have been errors produced by Neuroimage Denoiser: \n---\n%s\n---" % '\n'.join(stderr_unknown_lines))

        stdout_unknown_lines = []
        while (line := stdout.readline().removesuffix("\n").strip()) != "":
            re1 = re.search(r"on ([0-9]{1,3}): Skipped (.+), because file already exists", line)
            re2 = re.search(r"on ([0-9]{1,3}): Skipped (.+), due to an unexpected error", line)
            re3 = re.search(r"on ([0-9]{1,3}): Saved image \(([^\)]+)\) as:", line)
            if re1:
                status.append(FileStatus.ERROR_FILE_EXISTS)
                logger.warning(f"[Denoiser] Skipped {re1.groups(1)}, as the output file already exists")
            elif re2:
                status.append(FileStatus.ERROR_NDENOISER_UNKOWN)
                logger.warning(f"[Denoiser] Unkown error on {re1.groups(1)}")
            elif re3:
                status.append(FileStatus.FINISHED)
            elif(re.search(r"\| [0-9]{0,3}\/[0-9]{0,3} \[[0-9]{1,3}\%\] in ", line)):
                status.append(FileStatus.FINISHED)
            else:
                stdout_unknown_lines.append(line)
        
        if len(stdout_unknown_lines) > 0:
            logger.warning("There is unparsed output produced by Neuroimage Denoiser: \n---\n%s\n---" % '\n'.join(stdout_unknown_lines))

        qf.status = FileStatus.Get_MostSignificant(status)
        if (qf.status == None):
            if returncode == 1:
                qf.status = FileStatus.EARLY_TERMINATED
            else:
                qf.status = FileStatus.NO_OUTPUT
    
    def TryCanceling():
        Connector._threadStopRequest = True
        _sp_running = False
        if Connector.currentSubprocess is not None and Connector.currentSubprocess.poll() is None:
            _sp_running = True
            Connector.currentSubprocess.terminate()
        if not _sp_running and (Connector.thread is None or not Connector.thread.is_alive()): 
            logger.info("There is no denoising running")
        else:
            logger.warning("Canceled denoising")