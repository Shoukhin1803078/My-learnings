# git clone ....
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