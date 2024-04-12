#!/bin/bash

read -p 'Enter user.name for git config: ' name
read -p 'Enter user.email for git config: ' email

git config --global user.name $name
git config --global user.email $email

# Initialize the repository
echo '############################# Initializing repository #############################'
git init
git add .
git commit -m "feat!: 🎉 cookiecutter scaffold"

# Install pre-commit hooks
echo '############################# Installing pre-commit #############################'
pre-commit install
