"""
En marche, les humiliés du souffle ! Oui, le royaume des ciels est à eux !
En marche, les endeuillés ! Oui, ils seront réconfortés !
En marche, les humbles ! Oui, ils hériteront la terre !
En marche, les affamés et les assoiffés de justice ! Oui, ils seront rassasiés !
En marche, les matriciels* ! Oui, ils seront matriciés* !
En marche, les coeurs purs ! Oui, ils verront Elohîms* !
En marche, les faiseurs de paix ! Oui, ils seront criés fils d’Elohîms.
En marche, les persécutés à cause de la justice ! Oui, le royaume des ciels est à eux !
En marche, quand ils vous outragent et vous persécutent, en mentant vous accusent de tout crime, à cause de moi.
Jubilez, exultez ! Votre salaire est grand aux ciels ! Oui, ainsi ont-ils persécuté les inspirés, ceux d’avant vous.

Matyah 5, 3-12  - Traduction selon André Chouraki

J'aime beaucoup cette traduction.
Les évangiles ont été écrits en grec, par des gens qui pensaient en hébreu, voire en araméen.
Chouraki a traduit les textes du grec vers l'Araméen avant de le traduire en français.

Ce mot, qui a à la fois le sens "Heureux" et "en marche", me donne une idée de fierté.
Fierté d'être qui je suis, et d'agir selon mes croyances.

Dans la plupart des traductions de ce passage, il est toujours traduit "Heureux/Bienheureux les pauvres en esprit",
et cela est trop vite interprété comme un appel à la résignation, voire à l'auto-humiliation :
plus on serait malheureux sur terre, plus on serait saint.

A l'inverse, le sens de cette traduction rejoint d'autres bénédictions de Jésus.
Il nous dit, à toutes et tous : lève-toi, et marche. 
"""

import os, io
from urllib.parse import urlparse, urljoin, uses_relative, uses_netloc
import hashlib
import warnings
import inspect
import queue
import logging
from shutil import rmtree
from threading import Thread
# dependency: gitpython
from git import Repo, Commit, BadName, GitCommandError
import pgpy
from libgwit.GwitPetnames import Petname
from libgwit.common import ID_REGEX, INI_INTRODUCTION_FILE_REGEX, GWIT_BRANCH_REGEX, define_logger


# used to build URLs
uses_relative.append('gwit')
uses_netloc.append('gwit')

class ThreadSafeErrorHandler:
    """
    see https://labex.io/tutorials/python-how-to-handle-multithreading-exceptions-451635
    """
    def __init__(self):
        self.error_queue = queue.Queue()
        self.logger = logging.getLogger(__name__)

    def worker_with_error_handling(self, func, args):
        try:
            func(*args)
        except Exception as e:
            error_info = {
                'exception': e,
            }
            self.error_queue.put(error_info)
            self.logger.error(f"Thread exception: {e}")

    def create_thread(self, target, arguments):
        return Thread(
            target=self.worker_with_error_handling,
            args=(target, arguments)
        )

class GwitHelpers:

    def _check_id(self, id):
        if not id:
            raise Exception(f"Error: empty gwit ID.")
        elif not ID_REGEX.match(id):
            raise Exception(f"Error: {id} is not a valid gwit ID.")
        return id
    
    def extract_id(self, url):
        parsed_url = urlparse(url)
        return self._check_id(parsed_url.netloc)

    def branch_name_from_id(self, id: str):
        self._check_id(id)
        return f"gwit-0x{id[-8:]}"

    def sites_from_dir(repo:Repo):
        """Extracts the sites contained in a local repo.
        
        :param str repo: the repository
        :return list: list of sites IDs. Might be empty.
        """
        def match_gwit_branch(branch):
            return GWIT_BRANCH_REGEX.match(branch.name)

        gwit_branches = filter(
            match_gwit_branch,
            repo.heads
        )

        _return = []
        for branch in gwit_branches:
            try:
                public_key_pem = GwitHelpers.extract_public_key(repo, branch.commit)
            except KeyError as e:
                pass # there is no slef.key so the site is not valid

            public_key, _ = pgpy.PGPKey.from_blob(public_key_pem)
            _return.append(f"0x{public_key.fingerprint.lower()}")
        return _return

    def extract_public_key(repo:Repo, commit:Commit):
        """Extracts the public key in PEM format for a given branch.

        :param Repo repo: the repo where we search the key
        :param str ref: the git ref at which we search the key.
        :return: the extracted key
        :rtype: str
        :raises KeyError
        """
        pgp_key_path = commit.tree / '.gwit/self.key'
        key_hash = pgp_key_path.hexsha
        key_blob = repo.git.get_object_data(key_hash)

        return key_blob[3]

class GwitSiteException(Exception):
    pass
class VerifyPgpException (Exception):
    pass
class VerifyPgp:
    def __init__(self, repo: Repo, branch: str, site_id: str, log_level = 'ERROR'):
        self.logger = define_logger(log_level)
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, branch: {branch}, site_id: {site_id}")

        self.repo = repo
        # TODO make a regex check on branch
        self.branch_ref = branch
        # TODO make a regex check on site ID
        self.site_id = site_id
        self.head_commit = repo.commit(self.branch_ref)
        self.head_commit_verified = False
        try:
            self.public_key_pem = GwitHelpers.extract_public_key(repo, self.head_commit)
        except KeyError as e:
            raise VerifyPgpException("self.key file does not exist") from None
        self.public_key, _ = pgpy.PGPKey.from_blob(self.public_key_pem)
    
    def _get_commit_playload(self, commit: Commit):
        """
        Get the commit playload in order to verify the commit signature
        """
        headers  = f"tree {commit.tree.hexsha}\n"
        # try:
        headers += f"parent {commit.parents[0].hexsha}\n"
        # except Exception as e:
        #     print(e)
        headers += f"author {commit.author.name} <{commit.author.email}> {commit.authored_date} {commit.authored_datetime.strftime('%z')}\n"
        # try:
        headers += f"committer {commit.committer.name} <{commit.committer.email}> {commit.committed_date} {commit.committed_datetime.strftime('%z')}\n\n"
        # except Exception as e:
        #     print(e)
        headers += commit.message
        headers.encode()
        return headers

    def verify_id(self) -> None:
        """
        verifies that the site ID matches the provided PGP key

        @raise VerifyPgpException
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_code.co_name}: site_id: {self.site_id}, branch: {self.branch_ref}, pubkey: {self.public_key.fingerprint.lower()}")

        if f"0x{self.public_key.fingerprint.lower()}" != self.site_id.lower():
            raise VerifyPgpException(f"PGP key ID does not match site ID. fingerprint: {self.public_key.fingerprint}, site ID: {self.site_id}")

    def verify_head(self) -> None:
        """
        Verify that 
        - PGP key ID matches the site ID
        - HEAD is signed by the PGP key. (or commit if commit hashis provided)

        @raise VerifyPgpException
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_code.co_name}: site_id: {self.site_id}, branch: {self.branch_ref}")

        # get the playload
        playload = self._get_commit_playload(self.head_commit)
        # get the signature
        try:
            sig = pgpy.PGPSignature.from_blob(self.head_commit.gpgsig)
        except ValueError as e:
            raise VerifyPgpException(f"HEAD signature can't be found for branch {self.branch_ref}: {repr(e)}") from None

        # verify 
        ## hide PGPy warnings
        warnings.filterwarnings(
            "ignore",
            category = UserWarning,
            module = 'pgpy'
        )
        try:
            signatureVerification = self.public_key.verify(playload, sig)
        except Exception as e:
            raise VerifyPgpException(f"HEAD signature is not valid for branch {self.branch_ref}: {repr(e)} ")
        if not signatureVerification:
            raise VerifyPgpException(f"HEAD signature is not valid for branch {self.branch_ref}")
        self.head_commit_verified = True

    def verify_ref(self, ref:str = '') -> None:
        """
        Verifies that a ref is the ancestor of a signed HEAD.

        @raise VerifyPgpException
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_code.co_name}: site_id: {self.site_id}, branch: {self.branch_ref}, ref: {ref}")

        if not self.head_commit_verified:
            raise VerifyPgpException(f"HEAD signature is not valid for branch {self.branch_ref}. Verification for reference was not done.")
        if ref == '':
            return
        # Is the ref an ancestor of HEAD ?
        commit = self.repo.commit(ref)
        if not commit:
            raise VerifyPgpException(f"Reference {ref} is not available for site {self.site_id}")
        previous_to_head = self.head_commit.iter_parents()
        if not commit in previous_to_head:
            raise VerifyPgpException(f"Reference {ref} is not in branch {self.branch_ref} for site {self.site_id}")

    def verify(self, ref:str = '') -> None:
        """
        Verify that
        - the HEAD of branch is signed
        - the provided ref is an ancestor of HEAD

        @raise VerifyPgpException
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, ref: {ref}")

        self.verify_id()
        self.verify_head()
        self.verify_ref(ref)


class GwitSite:
    def __init__(self, repos_dir, log_level = 'ERROR'):
        self.repos_dir = repos_dir
        self.helper = GwitHelpers()
        self.id = ''
        self.remotes = []
        self.repo_dir = ''
        self.sites_config = {}
        self.logger = define_logger(log_level)

    def load_dir (self, asked_id):
        """
        Computes the local path to the repo dir.
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, asked_id: {asked_id}")

        self.id = self.helper._check_id(asked_id)
        self.site_id = self.id
        self.branch_ref = self.helper.branch_name_from_id(self.id)
        self.repo_dir = os.path.join(self.repos_dir, self.id)

    def load_remotes(self, remotes = []) -> None:
        """
        If a param is provided, will force remotes to the provided array.
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, remotes: {remotes}")

        if remotes != []:
            self.remotes = remotes

    def fetch_first (self, remotes) -> None:
        """
        Do the first fetch of a site.
        - clone repo on branch gwit_<id>
        - verify signature of HEAD
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, remotes: {remotes}, self.repo_dir: {self.repo_dir}")

        os.makedirs(self.repo_dir)
        repo = Repo.init(self.repo_dir)
        try:
            self.fetch_repo(repo, remotes, self.branch_ref)
        except:
            rmtree(self.repo_dir)
            raise

    def fetch_unique_remote(self, repo: Repo, remote:str, remote_name:str):
        """
        fetches a site on a unique remote.
        Verifies that the fetched git history is a valid gwit site.
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, remote: {remote}, remote_name: {remote_name}")

        try:
            origin = repo.remote(remote_name)
        except ValueError:
            origin = repo.create_remote(remote_name, remote)

        # Only fetch the branch I need
        # There is an example in the spec that shows that we can also fetch other branches, but I don't think it is a good idea since it consumes space.
        self.logger.info(f"{__name__}::{inspect.currentframe().f_code.co_name}: Fetching remote {remote} for site {self.id}")
        try:
            origin.fetch(self.branch_ref)
        except GitCommandError:
            repo.delete_remote(origin)
            self.logger.error(f"The remote {remote} could not be fetched")
            # TODO raise an error
            return
        self.logger.info(f"{__name__}::{inspect.currentframe().f_code.co_name}: Remote {remote} fetched for site {self.id}")

        # TODO remove other branches and tags matching hashes
        origin_branch_ref = f"{remote_name}/{self.branch_ref}"
        try:
            verify_repo = VerifyPgp(repo, origin_branch_ref, self.site_id, self.logger.getEffectiveLevel())
            verify_repo.verify()
        except Exception as e:
            repo.delete_remote(origin)
            self.logger.error(f"The remote {remote} could not be verified: {str(e)}")
            raise VerifyPgpException(f"{remote}: {repr(e)}") from None

        self.logger.info(f"{__name__}::{inspect.currentframe().f_code.co_name}: Remote {remote} verified for site {self.id}")
        repo.create_head(origin_branch_ref, origin_branch_ref)
        self.logger.info(f"{__name__}::{inspect.currentframe().f_code.co_name}: branch {origin_branch_ref} created for site {self.id}")

    def fetch_repo(self, repo: Repo, remotes:list, branch:str = '', rewrite:int = 0) -> None:
        """
        Fetches and verifies HEAD for the provided repo.
        Manages rewrite : 0 = never, 1 = rewrite with archive, 2 = rewrite without archive
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, remotes: {remotes}, branch: {branch}, rewrite: {rewrite}")
        
        # Fetch many remotes using threads
        # TODO limit threads number, use a queue.
        # print (remotes) #debug
        if not remotes:
            raise GwitSiteException(f"Error : no remotes given for site {self.id}")
        
        threads = []
        remote_names = []       
        for remote in remotes:
            remote_name = hashlib.sha256(remote.encode()).hexdigest()
            error_handler = ThreadSafeErrorHandler()
            t = error_handler.create_thread(target = self.fetch_unique_remote, arguments=[repo, remote, remote_name])
            t.start()
            threads.append(t)
            remote_names.append(remote_name)
        for t in threads:
            t.join()

        # If all remotes failed, all passed remotes have been removed from repo.
        fetch_success = False
        for remote in remote_names:
            try:
                rem = repo.remote(remote)
                fetch_success = True
            except ValueError:
                pass
        if not fetch_success:
            ## Check for any captured errors
            err_reasons = ''
            while not error_handler.error_queue.empty():
                error = error_handler.error_queue.get()
                err_reasons += f"\n{error['exception']}"
            raise GwitSiteException(f"No remote could be fetched. Reasons:{err_reasons}")

        # Sort remote branches
        # Manage rewriting
        heads = []
        for remote_name in remote_names:
            origin_branch_ref = f"{remote_name}/{self.branch_ref}"
            head = repo.commit(origin_branch_ref)
            if len(heads) == 0:
                heads.append(head)
            elif head in heads:
                continue
            else:
                for key, known_head in enumerate(heads):
                    if known_head in head.iter_parents():
                        heads[key] = head
                    elif head in known_head.iter_parents():
                        continue
        if len(heads) == 1:
            # print(repo.heads)
            repo.git.checkout(heads[0].hexsha)
            if self.branch_ref in repo.heads:
                repo.heads[self.branch_ref].delete(repo, self.branch_ref)
            repo.create_head(self.branch_ref, heads[0].hexsha)
        elif len(heads) > 1:
            # There is a rewrite.
            # Determine which is the most recent.
            # If current ref is ancestor of the most recent, update to it
            # Else, manage behavior on rewrites
            current_commit = self.repo.commit()
            most_recent = {
                'head': current_commit if current_commit else None,
                'datetime': current_commit.authored_datetime if current_commit else 0
            }
            for head in heads:
                if head.authored_datetime > most_recent['datetime']:
                    most_recent = {'head': head, 'datetime': head.authored_datetime}
            if current_commit != most_recent['head'] and current_commit in most_recent['head'].iter_parents():
                # no rewrite : fast-forward history
                repo.git.checkout(most_recent['head'].hexsha)
                if self.branch_ref in repo.heads:
                    repo.heads[self.branch_ref].delete()
                repo.create_head(self.branch_ref, most_recent['head'].hexsha)
            elif rewrite > 0 and current_commit not in most_recent['head'].iter_parents():
                if rewrite == 1:
                    # archive current state
                    now = now()
                    archive = f"{self.branch_ref}_{now.year}-{now.month}-{now.day}"
                    repo.create_head(archive, self.branch_ref)
                    warnings.warn('A rewrite has been done for branch {self.branch_ref}')
                # rewrite = 1 or 2
                repo.git.checkout(most_recent['head'].hexsha)
                if self.branch_ref in repo.heads:
                    repo.heads[self.branch_ref].delete()
                repo.create_head(self.branch_ref, most_recent['head'].hexsha)
                warn_message = f"A rewrite has been done for branch {self.branch_ref}."
                warn_message += ' Archiving done' if rewrite == 1 else ''
                warnings.warn(warn_message)
            else:
                raise GwitSiteException(f"A rewrite has happened but parameters forbid rewrite.")

        # print(repo.heads)
        repo.heads[self.branch_ref].checkout()
        # TODO load petnames

    def load_site_petnames(self) -> None:
        """
        Load sites information provided by the current site (self.ini and introductions).
        Will fill self.sites_config['self'] and self.sites_config['introductions'] 
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}")

        # TODO instead of doing a checkout, use direct access to commits
        repo = Repo(self.repo_dir)
        repo.git.checkout(self.branch_ref)

        gwit_dir = os.path.join(self.repo_dir, '.gwit')
        if not os.path.isdir(gwit_dir):
            msg = f"Error: no .gwit dir in {self.repo_dir}"
            raise GwitSiteException(msg)
        self.sites_config['self'] = Petname()
        self_ini_path = os.path.join(gwit_dir, 'self.ini')
        if os.path.isfile(self_ini_path):
            self.sites_config['self'].load_ini(self_ini_path)
        else:
            self.sites_config['self']._id = self.site_id
            self.sites_config['self'].name = "?"

        petnames = []
        with os.scandir(gwit_dir) as it:
            for entry in it:
                if entry.is_file() and INI_INTRODUCTION_FILE_REGEX.match(entry.name):
                    petnames.append(entry.name)

        self.sites_config['introductions'] = []
        for petname_file in petnames:
            self.logger.info(f"{__name__}::{inspect.currentframe().f_code.co_name}, loading petname file {petname_file} for site {self.id}")
            petname = Petname()
            petname.load_ini(os.path.join(gwit_dir, petname_file))
            self.sites_config['introductions'].append(petname)


    def fetch(self, url, remotes = [], rewrite = 0, refresh = 1) -> str:
        """"
        Fetch the content of URL
        url: URL 
        remotes: list of remotes to use. If empty, we will try to use those defined in self.ini
        rewrite: Should we rewrite history ? 0 : no, 1 : yes, 2 : keep an archive branch
        refresh: Use network to get new information. 0: no, 1: if the provided URL does not exist locally, 2: always

        returns the content of the URL
        """
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, remotes: {remotes}, rewrite: {rewrite}, refresh: {refresh}")

        self.url = url
        self.parsed_url = urlparse(self.url)
        if '@' in self.parsed_url.netloc:
            split_netloc = self.parsed_url.netloc.split('@')
            self.site_id = split_netloc[1]
            self.git_ref = split_netloc[0]
            if not self.git_ref or len (split_netloc) > 2:
                raise GwitSiteException(f"Git ref is not valid in {url}")
        else:
            self.site_id = self.parsed_url.netloc
            self.git_ref = self.helper.branch_name_from_id(self.site_id)

        self.load_remotes(remotes)
        self.load_dir(self.site_id)

        first_fetch = False
        if not os.path.isdir(self.repo_dir):
            if not refresh:
                msg = f"Error: {self.id} does not exist locally and can't be fetched because refreshing informations is forbidden."
                raise GwitSiteException(msg)
            self.logger.info(f"{__name__}::{inspect.currentframe().f_code.co_name}, repo {self.repo_dir} does not exist, first fetch for remotes: {remotes}")
            self.fetch_first(remotes)
            first_fetch = True


        self.load_site_petnames()

        repo = Repo(self.repo_dir)
        # print(self.git_ref)
        requested_commit = repo.commit(self.git_ref)
        req_path = self.parsed_url.path.strip('/')
        [full_url, repo_path, local_path, file_type] = self.build_path(requested_commit, req_path)
        # print ([full_url, repo_path, local_path, file_type])

        if not first_fetch and (refresh == 2 or (refresh == 1 and not file_type)):
            self.logger.info(f"{__name__}::{inspect.currentframe().f_code.co_name}, fetching remotes: {remotes} for site {self.id}")
            self.fetch_repo(repo, remotes, rewrite = rewrite)

            requested_commit = repo.commit(self.git_ref)
            [full_url, repo_path, local_path, file_type] = self.build_path(requested_commit, req_path)

        filepath = ''
        if file_type == 'blob':
            targetfile = self.build_git_path(requested_commit.tree, repo_path)
            filepath = os.path.join(self.repo_dir, repo_path)
            with io.BytesIO(targetfile.data_stream.read()) as f:
                content = f.read()

        elif file_type == 'tree':
            content = ''
            # print(requested_commit.tree)
            targetdir = requested_commit.tree / repo_path if repo_path else requested_commit.tree
            for entry in targetdir:
                if entry.name.startswith('.'):
                    continue
                content += f"{entry.name}\n"
        else:
            msg = f"Error: {self.parsed_url.path} does not exist in site {self.id}."
            raise GwitSiteException(msg)

        commit = self.git_ref if self.git_ref != self.branch_ref else ''
        return [full_url, content, filepath, commit]

    def build_git_path(self, tree, path, prev_tree = None):
        """Builds the path in a git tree.
        
        Follows symlinks.
        Follows links.
        """
        if not path:
            return tree
        elif path == '..':
            return tree

        comp_tree = self.build_git_path(tree, os.path.dirname(path))

        if comp_tree.type == 'blob': # it seems that we met a symlink
            with io.BytesIO(comp_tree.data_stream.read()) as f:
                sym_path = f.read().decode()
            if sym_path.startswith('/'):
                raise GwitSiteException('Error: path {path} seems to be in a symlink outside the git repo.')
            comp_tree = self.build_git_path(tree, sym_path)

        if os.path.basename(path) == '.':
            return comp_tree
        return comp_tree / os.path.basename(path)

    def build_path(self, commit, path: str = '', force_index = False):
        """
        Builds the path for the sepcified resource at the specified commit.
        Raises if the resource does not exist.
        """
        root_path = self.sites_config['self'].get_root().strip('/')
        index_path = self.sites_config['self'].get_index()
        
        self.logger.debug(f"{__name__}::{inspect.currentframe().f_code.co_name}, url: {self.url}, path: {path}, root_path: {root_path}, index_path: {index_path}, force_index: {force_index}")

        if path.find(root_path) == 0:
             path = path.replace(root_path, '', 1)
        root_url = self.parsed_url.scheme+'://' + self.parsed_url.netloc

        if path == '' and index_path:
            path = index_path

        repo_path_no_index = os.path.join(root_path, path)
        repo_path_with_index = os.path.join(repo_path_no_index, index_path)
        try:
            _file_no_index = self.build_git_path(commit.tree, repo_path_no_index) if repo_path_no_index else commit.tree
            path_exists = True
        except:
            path_exists = False
            
        repo_path = repo_path_no_index
        full_url = self.url
        file_type = None
        if path_exists:
            file_type = _file_no_index.type
            # if file_type == 'blob':
            #     repo_path = repo_path_no_index
            #     full_url = self.url
            # elif file_type == 'tree':
            if file_type == 'tree':
                try:
                    _file_with_index = commit.tree / repo_path_with_index if repo_path_with_index else commit.tree
                    file_type = _file_with_index.type
                    repo_path = repo_path_with_index
                    full_url = urljoin(self.url + '/', index_path)
                except: # provided path is a dir(tree), but the index file does not exits : we want to access the dir. 
                    repo_path = repo_path_no_index.rstrip('/')
                    full_url = self.url.rstrip('/')+'/'

        # print([full_url, local_abs_path])
        local_abs_path = os.path.join(self.repo_dir, repo_path)
        return [full_url, repo_path, local_abs_path, file_type]