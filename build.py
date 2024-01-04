import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from tree_sitter import Language


repos = []
with open("repos.txt", "r") as file:
    for line in file:
        url, commit = line.split()
        clone_directory = os.path.join("vendor", url.rstrip("/").split("/")[-1])
        repos.append((url, commit, clone_directory))


def clone_repo(url, commit, clone_directory):
    print()
    print(f"{sys.argv[0]}: Cloning: {url} (commit {commit}) --> {clone_directory}")
    print()

    if os.path.exists(clone_directory):
        return

    # https://serverfault.com/a/713065
    os.mkdir(clone_directory)
    subprocess.check_call(["git", "init"], cwd=clone_directory)
    subprocess.check_call(["git", "remote", "add", "origin", url], cwd=clone_directory)
    subprocess.check_call(["git", "fetch", "--depth=1", "origin", commit], cwd=clone_directory)
    subprocess.check_call(["git", "checkout", commit], cwd=clone_directory)

# During the build, this script runs several times, and only needs to download
# repositories on first time.
if os.path.isdir("vendor") and len(os.listdir("vendor")) == len(repos):
    print(f"{sys.argv[0]}: Language repositories have been cloned already.")
else:
    os.makedirs("vendor", exist_ok=True)
    futures = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for url, commit, clone_directory in repos:
            futures.append(executor.submit(clone_repo, url, commit, clone_directory))
    # Wait for all the clones to finish.
    for future in futures:
        future.result()


print()

if sys.platform == "win32":
    languages_filename = "tree_sitter_languages\\languages.dll"
else:
    languages_filename = "tree_sitter_languages/languages.so"

print(f"{sys.argv[0]}: Building", languages_filename)
Language.build_library(
    languages_filename,
    [
        clone_directory
        for url, commit, clone_directory in repos
    ]
)
