import os
import lolevel_util
import tempfile


def to_bytes(s):
    return bytes(s, encoding='utf-8')


def make_repo(repo_dir, readme_contents):
    lolevel_util.init(repo_dir)
    tree = lolevel_util.create_tree_with_one_file(
        repo_dir,
        blob_basename=to_bytes('README.md'),
        blob_content=readme_contents,
    )
    return tree


def set_head(repo_dir, commit_sha):
    lolevel_util.create_master(repo_dir, commit_sha)


def make_commit(repo_dir, tree, parent_sha, email, name, date):
    if parent_sha:
        parents = [parent_sha]
    else:
        parents = []

    timestamp = int(date.timestamp())

    commit_sha, _, _ = lolevel_util.save_commit_object(
        repo_dir,
        tree,
        parents,
        author_date_s=timestamp,
        author_email=email,
        author_name=name,
        committer_date_s=timestamp,
        committer_email=email,
        committer_name=name,
        message=to_bytes('Psych!'),
    )
    return commit_sha


def draw_git_history(repo_dir, email, name, dates, readme_contents):
    repo_dir = to_bytes(repo_dir)
    email = to_bytes(email)
    name = to_bytes(name)

    tree = make_repo(repo_dir, readme_contents)
    commit_sha = None

    for date in dates:
        for _ in range(100):
            commit_sha = make_commit(repo_dir, tree, commit_sha, email, name, date)

    set_head(repo_dir, commit_sha)
