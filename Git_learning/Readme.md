# Git Basics Link:
https://blog.w3programmers.com/git-%E0%A6%95%E0%A6%BF-%E0%A6%8F%E0%A6%AC%E0%A6%82-git-%E0%A6%95%E0%A6%BF%E0%A6%AD%E0%A6%BE%E0%A6%AC%E0%A7%87-%E0%A6%95%E0%A6%BE%E0%A6%9C-%E0%A6%95%E0%A6%B0%E0%A7%87/

# Git Basics
Git is a distributed version control system that helps you track changes in files, collaborate with others, and maintain a history of your project.

# Getting Started with Git

### Installation:
If you haven't installed Git yet, you can download it from git-scm.com.
### Configuration:
After installation, set up your identity:

- git config --global user.name "Your Name"
- git config --global user.email "your.email@example.com"


# Essential Git Commands
### Cloning a Repository
To clone (download) an existing repository:
git clone https://github.com/username/repository-name.git
This creates a local copy of the repository on your computer.


### Basic Workflow

#### Check status: See which files are modified
- > git status

#### Add changes: Stage files for commit
- > git add filename    # Add specific file
- > git add .           # Add all changes

#### Commit changes: Save your changes to history
- > git commit -m "Your commit message"

#### Push changes: Upload to remote repository
- > git push origin branch-name

#### Pull changes: Download latest changes
- > git pull


## Working with Branches

Create a new branch:
- > git branch branch-name

Switch to a branch:
- > git checkout branch-name

Create and switch in one command:
- > git checkout -b new-branch-name

Merge branches:
- > git merge branch-name


# 🚀 Basic Git Workflow
- > Clone the repository
- > Create a new branch
- > Make changes
- > Add and commit the changes
- > Push the changes to the remote repo
- > Create a pull request / merge branch


# Initial Setup (Only once per machine)

git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# 📁 Repository Commands
| Command                | Description                                              |
| ---------------------- | -------------------------------------------------------- |
| `git init`             | Initialize a new Git repository in the current directory |
| `git clone <repo-url>` | Clone a remote repo to your local machine                |


# 📄 Basic File Operations

| Command                   | Description                                   |
| ------------------------- | --------------------------------------------- |
| `git status`              | Show status of files (modified, staged, etc.) |
| `git add <file>`          | Stage a file for commit                       |
| `git add .`               | Stage all changes                             |
| `git commit -m "message"` | Commit staged changes with a message          |
| `git rm <file>`           | Remove a file from the repo                   |
| `git mv oldname newname`  | Rename or move a file                         |


# 🌲 Branching and Merging
| Command                  | Description                               |
| ------------------------ | ----------------------------------------- |
| `git branch`             | List all branches                         |
| `git branch <name>`      | Create a new branch                       |
| `git checkout <name>`    | Switch to another branch                  |
| `git checkout -b <name>` | Create and switch to a new branch         |
| `git merge <branch>`     | Merge another branch into the current one |
| `git branch -d <name>`   | Delete a branch                           |

# 🔄 Working with Remote Repositories
| Command                       | Description                                |
| ----------------------------- | ------------------------------------------ |
| `git remote -v`               | Show remote URLs                           |
| `git remote add origin <url>` | Add a remote repository                    |
| `git push -u origin <branch>` | Push current branch to remote (first time) |
| `git push`                    | Push changes to remote                     |
| `git pull`                    | Fetch and merge remote changes             |
| `git fetch`                   | Get updates from remote (doesn't merge)    |

# 🕰️ Viewing History
| Command             | Description                                            |
| ------------------- | ------------------------------------------------------ |
| `git log`           | Show commit history                                    |
| `git log --oneline` | Show compact log                                       |
| `git diff`          | Show changes between working directory and last commit |
| `git diff --staged` | Show staged changes                                    |


# 💡 Undo and Fix Mistakes
| Command                   | Description                                                   |
| ------------------------- | ------------------------------------------------------------- |
| `git restore <file>`      | Discard changes in working directory                          |
| `git reset <file>`        | Unstage a staged file                                         |
| `git reset --soft HEAD~1` | Undo last commit but keep changes staged                      |
| `git reset --hard HEAD~1` | Undo last commit and discard changes                          |
| `git revert <commit>`     | Create a new commit that undoes the changes of a previous one |


# 🧪 Stash Changes (Temporarily Save Work)

| Command           | Description                           |
| ----------------- | ------------------------------------- |
| `git stash`       | Save changes temporarily              |
| `git stash apply` | Apply the most recent stashed changes |
| `git stash list`  | List all stashes                      |
| `git stash drop`  | Delete a stash                        |



# Real-World Git Workflow Example
Clone the repo
- > git clone https://github.com/username/project.git
- > cd project
Create a new branch
- > git checkout -b feature-login
Make some changes...
- > git add .
- > git commit -m "feat: add login page"
Push the branch
- > git push -u origin feature-login
