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
        'vendor/tree-sitter-ada',
        'vendor/tree-sitter-agda',
        'vendor/tree-sitter-sfapex/sosl',
        'vendor/tree-sitter-arduino',
        'vendor/tree-sitter-astro',
        'vendor/tree-sitter-authzed',
        'vendor/tree-sitter-awk',
        'vendor/tree-sitter-bash',
        'vendor/tree-sitter-bass',
        'vendor/tree-sitter-beancount',
        'vendor/tree-sitter-bibtex',
        'vendor/tree-sitter-bicep',
        'vendor/tree-sitter-bitbake',
        'vendor/tree-sitter-blueprint.git',
        'vendor/tree-sitter-c',
        'vendor/tree-sitter-c-sharp',
        'vendor/tree-sitter-cairo',
        'vendor/tree-sitter-capnp',
        'vendor/tree-sitter-chatito',
        'vendor/tree-sitter-clojure',
        'vendor/tree-sitter-cmake',
        'vendor/tree-sitter-comment',
        'vendor/tree-sitter-commonlisp',
        'vendor/tree-sitter-cooklang',
        'vendor/tree-sitter-corn',
        'vendor/tree-sitter-cpon',
        'vendor/tree-sitter-cpp',
        'vendor/tree-sitter-css',
        'vendor/tree-sitter-csv/psv',
        'vendor/tree-sitter-cuda',
        'vendor/tree-sitter-cue',
        # 'vendor/tree-sitter-d',  # No parser.c
        'vendor/tree-sitter-dart',
        'vendor/tree-sitter-devicetree',
        'vendor/tree-sitter-dhall',
        'vendor/tree-sitter-diff',
        'vendor/tree-sitter-dockerfile',
        'vendor/tree-sitter-dot',
        'vendor/tree-sitter-doxygen',
        'vendor/tree-sitter-xml/tree-sitter-dtd',
        'vendor/ebnf/crates/tree-sitter-ebnf',
        'vendor/tree-sitter-eds',
        'vendor/tree-sitter-eex',
        'vendor/tree-sitter-elixir',
        'vendor/tree-sitter-elm',
        'vendor/tree-sitter-elsa',
        'vendor/tree-sitter-elvish',
        'vendor/tree-sitter-embedded-template',
        'vendor/tree-sitter-erlang',
        'vendor/tree-sitter-fennel',
        'vendor/tree-sitter-firrtl',
        'vendor/tree-sitter-fish',
        'vendor/tree-sitter-foam',
        'vendor/tree-sitter-forth',
        'vendor/tree-sitter-fortran',
        'vendor/tree-sitter-fsh',
        'vendor/tree-sitter-func',
        'vendor/tree-sitter-fusion.git',
        'vendor/tree-sitter-gdscript',
        'vendor/tree-sitter-git-config',
        'vendor/tree-sitter-git-rebase',
        'vendor/tree-sitter-gitattributes',
        'vendor/tree-sitter-gitcommit',
        'vendor/tree-sitter-gitignore',
        'vendor/tree-sitter-gleam',
        'vendor/tree-sitter-glimmer',
        'vendor/tree-sitter-glsl',
        'vendor/tree-sitter-gn',
        'vendor/tree-sitter-go',
        'vendor/tree-sitter-godot-resource',
        'vendor/tree-sitter-go-mod',
        'vendor/tree-sitter-go-sum',
        'vendor/tree-sitter-go-work',
        'vendor/tree-sitter-gpg-config',
        'vendor/tree-sitter-graphql',
        'vendor/tree-sitter-groovy',
        'vendor/tree-sitter-gstlaunch',
        'vendor/tree-sitter-hack',
        'vendor/tree-sitter-hare',
        'vendor/tree-sitter-haskell',
        'vendor/tree-sitter-haskell-persistent',
        'vendor/tree-sitter-hcl/dialects/terraform',
        'vendor/tree-sitter-heex',
        'vendor/tree-sitter-hjson',
        'vendor/tree-sitter-hlsl',
        'vendor/tree-sitter-hocon',
        'vendor/tree-sitter-hoon',
        'vendor/tree-sitter-html',
        'vendor/tree-sitter-htmldjango',
        'vendor/tree-sitter-http',
        'vendor/tree-sitter-hurl',
        'vendor/tree-sitter-ini',
        'vendor/tree-sitter-ispc',
        'vendor/tree-sitter-janet-simple',
        'vendor/tree-sitter-java',
        'vendor/tree-sitter-javascript',
        'vendor/tree-sitter-jq',
        'vendor/tree-sitter-jsdoc',
        'vendor/tree-sitter-json',
        'vendor/tree-sitter-json5',
        'vendor/tree-sitter-jsonc.git',
        'vendor/tree-sitter-jsonnet',
        'vendor/tree-sitter-julia',
        'vendor/tree-sitter-kconfig',
        'vendor/tree-sitter-kdl',
        'vendor/tree-sitter-kotlin',
        'vendor/tree-sitter-lalrpop',
        'vendor/tree-sitter-latex',
        'vendor/tree-sitter-ledger',
        'vendor/tree-sitter-leo',
        'vendor/tree-sitter-liquidsoap',
        'vendor/tree-sitter-llvm',
        'vendor/tree-sitter-lua',
        'vendor/tree-sitter-luadoc',
        'vendor/tree-sitter-luap',
        'vendor/tree-sitter-luau',
        'vendor/tree-sitter-m68k',
        'vendor/tree-sitter-make',
        'vendor/tree-sitter-markdown/tree-sitter-markdown',
        'vendor/tree-sitter-markdown/tree-sitter-markdown-inline',
        'vendor/tree-sitter-matlab',
        'vendor/tree-sitter-menhir',
        'vendor/tree-sitter-mermaid',
        'vendor/tree-sitter-meson',
        # 'vendor/tree-sitter-mlir',
        'vendor/tree-sitter-nasm',
        'vendor/tree-sitter-nickel',
        'vendor/tree-sitter-ninja',
        'vendor/tree-sitter-nix',
        'vendor/tree-sitter-norg',
        'vendor/tree-sitter-nqc',
        'vendor/tree-sitter-objc',
        'vendor/tree-sitter-objdump',
        'vendor/tree-sitter-ocaml/ocaml',
        'vendor/tree-sitter-ocaml/interface',
        'vendor/tree-sitter-ocamllex',
        'vendor/tree-sitter-odin',
        'vendor/tree-sitter-org',
        'vendor/tree-sitter-pascal.git',
        'vendor/tree-sitter-passwd',
        'vendor/tree-sitter-pem',
        'vendor/tree-sitter-perl',
        'vendor/tree-sitter-php',
        'vendor/tree-sitter-phpdoc',
        'vendor/tree-sitter-pioasm',
        'vendor/tree-sitter-po',
        'vendor/tree-sitter-pod',
        'vendor/tree-sitter-poe-filter',
        'vendor/tree-sitter-pony',
        'vendor/tree-sitter-prisma',
        'vendor/tree-sitter-promql',
        'vendor/tree-sitter-proto',
        'vendor/tree-sitter-prql',
        'vendor/tree-sitter-csv/tsv',
        'vendor/tree-sitter-pug',
        'vendor/tree-sitter-puppet',
        'vendor/tree-sitter-pymanifest',
        'vendor/tree-sitter-python',
        'vendor/tree-sitter-ql',
        'vendor/tree-sitter-qmldir',
        'vendor/tree-sitter-qmljs',
        'vendor/tree-sitter-query',
        'vendor/tree-sitter-r',
        'vendor/tree-sitter-racket',
        'vendor/tree-sitter-rasi',
        'vendor/tree-sitter-re2c',
        'vendor/tree-sitter-regex',
        'vendor/tree-sitter-rego',
        'vendor/tree-sitter-requirements',
        'vendor/tree-sitter-rnoweb',
        'vendor/tree-sitter-robot',
        'vendor/tree-sitter-ron',
        'vendor/tree-sitter-rst',
        'vendor/tree-sitter-ruby',
        'vendor/tree-sitter-rust',
        'vendor/tree-sitter-scala',
        # 'vendor/tree-sitter-scfg',
        'vendor/tree-sitter-scheme',
        'vendor/tree-sitter-scss',
        'vendor/tree-sitter-slint',
        # 'vendor/tree-sitter-smali',
        'vendor/tree-sitter-smithy',
        'vendor/tree-sitter-snakemake',
        'vendor/tree-sitter-solidity',
        'vendor/tree-sitter-sfapex/apex',
        'vendor/tree-sitter-sfapex/soql',
        'vendor/tree-sitter-sparql',
        'vendor/tree-sitter-sql',
        'vendor/tree-sitter-squirrel',
        'vendor/tree-sitter-ssh-config',
        'vendor/tree-sitter-starlark',
        'vendor/tree-sitter-strace',
        'vendor/tree-sitter-supercollider',
        'vendor/tree-sitter-surface',
        'vendor/tree-sitter-svelte',
        # 'vendor/tree-sitter-swift',
        'vendor/tree-sitter-sxhkdrc',
        'vendor/tree-sitter-systemtap',
        'vendor/tree-sitter-t32.git',
        'vendor/tree-sitter-tablegen',
        # 'vendor/tree-sitter-teal',
        'vendor/tree-sitter-hcl',
        'vendor/tree-sitter-textproto',
        'vendor/tree-sitter-thrift',
        'vendor/tree-sitter-tiger',
        'vendor/tree-sitter-tsq',
        'vendor/tree-sitter-tlaplus',
        'vendor/tree-sitter-todotxt.git',
        'vendor/tree-sitter-toml',
        'vendor/tree-sitter-csv/csv',
        'vendor/tree-sitter-typescript/tsx',
        'vendor/tree-sitter-turtle',
        'vendor/tree-sitter-twig',
        'vendor/tree-sitter-typescript/typescript',
        'vendor/tree-sitter-typoscript',
        'vendor/tree-sitter-ungrammar',
        # 'vendor/tree-sitter-unison',
        'vendor/tree-sitter-usd',
        'vendor/tree-sitter-uxntal',
        'vendor/v-analyzer/tree_sitter_v',
        'vendor/tree-sitter-vala',
        'vendor/tree-sitter-verilog',
        'vendor/tree-sitter-vhs',
        'vendor/tree-sitter-vim',
        'vendor/tree-sitter-vimdoc',
        'vendor/tree-sitter-vue',
        'vendor/tree-sitter-wgsl',
        'vendor/tree-sitter-wgsl-bevy',
        # 'vendor/wing/libs/tree-sitter-wing',
        'vendor/tree-sitter-xml/tree-sitter-xml',
        'vendor/tree-sitter-yaml',
        'vendor/tree-sitter-yang',
        'vendor/tree-sitter-yuck',
        'vendor/tree-sitter-zig',
    ]
)
