# GitHub publication audit

This is a local preparation checklist, not a grant of rights. The project has **not** been cleared for public redistribution as a complete character package.

## Completed local cleanup

- Removed the unused `core/`, `ui/`, project-level `config/` and placeholder `assets/` prototype trees, together with their two prototype-only tests.
- Removed optional movie, game and song quotation modules. Festival reminders continue using the remaining quotation libraries.
- Moved unused older character variants out of the project. The local backup is beside this project in `elysia-desktop-pet-removed-local/` and is not part of this repository.
- Excluded Python environments, caches, generated `characters/*/frameseq/` frames, logs and `.env` files from Git. The current `characters/elysia/` package is also excluded until redistribution rights are confirmed.

## Still to resolve before a public upload

1. **Character art:** Establish source, creator and public redistribution terms for each remaining image in `characters/elysia/`, including the current source artwork, generated static pose, icon and animations. The MIT code license does not grant those rights. Until resolved, omit the entire character package from a public repository and explain how users can supply their own assets.
2. **Upstream attribution:** Keep `LICENSE`, `UPSTREAM_THIRD_PARTY_NOTICES.md` and `resources/presentmon/LICENSE.txt` with the applicable code and tool. The upstream notice describes some resources not present here; review it against the final upload list.
3. **Personal information and credentials:** Review the exact staged file list and diff before committing. User settings normally live outside this repository, but no automated scan guarantees that all secrets or private paths are absent.
4. **Git remote:** The local `origin` still points to `MerZlin/dsh-pet-indesktop`. Replace it with the user's own GitHub repository URL before any push. There are currently no tracked files or commits in this local checkout.
5. **Distribution:** This source checkout does not include the desktop launcher EXE on the user's Desktop. The launcher source in `tools/ElysiaDesktopLauncher.cs` assumes the user's current Desktop folder layout, so it is not a general installer or portable launcher. If releasing an executable later, review its path handling, bundled assets and third-party licenses again.
