from libgwit.GwitPetnames import Petname
from libgwit.common import ID_REGEX
import yaml #import load, dump
from collections import OrderedDict


class SiteConfigException(Exception):
    pass
class SitesConfig:
    def __init__(self):
        self.locals = {}
        self.introductions = {}
        self.uniques = {}
        self.match_title = {}
        pass

    def __dict__(self):
        # TODO
        return OrderedDict(
            locals = self.locals,
            introductions = self.introductions,
            # following ines are for debug
            uniques = self.uniques,
            match = self.match_title
        )
        pass

    def load(self, path:str):
        # load config
        with open(path, 'r') as f:
            content = yaml.load(f, Loader=yaml.FullLoader)

        self.locals = content['locals']
        self.introductions = content['introductions']
        # self.compute_uniques()
        return self
        # load petnames
        # TODO

    def dump(self, path):
        yaml.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))
        with open(path, 'w') as f:
            yaml.dump(self.__dict__(), f)
        
    def search_in_dict(self, search:str, _dict:dict) -> list:
        """
        Search for a string in sites in a list with petnames dicts matching the search.
        May be used to search among the local sites, or among introductions of a specific site. 
        """
        if ID_REGEX.match(search):
            if search in _dict:
                return [_dict[search]]
        else:
            _return = []
            for elt in _dict.values():
                for key in ['name', 'desc']:
                    find_index = None
                    try:
                        find_index = elt[key].lower().index(search.lower())
                    except:
                        pass
                    if type(find_index) == int:
                        _return.append(elt)

            if _return == []:
                return
            return _return
            

    def search(self, search:str = '', mode:str = 'all') -> dict:
        """
        Search for a string in local sites and introductions.
        Returns a dict with results (even if no result): {locals: {}, introductions: {}}
        mode can be 'all', 'locals', 'introductions'
        """
        if not mode in ['all', 'locals', 'introductions']:
            raise ValueError(f"Error: mode must be 'all', 'local', 'introductions'. Received {mode}.")

        # Empty search -> return whole sites config
        if not search:
            return {
                'locals': self.locals,
                'introductions': self.introductions,
            }
        
        # Else process the search
        _return = {
            'locals': {},
            'introductions': {}
        }
        ## Search among local petnames
        if mode in ['all', 'locals']:
            local_finds = self.search_in_dict(search, self.locals)
            if local_finds:
                for local_find in local_finds:
                    _return['locals'][local_find['id']] = local_find
        
        ## Search among introductions
        if mode in ['all', 'introductions']:
            for introducer in self.introductions:
                edge_finds = self.search_in_dict(search, self.introductions[introducer])
                if (edge_finds):
                    if not introducer in _return['introductions']:
                        _return['introductions'][introducer] = {}
                    for edge in edge_finds:
                        _return['introductions'][introducer][edge['id']] = edge
        return _return
    
    def search_unique(self, search) -> dict:
        """
        Process a search that should return a unique site.
        If site is found in local sites, this function will return informations for this site.
        Else, If many introductions are found with same ID, this function will merge informations and indicate the IDs of the introducers.
        Returns a Petname object.

        @raise SiteConfigException
        """
        # First see if we find the search in locals
        results = self.search(search)
        if len(results['locals']) == 1:
            return results['locals']
        elif len(results['locals']) > 1:
            raise SiteConfigException(f"Error: many matches for a unique search on {search}. Consider using site ID.")

        # Else : no result in locals, we search in introductios. We need to deduplicate the results.
        _return = {}
        for introducer in results['introductions']:
            found = list(results['introductions'][introducer].values())
            if len(found) > 1:
                raise SiteConfigException(f"Error: There are many introductions for same search {search}. Please use site IDs.")
            elif len(found) <= 0:
                continue

            # We have only one result for an introducer
            if len(_return) == 0:
                _return[found[0]['id']] = found[0]
            elif found[0]['id'] in _return:
                _return[found[0]['id']] = self.merge_petname_dicts(_return[found[0]['id']], found[0])
            else:
                raise SiteConfigException(f"Error: There are many introductions for same search {search}. Please use site IDs.")
        return _return

    def merge_local(self, new_local: Petname):
        """
        Adds a petname into locally known petnames.
        Will fullfill information if the ID is already known but informations (alt, remote) is different.
        """
        new_id = new_local.get_id()
        if not new_id in self.locals:
            self.locals[new_id] = new_local.__dict__()
        else :
            self.merge_petname_dicts(self.locals[new_id], new_local.__dict__())
        
        # TODO compute uniques

        
    def merge_introductions(self, introducer:str, introductions) -> None:
        """
        Adds a petname into introductions of a specific site.
        Will fullfill information if the ID is already known but informations (alt, remote) is different.
        """
        # TODO check introducer regex
        if not introducer in introductions:
            self.introductions[introducer] = {}

        for introduction in introductions:
            new_id = introduction.get_id()
            if not new_id in self.introductions[introducer]:
                self.introductions[introducer][new_id] = introduction.__dict__()
            else :
                self.merge_petname_dicts(self.introductions[introducer][new_id], introduction.__dict__())

        # TODO compute uniques

    def merge_petname_dicts(self, keep: OrderedDict, discard: OrderedDict) -> None:
        """
        Will merge dicts representing the same site.
        If informations are different, keep infos from 'keep'.
        Fullfills 'alt' and 'remotes' if 'discard' informations are different from 'keep'.

        @raise SiteConfigException
        """
        if keep['id'] != discard['id']:
            raise SiteConfigException(f"Error: merging unrelated petnames: {discard['id']} into {keep['id']}")
        # we keep main informations from 'keep'.
        # We only add elements to dicts 'remote' and 'alt'.
        for remote in discard['remote']:
            if not remote in keep['remote']:
                keep['remote'][remote] = discard['remote'][remote]
        for u_alt in discard['alt']:
            if not u_alt in keep['alt']:
                keep['alt'].append(u_alt)
        return keep

    # def compute_uniques(self):
    #     """
    #     Not used.

    #     Compute a new array self.unique by merging all sites info from locals and introductions.
    #     """
    #     for local in self.locals:
    #         print (local)
    #         self.uniques[local] = self.locals[local]
    #     for introducer in self.introductions:
    #         for introduction in self.introductions[introducer]:
    #             print (introduction)
    #             if introduction in self.uniques:
    #                 self.merge_petname_dicts(self.uniques[local], self.introductions[introduction].__dict__())
    #             else:
    #                 self.uniques[introduction] = self.introductions[introducer][introduction]



