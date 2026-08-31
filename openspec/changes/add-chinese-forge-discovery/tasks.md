## 1. Discovery Rules And Prompt

- [x] 1.1 Update `docs/agent-rules.md` to include Gitee/GitCode first-class discovery, secondary regional source expansion, stable revision gates, and mirror deduplication; verify the document contains those named behaviors with `rg "Gitee|GitCode|mirror|stable revision" docs/agent-rules.md`
- [x] 1.2 Update `docs/research-scope.md` to document regional source discovery surfaces without adding a new topic family; verify the topic family list remains unchanged and regional forge guidance is present with `rg "Gitee|GitCode|regional" docs/research-scope.md`
- [x] 1.3 Update `scripts/run-codex-radar.sh` so the Architecture Radar prompt instructs the agent to search regional forges and defer inaccessible/non-stable sources; verify the prompt contains Gitee/GitCode and defer wording with `rg "Gitee|GitCode|defer|stable" scripts/run-codex-radar.sh`

## 2. Validation And Tests

- [x] 2.1 Inspect `scripts/validate-radar-state.py` for GitHub-only URL, commit, or discovery-source assumptions and update only if needed; verify non-GitHub Git forge ledger rows are accepted by targeted tests
- [x] 2.2 Add or update tests covering regional forge discovery rows, mirror/canonical-source wording, and non-stable regional source deferral; verify with `python3 -m unittest discover -s tests`

## 3. OpenSpec And Integration Validation

- [x] 3.1 Run `openspec validate add-chinese-forge-discovery --strict --no-interactive` and verify the change is valid
- [x] 3.2 Run `openspec validate --all --strict --no-interactive` and verify no existing change/spec drift is introduced
- [x] 3.3 Run `python3 scripts/validate-radar-state.py` and `git diff --check` to verify repository-level validation and formatting pass
