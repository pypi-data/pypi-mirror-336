import os
import platformdirs
import pathlib
import configparser
import atexit
import logging

logger = logging.getLogger("Neuroimage_Denoiser_GUI")

class NDenoiser_Settings:
    """ Static class to access the settings """

    config : configparser.ConfigParser = None
    default_settings = {"output_path": ""}
    app_data_path: pathlib.Path = None


    def _CreateStatic():
        NDenoiser_Settings.app_data_path = platformdirs.user_data_path(appname="Neuroimage Denoiser", appauthor=False, roaming=True)
        logger.debug(f"Creating user data dir at {NDenoiser_Settings.app_data_path}")
        NDenoiser_Settings.app_data_path.mkdir(parents=True, exist_ok=True)
        NDenoiser_Settings.config = configparser.ConfigParser()
        NDenoiser_Settings.ReadConfig()
    
    def ReadConfig():
        """ Read the config file and create it if does not exist. Add every value defined in default settings with default value if not already set """
        NDenoiser_Settings.config.read(NDenoiser_Settings.app_data_path / "settings.ini")
        if "SETTINGS" not in NDenoiser_Settings.config.sections():
            NDenoiser_Settings.config.add_section("SETTINGS")
        for k,v in NDenoiser_Settings.default_settings.items():
            if not NDenoiser_Settings.config.has_option("SETTINGS", k):
                NDenoiser_Settings.config.set("SETTINGS", k, v)

        if not (NDenoiser_Settings.app_data_path / "settings.ini").exists():
            NDenoiser_Settings.SaveConfig()

    def GetSettings(key: str) -> str|None:
        if not NDenoiser_Settings.config.has_option("SETTINGS", key):
            return None
        return NDenoiser_Settings.config.get("SETTINGS", key)
    
    def SetSetting(key: str, value: str, save:bool=False):
        NDenoiser_Settings.config.set("SETTINGS", key, str(value))
        if save:
            NDenoiser_Settings.SaveConfig()

    def SaveConfig():
        try:
            with open(NDenoiser_Settings.app_data_path / "settings.ini", 'w') as configfile:
                NDenoiser_Settings.config.write(configfile)
        except Exception as ex:
            logger.warning(f"Failed to save the config. The error message was: {str(ex)}")
    
NDenoiser_Settings._CreateStatic()
atexit.register(NDenoiser_Settings.SaveConfig)