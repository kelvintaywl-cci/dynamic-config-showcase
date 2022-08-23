# dynamic-config-showcase

Showcasing features and limitations of Dynamic Config.

Currently, this repo showcases how to use:

- path-filtering
- adding a "done" job for all continued workflows
- setting GitHub branch protection rule to look for "done"

## Brief

In this setup, we have a mono-repo with 2 main folders:

- repo-a
- repo-b

The goal is that we run specific workflows for the different folders.

**Any other changes outside of these 2 folders** would trigger another "no-op" workflow.

This "no-op" workflow will also have a final "done" job.

This way, the GitHub branch protection rule will pass when either of the 3 workflows run "done" job successfully.
