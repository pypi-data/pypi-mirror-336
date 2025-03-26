"""
Il y a un temps pour tout, un temps pour toute chose sous les cieux:

Un temps pour naître, et un temps pour mourir;
Un temps pour planter, et un temps pour arracher ce qui a été planté;

Un temps pour tuer, et un temps pour guérir;
Un temps pour abattre, et un temps pour bâtir;

Un temps pour pleurer, et un temps pour rire;
Un temps pour se lamenter, et un temps pour danser;

Un temps pour lancer des pierres, et un temps pour ramasser des pierres;
Un temps pour embrasser, et un temps pour s'éloigner des embrassements;

Un temps pour chercher, et un temps pour perdre;
Un temps pour garder, et un temps pour jeter;

Un temps pour déchirer, et un temps pour coudre;
Un temps pour se taire, et un temps pour parler;

Un temps pour aimer, et un temps pour haïr;
Un temps pour la guerre, et un temps pour la paix.

Ecclesiaste 3, 1-8 - Traduction Segond

Ce passage m'aide à me rappeler que personne ne peut être "au top" tout le temps,
ni "au fond du trou" éternellement.

C'est un appel à la tolérance et à la patience, envers moi-même et envers les circonstances.
"""

from syslog import LOG_ERR
import inspect
from libgwit.common import ID_REGEX, INI_INTRODUCTION_FILE_REGEX, define_logger
from libgwit.GwitParser import GwitIniParser
from collections import OrderedDict
from textwrap import wrap
import yaml
import json


class PetnameException(Exception):
    pass

class Petnames:
    pass

class Petname:
    def __init__(self, log_level = 'ERROR'):
        # informations from INI files
        self._id = ''
        self.name = ''
        self.title = ''
        self.desc = ''
        self.title_lang = {}
        self.desc_lang = {}
        self.license = ''
        self._root = ''
        self._index = ''
        self._remotes = {}
        self._alt = []
        self.logger = define_logger(log_level)
   
    def load_ini(self, path:str):
        """
        Load informations for the current petname from a gwit INI file.

        @raise PetnameException
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, path: {path}")

        def config_to_dict(config):
            dictionary = {}
            for section in config.sections():
                gwit_id = section.replace('site ', '').strip('"')
                dictionary[gwit_id] = {}
                for option in config.options(section):
                    dictionary[gwit_id][option] = config.get(section, option)
            return dictionary

        ini_parser = GwitIniParser()
        ini_parser.read(path)
        return self.from_dict(config_to_dict(ini_parser))

    def __dict__(self):
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}")

        return OrderedDict(
            id = self._id,
            name = self.name,
            title = self.title,
            desc = self.desc, 
            # TODO lang title and desc
            license = self.license,
            root = self._root,
            index = self._index,
            remote = self._remotes,
            alt = self._alt
        )

    def get_ini_dict(self) -> dict:
        """
        Returns a dict matching informations to be dumped in a gwit INI file (self.ini and introductions as well)
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}")

        infos_dict = self.__dict__()
        infos_dict.pop('id', None)
        # we only want keys from remotes dicts
        remotes = []
        for remote in infos_dict['remote']:
            remotes.append(remote)
        infos_dict['remote'] = remotes

        section_name = f"site \"{self._id}\""
        return {section_name: infos_dict}

    def from_dict(self, _dict: dict) -> None:
        """
        Loads informations for the current petname from a dict

        @raise PetnameException
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, _dict: {_dict}")

        def add_to_remotes(remote:str, remote_dict:dict):
            self.logger.info(f"{__name__}::{inspect.currentframe().f_code.co_name}: remote: {self._id}, remote_dict: {remote_dict}")

            active = remote_dict['active'] if 'active' in remote_dict else True
            last_successful_fetch = remote_dict['last_successful_fetch'] if 'last_successful_fetch' in remote_dict else ''
            self._remotes[remote] = {'active': active, 'last_successful_fetch': last_successful_fetch}

        keys = list(_dict.keys())
        if len(keys) == 0:
            raise PetnameException("Error : dict contains no section.")
        elif len(keys) > 1:
            raise PetnameException("Error : dict {keys[0]} contains more than one section.")
        key = keys[0]

        infos = _dict[key]

        if not ID_REGEX.match(key):
            raise PetnameException(f"Error: ID {key} is not valid.")
        self._id        = key

        self.logger.info(f"{__name__}::{inspect.currentframe().f_code.co_name}: building dict for petname {self._id}")
        self.name       = infos['name'].strip("'\"") if 'name' in infos else ''
        self.title      = infos['title'].strip("'\"") if 'title' in infos else ''
        self.desc       = infos['desc'].strip("'\"") if 'desc' in infos else ''
        self.desc       = self.desc.strip('"')
        self.license    = infos['license'].strip("'\"") if 'license' in infos else''
        self._root      = infos['root'].strip("'\"") if 'root' in infos else '/'
        self._index     = infos['index'].strip("'\"") if 'index' in infos else ''
        # TODO lang title and desc
        if not 'remote' in infos or infos['remote'] == [] or infos['remote'] == '':
            raise PetnameException(f"Error: no remote given for petname {key}")
        if type(infos['remote']) == str:
            add_to_remotes(infos['remote'].strip("'\""), {})
        else:
            for remote in infos['remote']:
                if type(infos['remote']) == tuple:
                    add_to_remotes(remote.strip("'\""), {})
                if type(infos['remote']) == dict:
                    add_to_remotes(remote.strip("'\""), infos['remote'][remote])
        if 'alt' in infos:
            if type(infos['alt']) == str:
                self._alt.append(infos['alt'])   
            else:
                for alt in infos['alt']:
                    self._alt.append(alt)   
   
    def format(self, _format:str) -> str:
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, _format: {_format}")

        if _format == 'yaml':
            return self.format_yaml()
        elif _format == 'json':
            return self.format_json()
        elif _format == 'ini':
            return self.format_ini()
        elif _format == 'pretty':
            return self.pretty_print()
        else:
            raise AttributeError(f"Error: format {_format} is not managed.")
        
    def pretty_print(self):
        title = f"{self.name} - {self._id}"
        title_underline = len(title) * '-'
        _return = f"{title}\n{title_underline}\n"
        for prop in ['desc', 'license', '_root', '_index']:
            attr = getattr(self, prop, None)
            if attr:
                indent = '  '
                attr = attr.replace("\n", f"\n{indent}") # manage indent after newlines
                wrapped = "\n".join(wrap(attr, replace_whitespace = False, initial_indent=indent, subsequent_indent=indent))
                if len(wrapped.split("\n")) > 1:
                    _return += f"- {prop.strip('_')}:\n{wrapped}\n"
                else:
                    _return += f"- {prop.strip('_')}: {wrapped}\n"

        for prop in ['_remotes', '_alt']:
            attr = getattr(self, prop, None)
            if attr and not attr == {}:
                _return += f"- {prop.strip('_')}:\n"
                for elt in attr:
                    _return += f"  - {elt}\n"
                
        return _return

    def format_yaml(self):
        yaml.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))
        return yaml.dump(self.__dict__())

    def format_json(self):
        return json.dumps(self.__dict__())
    
    def format_ini(self):   
        section_name = f"site \"{self._id}\""
        _return = f"[{section_name}]\n"
        for prop in ['name', 'title', 'desc', 'license', '_root', '_index']: # TODO langs
            attr = getattr(self, prop, None)
            if attr:
                attr = attr.replace("\n", "\\n")
                _return += f"{prop.strip('_')} = \"{attr}\"\n"

        # remote
        attr = getattr(self, '_remotes', None)
        if attr and not attr == {}:
            for elt in attr:
                _return += f"remote = {elt}\n"

        attr = getattr(self, '_alt', None)
        if attr and not attr == {}:
            for elt in attr:
                _return += f"alt = {elt}\n"
                
        return _return

    def set_id(self, id: str):
        pass

    def get_id(self):
        return self._id

    def set_root(self, id):
        pass

    def get_root(self):
        return self._root

    def set_index(self, id):
        pass

    def get_index(self):
        return self._index

    def add_remote(self, remote:str = ''):
        pass

    def get_remotes(self):
        pass

    def add_alt(self, remote:str = ''):
        pass

    def get_alt(self):
        pass