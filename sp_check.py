#!/usr/bin/env python3
import random
import argparse
import logging as log
from time import time
from datetime import timedelta

import smart_pipe


if __name__ == "__main__":
    log.basicConfig(format="%(asctime)-15s %(levelname)s %(message)s", level=log.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--random", type=int, help="Randomly access given number of top-lever keys")
    parser.add_argument("-l", "--limit", type=int, help="Limit amout of top-level keys we're fetching")
    parser.add_argument("file", help="Smart pipe prefix path")
    args = parser.parse_args()

    log.info("Scanning pipe for top-level keys...")
    pipe = smart_pipe.SmartPipeReader(args.file)
    top_keys = []
    total_bytes = 0
    total_pairs = 0
    time_started = time()

    while True:
        key = pipe.get_next_block_key()
        if key is None:
            break
        if args.limit is not None and len(top_keys) >= args.limit:
            log.info("Limit of top-level keys reached, stop reading")
            break
        top_keys.append(key)

        count = 0
        for k, v in pipe.pull_block():
            total_pairs += 1
            total_bytes += len(v) + len(k)
            count += 1
        if not count:
            log.warning("Key %s returned zero pairs", str(key))

    delta = time() - time_started
    log.info("Scanned %d top-level keys, %d pairs, %d bytes in %s, speed %.2f keys/sec", len(top_keys),
             total_pairs, total_bytes, timedelta(seconds=delta), len(top_keys) / delta)
    pipe.close()

    if args.random is not None:
        time_started = time()
        log.info("Randomly sample %d entries...", args.random)
        pipe = smart_pipe.SmartPipeReader(args.file)

        for _ in range(args.random):
            k = random.choice(top_keys)
            for k, v in pipe.pull_block(k):
                pass
        pipe.close()
        delta = time() - time_started
        log.info("Processed %d keys in %s, speed %.2f keys/sec", args.random, timedelta(seconds=delta),
                 args.random / delta)
