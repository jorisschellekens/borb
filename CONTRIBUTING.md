# Contributing to borb

We'd love for you to contribute to our source code and to make **borb** even better than it is
today! Here are the guidelines we'd like you to follow:

 - [Question or Problem?](#question)
 - [Issues and Bugs](#issue)
 - [New Features](#feature)
 - [Submission Guidelines](#submit)
 - [Coding Rules](#rules)
 - [Commit Message Guidelines](#commit)
 - [Signing the bCLA](#cla)
 - [Contributor Code of Conduct](#coc)


## <a name="question">Got a Question or Problem?</a>

If you have questions about how to use **borb**, please direct these to [Stack Overflow][stackoverflow].

If you are a customer with a [support agreement][support], you also have direct access to our JIRA and/or our developers.


## <a name="issue">Found an Issue?</a>
If you find a bug in the source code or a mistake in the documentation, you can help us by
submitting a [Pull Request][pull] with a fix.

**Please see the [Submission Guidelines](#submit) below**.


## <a name="feature">Want to implement a Feature?</a>
If you would like to implement a new feature then consider what kind of change it is:

* **Major Changes** that you wish to contribute to the project should be discussed first so that we can better
coordinate our efforts, prevent duplication of work, and help you to craft the change so that it is successfully
accepted into the project. Contact us at [borbpdf@gmail.com](mailto:borbpdf@gmail.com).
* **Small Changes** can be crafted and submitted to the [GitHub Repository][github] as a [Pull Request][pull].


## <a name="submit">Submission Guidelines</a>

### Submitting a Question or an Issue
Before you submit your question or issue, search [Stack Overflow][stackoverflow], maybe your question was already answered.

If your issue appears to be a bug, and hasn't been reported, ask a question on [Stack Overflow][stackoverflow] to verify that is indeed a bug and not a mistake in your own code.
Help us to maximize the effort we can spend fixing issues and adding new
features, by not reporting duplicate issues. Providing the following information will increase the
chances of your issue being dealt with quickly:

* **[How to ask good questions][good-questions]**
* **Overview of the Issue** - if an error is being thrown a non-minified stack trace helps
* **Motivation for or Use Case** - explain why this is a bug for you
* **borb Version(s)** - is it a regression?
* **Operating System** - is this a problem on Windows or Linux, maybe on Mac?
* **Reproduce the Error** - provide a [Short, Self Contained, Correct (Compilable), Example][sscce], also known as a [Minimal, Complete, and Verifiable example][mcve].
* **Related Issues** - has a similar issue been reported before?
* **Suggest a Fix** - if you can't fix the bug yourself, perhaps you can point to what might be
  causing the problem (line of code or commit)
* **Tag the question** - add the tag `borb` to your question so we can find it.

### Submitting a Pull Request
Before you submit your pull request consider the following guidelines:

* Search [GitHub][pull] for an open or closed Pull Request
  that relates to your submission. You don't want to duplicate effort.
* Verify that your proposed change hasn't already been addressed in the develop branch.
* Don't send a separate pull request for every single file you change.  
* Please sign the [borb Contributor License Agreement (bCLA)](#cla) before sending pull
  requests. We cannot accept code without this agreement.
* Fork the borb repository on GitHub.
* Clone your borb fork to your local machine.
* Make your changes, **including appropriate test cases**.
* Follow our [Coding Rules](#rules).
* Commit your changes using a descriptive commit message that follows our
  [commit message conventions](#commit-message-format).
* Now would be a good time to fix up your commits (if you want or need to) with `git rebase --interactive`.
* Build your changes locally to ensure all the tests pass.
* Push your changes to your GitHub account.
* Create a pull request in GitHub.
"Head fork" should be your repository, and the "base fork" should be the borb official repository.
* If we suggest changes then:
  * Make the required updates.
  * Fix up your commits if needed, with an interactive rebase.
  * Re-run the tests and make sure that they are still passing.
  * Force push to your GitHub repository. This will update your Pull Request.

That's it! Thank you for your contribution!

#### After your pull request is merged

After your pull request is merged, you can safely delete your fork and pull the changes
from the main (upstream) repository.


## <a name="rules">Coding Rules</a>
To ensure consistency throughout the source code, keep these rules in mind as you are working:

* All features or bug fixes **must be tested** by one or more unit tests.
* All public API methods **must be documented**.
* All code must be **formatted using black**.
* All code must be **type-checked using MyPy**.


## <a name="commit">Git Commit Guidelines</a>

We have guidelines on how our git commit messages should be formatted. This leads to **more
readable messages** that are easy to follow when looking through the **project history**.

These guidelines were taken from Chris Beams' blog post [How to Write a Git Commit Message][git-commit].

### Commit Message Format
Each commit message consists of a **subject**, a **body** and a **footer**:

```
<subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

Any line of the commit message should not be longer 72 characters! This allows the message to be easier
to read on GitHub as well as in various git tools.

### Subject
The subject contains succinct description of the change:

* [Separate subject from body with a blank line][git-commit-separate]
* [Limit the subject line to 50 characters][git-commit-limit-50]
* [Capitalize the subject line][git-commit-capitalize]
* [Do not end the subject line with a period][git-commit-end]
* [Use the imperative mood in the subject line][git-commit-imperative]

### Body
* [Wrap the body at 72 characters][git-commit-wrap-72]
* [Use the body to explain _what_ and _why_ vs. _how_][git-commit-why-not-how]

### Footer
The footer contains any information about **Breaking Changes** and is also the place to
reference JIRA or GitHub issues that this commit **Closes**.


## <a name="cla">Signing the bCLA</a>

Please sign the [**borb Contributor License Agreement (bCLA)**][cla] before sending pull requests. For any code changes to be accepted, the bCLA must be signed. It's a quick process, we promise!

We'll need you to [(digitally) sign and then email, fax or mail the form][cla].


## <a name="coc">Contributor Code of Conduct</a>
Please note that this project is released with a [Contributor Code of Conduct][coc]. By participating in this project you agree to abide by its terms.

We use the [Stack Exchange][stackoverflow] network for free support and [GitHub][github] for code hosting. By using these services, you agree to abide by their terms:

* StackExchange: [http://stackexchange.com/legal](http://stackexchange.com/legal)
* Github: [https://help.github.com/articles/github-terms-of-service/](https://help.github.com/articles/github-terms-of-service/)

[cla]: https://github.com/jorisschellekens/borb/BORB_CONTRIBUTOR_LICENSE_AGREEMENT.md
[coc]: CODE_OF_CONDUCT.md
[support]: https://borbpdf.com/
[github]: https://github.com/jorisschellekens/borb
[pull]: https://github.com/jorisschellekens/borb/pulls
[sscce]: http://sscce.org/
[stackoverflow]: https://stackoverflow.com/questions/tagged/borb
[good-questions]: https://stackoverflow.com/help/how-to-ask
[mcve]: https://stackoverflow.com/help/mcve
[git-commit]: https://chris.beams.io/posts/git-commit/
[git-commit-separate]: https://chris.beams.io/posts/git-commit/#separate
[git-commit-limit-50]: https://chris.beams.io/posts/git-commit/#limit-50
[git-commit-capitalize]: https://chris.beams.io/posts/git-commit/#capitalize
[git-commit-end]: https://chris.beams.io/posts/git-commit/#end
[git-commit-imperative]: https://chris.beams.io/posts/git-commit/#imperative
[git-commit-wrap-72]: https://chris.beams.io/posts/git-commit/#wrap-72
[git-commit-why-not-how]: https://chris.beams.io/posts/git-commit/#why-not-how