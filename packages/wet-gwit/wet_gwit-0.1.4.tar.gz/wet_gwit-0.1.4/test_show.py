import pytest
import argparse
import os
from shutil import rmtree

from wet import create_args, _get, _show

# remove testdirectory before each test
WET_TEST_DIR = '/tmp/test_wet'


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
        remote=['https://framagit.org/matograine/gwit-tests.git'],
        rewrite='archive',
        save_local=True,
        url='gwit://0x5b5a404b647a24c78f1a8efb2186a7ed03a08821',
        version=False,
        import_=None,
        export_=None,
    )
    args.func(args)


@pytest.mark.parametrize(
    "args,expected,not_expected,exits",
    # data dir is reseted before each test.
    [
        (
            argparse.Namespace(
                data_dir=[WET_TEST_DIR],
                func=_show,
                site='test',
                format=None,
                version=False
            ),
            [
'''Gwit tests - 0x5b5a404b647a24c78f1a8efb2186a7ed03a08821
-------------------------------------------------------
- license:   GFDL-1.3-or-later
- root:   /
- index:   index.gmi
- remotes:
  - https://framagit.org/matograine/gwit-tests.git'''
            ],
            [
                "AAA",
            ],
            False,
        ),
        (
            argparse.Namespace(
                data_dir=[WET_TEST_DIR],
                func=_show,
                site='00a',
                format=None,
                version=False
            ),
            [
'''introduce 00A - 0x0fa41b369f834ec61065a6f0f3e3302a6da3ef3a
----------------------------------------------------------
- root:   /
- remotes:
  - https://framagit.org/matograine/gwit-tests.git'''
            ],
            [
                "AAA",
                "Gwit tests"
            ],
            False,
        ),
        (
            argparse.Namespace(
                data_dir=[WET_TEST_DIR],
                func=_show,
                site='aaa',
                format=None,
                version=False
            ),
            [
'''introduce AAA - 0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079
----------------------------------------------------------
- root:   /
- remotes:
  - https://framagit.org/matograine/gwit-tests.git'''
            ],
            [
                "00A",
                "Gwit tests",
            ],
            False,
        ),
    ]
)
def test_show_first_fetch(capsys, args, expected, not_expected, exits):
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
    "petname_fetched,first_args,second_args,first_expected,second_expected,not_expected,exits",
    # data dir is reseted before each test.
    # First fetch is done on Gwit test site each time.
    [
        (
            'ccc',
            argparse.Namespace(
                data_dir=[WET_TEST_DIR],
                func=_show,
                site='ccc',
                format=None,
                version=False
            ),
            argparse.Namespace(
                data_dir=[WET_TEST_DIR],
                func=_show,
                site='ccc',
                format=None,
                version=False
            ),
            [
'''introduce CCC - 0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32
----------------------------------------------------------
- root:   /
- remotes:
  - https://framagit.org/matograine/gwit-tests.git'''
            ],
            [
'''CCC - 0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32
------------------------------------------------
- desc:   CCC description
- license:   WTF-PL
- root:   ccc_root_path
- index:   index.gmi
- remotes:
  - https://framagit.org/matograine/gwit-tests.git
- alt:
  - gemini://ccc.does.not.exist.net'''
            ],
            [
                "Gwit tests",
            ],
            False,
        ),
        # fetch another site that fullfills informations
        (
            'bbb',
            argparse.Namespace(
                data_dir=[WET_TEST_DIR],
                func=_show,
                site='ccc',
                format=None,
                version=False
            ),
            argparse.Namespace(
                data_dir=[WET_TEST_DIR],
                func=_show,
                site='ccc',
                format=None,
                version=False
            ),
            [
'''introduce CCC - 0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32
----------------------------------------------------------
- root:   /
- remotes:
  - https://framagit.org/matograine/gwit-tests.git'''
            ],
            [
'''introduce CCC - 0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32
----------------------------------------------------------
- root:   /
- remotes:
  - https://framagit.org/matograine/gwit-tests.git
  - https://thisremote.org/does-not/exist.git'''
            ],
            [
                "Gwit tests",
            ],
            False,
        ),
    ]
)
def test_show_second_fetch(capsys, petname_fetched, first_args, second_args, first_expected, second_expected, not_expected, exits):
    reset_data_dir()
    first_fetch()

    # first test
    if exits:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            if first_args.func:
                result = first_args.func(first_args)
        assert pytest_wrapped_e.type == SystemExit
    elif first_args.func:
        result = first_args.func(first_args)

    captured = capsys.readouterr()
    for expect in first_expected:
        assert expect in captured.out
    for n_expect in not_expected:
        assert not n_expect in captured.out

    # fetch petname to have more complete information
    args_petname = argparse.Namespace(
        context=None,
        data_dir=[WET_TEST_DIR],
        fresh='unknown',
        func=_get,
        petname=[petname_fetched],
        remote=None,
        rewrite='archive',
        save_local=True,
        url=None,
        version=False,
        import_=None,
        export_=None
    )
    args_petname.func(args_petname)

    # test more complete information
    if exits:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            if second_args.func:
                result = second_args.func(second_args)
        assert pytest_wrapped_e.type == SystemExit
    elif second_args.func:
        result = second_args.func(second_args)

    captured = capsys.readouterr()
    for expect in second_expected:
        assert expect in captured.out
    for n_expect in not_expected:
        assert not n_expect in captured.out