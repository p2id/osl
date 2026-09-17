# Agent System

## Core Agents

- Research Agent
- Specification Agent
- Architecture Agent
- Builder Agent
- Test Agent
- Security Agent
- Documentation Agent
- Release Agent
- Analytics Agent
- Maintenance Agent

## Agent Contract

Every agent receives:

- explicit objective;
- allowed tools;
- input artifacts;
- output schema;
- resource limits;
- timeout;
- success criteria;
- failure behavior.

## Permission Model

Agents should use least privilege.

Examples:

- Research: read-only access.
- Builder: isolated workspace.
- Test: execute inside a sandbox.
- Release: cannot publish without an approval gate.
- Analytics: read metrics but cannot modify production artifacts.

## Execution Loop

`Plan → Execute → Observe → Verify → Record → Continue / Retry / Escalate`

Agent output is an artifact, not an authority. Deterministic checks should verify important results.
