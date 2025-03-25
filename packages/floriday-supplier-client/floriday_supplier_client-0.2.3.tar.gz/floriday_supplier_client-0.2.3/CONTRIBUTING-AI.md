# AI Contributing Guide

This document provides guidance for AI agents working on the Floriday Supplier API Client project.

## Finding Work Items

To identify the next item to work on, follow these steps:

1. Check the GitHub project board for prioritized issues:

   ```bash
   # List all projects in the organization
   gh project list --owner serraict
   
   # View the Floriday Supplier Python Client project (project #3)
   gh project item-list 3 --owner serraict --format json
   ```

2. Look for issues with the status "Next" - these are the highest priority items to work on.

3. Issues in "Backlog" status are planned for future work but not immediate priorities.

4. Issues in "Inbox" status are new and need to be triaged.

## Workflow

1. Once you've identified the next work item, update the `work/doing.md` file with:
   - Goal: What you aim to accomplish
   - Analysis: Your understanding of the issue
   - Design: Your proposed solution
   - Steps: The implementation plan
   - Progress: Track your progress

2. Implement the solution following the project's contributing guidelines in CONTRIBUTING.md.

3. Create appropriate commits with descriptive messages.

4. Push your changes to the repository.

## Example

For example, to find that fixing the "Hardcoded Staging URL in Configuration Class" is the next priority:

```bash
gh project item-list 3 --owner serraict --format json
```

This would show that issue #1 "Hardcoded Staging URL in Configuration Class" has status "Next", indicating it's the next item to work on.

## Tips for AI Agents

- Always check the GitHub project board first to identify prioritized work
- Follow the workflow outlined in CONTRIBUTING.md
- Use the `work/doing.md` file to organize your approach to the current task
- Document your work clearly for human collaborators
- Commit changes with descriptive messages
- Execute commands from the root working directory whenever possible
- Add all files that should not be overwritten by swagger codegen to `.swagger-codegen-ignore`
