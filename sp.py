#!/usr/bin/env python
import argparse
import re

import smart_pipe


def command_ls(args):
    pipe = smart_pipe.SmartPipeReader(args.file)

    while True:
        key = pipe.get_next_block_key()
        if key is None:
            break
        print(str(key, encoding='utf-8'))
        for k, v in pipe.pull_block():
            if args.top:
                continue
            print("  %s %d" % (str(k, encoding='utf-8'), len(v)))
    pipe.close()


def command_cat(args):
    pipe = smart_pipe.SmartPipeReader(args.file)
    target_key = bytes(args.key, encoding='utf-8')
    for k, v in pipe.pull_block(bytes(args.chunk, encoding='utf-8')):
        if target_key == k:
            print(str(v, encoding='utf-8'))
    pipe.close()


def command_cat_all(args):
    pipe = smart_pipe.SmartPipeReader(args.file)
    pattern = None if args.pattern is None else re.compile(args.pattern)

    while True:
        for k, v in pipe.pull_block():
            key = str(k, encoding='utf-8')
            if pattern.match(key):
                print(key)
                print(str(v, encoding='utf-8'))
    pipe.close()


def command_check(args):
    print("Not implemented yet")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers()

    parser_ls = subparsers.add_parser('ls', help="List content of smart pipe")
    parser_ls.add_argument("file", help="Smart pipe prefix")
    parser_ls.add_argument("--top", action='store_true', default=False,
                           help="List only top-level chunks")
    parser_ls.set_defaults(func=command_ls)

    parser_cat = subparsers.add_parser('cat', help="Display entry from smart pipe")
    parser_cat.add_argument("file", help="Smart pipe prefix")
    parser_cat.add_argument("-c", "--chunk", required=True, help="Chunk key to show")
    parser_cat.add_argument("-k", "--key", required=True, help="Item key")
    parser_cat.set_defaults(func=command_cat)

    parser_cat = subparsers.add_parser('cat_all', help="Display several entries with optional pattern")
    parser_cat.add_argument("file", help="Smart pipe prefix")
    parser_cat.add_argument("-p", "--pattern", required=False, help="Optional regexp to apply to key")
    parser_cat.set_defaults(func=command_cat_all)

    parser_check = subparsers.add_parser('check', help="Check smart pipe consistency")
    parser_check.add_argument("file", help="Smart pipe prefix")
    parser_check.add_argument("--limit", type=int, help="Limit amount of entries to check")
    parser_check.set_defaults(func=command_check)

    args = parser.parse_args()
    if args.func is None:
        print("Subcommand wasn't specified! Use --help to see usage")
    else:
        args.func(args)
