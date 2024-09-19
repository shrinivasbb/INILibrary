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
        full_path = os.getcwd()+"/"+file_path
        if not os.path.exists(full_path):
            BuiltIn().log(
                f'File "{full_path}" not found. Please provide a valid file path.', "ERROR")
            return
        self.config = configparser.ConfigParser(interpolation=configparser.Interpolation(
                        )) if interpolation else configparser.ConfigParser()
        self.config.read(full_path)
        BuiltIn().log(f'Loaded INI file from {full_path}', "INFO")

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
                return None
            if section not in self.config:
                BuiltIn().log(
                    f'section "{section}" not found in the INI file.', "ERROR")
                return None
            if key not in self.config[section]:
                BuiltIn().log(
                    f'key "{key}" not found in section "{section}".', "ERROR")
                return None
        except:
            BuiltIn().log(f'An error occurred while retrieving the value.', "ERROR")
            return None
        finally:
            BuiltIn().log(
                f'Value return for section {section} and key {key} is {self.config.get(section, key)}', "INFO")
            return self.config.get(section, key)

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
                return None
            if section not in self.config:
                self.config.add_section(section)
            self.config.set(section, key, value)
        except:
            BuiltIn().log(f'An error occurred while Setting the value.', "ERROR")
            return
        finally:
            BuiltIn().log(
                f'Value set for section {section} and key {key} as {value}', "INFO")

    @keyword("Save INI File")
    def save_INI_file(self, file_path: str):
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
                BuiltIn().log("INI file not loaded. Cannot save to file.", "ERROR")
                return
            with open(os.getcwd()+"/"+file_path, 'w') as configfile:
                self.config.write(configfile)
            BuiltIn().log(
                f'INI file saved to {os.getcwd()+"/"+file_path}', "INFO")
        except Exception as e:
            BuiltIn().log(
                f'An error occurred while Saving the file. {e}', "ERROR")
            return
        finally:
            BuiltIn().log(
                f'Saved INI file to {os.getcwd()+"/"+file_path}', "INFO")

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
                return
            if section not in self.config:
                BuiltIn().log(
                    f'Section "{section}" not found in the INI file.', "ERROR")
                return
            self.config.remove_section(section)
        except Exception as e:
            BuiltIn().log(
                f'An error occurred while removing the section {e}.', "ERROR")
            return
        finally:
            BuiltIn().log(f'Removed section "{section}"', "INFO")

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
                return
            if section not in self.config:
                BuiltIn().log(
                    f'Section "{section}" not found in the INI file.', "ERROR")
                return
            if key not in self.config[section]:
                BuiltIn().log(
                    f'key "{key}" not found in section "{section}".', "ERROR")
                return
            self.config.remove_option(section, key)
        except Exception as e:
            BuiltIn().log(
                f'An error occurred while removing the key {e}.', "ERROR")
            return
        finally:
            BuiltIn().log(
                f'Removed key "{key}" from section "{section}"', "INFO")

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
                return None
            if section not in self.config:
                BuiltIn().log(
                    f'Section "{section}" not found in the INI file.', "ERROR")
                return None
            return dict(self.config.items(section))
        except Exception as e:
            BuiltIn().log(
                f'An error occurred while getting all keys and values. {e}', "ERROR")
            return None
        finally:
            BuiltIn().log(
                f'Fetched all the Keys and Values "{dict(self.config.items(section))}"', "INFO")

    @keyword("Get Values List")
    def get_values_list(self, section: str, key: str):
        """
        Gets a list of values for all matching keys under a specified ``section`` in the INI file.

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
                return values
            if section not in self.config:
                BuiltIn().log(
                    f'section "{section}" not found in the INI file.', "ERROR")
                return values
            if len(self.config.items(section)) == 0:
                BuiltIn().log(f'section "{section}". no keys present', "ERROR")
                return values
            for key, value in self.config.items(section):
                if key == key:
                    values.append(value)
        except Exception as e:
            BuiltIn().log(
                f'An error occurred while getting values list. {e}', "ERROR")
            return values
        finally:
            BuiltIn().log(
                f'Fetched all the values for key "{key}" under section "{section}" are {values}', "INFO")
            return values

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
                return None
            return section in self.config
        except Exception as e:
            BuiltIn().log(
                f'An error occurred while checking section "{section}" existence. {e}', "ERROR")
            return None
        finally:
            BuiltIn().log(
                f'Section "{section}" exists in the INI file', "INFO")
            return self.config.has_section(section)

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
                return False
            if section not in self.config:
                BuiltIn().log(
                    f'section "{section}" not found in the INI file.', "ERROR")
                return False
            return self.config.has_option(section, key)
        except Exception as e:
            BuiltIn().log(
                f'An error occurred while checking key existence. {e}', "ERROR")
            return False
        finally:
            BuiltIn().log(f'key "{key}" exists in section "{section}"', "INFO")
            return self.config.has_option(section, key)
