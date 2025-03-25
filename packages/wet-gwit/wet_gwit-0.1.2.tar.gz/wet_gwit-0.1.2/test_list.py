import pytest
import argparse
import os
from shutil import rmtree

from wet import create_args, _get, _list

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
        export_=None
    )
    args.func(args)


@pytest.mark.parametrize(
    "args,expected,not_expected,exits",
    # data dir is reseted before each test.
    # First fetch is done on Oldest gwit site each time.
    [
        (
            argparse.Namespace(
                data_dir=[WET_TEST_DIR],
                func=_list,
                site=None,
                version=False
            ),
            [
                'Locals',
                'Introductions',
                '- Gwit tests =>  0x5b5a404b647a24c78f1a8efb2186a7ed03a08821',
                "> Gwit tests - 0x5b5a404b647a24c78f1a8efb2186a7ed03a08821\n  - introduce 00A => 0x0fa41b369f834ec61065a6f0f3e3302a6da3ef3a\n  - introduce 000 => 0x2576b58e80c76698238b7efe738a47414f675edd\n  - introduce BBB => 0x4a44cc8dd1c04445ce30b1b1c9400a4525274543\n  - 00D => 0x4a7b97df1e85c632ca18b5d7f30bc0e69918e43c\n  - 00E => 0x5e79dc1e2e2234bbcf6f764e0b2b071d3ff6107c\n  - introduce 00C => 0x7c191d77732a9214aea91804a042204f9610669b\n  - introduce CCC => 0xcbdc3f0ba3b2068b7f383f6b2853c5c1080a6b32\n  - introduce AAA => 0xfd90e5c73e6ab603fe0c7f77a7615f89dfd9e079"
            ],
            [
                "- 00A => 0x0fa41b369f834ec61065a6f0f3e3302a6da3ef3a\n- Gwit tests =>  0x5b5a404b647a24c78f1a8efb2186a7ed03a08821",
                "- Gwit tests =>  0x5b5a404b647a24c78f1a8efb2186a7ed03a08821\n- 00A => 0x0fa41b369f834ec61065a6f0f3e3302a6da3ef3a",
            ],
            False,
        ),
        (
            argparse.Namespace(
                data_dir=[WET_TEST_DIR],
                func=_list,
                site='00a',
                version=False
            ),
            [
                'Locals :\n--------\n\nIntroductions :\n---------------\n> Gwit tests - 0x5b5a404b647a24c78f1a8efb2186a7ed03a08821\n  - introduce 00A => 0x0fa41b369f834ec61065a6f0f3e3302a6da3ef3a',
            ],
            [
                "Locals :\n--------\n- 00A => 0x0fa41b369f834ec61065a6f0f3e3302a6da3ef3a",
                'BBB'
            ],
            False,
        ),
        (
            argparse.Namespace(
                data_dir=[WET_TEST_DIR],
                func=_list,
                site='xxxxxx',
                version=False
            ),
            [
                'Locals :\n--------\n\nIntroductions :\n---------------',
            ],
            [
                "Locals :\n--------\n-",
                'Introductions :\n---------------\n> Gwit tests - 0x5b5a404b647a24c78f1a8efb2186a7ed03a08821\n  -',
            ],
            False,
        ),
    ]
)
def test_list(capsys, args, expected, not_expected, exits):
    reset_data_dir()
    first_fetch() # first fetch is on Oldest Gwit Site

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