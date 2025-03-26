# git-cmd

Simple shortcuts for flash actions.

## Installation

    pip install shooortcuts

Or install from source:

    git clone https://github.com/imhuwq/shooortcuts.git
    cd shooortcuts
    pip install -e .

## Commands

### `ass` (Auto Save State)

Creates a temporary commit with an auto-generated version string:

    $ ass
    Created temporary commit with version: __init__    # If this is first commit
    Created temporary commit with version: a1b2c3d     # If previous commit exists

Version string rules:
- If no commits exist: uses "__init__"
- If last commit was made by `ass`: reuses its version string
- Otherwise: uses the short hash of the last commit

### `css` (Commit Saved State)

Converts temporary commits into a permanent commit:

    $ css "feat: implement new feature"

Behavior:
1. If the oldest temporary commit is an "__init__" commit:
   - Replaces it with the new commit
   - Example: `__init__` -> `feat: implement new feature`

2. If there's a non-temporary commit before temporary commits:
   - Resets to that commit
   - Creates new commit with all changes
   - Example: `normal -> temp1 -> temp2` becomes `normal -> new`

3. If all commits are temporary:
   - Creates new commit replacing all temporary commits
   - Example: `temp1 -> temp2` becomes `new`

### `dss` (Drop State to Stash)

Saves uncommitted changes to stash:

    $ dss
    Saved changes to stash

Behavior:
- If there are no changes: prints "No changes to drop"
- Otherwise: saves all changes to stash with message "gitCMD: auto stash"
- Changes can be recovered later using `git stash pop` or `git stash apply`

### `fss` (Fuck off Saved State)

Moves temporary commits to a new branch and resets main branch:

    $ fss
    Saved current changes as temporary commit    # If there are uncommitted changes
    Created new branch: temp/abc123_250325
    Reset main to last non-temp commit

Behavior:
1. If there are uncommitted changes:
   - Creates a temporary commit with current changes
2. If no commits exist: prints "No commits to fuck off"
3. If all commits are temporary: prints warning and exits
4. If no temporary commits: prints "No temporary commits to fuck off"
5. Otherwise:
   - Creates new branch `temp/$version_YYMMDD`
   - Moves all temporary commits to new branch
   - Resets main branch to last non-temporary commit

## Use Case

Typical workflow:

    # Make some changes
    $ ass                              # Save temporary state
    Created temporary commit with version: __init__

    # Make more changes
    $ ass                              # Save another state
    Created temporary commit with version: __init__

    # Ready to commit properly
    $ css "feat: complete implementation"   # Convert to proper commit
    Created commit: feat: complete implementation

This allows you to:
1. Save work-in-progress changes frequently
2. Convert them into a clean commit when ready
3. Maintain a clean git history 
