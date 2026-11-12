# Poe Junkroan

Machine search for Path of Exile builds. Path of Building (PoB) runs headless as the numeric oracle; a deterministic
optimizer builds the passive tree, gear and config for each candidate build skeleton; a search over skeletons finds
strong builds, non-meta ones included. A language model proposes hypotheses and explains results; it never picks
nodes, affixes or config.

You ask for a build ("Storm Brand", "something around item X"); you get a ranked set of PoB import codes, each with
the reasons it is shaped the way it is.

```bash
pip install -e ".[dev]"
python -m pytest -q
python scripts/smoke_pob.py
junkroan build --skill "Storm Brand" --level 80
```

Requires Python 3.12. The pinned PoB release is downloaded to `var/` on first use.

- `docs/ARCHITECTURE.md`: design. `docs/LAYOUT.md`: layout and commands. `docs/TESTING.md`: how a change is proven.
- `docs/adr/`: one decision per file (D57 = `docs/adr/0057-*.md`). `GLOSSARY.md`: the vocabulary.
- `CLAUDE.md`: how agent chats work in this repo.

Copyright and game-data notice: `NOTICE`.
