## 1. Discovery Configuration

- [x] 1.1 Add `deepseek-ai/deepseek-harness` and `TencentCloud/TencentDB-Agent-Memory` to `watchlist.yml` and verify both entries include family, artifact type, review mode, reason, external artifacts, and search terms.
- [x] 1.2 Add AI runtime and agent-memory launch seeds to `docs/research-scope.md` and verify DeepSeek Harness, TencentDB Agent Memory, and their aliases are present.

## 2. Source Expansion Rules

- [x] 2.1 Update `docs/agent-rules.md` so secondary DeepSeek Harness and Tencent Agent Memory artifacts require canonical source expansion before rejection, and verify the rule preserves the normal source evidence bar.
- [x] 2.2 Verify the Architecture Radar prompt path inherits the updated rules from `docs/agent-rules.md` and `docs/research-scope.md` without duplicating a separate hard-coded policy.

## 3. Validation

- [x] 3.1 Run `openspec validate add-agent-runtime-memory-watchlist --strict` and verify the change is valid.
- [x] 3.2 Run the relevant repository validation command and verify existing generated artifacts still pass.
