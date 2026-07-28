# Access Model

## Principles

- Access belongs to a GitHub user or GitHub App installation, not to a model name.
- The owner retains administrative authority.
- The History-writing GPT workflow receives write capability only for the private History repository.
- Public reference repositories can be read without granting private-repository write access.
- Private reference access requires an identity that can enforce read-only permissions.
- Agent changes arrive through branches and pull requests; default branches are owner-controlled.

## Credentials

Never put a password, personal access token, API key, SSH private key, app private key, or replacement credential in a repository or chat transcript. Repository history is not a secret store.

Use a GitHub App, service identity, or credential manager with least privilege. If one integration cannot enforce different per-repository permission levels, use separate writer and reader identities rather than sharing an owner credential.

## Current practical boundary

`azoth-commons` is public and sanitized, so GPT workflows and contributors can read it without access to private AZOTH history. The private History repository remains the only initial write target for the designated History workflow.
