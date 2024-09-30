import configparser
import os
from typing import Sequence
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import library


@library(scope="GLOBAL", version="1.0.0")
class INILibrary:
    """
    INILibrary 

    This library allows you to load and manipulate INI files.

    The library uses Python's built-in configparser library.

    Example:
    | Load INI File | path/to/your/ini/file.ini |
    | Get INI Value | section | key |
    | Get INI Value | section2 | key2 |

    """

    def __init__(self):
        self.config = None
        self.inifile= None

    @keyword("Load INI File")
    def load_INI_file(self, file_path: str, interpolation: str = False):
        """
        Loads the INI file from the specifed path.

        The ``file_path`` is relative to the current working directory.

        Fails If the ``file_path`` does not exist, an error message is logged and the method returns.

        === Mandatory args ===

        - ``file_path`` (str): The path to the INI file relative to the current working directory.

        === Optional args ===

        - ``interpolation`` (str): The interpolation method. The default is ``configparser.Interpolation()``.

        Example usage:
        | Load INI File | path/to/your/ini/file.ini |

        """
        try:
            full_path = os.getcwd()+"/"+file_path
            if not os.path.exists(full_path):
                BuiltIn().log(
                    f'File "{full_path}" not found. Please provide a valid file path.', "ERROR")
                raise FileNotFoundError
            self.config = configparser.ConfigParser(interpolation=configparser.Interpolation(
                            )) if interpolation else configparser.ConfigParser()
            self.config.read(full_path)
            BuiltIn().log(f'Loaded INI file from {full_path}', "INFO")
            self.inifile=file_path
        except FileNotFoundError:
            BuiltIn().log("INI file not loaded. Please load an INI file first.", "ERROR")
            raise FileNotFoundError(f"File does not exists {full_path}")
        except Exception as e:
            raise Exception(e)

    @keyword("Get INI Value")
    def get_INI_value(self, section: str, key: str):
        """
        Gets a value from the INI file.

        Fails if the ``config`` is None or INI File is not loaded.

        Fails if the ``section`` does not exist or if the ``key`` is not present.

        Returns: The value of the ``key`` or None if the ``section`` does not exist or is not present. 

        === Mandatory args ===

        - ``section`` (str): The ``section`` in the INI file.
        - ``key`` (str): The ``key`` in the INI file.

        Example usage:
        | Load INI File | path/to/your/ini/file.ini |
        | Get INI Value | section | key |

        """
        try: 
            if self.config is None:
                BuiltIn().log("INI file not loaded. Please load an INI file first.", "ERROR")
                raise Exception("INI File not loaded")
            if section not in self.config:
                BuiltIn().log(f'section "{section}" not found in the INI file.', "ERROR")
                raise Exception("Section not Found")
            if key not in self.config[section]:
                BuiltIn().log(f'key "{key}" not found in section "{section}".', "ERROR")
                raise Exception("key/option not Found")
            BuiltIn().log(
                f'Value return for section {section} and key {key} is {self.config.get(section, key)}', "INFO")
            return self.config.get(section, key)
        except Exception as e:
            raise Exception(e)
            

    @keyword('Set INI Value')
    def set_INI_value(self, section: str, key: str, value: str):
        """
        Sets a value in the INI file for specified ``section`` and ``key``.

        Fails if the ``config`` is None or INI File is not loaded.

        === Mandatory args ===

        - ``section`` (str): The section to which the following ``key`` and ``value`` to be added in the INI file.
        - ``key`` (str): The ``key`` to add in the INI file.
        - ``value`` (str): The ``value`` to set in the INI file.

        Example usage:
        | Load INI File | path/to/your/ini/file.ini |
        | Set INI Value | section | key | value |
        | Save INI File | path/to/your/ini/file.ini |

        """
        try:
            if self.config is None:
                BuiltIn().log("INI file not loaded. Please load an INI file first.", "ERROR")
                raise Exception("INI File not loaded")
            if section not in self.config:
                self.config.add_section(section)
            self.config.set(section, key, value)
            BuiltIn().log(f'Value set for section {section} and key {key} as {value}', "INFO")
        except Exception as e:
            raise Exception(e)
            

    @keyword("Save INI File")
    def save_INI_file(self, file_path: str=None):
        """
        Saves the INI file.

        Fails if the ``config`` is None or INI File is not loaded.

        === Mandatory args ===

        - ``file_path`` (str): The path to the INI file relative to the current working directory.

        Example usage:
        | Save INI File | path/to/your/ini/file.ini |
        """
        try:
            if self.config is None:
                BuiltIn().log("INI file not loaded. Please load an INI file first.", "ERROR")
                raise Exception("INI File not loaded")
            if file_path is None:
                with open(os.getcwd()+"/"+self.inifile, 'w') as configfile:
                    self.config.write(configfile)
                    BuiltIn().log(f'INI file saved to {os.getcwd()+"/"+self.inifile}', "INFO")
            else:
                with open(os.getcwd()+"/"+file_path, 'w') as configfile:
                    self.config.write(configfile)
                    BuiltIn().log(f'INI file saved to {os.getcwd()+"/"+file_path}', "INFO")
        except Exception as e:
            raise Exception(e)

    @keyword("Remove Section")
    def remove_section(self, section: str):
        """
        Removes the specified ``section`` from the INI file.

        Fails if the ``config`` is None or INI File is not loaded.

        Fails if the ``section`` does not exist.

        === Mandatory args ===

        - ``section`` (str): The ``section`` in the INI file.

        Example usage:
        | Load INI File | path/to/your/ini/file.ini |
        | Remove Section | section |
        | Save INI File | path/to/your/ini/file.ini |
        """
        try:
            if self.config is None:
                BuiltIn().log("INI file not loaded. Please load an INI file first.", "ERROR")
                raise Exception("INI File not loaded")
            if section not in self.config:
                BuiltIn().log(f'Section "{section}" not found in the INI file.', "ERROR")
                raise Exception('Section not found')
            self.config.remove_section(section)
            BuiltIn().log(f'Removed section "{section}"', "INFO")
        except Exception as e:
            raise Exception(e)
            

    @keyword('Remove INI Key')
    def remove_INI_key(self, section: str, key: str):
        """
        Removes a ``key`` from the specified ``section`` in the INI file.

        Fails if the ``config`` is None or INI File is not loaded.

        Fails if the ``section`` does not exist or if the ``key`` is not present.

        === Mandatory Args ===

        - ``section`` (str): The ``section`` in the INI file.
        - ``key`` (str): The ``key`` in the INI file.

        Example usage:
        | Load INI File | path/to/your/ini/file.ini |
        | Remove INI Key | section | key |
        | Save INI File | path/to/your/ini/file.ini |

        """
        try:
            if self.config is None:
                BuiltIn().log("INI file not loaded. Please load an INI file first.", "ERROR")
                raise Exception("INI File not loaded")
            if section not in self.config:
                BuiltIn().log(f'Section "{section}" not found in the INI file.', "ERROR")
                raise Exception('Section not found')
            if key not in self.config[section]:
                BuiltIn().log(f'key "{key}" not found in section "{section}".', "ERROR")
                raise Exception("Key not found")
            self.config.remove_option(section, key)
            BuiltIn().log(f'Removed key "{key}" from section "{section}"', "INFO")
        except Exception as e:
            raise Exception(e)
            

    @keyword("Get All Keys And Values")
    def get_all_keys_and_values(self, section: str):
        """
        Gets all keys and values under the specified ``section``.

        Fails if the ``config`` is None or INI File is not loaded.

        Returns: A dictionary with the keys and values or None if the ``section`` does not exist.

        === Mandatory Args ===

        - ``section`` (str): The ``section`` in the INI file.

        Example usage:
        | Load INI File | path/to/your/ini/file.ini |
        | ${dict}= | Get All Keys And Values | section |
        """
        try:
            if self.config is None:
                BuiltIn().log("INI file not loaded. Please load an INI file first.", "ERROR")
                raise Exception("INI File not loaded")
            if section not in self.config:
                BuiltIn().log(f'Section "{section}" not found in the INI file.', "ERROR")
                raise Exception('Section not found')
            BuiltIn().log(f'Fetched all the Keys and Values "str({dict(self.config.items(section))})"', "INFO")
            return dict(self.config.items(section))
        except Exception as e:
            raise Exception(e)
            

    @keyword("Get Values List")
    def get_values_list(self, section: str, key: str):
        """
        Gets a list of values for all matching ``key`` under a specified ``section`` in the INI file.

        Fails if the ``config`` is None or INI File is not loaded.

        Fails if the ``section`` does not exist.

        Returns: A list of values or an empty list if the ``section`` or ``key`` does not exist.

        Returns: An empty list if the length of ``section`` items is zero.

        === Mandatory Args ===

        - ``section`` (str): The ``section`` in the INI file.
        - ``key`` (str): The ``key`` in the INI file.

        Example usage:
        | Load INI File | path/to/your/ini/file.ini |
        | ${list}= | Get Values List | section | key |

        """
        values = []
        try:
            if self.config is None:
                BuiltIn().log("INI file not loaded. Please load an INI file first.", "ERROR")
                raise Exception("INI File not loaded")
            if section not in self.config:
                BuiltIn().log(f'section "{section}" not found in the INI file.', "ERROR")
                raise Exception('Section not found')
            if len(self.config.items(section)) == 0:
                BuiltIn().log(f'section "{section}". no keys present', "ERROR")
                raise Exception('Atleast one pair of key-value should exist')
            for akey, value in self.config.items(section):
                if akey == key:
                    values.append(value)
            if len(values)==0:
                BuiltIn().log(f'No matching keys "{key}" under section "{section}"', "INFO")
                return values
            BuiltIn().log(f'Fetched all the values for key "{key}" under section "{section}" are {values}', "INFO")
            return values
        except Exception as e:
            Exception(e)
            
    @keyword("Section Exists")
    def section_exists(self, section: str):
        """
        Checks if the specified ``section`` exists in the INI file.

        Fails if the ``config`` is None or INI File is not loaded.

        Returns: True if the ``section`` exists and None if the Exception occurs, False If ``section`` does not exists.

        === Mandatory Args ===

        - ``section`` (str): The ``section`` in the INI file.

        Example usage:
        | Load INI File | path/to/your/ini/file.ini |
        | ${bool}= | Section Exists | section |

        """
        try:
            if self.config is None:
                BuiltIn().log("INI file not loaded. Please load an INI file first.", "ERROR")
                raise Exception("INI File not loaded")
            BuiltIn().log(
                f'Section "{section}" exists in the INI file', "INFO")
            return self.config.has_section(section)
        except Exception as e:
            raise Exception(e)
            

    @keyword("Key Exists")
    def key_exists(self, section: str, key: str):
        """
        Checks if the specified ``key`` exists in the specified ``section`` in the INI file.

        Fails if the ``config`` is None or INI File is not loaded.

        Fails if the specified ``section`` does not exist.

        Returns: True if the ``key`` exists, False otherwise.

        === Mandatory Args ===

        - ``section`` (str): The ``section`` in the INI file.

        Example usage:
        | Load INI File | path/to/your/ini/file.ini |
        | ${bool}= | Key Exists | section | key |

        """
        try:
            if self.config is None:
                BuiltIn().log("INI file not loaded. Please load an INI file first.", "ERROR")
                raise Exception("INI File not loaded")
            if section not in self.config:
                BuiltIn().log(f'section "{section}" not found in the INI file.', "ERROR")
                raise Exception('Section not found')
            BuiltIn().log(f'key "{key}" exists in section "{section}" is {self.config.has_option(section, key)}', "INFO")
            return self.config.has_option(section, key)
        except Exception as e:
            raise Exception(e)
           
