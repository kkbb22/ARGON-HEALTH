# How to apply this normalization to origin/main

I have no push credentials to `kkbb22/ARGON-HEALTH` — everything below
must be run by you, from a machine that has your own git push access.

## Option A — git bundle (preserves full commit history, recommended)
```bash
git clone https://github.com/kkbb22/ARGON-HEALTH.git
cd ARGON-HEALTH
git checkout main
git fetch /path/to/argon-normalization.bundle HEAD:normalization
git merge normalization
git push origin main
```
This brings in 3 real commits with full messages/history:
`6e651d4` (repository restructure), `b967535` (governance layer),
`0ed5463` (reserved directories) — all built on top of the exact
`origin/main` commit (`3396a1f`) that existed at verification time, so
it should fast-forward cleanly. If `origin/main` has moved again since,
`git merge` will show you exactly what conflicts, if any.

## Option B — patch file
```bash
cd ARGON-HEALTH
git am /path/to/normalization.patch
git push origin main
```

## Option C — plain zip (no git history, simplest)
```bash
cd ARGON-HEALTH
# remove the current flat/hybrid state entirely
git rm -rf --cached .
rm -f *.md "*.md"
# extract the zip contents here
unzip /path/to/ARGON-HEALTH-normalized.zip -d .
git add -A
git commit -m "docs: normalize repository into docs/ governance structure"
git push origin main
```

## Verifying after push
```bash
git log --oneline --decorate -5
find docs README.md -type f | sort
```
You should see 40 governed files under `docs/` + `README.md`, zero
`" (1)"` filenames anywhere, and `docs/governance/FINAL-GATE.md` present.
