import pytest
import argparse
import os
from shutil import rmtree
import warnings

from wet import create_args, _get

# remove testdirectory before each test
WET_TEST_DIR = '/tmp/test_wet'
WET_TEST_REMOTE_DIR = 'testing_remote'
WET_TEST_REMOTE_DIR_ABSOLUTE = os.path.abspath(WET_TEST_REMOTE_DIR)

def reset_data_dir():
    if os.path.isdir(WET_TEST_DIR):
        rmtree(WET_TEST_DIR)

def first_fetch():
    """
    Fetch a site that provides introductions.
    """
    # gwit tests site
    args = argparse.Namespace(
        context=None,
        data_dir=[WET_TEST_DIR],
        fresh='unknown',
        func=_get,
        petname=None,
        remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
        rewrite='archive',
        save_local=True,
        url='gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821',
        version=False,
        import_=None,
        export_=None
    )
    args.func(args)


@pytest.mark.parametrize(
    "args,expected,not_expected,found_in_petnames,not_found_in_petnames,exits",
    [
        # BBB on gwit-tests : site with a self.ini but without index nor root path.
        # the content of the repo dir should be listed
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0x4a44cc8dd1c04445ce30b1b1c9400a4525274543', # BBB on gwit-tests : site with a self.ini but without index
                version=False,
                import_=None,
                export_=None
            ),
            [
                'content.txt',
                'files',
                'icon-gwit.png',
            ],
            [
                '.git',
                '.gwit',
                'Site BBB'
            ],
            [
                '0x4a44cc8dd1c04445ce30b1b1c9400a4525274543',
                'name: BBB',
                'title: BBB title',
                'license: GFDL-1.3-or-later',
                'remote:',
                'https://framagit.org/matograine/gwit-tests.git',
                'name: introduce AAA',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079':",
                'name: introduce CCC',
                "'0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32':",
            ],
            [
                'desc: BBB description'
            ],
            False
        ),
        # Same request using #?? syntax
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://0x4a44cc8dd1c04445ce30b1b1c9400a4525274543#??https://framagit.org/matograine/gwit-tests.git',
                version=False,
                import_=None,
                export_=None
            ),
            [
                'content.txt',
                'files',
                'icon-gwit.png',
            ],
            [
                '.git',
                '.gwit'
                'Site BBB',
            ],
            [
                '0x4a44cc8dd1c04445ce30b1b1c9400a4525274543',
                'name: BBB',
                'title: BBB title',
                'license: GFDL-1.3-or-later',
                'remote:',
                'https://framagit.org/matograine/gwit-tests.git',
                'name: introduce AAA',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079':",
                'name: introduce CCC',
                "'0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32':",
            ],
            [
                'desc: BBB description'
            ],
            False
        ),
        # providing a path
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/content.txt',
                version=False,
                import_=None,
                export_=None
            ),
            [
                'Site BBB',
            ],
            [
                '.git',
                '.gwit'
            ],
            [
                '0x4a44cc8dd1c04445ce30b1b1c9400a4525274543',
                'name: BBB',
                'title: BBB title',
                'license: GFDL-1.3-or-later',
                'remote:',
                'https://framagit.org/matograine/gwit-tests.git',
                'name: introduce AAA',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079':",
                'name: introduce CCC',
                "'0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32':",
            ],
            [
                'desc: BBB description'
            ],
            False
        ),
        # same request with syntax #??
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/content.txt#??https://framagit.org/matograine/gwit-tests.git',
                version=False,
                import_=None,
                export_=None
            ),
            [
                'Site BBB',
            ],
            [
                '.git',
                '.gwit'
            ],
            [
                '0x4a44cc8dd1c04445ce30b1b1c9400a4525274543',
                'name: BBB',
                'title: BBB title',
                'license: GFDL-1.3-or-later',
                'remote:',
                'https://framagit.org/matograine/gwit-tests.git',
                'name: introduce AAA',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079':",
                'name: introduce CCC',
                "'0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32':",
            ],
            [
                'desc: BBB description'
            ],
            False
        ),
        # AAA on gwit-tests : no self.ini
        # the content of the repo dir should be listed
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079', # AAA on gwit-tests : site without self.ini
                version=False,
                import_=None,
                export_=None
            ),
            [
                'content.txt',
                'files',
                'icon-gwit.png',
            ],
            [
                '.git',
                '.gwit'
            ],
            [
                '0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079': {}" # introductions
            ],
            [
                'AAA'
            ],
            False
        ),
        # Same request using #?? syntax
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079#??https://framagit.org/matograine/gwit-tests.git',
                version=False,
                import_=None,
                export_=None
            ),
            [
                'content.txt',
                'files',
                'icon-gwit.png',
            ],
            [
                '.git',
                '.gwit'
            ],
            [
                '0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079': {}" # introductions
            ],
            [
                'AAA'
            ],
            False
        ),
        # providing a path
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079/content.txt',
                version=False,
                import_=None,
                export_=None
            ),
            [
                'Site AAA',
            ],
            [
                '.git',
                '.gwit'
            ],
            [
                '0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079': {}" # introductions
            ],
            [
                'AAA'
            ],
            False
        ),
        # same request with syntax #??
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079/content.txt#??https://framagit.org/matograine/gwit-tests.git',
                version=False,
                import_=None,
                export_=None
            ),
            [
                'Site AAA',
            ],
            [
                '.git',
                '.gwit'
            ],
            [
                '0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079': {}" # introductions
            ],
            [
                'AAA'
            ],
            False
        ),
        # CCC on gwit-tests : site with a self.ini but without index nor root path.
        # the content of the repo dir should be listed
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32', # CCC on gwit-tests : full self.ini
                version=False,
                import_=None,
                export_=None
            ),
            [
                'Index of CCC',
            ],
            [
                '.git',
                '.gwit',
            ],
            [
                '0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32',
                'name: CCC',
                'title: CCC title',
                'desc: CCC description',
                'license: WTF-PL',
                'root: ccc_root_path',
                'index: index.gmi',
                'alt:',
                'gemini://ccc.does.not.exist.net',
                'remote:',
                'https://framagit.org/matograine/gwit-tests.git',
                'name: introduce AAA',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079':",
                'name: introduce BBB',
                "'0x4a44cc8dd1c04445ce30b1b1c9400a4525274543':",
            ],
            [],
            False
        ),
        # Same test with syntax #??
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32#??https://framagit.org/matograine/gwit-tests.git', # CCC on gwit-tests : full self.ini
                version=False,
                import_=None,
                export_=None
            ),
            [
                'Index of CCC',
            ],
            [
                '.git',
                '.gwit',
            ],
            [
                '0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32',
                'name: CCC',
                'title: CCC title',
                'desc: CCC description',
                'license: WTF-PL',
                'root: ccc_root_path',
                'index: index.gmi',
                'alt:',
                'gemini://ccc.does.not.exist.net',
                'remote:',
                'https://framagit.org/matograine/gwit-tests.git',
                'name: introduce AAA',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079':",
                'name: introduce BBB',
                "'0x4a44cc8dd1c04445ce30b1b1c9400a4525274543':",
            ],
            [],
            False
        ),
        # getting a file
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32/content.txt', # CCC on gwit-tests : full self.ini
                version=False,
                import_=None,
                export_=None
            ),
            [
                'Site CCC',
            ],
            [
                '.git',
                '.gwit',
                'content.txt',
            ],
            [
                '0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32',
                'name: CCC',
                'title: CCC title',
                'desc: CCC description',
                'license: WTF-PL',
                'root: ccc_root_path',
                'index: index.gmi',
                'alt:',
                'gemini://ccc.does.not.exist.net',
                'remote:',
                'https://framagit.org/matograine/gwit-tests.git',
                'name: introduce AAA',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079':",
                'name: introduce BBB',
                "'0x4a44cc8dd1c04445ce30b1b1c9400a4525274543':",
            ],
            [],
            False
        ),
        # same test with syntax #??
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32/content.txt#??https://framagit.org/matograine/gwit-tests.git', # CCC on gwit-tests : full self.ini
                version=False,
                import_=None,
                export_=None
            ),
            [
                'Site CCC',
            ],
            [
                '.git',
                '.gwit',
                'content.txt',
            ],
            [
                '0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32',
                'name: CCC',
                'title: CCC title',
                'desc: CCC description',
                'license: WTF-PL',
                'root: ccc_root_path',
                'index: index.gmi',
                'alt:',
                'gemini://ccc.does.not.exist.net',
                'remote:',
                'https://framagit.org/matograine/gwit-tests.git',
                'name: introduce AAA',
                "'0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079':",
                'name: introduce BBB',
                "'0x4a44cc8dd1c04445ce30b1b1c9400a4525274543':",
            ],
            [],
            False
        ),
        # Error: remote does not exist
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079/content.txt#??https://aaaaaaaaaaaaaaa.net/git-repo/does-not-exist.git',
                version=False,
                import_=None,
                export_=None
            ),
            [
                'No remote could be fetched',
            ],
            [
                '.git',
                '.gwit'
            ],
            [],
            [],
            True
        ),
        # Error: remote does not exist
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=['https://aaaaaaaaaaaaaaa.net/git-repo/does-not-exist.git'],
                rewrite='archive',
                save_local=False,
                url='gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079',
                version=False,
                import_=None,
                export_=None
            ),
            [
                'No remote could be fetched',
            ],
            [
                '.git',
                '.gwit'
            ],
            [],
            [],
            True
        ),
        # Error: no .gwit dir
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0x2576b58e80c76698238b7efe738a47414f675edd', # 000 on gwit-tests : no .gwit dir
                version=False,
                import_=None,
                export_=None
            ),
            [
                'No remote could be fetched. Reasons:',
                WET_TEST_REMOTE_DIR_ABSOLUTE,
                'self.key file does not exist',
            ],
            [],
            [],
            [],
            True
        ),
        # Error: empty .gwit dir
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0x0fa41b369f834ec61065a6f0f3e3302a6da3ef3a', # 00A on gwit-tests : empty .gwit dir
                version=False,
                import_=None,
                export_=None
            ),
            [
                'No remote could be fetched. Reasons:',
                WET_TEST_REMOTE_DIR_ABSOLUTE,
                'self.key file does not exist',
            ],
            [],
            [],
            [],
            True
        ),
        # Error: no self.key
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0x7c191d77732a9214aea91804a042204f9610669b/', # 00C on gwit-tests : no self.key
                version=False,
                import_=None,
                export_=None
            ),
            [
                'No remote could be fetched. Reasons:',
                WET_TEST_REMOTE_DIR_ABSOLUTE,
                'self.key file does not exist',
            ],
            [],
            [],
            [],
            True
        ),
        # Error: not signed
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0x4a7b97df1e85c632ca18b5d7f30bc0e69918e43c/', # 00C on gwit-tests : no self.key
                version=False,
                import_=None,
                export_=None
            ),
            [
                'No remote could be fetched. Reasons:',
                WET_TEST_REMOTE_DIR_ABSOLUTE,
                'HEAD signature can\'t be found for branch',
                'Expected: ASCII-armored PGP data',
            ],
            [],
            [],
            [],
            True
        ),
        # Error: signed by wrong key
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0x5e79dc1e2e2234bbcf6f764e0b2b071d3ff6107c/', # 00C on gwit-tests : no self.key
                version=False,
                import_=None,
                export_=None
            ),
            [
                'No remote could be fetched. Reasons:',
                WET_TEST_REMOTE_DIR_ABSOLUTE,
                'HEAD signature is not valid for branch',
            ],
            [],
            [],
            [],
            True
        ),
        # Error: petname does not exist
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=['xxxxxx'],
                remote=None,
                rewrite='archive',
                save_local=False,
                url=None,
                version=False,
                import_=None,
                export_=None
            ),
            [
                'Could not find xxxxxx in known sites',
            ],
            [
                '.git',
                '.gwit'
            ],
            [],
            [],
            True
        ),
        # Error: no context for relative path
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='xxxxxx',
                version=False,
                import_=None,
                export_=None
            ),
            [
                'Could not find remotes for URL xxxxxx',
            ],
            [
                '.git',
                '.gwit'
            ],
            [],
            [],
            True
        ),
        # Error: nothing provided
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url=None,
                version=False,
                import_=None,
                export_=None
            ),
            [
                'URL is empty',
            ],
            [
                '.git',
                '.gwit'
            ],
            [],
            [],
            True
        ),
    ]
)
def test_first_fetch(capsys, args, expected, not_expected, found_in_petnames, not_found_in_petnames, exits):
    reset_data_dir()
    if exits:
        warnings.filterwarnings(
            "ignore",
            category = pytest.PytestUnhandledThreadExceptionWarning,
        )
        with pytest.raises(BaseException) as pytest_wrapped_e:
            if args.func:
                result = args.func(args)
        assert pytest_wrapped_e.type == SystemExit
    elif args.func:
        result = args.func(args)

    captured = capsys.readouterr()
    for expect in expected:
        assert expect in captured.out
    for unexpect in not_expected:
        assert unexpect not in captured.out

    if found_in_petnames or not_found_in_petnames:
        with open (WET_TEST_DIR+"/petnames.yaml", 'r') as f:
            petnames_yaml = f.read()
        for fip in found_in_petnames:
            assert fip in petnames_yaml
        for nfip in not_found_in_petnames:
            assert not nfip in petnames_yaml


@pytest.mark.parametrize(
    "args,expected,exits",
    # data dir is reseted before each test.
    # First fetch is done on "Gwit tests" site each time.
    [
        # Load AAA on a specific path at a specific commit (this should test most 'difficult' parts)
        # we do it first to check commit + path works even on not locally stored site. 
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://e3803ae@0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079/content.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'Site AAA - first commit',
            False,
        ),
        # The page does not exist
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079/blog/aaaaaa.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'does not exist',
            True,
        ),
        # The page does not exist at this commit
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://e3803ae@0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079/files/files.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'does not exist',
            True,
        ),
        # Then load AAA gwit site from petname
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname= ['AAA'],
                remote=None,
                rewrite='archive',
                save_local=False,
                url=None,
                version=False,
                import_=None,
                export_=None
            ),
            'content.txt',
            False,
        ),

        # Load CCC on a specific path at a specific commit (this should test most 'difficult' parts)
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://e60169c@0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32/content.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'Site CCC - first commit',
            False,
        ),
        # Error: signed by wrong key
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://0x5e79dc1e2e2234bbcf6f764e0b2b071d3ff6107c/', # 00C on gwit-tests : no self.key
                version=False,
                import_=None,
                export_=None
            ),
            'HEAD signature is not valid for branch',
            True
        ),
        # Error : not signed
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=[WET_TEST_REMOTE_DIR_ABSOLUTE],
                rewrite='archive',
                save_local=False,
                url='gwit://0x4a7b97df1e85c632ca18b5d7f30bc0e69918e43c/', # 00C on gwit-tests : no self.key
                version=False,
                import_=None,
                export_=None
            ),
            'HEAD signature can\'t be found for branch',
            True
        ),
    ]
)
def test_second_fetch(capsys, args, expected, exits):
    reset_data_dir()
    first_fetch()

    if exits:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            if args.func:
                result = args.func(args)
        assert pytest_wrapped_e.type == SystemExit
    elif args.func:
        result = args.func(args)
    captured = capsys.readouterr()
    assert expected in captured.out


@pytest.mark.parametrize(
    "args,expected,exits",
    [
        # Relative to a local site (gwit-tests)
        (
            argparse.Namespace(
                context=['gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821/index.gmi'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='README.md',
                version=False,
                import_=None,
                export_=None
            ),
            '# Gwit tests',
            False,
        ),
        (
            argparse.Namespace(
                context=['gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821/index.gmi'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='./README.md',
                version=False,
                import_=None,
                export_=None
            ),
            '# Gwit tests',
            False,
        ),
        (
            argparse.Namespace(
                context=['gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821/index.gmi'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='/README.md',
                version=False,
                import_=None,
                export_=None
            ),
            '# Gwit tests',
            False,
        ),
        # Relative to a local site, at a given commit (here the path does not exist at this commit)
        (
            argparse.Namespace(
                context=['gwit://e109a655@0x5b5a404b647a24c78f1a8efb2186a7ed03a08821/README.md'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='/index.gmi',
                version=False,
                import_=None,
                export_=None
            ),
            'does not exist in site',
            True,
        ),
        # Relative to a local site, at a given commit (here the path exists at this commit)
        (
            argparse.Namespace(
                context=['gwit://d00333d@0x5b5a404b647a24c78f1a8efb2186a7ed03a08821/README.md'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='/index.gmi',
                version=False,
                import_=None,
                export_=None
            ),
            '# Gwit tests',
            False,
        ),

        # relative to a non-local site (BBB)
        (
            argparse.Namespace(
                context=['gwit://0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/icon-gwit.png'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='file.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'some content',
            False,
        ),
        # relative to a non-local site, using absolute path
        (
            argparse.Namespace(
                context=['gwit://0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/icon-gwit.png'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='/files/file.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'some content',
            False,
        ),

        # The page exists at this commit `a60299f`
        (
            argparse.Namespace(
                context=['gwit://a60299f@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/icon-gwit.png'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='file.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'some content',
            False,
        ),

        # The page does not exist at this commit `a60299f`
        (
            argparse.Namespace(
                context=['gwit://a60299f@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/icon-gwit.png'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='/.gwit/0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079.ini',
                version=False,
                import_=None,
                export_=None
            ),
            'does not exist',
            True,
        ),
        # Using self
        (
            argparse.Namespace(
                context=['gwit://a60299f@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/icon-gwit.png'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://self/content.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'Site BBB - third commit',
            False,
        ),
        # Using self : The page exists at this commit `a60299f`
        (
            argparse.Namespace(
                context=['gwit://a60299f@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/icon-gwit.png'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://a60299f@self/files/file.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'some content',
            False,
        ),
        # Using self : The page does not exist at this commit `a60299f`
        (
            argparse.Namespace(
                context=['gwit://a60299f@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/icon-gwit.png'],
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://a60299f@self/.gwit/0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079.ini',
                version=False,
                import_=None,
                export_=None
            ),
            'does not exist',
            True,
        ),
    ],
)
def test_relative_to_context(capsys, args, expected, exits):
    reset_data_dir()
    first_fetch()

    if exits:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            if args.func:
                result = args.func(args)
        assert pytest_wrapped_e.type == SystemExit
    elif args.func:
        result = args.func(args)

    captured = capsys.readouterr()
    assert expected in captured.out


@pytest.mark.parametrize(
    "previous_args,args,expected,exits",
    [
        # Relative to a specific commit (file exists)
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=True,
                url='gwit://a60299fc3@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/file.txt',
                version=False,
                import_=None,
                export_=None
            ),
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='../content.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'Site BBB - second commit',
            False,
        ),
        # Relative to a specific commit (file does not exist)
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=True,
                url='gwit://a60299fc3@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/file.txt',
                version=False,
                import_=None,
                export_=None
            ),
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='../content_does_not_exist.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'does not exist',
            True,
        ),
        # Using self: previous commit is not used to compute context
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=True,
                url='gwit://a60299fc3@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/file.txt',
                version=False,
                import_=None,
                export_=None
            ),
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://self/content.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'Site BBB - third commit',
            False,
        ),

        # Using self: page does not exist at HEAD
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=True,
                url='gwit://a60299fc3@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/files/file.txt',
                version=False,
                import_=None,
                export_=None
            ),
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://self/dir/aaaaaaaaaaaaaaaaaaaaaaaaaaaa.gmi',
                version=False,
                import_=None,
                export_=None
            ),
            'does not exist',
            True,
        ),

        # Using self: page does not exist at this commit bba287e
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=True,
                url='gwit://bba287e@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/content.txt',
                version=False,
                import_=None,
                export_=None
            ),
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://bba287e@self/files/file.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'does not exist',
            True,
        ),

        # Using self: page exists at this commit a60299fc3
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=True,
                url='gwit://a60299fc3@0x4a44cc8dd1c04445ce30b1b1c9400a4525274543/content.txt',
                version=False,
                import_=None,
                export_=None
            ),
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=False,
                url='gwit://a60299fc3@self/files/file.txt',
                version=False,
                import_=None,
                export_=None
            ),
            'some content',
            False,
        ),
    ]
)
def test_relative_to_previous(capsys, previous_args, args, expected, exits):
    reset_data_dir()
    first_fetch()
    # fetch a previous URL
    if previous_args.func:
        previous_args.func(previous_args)

    if exits:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            if args.func:
                result = args.func(args)
        assert pytest_wrapped_e.type == SystemExit
    elif args.func:
        result = args.func(args)

    captured = capsys.readouterr()
    assert expected in captured.out

@pytest.mark.parametrize(
    "args,expected,not_expected,exits",
    [
        # First visit "Gwit tests" site
        (
            argparse.Namespace(
                context=None,
                data_dir=[WET_TEST_DIR],
                fresh='unknown',
                func=_get,
                petname=None,
                remote=None,
                rewrite='archive',
                save_local=True,
                url=None,
                version=False,
                import_=None,
                export_=None
            ),
            ['gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821 - Gwit tests'],
            ['Error', 'AAA', 'BBB', 'CCC', '000', '00E'],
            False
        ),
        # TODO - test a site with a root path.
    ]
)
def test_get_all(capsys,args,expected,not_expected,exits):
    reset_data_dir()
    first_fetch()

    if exits:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            if args.func:
                result = args.func(args)
        assert pytest_wrapped_e.type == SystemExit
    elif args.func:
        result = args.func(args)

    captured = capsys.readouterr()
    for expect in expected:
        assert expect in captured.out
    for n_expect in not_expected:
        assert not n_expect in captured.out

@pytest.mark.parametrize(
    "import_,branch_expect,not_expected",
    [
        # without search
        (
            [WET_TEST_REMOTE_DIR],
            [
                {'url': 'gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821', 'expected_at_import': 'gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821 -', 'expected_content':'Gwit tests'  , 'expected_error': False},
                {'url': 'gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079', 'expected_at_import': 'gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079 -', 'expected_content': 'content.txt', 'expected_error': False},
                {'url': 'gwit://0x4a44cc8dd1c04445ce30b1b1c9400a4525274543', 'expected_at_import': 'gwit://0x4a44cc8dd1c04445ce30b1b1c9400a4525274543 -', 'expected_content': 'content.txt', 'expected_error': False},
                {'url': 'gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32', 'expected_at_import': 'gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32 -', 'expected_content': 'CCC', 'expected_error': False},
                {'url': 'gwit://0x4a7b97df1e85c632ca18b5d7f30bc0e69918e43c', 'expected_at_import': 'HEAD signature can\'t be found for branch', 'expected_content': 'does not exist locally', 'expected_error': True},
                {'url': 'gwit://0x5e79dc1e2e2234bbcf6f764e0b2b071d3ff6107c', 'expected_at_import': 'HEAD signature is not valid for branch', 'expected_content': 'does not exist locally', 'expected_error': True},
            ],
            # The 3 next sites don't have a self.key.
            [
                '0x2576b58e80c76698238b7efe738a47414f675edd',
                '0x0fa41b369f834ec61065a6f0f3e3302a6da3ef3a',
                '0x7c191d77732a9214aea91804a042204f9610669b'
            ]
        ),
        # with searches
        (
            [WET_TEST_REMOTE_DIR,'ccc','test'],
            [
                {'url': 'gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821', 'expected_at_import': 'gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821 -', 'expected_content':'Gwit tests'  , 'expected_error': False},
                {'url': 'gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32', 'expected_at_import': 'gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32 -', 'expected_content': 'CCC', 'expected_error': False},
            ],
            # These sites should be excluded by filters
            [
                '0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079',
                '0x4a44cc8dd1c04445ce30b1b1c9400a4525274543',
                '0x4a7b97df1e85c632ca18b5d7f30bc0e69918e43c',
                '0x5e79dc1e2e2234bbcf6f764e0b2b071d3ff6107c'
            ]
        ),
    ]
)
def test_import(capsys,import_,branch_expect, not_expected):
    reset_data_dir()
    args_import = argparse.Namespace(
        context=None,
        data_dir=[WET_TEST_DIR],
        fresh='unknown',
        func=_get,
        petname=None,
        remote=None,
        rewrite='archive',
        save_local=True,
        import_=import_,
        export_=None,
        url=None,
        version=False
    )
    result = args_import.func(args_import)
    captured_import = capsys.readouterr()
    for branch in branch_expect:
        assert branch['expected_at_import'] in captured_import.out
    for id in not_expected:
        assert not id in captured_import.out

    for branch in branch_expect:
        # We test locally-stored data
        args_get = argparse.Namespace(
            context=None,
            data_dir=[WET_TEST_DIR],
            fresh='no',
            func=_get,
            petname=None,
            remote=None,
            rewrite='archive',
            save_local=False,
            url=branch['url'],
            version=False,
            import_=None,
            export_=None,
        )
        if branch['expected_error']:
            with pytest.raises(BaseException) as pytest_wrapped_e:
                result = args_get.func(args_get)
            assert pytest_wrapped_e.type == SystemExit
        else:
            args_get.func(args_get)

        captured = capsys.readouterr()
        assert branch['expected_content'] in captured.out

@pytest.mark.parametrize(
    "source_dir,target,branch_expect,not_expected",
    [
        # without search
        (
            [WET_TEST_REMOTE_DIR],
            [WET_TEST_DIR+'/export'],
            [
                {'url': 'gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821', 'expected_at_import': 'gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821 -', 'expected_content':'Gwit tests'  },
                {'url': 'gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079', 'expected_at_import': 'gwit://0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079 -', 'expected_content': 'content.txt'},
                {'url': 'gwit://0x4a44cc8dd1c04445ce30b1b1c9400a4525274543', 'expected_at_import': 'gwit://0x4a44cc8dd1c04445ce30b1b1c9400a4525274543 -', 'expected_content': 'content.txt'},
                {'url': 'gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32', 'expected_at_import': 'gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32 -', 'expected_content': 'CCC'},
            ],
            [
                # the 2 next sites meet an error during import
                '0x4a7b97df1e85c632ca18b5d7f30bc0e69918e43c',
                '0x5e79dc1e2e2234bbcf6f764e0b2b071d3ff6107c',
                # the 3 next sites don't have a self.key and will not be imported
                '0x2576b58e80c76698238b7efe738a47414f675edd',
                '0x0fa41b369f834ec61065a6f0f3e3302a6da3ef3a',
                '0x7c191d77732a9214aea91804a042204f9610669b',
            ]
        ),
        (
            [WET_TEST_REMOTE_DIR],
            [WET_TEST_DIR+'/export', 'test', 'ccc'],
            [
                {'url': 'gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821', 'expected_at_import': 'gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821 -', 'expected_content':'Gwit tests'  },
                {'url': 'gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32', 'expected_at_import': 'gwit://0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32 -', 'expected_content': 'CCC'},
            ],
            [
                # the 2 next sites do not match search
                '0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079',
                '0x4a44cc8dd1c04445ce30b1b1c9400a4525274543',
                # the 2 next sites meet an error during import
                '0x4a7b97df1e85c632ca18b5d7f30bc0e69918e43c',
                '0x5e79dc1e2e2234bbcf6f764e0b2b071d3ff6107c',
                # the 3 next sites don't have a self.key and will not be imported
                '0x2576b58e80c76698238b7efe738a47414f675edd',
                '0x0fa41b369f834ec61065a6f0f3e3302a6da3ef3a',
                '0x7c191d77732a9214aea91804a042204f9610669b',
            ]
        )
    ]
)
def test_export_without_search(capsys,source_dir,target,branch_expect,not_expected):
    target_dir = target[0]
    reset_data_dir()
    # import
    args_import = argparse.Namespace(
        context=None,
        data_dir=[WET_TEST_DIR],
        fresh='unknown',
        func=_get,
        petname=None,
        remote=None,
        rewrite='archive',
        save_local=True,
        import_=source_dir,
        export_=None,
        url=None,
        version=False
    )
    result = args_import.func(args_import)
    captured_import = capsys.readouterr()
    for branch in branch_expect:
        assert branch['expected_at_import'] in captured_import.out

    # export
    args_export = argparse.Namespace(
        context=None,
        data_dir=[WET_TEST_DIR],
        fresh='unknown',
        func=_get,
        petname=None,
        remote=None,
        rewrite='archive',
        save_local=True,
        import_=None,
        export_=target,
        url=None,
        version=False
    )
    result = args_export.func(args_export)
    captured_import = capsys.readouterr()
    for id in not_expected:
        assert not id in captured_import.out

    for branch in branch_expect:
        # We test locally-stored data
        args_get = argparse.Namespace(
            context=None,
            data_dir=[target_dir],
            fresh='no',
            func=_get,
            petname=None,
            remote=None,
            rewrite='archive',
            save_local=False,
            url=branch['url'],
            version=False,
            import_=None,
            export_=None,
        )
        args_get.func(args_get)

        captured = capsys.readouterr()
        assert branch['expected_content'] in captured.out
    