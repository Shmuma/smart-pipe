Architecture of SmartPipe
=========================

It's very simple and straightforward. There are two angles architecture can be described: logical and physical.

* Logical is more about **what** you can store and do with this storage class,
* physical is about **how** data is stored and what to expect from it.

Logical model
-------------

Blocks
``````

Logically, smart pipe is a sequence of blocks. Every block block has key, which has to be uniq byte sequence.
Like this:

.. image:: 01-Blocks.png

We don't require keys to be numbers or strings of some form or ordered, etc. They just need to be uniq, that's it.

We remember position of every block in separate index, so, every individual block can be accessed by it's key. Or you
can read all blocks sequentially, like file.

Every block should have reasonable size -- during reading, all it's contents are read into memory, so,
several megabytes will be fine, but couple of gigabytes can be too much. But library never keeps several blocks
in memory at the same time, so, with modern memory prices it's not too strict (otherwise, why are you using Python?).

Block structure: key-values
```````````````````````````
Inside every block can contain any amount of key-value pairs which both are just byte sequences.

.. image:: 02-KeyValues.png

Key and values have even less limitations than block keys -- they can be uniq, empty, etc. So, technically,
only one limitation: they have to fit in your memory.

Access pattern is simple: you need to iterate all key-value pairs of the block to go to next block's data. You can't
efficiently seek inside the block, so, keep this in mind designing your app.

Usage example
`````````````
This library was designed to efficiently save and re-process results obtained from the web, but can be applied to
other areas. Our particular example is:

1. Every block is a site we've processed, addressed by our uniq internal id (or url)
2. Inside the block we can have various key-value pairs:
  1. raw html result from site (with 'raw' key),
  2. server's response text ('response' key),
  3. processing results in json form ('result' key)
  4. log information from processing ('log' key)

After data was downloaded and processed, smart pipe file are almost immutable (in theory, it won't be too hard to append
but currently it's not implemented), but can be efficiently read sequentially or you can efficiently read individual
blocks, which is mostly useful for debugging specific problematic cases.

Physical model
--------------

There are two files per smart pipe:

1. with data blocks, can have extension .dat (for uncompressed smart pipes) or .datz (for compressed)
2. with index, containing index of every blocks' key and offset withing data file.

Index is just binary file with raw keys of blocks and offsets and this file is read completely into memory on smart pipe
reader creation. So, please, don't try to store trillions of blocks inside single pipe!

Data blocks have slightly more complicated structure, but also simple: every block has keys and values in
serialized form, and whole block's data is optionally compressed by zlib library.

