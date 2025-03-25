#!/usr/bin/env python3
"""
The real way to get happiness is by giving out happiness to other people.
Try and leave this world a little better than you found it,
and when your turn comes to die you can die happy in feeling that
at any rate you have not wasted your time but have done your best.

Baden-Powell's last message, founder of Scouting.
"""

__version__ = "0.1.3"


import os
import sys
from time import time
import logging
import logging.handlers
from urllib.parse import urlparse, urljoin, uses_relative, uses_netloc
import argparse
import hashlib
import shutil
import subprocess
from git import Repo, InvalidGitRepositoryError
from libgwit.GwitSite import GwitSite, GwitHelpers, GwitSiteException, VerifyPgpException, Petname
from libgwit.SitesConfig import SitesConfig, SiteConfigException
from libgwit.common import ID_REGEX

# used to build URLs
uses_relative.append('gwit')
uses_netloc.append('gwit')

# to write temporary data
TEMP_DIR = '/tmp/wet'

def __init__():
    pass

#get xdg folder. Folder should be "data" or "config"
def xdg(folder="cache"):
    ## Config directories
    ## We implement our own python-xdg to avoid conflict with existing libraries.
    _home = os.path.expanduser('~')
    data_home = os.environ.get('XDG_DATA_HOME') or \
                os.path.join(_home,'.local','share')
    config_home = os.environ.get('XDG_CONFIG_HOME') or \
                    os.path.join(_home,'.config')
    _CONFIG_DIR = os.path.join(os.path.expanduser(config_home),"gwit/")
    _DATA_DIR = os.path.join(os.path.expanduser(data_home),"gwit/")

    if folder == "config":
        return _CONFIG_DIR
    elif folder == "data":
        return _DATA_DIR
    else:
        print("No XDG folder for %s. Check your code."%folder)
        return None

def create_args():
    descri="Wet is a tool to get Gwit sites."
    # Parse arguments
    parser = argparse.ArgumentParser(prog="wet",description=descri)
    parser.add_argument(
        "-d",
        "--data-dir",
        nargs=1,
        help="The directory in which wet will find existing files. Defaults to $XDG_DATA_PATH/gwit or ~/.local/share/gwit if no $XDG_DATA_PATH."
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Display version"
    )

    sub_parser = parser.add_subparsers(title='Commands')

    ## GET parser ##
    get_parser = sub_parser.add_parser('get', help='Fetch and display documents over gwit.')
    get_parser.set_defaults(func=_get)
    get_parser.add_argument(
        "-r",
        "--remote",
        nargs=1,
        help="Git remote for the gwit site. If not provided, wet will search among known petnames."
    )
    get_parser.add_argument(
        "-c",
        "--context",
        nargs=1,
        help="If the link comes from a local site, indicate which one. Petnames and gwit IDs are accepted."
    )
    get_parser.add_argument(
        "-p",
        "--petname",
        nargs=1,
        help="Fetch a site by its petname."
    )
    get_parser.add_argument(
        "-f",
        "--fresh",
        choices=['yes', 'no', 'unknown'],
        default='unknown',
        help="Should we try to pull from remotes ? yes: yes, no: no, unknown: if the resource is not available locally."
    )
    get_parser.add_argument(
        "-l",
        "--save-local",
        action="store_true",
        help="Don't display the document. Useful to only refresh data. If no URL provided, will force refresh all local sites."
    )
    get_parser.add_argument(
        "-w",
        "--rewrite",
        choices=['never', 'always', 'archive'],
        default='archive',
        help="Format the result."
    )

    transfers_parser_group = get_parser.add_mutually_exclusive_group()
    transfers_parser_group.add_argument(
        "-i",
        "--import",
        dest='import_',
        metavar='IMPORT_DIR',
        nargs='*',
        help="Try to import a directory as a gwit site. If the directory is not a gwit site, try to import each subdirectory as a gwit site. If the directry hosts a `sites` dir, the searches will be done in this `sites` directory."
    )
    transfers_parser_group.add_argument(
        "-e",
        "--export",
        dest='export_',
        metavar='EXPORT_DIR [SITE_SEARCHES...]',
        nargs='*',
        help="Exports gwit sites to another directory. If no searches, all local sites will be exported. If there are searches, all sites for which id, name or title match the searches are exported. `get --export TARGET_DIR` quivalent to `-d TARGET_DIR get --import DATA_DIR.`"
    )
    #URL
    get_parser.add_argument(
        'url',
        metavar='URL',
        nargs='?',
        help='URL to download and display.'
    )

    ## News subcommand ##
    # news_parser = sub_parser.add_parser('news', help='Display last commits (10 by default)')
    # news_parser.set_defaults(func=_news)
    # news_parser.add_argument(
    #     "--since",
    #     nargs='*',
    #     help="Display all commits since <date>"
    # )
    # news_parser.add_argument(
    #     "--n",
    #     "--number",
    #     nargs='*',
    #     help="Display all commits since <date>"
    # )

    ## list subcommand ##
    list_parser = sub_parser.add_parser('list', aliases=['search'], help='List and search known sites')
    list_parser.set_defaults(func=_list)
    list_parser_group = list_parser.add_mutually_exclusive_group()
    # list_parser_group.add_argument(
    #     "-k",
    #     "--known-petnames",
    #     action="store_true",
    #     help="Only locally stored sites"
    # )
    # list_parser_group.add_argument(
    #     "-i",
    #     "--introductions",
    #     action="store_true",
    #     help="Suggested by locally stored sites"
    # )
    # list_parser.add_argument(
    #     "--f",
    #     "--format",
    #     choices=['json', 'yaml'],
    #     help="Format the result."
    # )
    list_parser.add_argument(
        'site',
        nargs='?',
        help='Petnames or site ID to list or search (case-insensitive)'
    )

    ## show command ##
    show_parser = sub_parser.add_parser('show', aliases=['search'], help='Show complete information about a site')
    show_parser.set_defaults(func=_show)
    show_parser.add_argument(
        "-f",
        "--format",
        choices=['json', 'yaml', 'ini'],
        help="Format the result."
    )
    show_parser.add_argument(
        'site',
        nargs='?',
        help='Petnames or site ID to list or search (case-insensitive)'
    )

    ## remove subcommand ##
    # remove_parser = sub_parser.add_parser('remove', aliases=['search'], help='Remove a locally stored site.')
    # remove_parser.set_defaults(func=_remove)
    # remove_parser.add_argument(
    #     "-y",
    #     "--yes",
    #     action="store_true",
    #     help="don't ask for confirmation"
    # )
    # remove_parser.add_argument(
    #     'site',
    #     nargs='*',
    #     help='Petname or site ID to remove'
    # )

    return parser

def init_dirs(conf):
    data_dir = conf.data_dir if conf.data_dir else xdg("data")
    # conf_dir = conf.config_dir if conf.config_dir else xdg("config")
    conf_dir = xdg("config")
    for f in [conf_dir, data_dir, TEMP_DIR]:
        if not os.path.exists(f):
            # print("Creating directory {}".format(f))
            os.makedirs(f)

def define_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    slog = logging.handlers.SysLogHandler(address='/dev/log')
    formatter = logging.Formatter('%(module)s: %(message)s')
    slog.setFormatter(formatter)
    logger.addHandler(slog)
    logger.info('Logger set up')
    return logger

def load_conf(args):
    logger = define_logger()
    logger.info(f"arguments: {args}")

    sid = os.getsid(os.getpid())

    conf = args
    conf.logger = logger
    if hasattr(conf, 'remote') and conf.remote != None:
        conf.remote = conf.remote[0]
    conf.data_dir = xdg('data') if (conf.data_dir == None) else conf.data_dir[0]
    conf.repos_dir = os.path.join(conf.data_dir, 'sites')
    conf.petnames_file = os.path.join(conf.data_dir, 'petnames.yaml')
    conf.context_file = os.path.join(conf.data_dir, str(sid) +'_context.txt')
    conf.sites_config = SitesConfig()
    if (os.path.isfile(conf.petnames_file)):
        conf.sites_config.load(conf.petnames_file)

    if hasattr(conf, 'rewrite'):
        rewrite_match = {
            'never': 0,
            'archive': 1,
            'always': 2,
        }
        conf.rewrite_entered = conf.rewrite
        conf.rewrite = rewrite_match[conf.rewrite]

    if hasattr(conf, 'context'):
        conf.context = conf.context[0] if conf.context else ''
        if not conf.context and os.path.isfile(conf.context_file) :
            with open (conf.context_file, 'r') as f:
                conf.context = f.read()
    
    if hasattr(conf, 'petname'):
        conf.petname = conf.petname[0] if conf.petname else ''

    conf.logger.info(f"conf: {conf}")
    return conf

def clean_context(conf):
    for context_file in os.listdir(conf.data_dir):
        if not os.path.isfile(context_file):
            continue
        stat = os.stat(context_file)
        destroy_before = time() - 86400
        if "context" in context_file and stat.st_mtime < destroy_before:
            os.unlink(context_file)

def load_infos_to_fetch_relative(conf, site):
    parsed_url = urlparse(conf.url)

    if not conf.context:
        raise Exception('No context given to compute relative path')
    
    parsed_url_context = urlparse(conf.context)
    if parsed_url.scheme == 'gwit' and 'self' in parsed_url.netloc:
        split_netloc = parsed_url_context.netloc.split("@")
        id = ID_REGEX.match(split_netloc[-1])[0]
        if not id:
            raise Exception(f"Site Id could not be found in context {conf.context}")
        url_root = 'gwit://' + parsed_url.netloc.replace('self', id)
        url = urljoin(url_root, parsed_url.path)
    elif parsed_url.netloc:
        raise Exception('URL is not relative.')
    elif not parsed_url.path:
        raise Exception('Relative URL has no path.')
    else:
        url = urljoin(conf.context, parsed_url.path)

    id_search = parsed_url_context.netloc.split('@')[-1]
    search_results = conf.sites_config.search_unique(id_search)
    if not search_results:
        raise Exception(f"No result for gwit ID {id_search}")
    site_infos = list(search_results.values())[0]
    [url, remotes] = load_remotes_to_fetch(conf, site_infos, url)

    refresh = load_refresh_value(conf)

    return [url, remotes, refresh]

def load_refresh_value(conf):
    if conf.fresh == 'unknown':
        return 1
    elif conf.fresh == 'yes':
        return 2
    else:
        return 0
    
def load_remotes_to_fetch(conf, site_infos, url:str, set_url: bool = False):
    parsed_url = urlparse(url)
    split_fragment = parsed_url.fragment.split('??') if conf.url else []

    # user-set remote
    if (conf.remote):
        remotes = conf.remote
    # remote is set in URL fragment
    elif len(split_fragment) >= 2 and split_fragment[-1]:
        remotes = [split_fragment[-1]]
    # find remotes in known sites
    elif site_infos:
        remotes = list(site_infos['remote'])
        if set_url:
            url = f"gwit://{site_infos['id']}/"
    else:
        raise Exception(f"Could not find remotes for URL {url}.")

    return [url, remotes]

def load_infos_to_fetch(conf, site):
    parsed_url = urlparse(conf.url)
    url = conf.url

    must_set_url = False
    if parsed_url.netloc:
        id_search = parsed_url.netloc.split('@')[-1]
    elif conf.petname: # A petname was provided, no URL.
        id_search = conf.petname
        must_set_url = True
    elif conf.url:
        id_search = conf.url
        must_set_url = True
    else:
        raise Exception(f"URL is empty.")
    

    site_infos = []
    search_results = conf.sites_config.search_unique(id_search)
    if search_results:
        site_infos = list(search_results.values())[0]
    elif conf.petname:
        raise Exception(f"Could not find {id_search} in known sites.")
    
    [url, remotes] = load_remotes_to_fetch(conf, site_infos, url, must_set_url)
    
    refresh = load_refresh_value(conf)

    return [url, remotes, refresh]

def save_context(conf, full_url):
    with open (conf.context_file, 'w') as f:
        f.write(full_url)

def get_many(conf, to_get: dict):
    """
    Fetches many sites. 
    to_get : [{id:<id>, name:<name>, remotes: [<remote1>, <remote2>]},...]
    """
    print (f"Transferring {len(to_get)} sites...")
    processed = []
    for f_site in to_get:
        if f_site in processed:
            continue
        processed.append(f_site)

        display = f"gwit://{f_site['id']} - {f_site['name']}"

        site = GwitSite(conf.repos_dir, conf.logger.getEffectiveLevel())

        try:
            [full_url, content, file_path, commit] = site.fetch(
                f"gwit://{f_site['id']}",
                remotes = f_site['remotes'],
                rewrite = conf.rewrite,
                refresh = 2
            )
            print (display)
        except GwitSiteException as e:
            s = str(e)
            print (f"{display}: {str(e)}")
        except VerifyPgpException as e:
            s = str(e)
            print (f"{display}: {str(e)}")

        if site.sites_config:
            conf.sites_config.merge_local(site.sites_config['self'])
            conf.sites_config.merge_introductions(site.id, site.sites_config['introductions'])
            conf.sites_config.dump(conf.petnames_file)


def get_from_dir(conf, dir: str, searches:list = [], level_down:bool = False):
    """
    Try to import a directory as a site.
    If the provided directory is not a site, try to import all its inner directories as sites. No recursion.
    """
    try:
        repo = Repo(dir)
        dir_ids = GwitHelpers.sites_from_dir(repo)
    except InvalidGitRepositoryError as e:
        if level_down:
            return []
        dir_ids = []

    to_get = []
    if dir_ids:
        for dir_id in dir_ids:
            if (not searches) or (dir_id in searches):
                to_get.append({'id':dir_id, 'name':'', 'remotes':[os.path.abspath(dir)]})
                continue
            else: # filter searches
                site = GwitSite(os.path.dirname(dir), conf.logger.getEffectiveLevel())
                site.load_dir(dir_id)
                site.repo_dir = dir # overwrite value set by load_dir
                site.load_site_petnames()
                for search in searches:
                    if hasattr(site.sites_config['self'], 'name') and search.lower() in site.sites_config['self'].name.lower():
                        to_get.append({'id':dir_id, 'name':site.sites_config['self'].name, 'remotes':[os.path.abspath(dir)]})
                        break
                    if hasattr(site.sites_config['self'], 'title') and search.lower() in site.sites_config['self'].title.lower():
                        to_get.append({'id':dir_id, 'title':site.sites_config['self'].title, 'remotes':[os.path.abspath(dir)]})
                        break
    elif os.path.isdir(os.path.join(dir, 'sites')):
        new_ids = get_from_dir(conf, os.path.join(dir, 'sites'), searches, False)
        if new_ids :
            to_get.extend(new_ids)
    elif not level_down:
        for subdir in os.listdir(dir):
            sub_path = os.path.join(dir, subdir)
            if not os.path.isdir(sub_path):
                continue
            new_ids = get_from_dir(conf, sub_path, searches, True)
            if new_ids :
                to_get.extend(new_ids)

    return to_get
        

def _get_all(conf):
    """
    Fetch all local sites. Force refresh.
    """
    local_sites = conf.sites_config.locals
    to_get = []
    for id_site in local_sites:
        l_site = local_sites[id_site]
        url = 'gwit://'+l_site['id']
        [url, remotes] = load_remotes_to_fetch (conf, l_site, url, True)
        to_get.append({'id': l_site['id'], 'name':l_site['name'], 'remotes': remotes})

    return get_many(conf, to_get)

def _news(args):
    init_dirs()
    # print (args) # debug

def _get(args):
    # print (args)
    conf = load_conf(args) 
    # print (conf) # debug
    init_dirs(conf)
    clean_context(conf)

    if conf.import_:
        dir = conf.import_.pop(0)
        to_get = get_from_dir(conf, dir, conf.import_)
        return get_many(conf, to_get)
    elif conf.export_:
        tmp_data_dir = conf.data_dir 
        conf.data_dir = conf.export_.pop(0)
        conf.repos_dir = os.path.join(conf.data_dir, 'sites')
        conf.petnames_file = os.path.join(conf.data_dir, 'petnames.yaml')
        init_dirs(conf)
        to_get = get_from_dir(conf, tmp_data_dir, conf.export_)
        return get_many(conf, to_get)


    if conf.save_local and not conf.url and not conf.petname:
        return _get_all(conf)

    site = GwitSite(conf.repos_dir, conf.logger.getEffectiveLevel())

    if conf.remote and conf.url:
        url = conf.url
        remotes = [conf.remote]
        refresh = load_refresh_value(conf)
    else:
        met_exceptions = []
        try:
            try:
                [url, remotes, refresh] = load_infos_to_fetch_relative(conf, site)
            except Exception as e:
                [url, remotes, refresh] = load_infos_to_fetch(conf, site)
        except Exception as e:
            print(str(e))
            exit(1)

    ## If needed, fetch it
    try:
        [full_url, content, file_path, commit] = site.fetch(
            url,
            remotes = remotes,
            rewrite = conf.rewrite,
            refresh = refresh
        )
    except GwitSiteException as e:
        s = str(e)
        print (str(e))
        exit(1)
    except VerifyPgpException as e:
        s = str(e)
        print (str(e))
        exit(1)

    if site.sites_config:
        conf.sites_config.merge_local(site.sites_config['self'])
        conf.sites_config.merge_introductions(site.id, site.sites_config['introductions'])
        conf.sites_config.dump(conf.petnames_file)

    save_context(conf, full_url)

    if (not conf.save_local):
        if type(content) == str:
            print(content)
        else:
            try:
                content = content.decode()
                print(content)
            except UnicodeDecodeError as e:
                if shutil.which('xdg-open'):
                    data_hash = hashlib.sha1(content).hexdigest()
                    filepath = os.path.join(TEMP_DIR, f"{data_hash}_{os.path.basename(file_path)}")
                    if not os.path.isfile(filepath):
                        with open(filepath, 'wb') as f:
                            f.write(content)
                    subprocess.run(['xdg-open', filepath])
                else:
                    msg = f'The file you want to see is not a text file.\nCommand `xdg-open` is not available.\nYou will find the file at:\n\n  {file_path}\n\n'
                    if commit:
                        msg += f'Don\'t forget to checkout commit/reference `{commit}`'
                    print(msg)
                    return

def _list(args):
    conf = load_conf(args)
    init_dirs(conf)

    # TODO manage search parameters (locals, introductions, etc.)
    _list = conf.sites_config.search(conf.site)

    print ("\nLocals :\n--------")
    for local in _list['locals']:
        print (f"- {_list['locals'][local]['name']} =>  {_list['locals'][local]['id']}")
    
    print ("\nIntroductions :\n---------------")
    for introducer in _list['introductions']:
        if _list['introductions'][introducer] != {}:
            print (f"> {conf.sites_config.locals[introducer]['name']} - {conf.sites_config.locals[introducer]['id']}")
            for introduction in _list['introductions'][introducer]:
                print (f"  - {_list['introductions'][introducer][introduction]['name']} => {_list['introductions'][introducer][introduction]['id']}")

def _show(args):
    conf = load_conf(args)
    init_dirs(conf) # TODO just exit if no dir
    # print (args) # debug
    try:
        found = conf.sites_config.search_unique(conf.site)
    except SiteConfigException as e:
        print(e)
        exit(1)
    if not found:
        print(f"{conf.site} could not be found")
        exit(1)
    petname = Petname()
    petname.from_dict(found)
    if conf.format in ['yaml', 'json', 'ini']:
        content = petname.format(conf.format)
    else:
        content = petname.format('pretty')
    print (content)

def _remove(args):
    init_dirs() # TODO just exit if no dir
    # print (args) # debug

def main():
    parser = create_args()
    if len(sys.argv) == 1:
        parser.print_help()
        exit()
    args = parser.parse_args()
    if hasattr(args, 'func') and args.func:
        args.func(args)

    # Handle -v, --version
    if args.version:
        print("Wet " + __version__)
        sys.exit()


if __name__== '__main__':
    main()