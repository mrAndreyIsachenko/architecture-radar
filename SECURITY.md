# Security Policy

## Supported Scope

This repository contains a GitHub Actions workflow, local helper scripts, prompts, templates, and generated research artifacts.

Security-sensitive areas include:

- handling of `OPENAI_API_KEY`;
- separation between the Codex research step and GitHub publishing credentials;
- GitHub Actions permissions;
- branch protection and validation checks;
- scripts that publish generated artifacts;
- accidental exposure of private project context in research files.

## Reporting A Vulnerability

Do not open a public issue for vulnerabilities or exposed secrets.

Report security concerns privately to the repository owner through GitHub.

Include:

- affected file, workflow, or script;
- what an attacker or untrusted model output could do;
- whether credentials, private data, or repository write access are involved;
- minimal reproduction steps when safe to share;
- suggested mitigation if known.

## Response Expectations

The maintainer will review reports as availability allows. High-impact issues involving credential exposure or unintended repository writes should be treated as urgent.

## Non-Security Issues

Use normal issues or pull requests for:

- research quality problems;
- missing evidence labels;
- false positives in validation;
- unclear documentation;
- model cost concerns;
- feature requests.
