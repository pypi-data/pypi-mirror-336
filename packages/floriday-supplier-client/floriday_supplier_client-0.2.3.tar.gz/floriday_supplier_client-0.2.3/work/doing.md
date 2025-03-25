# Doing

## Goal
Fix the `make release` command to properly handle the force-pushing of the `floriday_api_v2024v2` tag while ensuring version tags are never force-pushed.

## Analysis
When running `make release`, the following error occurs:
```
Updated tag 'floriday_api_v2024v2' (was 579538e)
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/serraict/vine-floriday-python-supplier-api-client.git
 * [new tag]         v0.2.2 -> v0.2.2
 ! [rejected]        floriday_api_v2024v2 -> floriday_api_v2024v2 (already exists)
error: failed to push some refs to 'https://github.com/serraict/vine-floriday-python-supplier-api-client.git'
hint: Updates were rejected because the tag already exists in the remote.
make: *** [release] Error 1
```

The issue is that the `release` target in the makefile is using `git tag -f floriday_api_v$(api_version)` to force-update the tag locally, but when pushing to the remote with `git push origin --tags`, it's not using the force flag. Since the tag already exists on the remote, the push is rejected.

Important note: Version tags (like v0.2.2) should never be force-pushed, only the floriday_api tag should be force-pushed.

## Design
Modify the `release` target in the makefile to:
1. Push the version tags normally (without force)
2. Force-push only the floriday_api tag

This ensures that version tags are preserved while allowing the floriday_api tag to be updated.

## Steps
1. Update the makefile to modify the `release` target to separately push version tags and force-push the floriday_api tag.
2. Test the changes by running `make release`.

## Progress
- [x] Analyzed the issue
- [x] Updated the makefile
- [x] Changes committed with message: "Fix release target to force-push floriday_api tag while preserving version tags"
- [x] Changes pushed to the remote repository
- [ ] Tested the changes

## Testing
To test these changes, you can run:

```bash
make release
```

This should now successfully push both the version tag and the floriday_api tag, with the latter being force-pushed.
