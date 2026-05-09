# PROJECT_RULES.md

Project-specific overlay for agent behavior.
Project-specific notes may be written in the owner’s preferred language, but operational rules should stay concise and unambiguous for agents.

Fill this file in after copying the template into a target project. Keep common
agent rules in `AGENTS.md`.

## 1. Project Identity

- Name: `<project name>`
- Purpose: `<what this project does>`
- Primary users: `<who uses it>`
- Expected runtime: `<runtime, platform, or environment>`

## 2. Important Files

- Main entry point: `<path>`
- Core source: `<path or directory>`
- Tests: `<path or directory>`
- Documentation: `<path or directory>`

## 3. Do Not Change Without Approval

- `<protected file or directory>`
- `<generated file or external contract>`
- `<configuration that affects deployment or data>`

## 4. Dependencies and Tools

- Language/runtime: `<version or constraint>`
- Package manager: `<tool>`
- Required local tools: `<tools>`
- Dependency policy: `<when dependencies may be added>`

## 5. Build / Run / Test Commands

- Install: `<command>`
- Run: `<command>`
- Test: `<command>`
- Lint or format: `<command>`

## 6. Data / Privacy / External Side Effects

- Local data paths: `<paths>`
- Sensitive data rules: `<rules>`
- Network or API usage: `<allowed or restricted behavior>`
- External side effects: `<files, services, deployments, or accounts>`

## 7. Domain-Specific Rules

- `<domain rule>`
- `<business rule>`
- `<input or output constraint>`

## 8. Notes for Agents

- `<workflow note>`
- `<known limitation>`
- `<manual verification step>`
