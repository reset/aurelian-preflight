# AGENTS.md — aurelian-preflight

Guidance for coding agents changing this repository. `README.md` says what it does; this says how to change it.

## What this is

Say in one or two sentences what the repository is and is not.

Stack: Python. The build and development skeleton is scaffolded by `smk proj` from
`smkproj.toml`; re-render with `smk proj` rather than editing a generated file.

## Check

`make ci` is the gate every change passes before it lands. Name any further gate here (a device run, a manual
check) with the command that runs it.

## Landing

Work in a tree (`trees add <name>`), commit on its `worktree/<name>` branch, open the pull request with
`smk pr create` and request its merge with `smk pr merge`, without asking. Live-state changes outside
a merge (deploy, publish, apply) need explicit authorization.

## Where the rest lives

Per-skill facts (hosts, trackers, service bindings, commands) live in `.agents/smk-context.md`, loaded by the
skill that needs them, not at startup. Keep this file under 2300 bytes.
