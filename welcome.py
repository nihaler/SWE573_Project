# -*- coding: utf-8 -*-
def intro():
    return dict()

@auth.requires_login()
def mysearch_history():
    rows=db(db.t_keyword_table.created_by==session.auth.user.id).select(db.t_keyword_table.ALL,orderby=db.t_keyword_table.id)
    return locals()

@auth.requires_login()
def guideline():
    return dict()

@auth.requires_login()
def clean_mydatabase():
    db.t_keyword_table.truncate('RESTART IDENTITY CASCADE')
    return locals()
