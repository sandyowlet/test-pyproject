# GitFlow Workflow

This project follows the GitFlow branching model, which provides a robust framework for managing larger projects.

This guide explains how the administrators of this project use GitFlow to manage the development process. If you are a developer, please refer to the [CONTRIBUTING.md](../CONTRIBUTING.md) file for instructions on how to create a feature branch and submit a pull request.

## Branch Structure

- **main**: Production code that has been released
- **develop**: Main development branch where features are integrated
- **feature/\***: Feature branches for new functionality
- **release/v\***: Release branches for preparing new production releases
- **hotfix/\***: Hotfix branches for urgent production fixes

## Workflow

### Feature Development

The developers should refer to the [CONTRIBUTING.md](../CONTRIBUTING.md) file for instructions on how to create a feature branch and submit a pull request.

Once the administrators receive a pull request review, they should:

1. Check if the pull request meets the [Pull Request Guidelines](../CONTRIBUTING.md#pull-request-guidelines).
2. Check if the pull request passes the necessary checks in the CI/CD pipeline.
3. If CI/CD pipeline checks pass, approve the pull request and merge it into the `develop` branch.
   - If the admin choose to squash the commits, they should handle the commit message carefully, because the commit messages will be used to generate the version and change log.

### Preparing a Release

1. When `develop` has accumulated enough features for a release, create a release branch:

   ```bash

   # 1. Determine the next version
   cz bump --get-next

   # Output: X.Y.Z

   # 2. Create the release branch

   # Using git-flow
   git flow release start vX.Y.Z

   # Using standard git
   git checkout -b release/vX.Y.Z develop

   # 3. Push the release branch.
   git push origin release/vX.Y.Z
   ```

   Then the CI/CD pipeline will auto create a bump commit for the release

2. On this branch, only bug fixes, documentation, and release-oriented tasks should be committed
3. When the release is ready, finish the release:

   ```bash
   # Using git-flow
   git flow release finish vX.Y.Z

   # Using standard git
   git checkout main
   git merge --no-ff release/vX.Y.Z
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git checkout develop
   git merge --no-ff release/vX.Y.Z
   git branch -d release/vX.Y.Z
   ```

   This will merge the release into both `main` and `develop`, and create a tag for the release

   Then the CI/CD pipeline will be triggered to build and publish the release

### Hotfixes

1. If a critical issue is found in production, create a hotfix branch from `main`:

   ```bash
   # Using git-flow
   git flow hotfix start vX.Y.Z

   # Using standard git
   git checkout main
   git pull
   git checkout -b hotfix/vX.Y.Z
   ```

2. Fix the issue with minimal changes
3. When complete, finish the hotfix:

   ```bash
   # Using git-flow
   git flow hotfix finish vX.Y.Z

   # Using standard git
   git checkout main
   git merge --no-ff hotfix/vX.Y.Z
   git tag -a vX.Y.Z -m "Hotfix vX.Y.Z"
   git checkout develop
   git merge --no-ff hotfix/vX.Y.Z
   git branch -d hotfix/vX.Y.Z
   ```

   This will merge the hotfix into both `main` and `develop`, and create a tag for the hotfix

## Automated Workflows

The project includes GitHub Actions workflows that automate the GitFlow process:

1. **Continuous Integration**: Runs on all branches to ensure code quality
2. **Release Flow**: Handles release and hotfix branches, preparing them for production
3. **Production Release**: Manages the final release process when code is merged to main

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

Release branch and tag names should follow the format `vX.Y.Z` (e.g., `v1.2.3`).
