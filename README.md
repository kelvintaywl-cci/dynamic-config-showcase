# dynamic-config-showcase

Showcasing how to "work with" [Dynamic Configuration](https://circleci.com/docs/dynamic-config) on CircleCI.


## About

Currently, this project simulates the scenario where:

- This is a monorepo.
- We have separate workflows to trigger based on folders changed (via [the path-filtering Orb](https://circleci.com/developer/orbs/orb/circleci/path-filtering)).
- We want to use GitHub branch protection rules, for pull requests (PRs).

<img width="403" alt="Screen Shot 2022-08-27 at 9 19 16" src="https://user-images.githubusercontent.com/2164346/187006304-33a4d0bb-cca9-4c0e-ae6a-281dceefd3a9.png">


## Problems

The main challenge:

> We cannot merge some pull requests because the GitHub branch protection rules expects all listed workflows to run.
> However, depending on the folders modified, some workflows would not necessarily run.

## Solution

This setup deploys a solution where:

- All listed workflows (and their jobs) will **always run**.
- However, depending on the folders changed, jobs [exit early](https://circleci.com/docs/configuration-reference#ending-a-job-from-within-a-step) if it is not relevant.

By ensuring all workflows run, all jobs in the workflows are reported back to GitHub.

By exiting early for non-relevant jobs, these jobs are still "green" (successful).

You can see this in action in https://github.com/kelvintaywl-cci/dynamic-config-showcase/pull/6 where we only run repo_c workflow effectively when repo-c folder is modified;
All other jobs in the other workflows exited early.

## Explanation

This monorepo has 3 repos, namely _repo-a_, _repo-b_ and _repo-c_.

Our continued configuration is over at [_.circleci/next.yml_](.circleci/next.yml).

In _.circleci/next.yml_, we have 3 workflows, named _repo_a_, _repo_b_ and _repo_c_.
Each workflow is meant for the individial repos then.

For each job in the workflows, we:

- inject pipeline parameters as env vars
- define the job's `parameters.for` to indicate which repo it is relevant for
- allow job to continue **ONLY IF**:
   * the relevant pipeline parameter is truthy (e.g., `pipeline.parameters.repo_b = true` when job's `parameters.for = repo_b`)

## Additional

Ideally, we could have simplified the `exit-early-if-irrelevant` command:

```diff
commands:
  exit-early-if-irrelevant:
    parameters:
      for:
        type: enum
        enum:
          - repo_a
          - repo_b
          - repo_c
    steps:
-     - run:
-         name: stop early unless relevant
-         command: |
-           export RELEVANT=$(eval echo "\$<< parameters.for >>")
-           if [ "${RELEVANT}" = "1" ]; then
-             echo "continuing, since job is for << parameters.for >>"
-           else
-             echo "stopping early!"
-             circleci-agent step halt
-           fi
-         environment:
-           repo_a: << pipeline.parameters.repo_a >>
-           repo_b: << pipeline.parameters.repo_b >>
-           repo_c: << pipeline.parameters.repo_c >>
+     - unless:
+         condition: << pipeline.parameters.<< parameters.for >> >>
+         steps:
+           - run: |
+               circleci-agent step halt
```

**However**, it seems not possible to inject a `<<>>` within another `<<>>` for CircleCI's [mustache](http://mustache.github.io/) implementation.


I have constructed repo_a workflow to be slightly different.

It is a simpler, and is a simpler alternative to using the common `exit-early-if-irrelevant` command.
This may be an option if you are okay with not using a common/reusable command;
In other words, you would copy and paste the exit-early command for each job, and modify accordingly.
