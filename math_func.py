import re
import pandas as pd

df = pd.DataFrame(data={'Info_window_seq' : ['CCAKJATJXARRRZS', 'BJKSLADKZSKDJAXSKJDJK']})

#print(df)

def remove_invalid_aa():
    df['team'] = [re.sub("[BJXZ]", "", str(x)) for x in df['team']]
    print(df)





print(replace())
#
# def test_prod():
#     assert replace('CCAKJATJXARRRZS') == 'CCAKJATJARRRS'
#
# # test_prod('CCAKJATJXARRRZS')