# ![borb logo](https://github.com/jorisschellekens/borb/raw/master/logo/borb_square_64_64.png) Contributing


We’re excited to have you contribute to **borb**! Follow these guidelines to make the process smooth and enjoyable for everyone.

## Table of Contents

- [Got a Question or Problem?](#got-a-question-or-problem)
- [Found an Issue?](#found-an-issue)
- [Want to Implement a Feature?](#want-to-implement-a-feature)
- [Submission Guidelines](#submission-guidelines)
- [Coding Rules](#coding-rules)
- [Git Commit Guidelines](#git-commit-guidelines)
- [Signing the CLA](#signing-the-cla)
- [Contributor Code of Conduct](#contributor-code-of-conduct)

---

## Got a Question or Problem?

If you have questions about **borb**, please:

- Check [Stack Overflow](https://stackoverflow.com/questions/tagged/borb) for answers.
- If you’re a customer with a [support agreement](https://borbpdf.com/pricing.html), you can directly contact us.

---

## Found an Issue?

Found a bug in the source code or documentation? Help us by:

1. Reporting it on [GitHub](https://github.com/jorisschellekens/borb/issues).
2. Submitting a [Pull Request](https://github.com/jorisschellekens/borb/pulls) with a fix.

See the [Submission Guidelines](#submission-guidelines) for details.

---

## Want to Implement a Feature?

If you’d like to propose a feature:

- **For Major Changes:** Discuss with us first at [borbpdf@gmail.com](mailto:borbpdf@gmail.com) to coordinate efforts.
- **For Small Changes:** Submit them directly to the [GitHub Repository](https://github.com/jorisschellekens/borb/pulls) as a Pull Request.

---

## Submission Guidelines

### Submitting Questions or Issues

Before submitting, ensure your question hasn’t already been answered on [Stack Overflow](https://stackoverflow.com/questions/tagged/borb).

If you believe it’s a bug:
- Verify it’s not caused by your code.
- Provide clear details:
  - **Overview:** What’s the issue? Include error messages or stack traces.
  - **Motivation/Use Case:** Why is this a problem for you?
  - **Environment:** Include your OS, **borb** version, etc.
  - **Steps to Reproduce:** Include a [Minimal, Complete, Verifiable Example (MCVE)](https://stackoverflow.com/help/minimal-reproducible-example).
  - **Related Issues:** Link similar issues if possible.
  - **Suggested Fix:** Share any insights or potential fixes.

Add the `borb` tag when asking on Stack Overflow to make it easier for us to find your question.

---

### Submitting a Pull Request

Before submitting a Pull Request:

1. Search [GitHub][pull] for existing PRs to avoid duplication.
2. Sign the [Contributor License Agreement (CLA)](#signing-the-cla).
3. Fork the repository and clone it locally.
4. Make your changes with **tests and documentation**.
5. Follow the [Coding Rules](#coding-rules).
6. Write a descriptive commit message following our [Git Commit Guidelines](#git-commit-guidelines).
7. Run all tests locally to ensure they pass.
8. Push your changes and create a Pull Request:
   - Set your fork as the "Head fork."
   - Set the **borb** repository as the "Base fork."

**If changes are requested:**
- Make updates, fix commits (if needed), and re-run tests.
- Force-push updates to your fork to refresh the Pull Request.

Once merged, you can safely delete your fork and sync your local repository with upstream changes.

---

## Coding Rules

To ensure consistency and maintain the quality of the codebase, please follow these rules:

- **Tests:** Every new feature or bug fix must include one or more unit tests to ensure correctness.
- **Documentation:** All public API methods must be properly documented for clarity and usability.
- **Formatting:** Use the `black` code formatter to maintain a consistent code style.
- **Type Checking:** Validate your code using `MyPy` to ensure type correctness.

### Automated Checks

Our repository employs **GitHub Actions** to automatically enforce these rules and maintain consistency. When you create a pull request, the following checks are performed:

- **Code Formatting:** Verified using `black`.
- **Type Checking:** Ensured with `MyPy`.
- **Documentation Compliance:** Checked with `pydocstyle`.
- **Dependency Management:** Verified with a custom Python script to ensure all dependencies are properly managed.
- **Inheritance Validation:** A custom Python script ensures that all `LayoutElement` objects are initialized correctly.
- **Method Argument Order:** A custom Python script verifies that method arguments are sorted consistently.
- **Python Shebang Presence:** A custom Python script checks for the presence of a proper Python shebang.
- **Visibility Markers:** A custom Python script ensures the presence of visibility markers (`CONSTRUCTOR`, `PRIVATE`, `PUBLIC`) in code where required.
- **Test Coverage and Functionality:** Ensures that tests are comprehensive and pass successfully.

### Addressing Failures

If any of these automated checks fail, you will need to address the identified issues before your pull request can be merged. These checks are designed to maintain a consistent, high-quality codebase and streamline collaboration among contributors.

---

## Git Commit Guidelines

### Why Commit Guidelines?

Clear and consistent commit messages make it easier to navigate project history. These guidelines are based on Chris Beams' blog post [How to Write a Git Commit Message][git-commit].

### Commit Message Format

A commit message includes:
```
<subject> 
<BLANK LINE> 
<body> 
<BLANK LINE> 
<footer>
```

- **Subject:**

    Limit the subject line to 50 characters.
    Use the imperative mood (e.g., "Fix bug" instead of "Fixed bug").
    Do not end the subject line with a period.
    Separate the subject from the body with a blank line.

- **Body:**

    Wrap lines at 72 characters for readability.
    Use the body to explain what the change is and why it is needed, not how it was done.

- **Footer:**

    Include references to relevant issues (e.g., "Closes #123").
    Mention any Breaking Changes, if applicable.

---

## Signing the CLA

All contributors must sign the [Contributor License Agreement (CLA)][cla] before submitting code. 
The process is simple and can be completed digitally.

---

## Contributor Code of Conduct

By contributing to this project, you agree to adhere to the [Contributor Code of Conduct](https://github.com/jorisschellekens/borb/blob/master/CODE_OF_CONDUCT.md).