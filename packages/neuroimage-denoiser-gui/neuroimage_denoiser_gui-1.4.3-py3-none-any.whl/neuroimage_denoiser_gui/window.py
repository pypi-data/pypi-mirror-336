import logging.handlers
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pathlib
import psutil
import gpustat
import subprocess
from datetime import datetime
import shutil
import platform
import os

import logging
logger = logging.getLogger("Neuroimage_Denoiser_GUI")

from .utils import *
from .connector import Connector
from .config import NDenoiser_Settings as Settings


class NDenoiser_GUI:

    def __init__(self):
        self.gpu_error = None # If a query for the GPU fails, only log the first message
        self.gpu_stats = None # The first GPU request is logged

        self.queueFiles = FileQueue()
        self.InitGUI()

    def InitGUI(self):
        self.root = tk.Tk()
        self.root.iconbitmap(default=pathlib.Path(__file__).parent / "icon.ico")
        self.root.title("Neuroimage Denoiser GUI")
        self.root.geometry("900x600")
        

        self.frameStatusbar = tk.Frame(self.root)
        self.frameStatusbar.pack(side=tk.BOTTOM, fill="x")
        self.lblStatusCPU = tk.Label(self.frameStatusbar, text="")
        self.lblStatusCPU.grid(row=0, column=0)
        self.lblStatusRAM = tk.Label(self.frameStatusbar, text="")
        self.lblStatusRAM.grid(row=0, column=1)
        self.lblStatusGPU = tk.Label(self.frameStatusbar, text="")
        self.lblStatusGPU.grid(row=0, column=2)
        self.lblStatusGPU2 = tk.Label(self.frameStatusbar, text="")
        self.lblStatusGPU2.grid(row=0, column=3)
        self.lblStatusGPU3 = tk.Label(self.frameStatusbar, text="")
        self.lblStatusGPU3.grid(row=0, column=4)
        self.frameStatusbar.columnconfigure((0,1,2,3,4), weight=1)

        self.txtLog = scrolledtext.ScrolledText(self.root, height=10)
        self.txtLog.configure(state='disabled')
        self.txtLog.pack(side=tk.BOTTOM, fill="x")
        self.txtLoggingHandler = LoggingHandlerTxt(self.txtLog)
        self.txtLoggingHandler.setLevel(logging.INFO)
        logger.addHandler(self.txtLoggingHandler)

        Connector.ImportNDenoiser()

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.menuFile = tk.Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.menuFile)
        self.menuFile.add_command(label="Open File(s)", command=self.MenuFile_OpenFile)
        self.menuFile.add_command(label="Open Folder", command=self.MenuFile_OpenFolder)
        self.menuFile.add_command(label="Select Output Folder", command=self.MenuFile_SelectOutputFolder)
        self.menuFile.add_command(label="Open Output Folder", command=self.MenuFile_OpenOutputFolder)
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Remove selected file from list", command=self.MenuFile_RemoveSelected)

        self.menuDenoiser = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Neuroimage Denoiser", menu=self.menuDenoiser)
        self.menuDenoiser.add_command(label="Test Installation", command=self.MenuDenoiser_TestInstallation)
        self.menuDenoiser.add_command(label="Install CUDA Fix", command=self.MenuDenoiser_CUDAFix)
        self.menuDenoiser.add_command(label="Import Model", command=self.MenuDenoiser_ImportModel)
        self.menuDenoiser.add_separator()
        self.menuDenoiser.add_command(label="Denoise", command=self.MenuDenoiser_Denoise)
        self.menuDenoiser.add_command(label="Cancel Denoising", command=self.MenuDenoiser_Cancel)

        self.menuAbout = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="About", menu=self.menuAbout)
        self.menuAbout.add_command(label="Info", command=self.MenuAbout_Info)
        self.menuAbout.add_command(label="Start debugging", command=self.MenuAbout_Debug)
        self.menuAbout.add_command(label="Open logs", command=self.MenuAbout_OpenLog)

        self.frameTools = tk.Frame(self.root)
        self.frameTools.pack(side=tk.TOP, fill="x")
        self.frameTools.grid_columnconfigure(1, weight=1)
        self.frameToolsLeft = tk.Frame(self.frameTools)
        self.frameToolsLeft.grid(row=0, column=0)
        self.frameToolsInner = tk.Frame(self.frameTools)
        self.frameToolsInner.grid(row=0, column=1)
        self.frameToolsRight = tk.Frame(self.frameTools)
        self.frameToolsRight.grid(row=0, column=2, sticky="ne")

        self.framePaths = tk.Frame(self.frameTools)
        self.framePaths.grid(row=1, column=0, columnspan=3, sticky="news")
        self.framePaths.columnconfigure(3, weight=1)
        self.btnImportModel = tk.Button(self.framePaths, text="Import Model", command=self.MenuDenoiser_ImportModel)
        self.btnImportModel.grid(row=0, column=0)
        self.varModelName = tk.StringVar(self.root, Settings.GetSettings("model_name") if Settings.GetSettings("model_name") is not None else "")
        self.txtModelName = tk.Entry(self.framePaths, state="disabled", textvariable=self.varModelName, width=30)
        self.txtModelName.bind("<Button-1>", lambda _:self.MenuDenoiser_ImportModel())
        self.txtModelName.grid(row=0,column=1, sticky="news")

        self.varTxtOutputPath = tk.StringVar(self.root, Settings.GetSettings("output_path"))
        self.txtOutputPath = tk.Entry(self.framePaths, state="disabled", textvariable=self.varTxtOutputPath)
        self.txtOutputPath.bind("<Button-1>", lambda _:self.MenuFile_OpenOutputFolder())
        self.txtOutputPath.grid(row=0,column=3, sticky="news")
        self.btnSelectPath = tk.Button(self.framePaths, text="Select Output Path", command=self.MenuFile_SelectOutputFolder)
        self.btnSelectPath.grid(row=0, column=2)

        self.btnOpenFiles = tk.Button(self.frameToolsInner, text="📗 Open File(s)", command=self.MenuFile_OpenFile)
        self.btnOpenFiles.pack(side=tk.LEFT, padx=15)
        self.btnOpenFolder = tk.Button(self.frameToolsInner, text="📁 Open Folder", command=self.MenuFile_OpenFolder)
        self.btnOpenFolder.pack(side=tk.LEFT, padx=15)
        self.btnRemoveSelected = tk.Button(self.frameToolsInner, text="Remove selected file", command=self.MenuFile_RemoveSelected)
        self.btnRemoveSelected.pack(side=tk.LEFT, padx=15)
        self.btnDenoise = tk.Button(self.frameToolsInner, text="Start Denoising", command=self.MenuDenoiser_Denoise)
        self.btnDenoise.pack(side=tk.LEFT, padx=15)
        self.btnCancel = tk.Button(self.frameToolsInner, text="Cancel Denoising", command=self.MenuDenoiser_Cancel)
        self.btnCancel.pack(side=tk.LEFT,padx=15)


        self.tvFiles = ttk.Treeview(self.root, columns=("Status", "Path", "Name"))
        self.tvFiles.heading("#0", text="")
        self.tvFiles.heading("Status", text="Status")
        self.tvFiles.heading("Path", text="Path")
        self.tvFiles.heading("Name", text="Name")
        self.tvFiles.column("#0", width=40, stretch=False)
        self.tvFiles.column("Status", width=200, stretch=False)
        self.tvFiles.tag_configure('', background = '#ededed')
        self.tvFiles.tag_configure('grey', background = '#c4c4c4')
        self.tvFiles.tag_configure('red', background = '#e38686')
        self.tvFiles.tag_configure('green', background = '#8adba0')
        self.tvFiles.tag_configure('light_orange', background = '#f2c377')
        self.tvFiles.pack(fill="both", expand=True)

        logger.info("Started Neuroimage Denoiser GUI")
        self.UpdateTVFiles()
        self._Statusbar_Tick()
        self.root.mainloop()

    def _Statusbar_Tick(self):
        def _printGPUStats(gpu_stats: gpustat.GPUStatCollection):
            if self.gpu_stats is None:
                self.gpu_stats = gpu_stats
                logger.debug(f"Nvidia driver {gpu_stats.driver_version} ({gpu_stats.hostname})")
                for i, g in enumerate(gpu_stats.gpus):
                    logger.debug(f"GPU {i}: {g.name} ({g.power_limit}W, {g.memory_total}MB)")
            self.lblStatusGPU["text"] = f"Nvidia driver {gpu_stats.driver_version}"
            self.lblStatusGPU2["text"] = ""
            self.lblStatusGPU3["text"] = ""
            if len(gpu_stats.gpus) == 0:
                return
            if len(gpu_stats.gpus) >= 1:
                g: gpustat.GPUStat = gpu_stats.gpus[0] 
                self.lblStatusGPU2["text"] = f"{g.name}: {g.utilization}% {g.temperature}°C {g.power_draw}W"
            if len(gpu_stats.gpus) >= 2:
                g: gpustat.GPUStat = gpu_stats.gpus[1]
                self.lblStatusGPU3["text"] = f"{g.name}: {g.utilization}% {g.temperature}°C {g.power_draw}W"
        self.lblStatusCPU["text"] = f"CPU: {psutil.cpu_percent(interval=None)}%"
        self.lblStatusRAM["text"] = f"Memory: {psutil.virtual_memory().percent}%"
        try:
            gpu_stats = gpustat.GPUStatCollection.new_query()
            _printGPUStats(gpu_stats)
        except Exception as ex:
            self.lblStatusGPU["text"] = "GPU: Not available"
            self.lblStatusGPU2["text"] = ""
            self.lblStatusGPU3["text"] = ""
            if self.gpu_error is None:
                self.gpu_error = ex
                logger.debug(f"Failed to query the GPU stats. The error was:\n---\n%s\n---" % str(ex))
        self.root.after(1000, self._Statusbar_Tick)

    def UpdateTVFiles(self):
        _files = [x for x in self.queueFiles.keys()]
        for qfIndex in self.tvFiles.get_children():
            entryValues = self.tvFiles.item(qfIndex)["values"]
            if not qfIndex in _files:
                self.tvFiles.delete(qfIndex)
                continue
            _files.remove(qfIndex)
            qf: QueuedObject = self.queueFiles[qfIndex]
            if entryValues[0] != qf.status.value:
                self.tvFiles.item(qf.id, tags=[FileStatus.Get_Color(qf.status)])
                self.tvFiles.set(qf.id, column="Status", value=qf.status.value)
        for qfIndex in _files:
            qf = self.queueFiles[qfIndex]
            if isinstance(qf, QueuedFile):
                text = "🖻"
            elif isinstance(qf, QueuedFolder):
                text = "📁"
            else:
                text = ""
            self.tvFiles.insert('', 'end', iid=qf.id, text=text, values=(qf.status.value, qf.basepath, qf.filename), tags=[FileStatus.Get_Color(qf.status)])

    def MenuFile_OpenFile(self):
        files = filedialog.askopenfilenames(parent=self.root, title="Neuroimage Denoiser - Open a file", 
                filetypes=(("All compatible files", "*.tif *.tiff *.stk *.nd2"), 
                           ("TIF File", "*.tif *.tiff *.stk"), 
                           ("ND2 Files (NIS Elements)", "*.nd2"), 
                           ("All files", "*.*")) )
        if files is None or files == "":
            return
        for path in files:
            qf = QueuedFile(path)
            self.queueFiles[qf.id] = qf
        self.UpdateTVFiles()

    def MenuFile_OpenFolder(self):
        path = filedialog.askdirectory(parent=self.root, title="Neuroimage Denoiser - Open a folder")
        if path is None or path == "":
            return
        qf = QueuedFolder(path)
        self.queueFiles[qf.id] = qf
        self.UpdateTVFiles()
        

    def MenuFile_SelectOutputFolder(self):
        path = filedialog.askdirectory(parent=self.root, title="Neuroimage Denoiser - Select output path")
        if path is None or path == "":
            return
        Settings.SetSetting("output_path", path, save=True)
        self.varTxtOutputPath.set(path)
        logger.info(f"Set output path to {path}")
        

    def MenuFile_OpenOutputFolder(self):
        path = Settings.GetSettings("output_path")
        if path is None or path == "":
            messagebox.showwarning("Neuroimage Denoiser", "You must first set an output path")
            return
        path = pathlib.Path(path)
        if not path.exists():
            messagebox.showerror("Neuroimage Denoiser", "The path is invalid")
            return
        if platform.system() == 'Darwin': # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows': # Windows
            os.startfile(path)
        else: # linux variants
            subprocess.call(('xdg-open', path))

    def MenuFile_RemoveSelected(self):
        if len(self.tvFiles.selection()) != 1:
            self.root.bell()
            return
        selectionIndex = self.tvFiles.selection()[0]
        qf = self.queueFiles[selectionIndex]
        if qf.status == FileStatus.RUNNING:
            messagebox.showinfo("Neuroimage Denoiser", "Can't remove running items from the list")
            return
        logger.debug(f"Removing {selectionIndex}")
        self.queueFiles.remove(selectionIndex)
        self.UpdateTVFiles()

    def MenuDenoiser_TestInstallation(self):
        Connector.TestInstallation()

    def MenuDenoiser_CUDAFix(self):
        if messagebox.askokcancel("Neuroimage Denoiser GUI", "Do you really want to install the CUDA drivers for torch? You need this to use a NVIDIA GPU, but on other systems this may crash your installation. Do you want to continue?"):
            Connector.CudaFix()

    def MenuDenoiser_Cancel(self):
        Connector.TryCanceling()
    
    def MenuDenoiser_ImportModel(self):
        file = filedialog.askopenfilename(parent=self.root, title="Neuroimage Denoiser - Select the model", 
                filetypes=(("Pytorch model", "*.pt"),  
                           ("All files", "*.*")) )
        if file is None or file == "":
            return
        file = pathlib.Path(file)
        shutil.copy(file, Settings.app_data_path / ("model" + file.suffix))
        Settings.SetSetting("model_name", file.name, save=True)
        self.varModelName.set(file.name)
        logger.info(f"Imported model '{file.name}' into the application. As there is a copy of this file cached, you don't need to keep the file anymore")

    def MenuDenoiser_Denoise(self):
        outputpath = self.varTxtOutputPath.get()
        if outputpath is None or outputpath == "":
            self.root.bell()
            logger.error("Please first set an output path")
            return
        Connector.Denoise(self.queueFiles, pathlib.Path(outputpath), self.UpdateTVFiles)

    def MenuAbout_Info(self):
        messagebox.showinfo("Neuroimage Denoiser", "Neuroimage Denoiser for removing noise from transient fluorescent signals in functional imaging\nStephan Weissbach, Jonas Milkovits, Michela Borghi, Carolina Amaral, Abderazzaq El Khallouqi, Susanne Gerber, Martin Heine bioRxiv 2024.06.08.598061; doi: https://doi.org/10.1101/2024.06.08.598061\n\nGUI Implementation by Andreas Brilka")

    def MenuAbout_Debug(self):
        if(not messagebox.askyesnocancel("Neuroimage Denoiser", "Are you sure you want to enable debugging mode?")):
            return
        self.txtLoggingHandler.setLevel(logging.DEBUG)
        logger.debug("Enabled debugging output")

    def MenuAbout_OpenLog(self):
        path = Settings.app_data_path / "log.txt"
        if platform.system() == 'Darwin': # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows': # Windows
            os.startfile(path)
        else: # linux variants
            subprocess.call(('xdg-open', path))


class LoggingHandlerTxt(logging.Handler):
    """ Add a handler to capture the logs into a textbox """

    def __init__(self, txt_log: scrolledtext.ScrolledText):
        self.txt_log = txt_log
        self.txt_log.tag_config('prefix', foreground='#3d6cd1')
        self.txt_log.tag_config('error', foreground='#c73030')
        self.txt_log.tag_config('darkgrey', foreground='#595959')
        super().__init__()

    def handle(self, record):
        scrollDown = True if (self.txt_log.yview()[1] > 0.8) else False
        tag = ""
        if record.levelno >= logging.WARNING:
            tag = "error"
        elif record.levelno < logging.INFO:
            tag = "darkgrey" 
        self.txt_log.configure(state='normal')
        self.txt_log.insert(tk.END, f"{datetime.now().strftime('[%x %X]:')} ", "prefix")
        self.txt_log.insert(tk.END, f"{record.msg}\n", tag)
        self.txt_log.configure(state='disabled')
        if scrollDown:
            self.txt_log.see(tk.END)
        return True