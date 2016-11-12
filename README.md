# smart-pipe
Small and fast storage container for key-value entries, optimised for 
sequential data access, but allowing fast individual entry lookup.

## Overview
Quite frequently it is required to save large amount of objects for later sequential process. 
For example: list of downloaded files, entries queried from DB, log entries, etc.

Such storage can be organized in various ways, like:

1. dump all entries in one file, 
2. create tar archive,
3. save in sqlite db, etc.

Unfortunately, if your access to data is expected to be sequential, those options are not exactly what is required for
fast access and efficient on-disk storage.

## Quick example

But let's look at small example.

```python
import smart_pipe as sp

# save some data
writer = sp.SmartPipeWriter("my_data", compress=True)
writer.checkpoint(b'block-1')
writer.append(b'info', b'value')
writer.append(b'other-info', b'value2')
writer.checkpoint(b'block-2')
writer.append(b'info', b'value for block 2')
writer.append(b'error', b'failed, dude')
writer.close()

# read data back
reader = sp.SmartPipeReader("my_data")
while True:
    block_key = reader.get_next_block_key()
    if block_key is None:
        break
    print("Processing block: %s" % (str(block_key)))
    for key, value in reader.pull_block():
        print("  key: %s, value len %d" % (str(key), len(value)))
reader.close()
```
