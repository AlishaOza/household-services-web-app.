def callback(commit):
    if commit.author_name == b"Vikas Jaiswal":
        commit.skip()