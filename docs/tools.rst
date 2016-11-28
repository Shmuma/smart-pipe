Tools
=====
There are special command-line tools, which can help access smart pipe data files, look inside them,
analize their performance etc.

All of them are inside single python program called **sp.py**, which is added to path automatically on installation
of package (if you're installing smart_pipe package inside VE, you need to activate VE first).

There are four tools available at the moment:

1. **ls** -- list block indices and block's contents
2. **cat** -- retrieve individual block's key/value pair
3. **cat_all** -- list all entries with optional regexp applied to key
4. **check** -- check smart pipe consistency and performance by reading data sequentially and randomly

All tools are available as sp.py subcommand, for example::

    $ sp.py ls ~/work/data/2016_11_17_231501/visual_annotations/ve
    1
      1:room_container_Tab2_after_click 266937
      1:room_container_Tab3_before_click 158908
      1:whole_page 1157479
      1:room_container_Tab1_before_click 304945
      1:room_container_Tab0_before_click 125256
      1:room_container_Tab2_after_reprocess 254864
      1:room_container_Tab0_after_reprocess 125723
      1:room_container_Tab2_before_click 253828
      1:room_container_Tab3_after_click 167145
      1:room_container_Tab1_after_click 318049
      1:room_container_Tab0_after_click 131816
      1:shop_summary 75227
      1:room_container_Tab3_after_reprocess 159497
      1:room_container_Tab1_after_reprocess 305962
    2
      2:whole_page 262741
      2:room_container_before_click 16203
      2:shop_summary 6724
    --- output truncated ---

