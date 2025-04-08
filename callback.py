def callback(commit):
    if commit.author_name == b"Alisha_Dhruvi_Diya":
        commit.skip()
