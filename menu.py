# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu, we can add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
(T('Welcome to Markbis'),URL('welcome','intro')==URL(),URL('welcome','intro'),[]),
(T('User Guideline'),URL('welcome','guideline')==URL(),URL('welcome','guideline'),[]),
(T('My Search History'),URL('welcome','mysearch_history')==URL(),URL('welcome','mysearch_history'),[]),
(T('Start A New Search'),URL('datacollection','get_keyword')==URL(),URL('datacollection','get_keyword'),[]),
(T('Clean My Databases'),URL('welcome','clean_mydatabase')==URL(),URL('welcome','clean_mydatabase'),[]),

]
