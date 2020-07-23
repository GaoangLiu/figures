import base64
from github import Github
from github import InputGitTreeElement
import sys 


if __name__ == "__main__":
    user = "Elon Tusk"
    password = "spaceX-rules"
    g = Github(user,password)
    repo = g.get_user().get_repo('figures')

    # ----------------------------------------
    image_name = sys.argv[1]
    data = base64.b64encode(open(image_name, "rb").read())
    # path = "{}/{}/{}".format(now.year, now.month, "tweets.zip")
    path = f'2020/{image_name}'
    blob = repo.create_git_blob(data.decode("utf-8"), "base64")
    element = InputGitTreeElement(path=path, mode='100644', type='blob', sha=blob.sha)
    element_list = list()
    element_list.append(element)

    master_ref = repo.get_git_ref('heads/master')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(f"Uploading figure {image_name}", tree, [parent])
    master_ref.edit(commit.sha)
    
    print(f"https://raw.githubusercontent.com/ElonTusk/figures/master/2020/{image_name}")
