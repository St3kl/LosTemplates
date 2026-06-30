# 07_Git_and_Version_Control.md

# LosTemplates Git & Version Control Guide

**Project:** LosTemplates
**Version:** 0.3.0
**System:** Git + GitHub (recommended)

---

# 1. Purpose

This document defines how Git is used in the LosTemplates project.

It ensures:

* Clean commit history
* Safe collaboration
* Easy rollback
* Structured feature development
* Reliable releases

---

# 2. Repository Structure

Main branches:

```text id="gtr1aa"
main
develop
```

Optional supporting branches:

```text id="qwe882"
feature/*
fix/*
hotfix/*
release/*
```

---

# 3. Branch Strategy

## Main Branch (main)

* Production-ready code
* Always stable
* Only merged from `release/` or approved PRs

---

## Develop Branch (develop)

* Integration branch
* Contains latest completed features
* Used for staging/testing

---

## Feature Branches

Used for new features:

```text id="ftr123"
feature/cart-system
feature/paystack-integration
feature/download-system
```

Created from:

```bash id="brc1"
git checkout -b feature/feature-name develop
```

---

## Fix Branches

Used for bug fixes:

```text id="fix123"
fix/cart-total-bug
fix/login-error
```

---

## Hotfix Branches

Used for critical production issues:

```text id="hot1"
hotfix/payment-failure
```

Created from:

```bash id="hot2"
git checkout -b hotfix/issue main
```

---

## Release Branches

Used for preparing production releases:

```text id="rel1"
release/1.0.0
```

---

# 4. Commit Standards

Each commit must be:

* Small
* Focused
* Descriptive

## Format

```text id="cmt1"
type: short description
```

## Types

* feat → new feature
* fix → bug fix
* refactor → code restructuring
* docs → documentation changes
* style → formatting only
* test → adding tests

---

## Examples

```text id="cmtex1"
feat: add shopping cart system

fix: resolve duplicate order creation

refactor: simplify checkout logic

docs: update development workflow guide
```

---

# 5. Commit Rules

* One logical change per commit
* No mixed features
* No unrelated fixes in same commit
* Commit early and often

---

# 6. Git Workflow (Daily)

```bash id="daily1"
git pull origin develop

git checkout -b feature/new-feature

# work on feature

git add .

git commit -m "feat: implement new feature"

git push origin feature/new-feature
```

Then open a pull request into `develop`.

---

# 7. Merge Strategy

## Feature → Develop

* Requires review
* Must pass tests
* Must not break existing features

## Develop → Main

* Only after full testing
* Tagged release version required

---

# 8. Version Tagging

Use semantic versioning:

```text id="ver1"
MAJOR.MINOR.PATCH
```

Examples:

```text id="ver2"
v1.0.0
v1.1.0
v1.1.1
```

### Tagging Command

```bash id="tag1"
git tag v1.0.0

git push origin v1.0.0
```

---

# 9. Rollback Strategy

If something breaks:

### Step 1: Identify last stable commit

```bash id="rb1"
git log
```

### Step 2: Revert

```bash id="rb2"
git revert <commit_id>
```

OR hard reset (only in local/dev):

```bash id="rb3"
git reset --hard <commit_id>
```

---

# 10. Conflict Resolution

When conflicts occur:

1. Identify conflicting files
2. Open file manually
3. Choose correct changes
4. Remove conflict markers
5. Re-test application
6. Commit resolution

---

# 11. Git Ignore Rules

Always include `.gitignore`:

```text id="gi1"
venv/
__pycache__/
db.sqlite3
.env
*.pyc
media/
```

---

# 12. Safe Push Rules

Before pushing:

* Run migrations
* Run server locally
* Check dashboard
* Verify cart & checkout
* Ensure no broken URLs

---

# 13. Release Process

```text id="relflow"
feature complete → develop → release branch → main → tag version
```

Steps:

1. Merge features into `develop`
2. Create `release/x.x.x`
3. Fix last issues
4. Merge into `main`
5. Tag release
6. Deploy

---

# 14. Hotfix Process

For production issues:

1. Create hotfix from `main`
2. Fix issue
3. Test locally
4. Merge into `main`
5. Merge into `develop`
6. Tag patch version

---

# 15. Collaboration Rules

* Never push directly to `main`
* Never force push shared branches
* Always use pull requests
* Always review code before merging

---

# 16. Commit Hygiene

Good habits:

* Write meaningful messages
* Avoid "final fix", "update", "stuff"
* Keep commits atomic
* Use consistent prefixes

---

# 17. Git History Quality

A good history should:

* Tell a story of development
* Be easy to navigate
* Allow rollback at any point
* Be readable by new developers

---

# 18. Summary

Git is the backbone of LosTemplates development. A disciplined Git workflow ensures:

* Stability
* Scalability
* Collaboration
* Professional-grade development

Every feature, fix, and release must follow this structure.

---

# Revision History

| Version | Date      | Changes                            |
| ------- | --------- | ---------------------------------- |
| 0.3.0   | June 2026 | Initial Git workflow documentation |
