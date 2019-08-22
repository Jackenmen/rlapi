## Contributing to rlapi

First off, thanks for taking the time to contribute. It makes the library substantially better. 👍

The following is a set of guidelines for contributing to the repository. These are guidelines, not hard rules.

## Good Bug Reports

Please be aware of the following things when filing bug reports.

1. Don't open duplicate issues. Please search your issue to see if it has been asked already. Duplicate issues will be closed.
2. When filing a bug about exceptions or tracebacks, please include the *complete* traceback. Without the complete traceback the issue might be **unsolvable** and you will be asked to provide more information.
3. Make sure to provide enough information to make the issue workable. The issue template will generally walk you through the process but they are enumerated here as well:
    - A **summary** of your bug report. This is generally a quick sentence or two to describe the issue in human terms.
    - Guidance on **how to reproduce the issue**. Ideally, this should have a small code sample that allows us to run and see the issue for ourselves to debug. **Please make sure that the token is not displayed**. If you cannot provide a code snippet, then let us know what the steps were, how often it happens, etc.
    - Tell us **what you expected to happen**. That way we can meet that expectation.
    - Tell us **what actually happens**. What ends up happening in reality? It's not helpful to say "it fails" or "it doesn't work". Say *how* it failed, do you get an exception? Does it hang? How are the expectations different from reality?
    - Tell us **information about your environment**. What version of discord.py are you using? How was it installed? What operating system are you running on? These are valuable questions and information that we use.

If the bug report is missing this information then it'll take us longer to fix the issue. We will probably ask for clarification, and barring that if no response was given then the issue will be closed.

## Submitting a Pull Request

Submitting a pull request is fairly simple, just make sure it focuses on a single aspect and doesn't manage to have scope creep and it's probably good to go.

### Coding Rules

To ensure consistency throughout the source code, keep these rules in mind as you are working:

* All public API methods **must be documented**.
* This project follows the [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style.html). You should use `black` tool to format your code before sending PR. If the source code is not properly formatted, the CI will fail and the PR cannot be merged.
* To make this project more maintainable, it uses type hints, The CI runs `mypy` against source code on each PR so all the new code has to be properly typed as well.

### Commit Message Guidelines

This project has very precise rules over how its git commit messages can be formatted. This leads to **more readable messages** that are easy to follow when looking through the **project history**. While I recommend using those conventions in all of your commit messages, this project only requires contributors to use valid commit message header format in title of PR.

#### Commit Message Header Format

The header has a special format that includes a **type**, a **scope** and a **subject**:

```
<type>(<scope>): <subject>
```

The **scope** of the header can be omitted (`<type>: <subject>`).

Our recommended character limit is 66 characters, so please try to fit in it. Commit messages are easier to read on GitHub when their header doesn't exceed it. However, if shortening it to that value will make the message less clear, you are allowed to use up to 100 characters.

## Type
Must be one of the following:

* **build**: Changes that affect the build system or external dependencies (example scopes: setup.cfg, manifest)
* **chore**: Other changes that don't modify src or test files
* **ci**: Changes to our CI configuration files and scripts (example scopes: Travis)
* **docs**: Documentation only changes
* **enhance**: A code change that improves current functionality
* **feat**: A new feature
* **fix**: A bug fix
* **perf**: A code change that improves performance
* **refactor**: A code change that neither fixes a bug nor adds a feature
* **revert**: Reverts a previous commit
* **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* **test**: Adding missing tests or correcting existing tests

### Subject
The subject contains a succinct description of the change:

* use the imperative, present tense: "change" not "changed" nor "changes"
* don't capitalize the first letter
* no dot (.) at the end

If you do not meet any of these guidelines, don't worry. Chances are they will be fixed upon rebasing but please do try to meet them to remove some of the workload.

---

Contributing guidelines strongly based on discord.py's CONTRIBUTING.md
