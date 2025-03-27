import sys,os
if __name__ == "__main__":
    path = os.path.join(os.path.join(__file__, os.pardir), os.pardir)
    path = os.path.abspath(path)
    sys.path.insert(1, path)

import neuroimage_denoiser_gui
gui = neuroimage_denoiser_gui.NDenoiser_GUI()