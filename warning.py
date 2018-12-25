def wait_time():
    myrows=db(db.t_keyword_table.created_by==session.auth.user.id).select(db.t_keyword_table.ALL,orderby=db.t_keyword_table.id)
    last_row=myrows.last()
    tweetlimit = last_row.f_tweet_count
    wait_time=(tweetlimit*30)/60
    return locals()

def check_keywordtable():
    myrows=db(db.t_keyword_table.created_by==session.auth.user.id).select(db.t_keyword_table.ALL,orderby=db.t_keyword_table.id)
    last_row=myrows.last()
    tweetlimit = last_row.f_tweet_count
    weight1=last_row.f_weight_1
    weight2=last_row.f_weight_2
    weight3=last_row.f_weight_3
    if weight1==None:
        weight1=0
    if weight2==None:
        weight2=0
    if weight3==None:
        weight3=0
    weight_sum= (weight1+weight2+weight3)
    message1=""
    message2=""
    message3=""

    if (last_row.f_marketing_aim1 == "" or last_row.f_marketing_aim2 == "" or last_row.f_search_key1 == "" or last_row.f_search_key2 == "" or last_row.f_search_key3 == "" or last_row.f_weight_1 == "" or last_row.f_weight_2 == "" or last_row.f_weight_3 == "" or last_row.f_tweet_count == ""):
        message1="- You have missing values in the search keys, please go back and check again !"
    if weight_sum !=100:
        message2="- Your weight is not equal to 100, please go back and check again !"
    if tweetlimit>50001:
        message3="- You have exceeded the allowed tweet limit of 50.000, please go back and check again !"
    last_row.delete_record()
    return locals()
