# Rafeeq Security Notes

## Scope
Rafeeq is a demonstration assistant. It is not connected to official
municipal systems, and its permit requirements are illustrative only.

## The Lethal Trifecta
The three risk factors are:
1. Access to sensitive data.
2. Exposure to untrusted content, such as user messages or retrieved documents.
3. Ability to perform external actions or modify records.

Combining these factors can allow malicious content to influence an agent
that has access to private information and powerful tools.

## Example Attack
An attacker submits a message or document containing instructions to ignore
the system rules and disclose private applicant information or submit an
application without authorization.

## Defenses
- Treat user input and retrieved documents as untrusted data.
- Never treat instructions inside external content as system-level policy.
- Require explicit human approval before consequential write actions.
- Apply least-privilege access and validate tool arguments.
- Keep secrets out of prompts, logs, and source control.
- Limit memory and execution steps.
- Log tool calls without recording unnecessary personal information.
- Test refusal, authorization, and prompt-injection cases before deployment.

## Current Demo Limitations
- Data is local demonstration data, not an official municipal database.
- Application approval is represented by an explicit `approved` argument.
- The evaluation suite uses keyword matching and does not prove security.
- Production deployment would require authentication, authorization,
  secure logging, rate limits, and independent security testing.
