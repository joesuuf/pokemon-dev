# Pull Request Creation Guide

**Date:** November 1, 2025
**Version:** 1.0.0

---

## Overview

This document provides step-by-step instructions for creating the pull request(s) to integrate the security agent planning documentation into the repository.

---

## PR Strategy

### Option 1: Single Documentation PR (Recommended)

**Description**: One PR containing all planning documentation

**Pros**:
- Easy to review as a cohesive whole
- Clear approval process
- Single merge point

**Cons**:
- Large PR size
- All docs must be finalized

**Use When**: Documentation is complete and ready for review

---

### Option 2: Multi-PR Strategy

**Description**: Separate PRs for different aspects

**PRs**:
1. **PR #1**: Core planning docs (INDEX, COMPLETE-INTEGRATION-PLAN)
2. **PR #2**: Technical docs (JSON-COMM, ARCHITECTURE)
3. **PR #3**: Implementation docs (MIGRATION-PLAN, PRIORITIES)
4. **PR #4**: Operational docs (DELIVERABLES, PR-GUIDE)

**Pros**:
- Smaller, focused reviews
- Can proceed in parallel
- Incremental approval

**Cons**:
- More overhead
- Need to coordinate order
- May have dependencies

**Use When**: Need faster initial reviews or docs at different stages of readiness

---

## Recommended Approach: Single PR

For this planning documentation, we recommend **Option 1: Single Documentation PR**.

---

## Step-by-Step Instructions

### Step 1: Verify Current Branch

Ensure you're on the correct feature branch:

```bash
git branch
# Should show: * claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb
```

If not on the correct branch:

```bash
git checkout claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb
```

---

### Step 2: Review Changes

Verify all documentation files are present:

```bash
ls -la docs-int-plan--security-agent/
```

Expected files:
- INDEX.md
- COMPLETE-INTEGRATION-PLAN.md
- PROPOSED-JSON-COMM-STRUCTURE.md
- INTEGRATION-ARCHITECTURE.md
- STEP-BY-STEP-MIGRATION-PLAN.md
- IMPLEMENTATION-PRIORITIES.md
- DELIVERABLES-AND-SUCCESS-CRITERIA.md
- PR-CREATION-GUIDE.md

Check git status:

```bash
git status
```

---

### Step 3: Stage Files in Logical Order

Stage files in order of importance/reading order:

```bash
# 1. Index first (entry point)
git add docs-int-plan--security-agent/INDEX.md

# 2. Complete plan (main reference)
git add docs-int-plan--security-agent/COMPLETE-INTEGRATION-PLAN.md

# 3. Core technical docs
git add docs-int-plan--security-agent/PROPOSED-JSON-COMM-STRUCTURE.md
git add docs-int-plan--security-agent/INTEGRATION-ARCHITECTURE.md

# 4. Implementation docs
git add docs-int-plan--security-agent/STEP-BY-STEP-MIGRATION-PLAN.md
git add docs-int-plan--security-agent/IMPLEMENTATION-PRIORITIES.md

# 5. Operational docs
git add docs-int-plan--security-agent/DELIVERABLES-AND-SUCCESS-CRITERIA.md
git add docs-int-plan--security-agent/PR-CREATION-GUIDE.md
```

Verify staging:

```bash
git status
```

All files should be green (staged).

---

### Step 4: Create Commit

**Commit Message Format**:

```
docs: add security agent integration planning documentation

Add comprehensive planning documentation for integrating the security
agent into the modular framework with standardized JSON communication.

Documentation includes:
- Complete integration plan
- JSON communication structure and schemas
- System architecture and design patterns
- Step-by-step migration plan (6 phases)
- Implementation priorities and timeline (3 weeks)
- Deliverables and success criteria
- PR creation guide

This planning documentation prepares for:
- Extracting 7 modular security skills
- Creating 4 security workflows
- Implementing standardized JSON agent outputs
- Enabling inter-agent communication
- Maintaining backward compatibility

Related to: #[ISSUE_NUMBER]
```

**Create the commit**:

```bash
git commit -m "docs: add security agent integration planning documentation

Add comprehensive planning documentation for integrating the security
agent into the modular framework with standardized JSON communication.

Documentation includes:
- Complete integration plan
- JSON communication structure and schemas
- System architecture and design patterns
- Step-by-step migration plan (6 phases)
- Implementation priorities and timeline (3 weeks)
- Deliverables and success criteria
- PR creation guide

This planning documentation prepares for:
- Extracting 7 modular security skills
- Creating 4 security workflows
- Implementing standardized JSON agent outputs
- Enabling inter-agent communication
- Maintaining backward compatibility"
```

---

### Step 5: Push to Remote

Push to the feature branch:

```bash
git push -u origin claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb
```

If this is a retry, the branch may already exist. Verify with:

```bash
git branch -r | grep claude/integrate-security-agent
```

If push fails due to network errors, retry up to 4 times with exponential backoff:

```bash
# First attempt
git push -u origin claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb

# If failed, wait 2 seconds and retry
sleep 2
git push -u origin claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb

# If failed, wait 4 seconds and retry
sleep 4
git push -u origin claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb

# If failed, wait 8 seconds and retry
sleep 8
git push -u origin claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb
```

---

### Step 6: Create Pull Request

**Using GitHub CLI** (if available):

```bash
gh pr create \
  --title "docs: Security Agent Integration Planning Documentation" \
  --body-file docs-int-plan--security-agent/.github/pr-body.md \
  --base main \
  --head claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb
```

**Using GitHub Web Interface**:

1. Navigate to repository on GitHub
2. Click "Pull requests" tab
3. Click "New pull request"
4. Set base branch to `main` (or default branch)
5. Set compare branch to `claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb`
6. Click "Create pull request"
7. Fill in PR details (see below)

---

## PR Title

```
docs: Security Agent Integration Planning Documentation
```

**Format**: `<type>: <description>`
- Type: `docs` (documentation)
- Description: Clear, concise summary

---

## PR Description

Use this template:

```markdown
## Summary

This PR adds comprehensive planning documentation for integrating the security agent into the modular framework with standardized JSON communication based on Anthropic best practices as of November 2025.

## Documentation Structure

The planning documentation is organized in 8 files:

1. **INDEX.md** - Navigation hub and quick reference
2. **COMPLETE-INTEGRATION-PLAN.md** - Complete plan in one document
3. **PROPOSED-JSON-COMM-STRUCTURE.md** - JSON schemas and communication patterns
4. **INTEGRATION-ARCHITECTURE.md** - System architecture and component design
5. **STEP-BY-STEP-MIGRATION-PLAN.md** - Detailed 6-phase implementation plan
6. **IMPLEMENTATION-PRIORITIES.md** - 3-week timeline with priorities and resources
7. **DELIVERABLES-AND-SUCCESS-CRITERIA.md** - What we're delivering and success metrics
8. **PR-CREATION-GUIDE.md** - This guide for creating PRs

## What This Plan Covers

### High-Level Goals
- ✅ Integrate security agent into modular framework
- ✅ Establish standardized JSON communication for all agents
- ✅ Create 7 modular security skills
- ✅ Build 4 composable security workflows
- ✅ Maintain backward compatibility

### Technical Details
- **JSON Schemas**: Base agent output, security findings, inter-agent messages
- **Communication Library**: Message passing between agents
- **Validation**: JSON schema validation for all outputs
- **Skills**: XSS scanner, CSRF validator, CORS checker, CSP analyzer, TS/Python standards, dead code detector
- **Workflows**: Full audit, mobile attack scan, standards check, dead code cleanup

### Timeline
- **Week 1**: Core infrastructure & skills extraction
- **Week 2**: Agent integration & testing
- **Week 3**: Polish & production readiness
- **Total**: 3 weeks, 90-200 hours depending on team size

### Success Criteria
- All outputs conform to standardized JSON schema
- 100% test coverage for new components
- No performance regression
- 100% adoption by Week 16

## Changes Made

### New Directory
```
docs-int-plan--security-agent/
├── INDEX.md                                    (Navigation & quick ref)
├── COMPLETE-INTEGRATION-PLAN.md                (Complete 400+ page plan)
├── PROPOSED-JSON-COMM-STRUCTURE.md             (Schemas & communication)
├── INTEGRATION-ARCHITECTURE.md                 (Architecture & design)
├── STEP-BY-STEP-MIGRATION-PLAN.md              (6 phases, detailed tasks)
├── IMPLEMENTATION-PRIORITIES.md                (Timeline, priorities, resources)
├── DELIVERABLES-AND-SUCCESS-CRITERIA.md        (Deliverables & acceptance)
└── PR-CREATION-GUIDE.md                        (PR instructions)
```

### Files Changed
- Created: 8 documentation files
- Modified: None (pure addition)
- Deleted: None

## Why This Matters

### Current State
- Security agent exists as standalone `/security-agent/`
- No standardized JSON communication between agents
- Manual integration required for agent orchestration

### Future State (After Implementation)
- Security agent fully integrated into `/agents/` framework
- All agents produce standardized JSON outputs
- Agents can automatically exchange data
- Skills are reusable and composable
- Workflows enable complex multi-agent operations

### Benefits
1. **Standardization**: All agents follow same patterns
2. **Interoperability**: Agents can communicate seamlessly
3. **Reusability**: Skills can be mixed and matched
4. **Maintainability**: Modular, testable components
5. **Scalability**: Easy to add new skills and workflows

## Next Steps

After this planning documentation is approved:

1. **Week 1**: Implement JSON schemas and extract security skills
2. **Week 2**: Build modular security agent and integrate
3. **Week 3**: Polish, optimize, and prepare for production
4. **Week 4+**: Deploy, monitor adoption, gather feedback

## Review Checklist

Reviewers, please verify:

- [ ] Planning approach is sound
- [ ] Architecture makes sense
- [ ] Timeline is realistic
- [ ] Success criteria are clear
- [ ] Documentation is comprehensive
- [ ] No major gaps or issues identified

## Questions for Reviewers

1. Does the 3-week timeline seem realistic?
2. Are there any architectural concerns?
3. Should we adjust priorities or scope?
4. Are success criteria appropriate?
5. Any other feedback or concerns?

## Related Issues

- Related to: #[ISSUE_NUMBER] (if exists)

## References

- **Anthropic Best Practices**: https://www.anthropic.com/research/building-effective-agents
- **JSON Schema**: http://json-schema.org/
- **Existing Security Agent**: `/security-agent/`
- **Modular Framework**: `/agents/`

---

**Type**: Documentation
**Priority**: High
**Estimated Review Time**: 30-60 minutes (skim all docs)
**Estimated Implementation Time**: 3 weeks (after approval)
```

---

## Reviewers

### Required Reviewers

Add these reviewers to the PR:

1. **Tech Lead** - Architecture and technical review
2. **Engineering Manager** - Resource and timeline approval
3. **Security Lead** - Security-specific review
4. **Product Manager** - Business alignment

### Optional Reviewers

5. **Senior Engineers** - Technical feedback
6. **DevOps Lead** - CI/CD integration review
7. **QA Lead** - Testing strategy review

---

## Labels

Add these labels to the PR:

- `documentation`
- `planning`
- `security-agent`
- `high-priority`
- `needs-review`

---

## PR Checklist

Before submitting, verify:

### Content
- [ ] All 8 documentation files created
- [ ] No broken internal links
- [ ] No typos or major errors
- [ ] Consistent formatting
- [ ] Examples are clear

### Git
- [ ] On correct feature branch
- [ ] All files staged
- [ ] Commit message follows conventions
- [ ] Pushed to remote
- [ ] No merge conflicts

### PR
- [ ] Title is clear and follows convention
- [ ] Description is comprehensive
- [ ] Reviewers added
- [ ] Labels added
- [ ] Linked to related issues

---

## Review Process

### Expected Timeline

| Stage | Duration | Owner |
|-------|----------|-------|
| **Initial Review** | 1-2 days | Reviewers |
| **Feedback & Discussion** | 1-2 days | Team |
| **Revisions** | 1 day | Author |
| **Final Approval** | 1 day | Tech Lead |
| **Merge** | Immediate | Tech Lead |
| **Total** | **4-6 days** | |

### Review Focus Areas

**Reviewers should focus on**:
1. **Completeness**: Are all aspects covered?
2. **Clarity**: Is the plan clear and understandable?
3. **Feasibility**: Is the timeline realistic?
4. **Soundness**: Is the technical approach solid?
5. **Alignment**: Does this align with our goals?

**Reviewers should NOT focus on**:
- Minor typos (can be fixed later)
- Formatting details (as long as readable)
- Perfect wording (good enough is fine)

---

## Handling Feedback

### If Feedback is Minor

Example: Typos, formatting, clarifications

**Action**: Make changes directly in PR
1. Pull latest from branch
2. Make changes
3. Commit with: `docs: address review feedback`
4. Push to same branch
5. Comment on PR with changes made

### If Feedback is Major

Example: Architectural concerns, scope changes, timeline adjustments

**Action**: Discuss first, then revise
1. Respond to comments with questions/clarifications
2. Schedule sync meeting if needed
3. Reach consensus on changes
4. Update documentation
5. Request re-review

### If Feedback Requires Scope Change

Example: "This is too ambitious", "We need to add X", "Remove Y"

**Action**: Update plan and get re-approval
1. Discuss with team and stakeholders
2. Update affected documents
3. Update timeline and priorities
4. Update success criteria
5. Request comprehensive re-review

---

## Merge Strategy

### When to Merge

Merge when:
- [ ] All required reviewers approved
- [ ] All discussions resolved
- [ ] No merge conflicts
- [ ] CI checks passing (if any)
- [ ] Stakeholder sign-off obtained

### How to Merge

**Preferred Method**: Squash and merge

**Reason**: Keeps main branch history clean

**Steps**:
1. Click "Squash and merge" button
2. Edit commit message if needed
3. Confirm merge
4. Delete feature branch (optional)

**Alternative Method**: Regular merge

Use if: Commit history is valuable

---

## After Merge

### Immediate Actions

1. **Verify Merge**
   ```bash
   git checkout main
   git pull origin main
   ls docs-int-plan--security-agent/
   ```

2. **Notify Team**
   - Post in #security-agent-integration Slack channel
   - Email security-agent-team@company.com
   - Update project board

3. **Update References**
   - Update any links pointing to PR
   - Add to project documentation index
   - Update roadmap/timeline

### Next Steps

1. **Schedule Kickoff** - Plan Week 1 work
2. **Allocate Resources** - Assign team members
3. **Create Tasks** - Break down Phase 1 into tasks
4. **Set Up Infrastructure** - Repos, boards, channels
5. **Begin Implementation** - Start Phase 1!

---

## Troubleshooting

### Push Failed

**Error**: `! [rejected] ... (fetch first)`

**Solution**:
```bash
git pull --rebase origin claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb
git push -u origin claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb
```

### Branch Name Error

**Error**: `403 Forbidden` when pushing

**Cause**: Branch name doesn't match required pattern

**Solution**: Branch MUST start with `claude/` and end with session ID
- Correct: `claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb`
- Incorrect: `security-agent-integration`

### Merge Conflicts

**Error**: "This branch has conflicts that must be resolved"

**Solution**:
```bash
git checkout claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb
git fetch origin main
git merge origin/main
# Resolve conflicts in files
git add <resolved-files>
git commit -m "docs: resolve merge conflicts"
git push origin claude/integrate-security-agent-011CUhexCxHke2zNNNGED3ogb
```

### PR Not Showing

**Issue**: Created PR but can't find it

**Check**:
1. Correct repository?
2. Correct branch names?
3. Already merged?
4. Check closed PRs
5. Check draft PRs

---

## Best Practices

### For Authors

1. **Review before submitting** - Read through all docs
2. **Check links** - Verify internal links work
3. **Test examples** - Ensure code examples are correct
4. **Be responsive** - Respond to feedback promptly
5. **Ask questions** - Clarify feedback if unclear

### For Reviewers

1. **Review promptly** - Don't block progress
2. **Be constructive** - Suggest improvements
3. **Focus on value** - Don't nitpick minor issues
4. **Ask questions** - Clarify anything unclear
5. **Approve when ready** - Don't hold up good-enough work

### For Everyone

1. **Communicate** - Keep team informed
2. **Collaborate** - Work together on solutions
3. **Be flexible** - Plans may need adjustment
4. **Stay positive** - We're building something great!
5. **Celebrate** - Acknowledge progress and wins

---

## Example Commands Summary

```bash
# 1. Verify branch
git branch

# 2. Stage files in order
git add docs-int-plan--security-agent/INDEX.md
git add docs-int-plan--security-agent/COMPLETE-INTEGRATION-PLAN.md
git add docs-int-plan--security-agent/PROPOSED-JSON-COMM-STRUCTURE.md
git add docs-int-plan--security-agent/INTEGRATION-ARCHITECTURE.md
git add docs-int-plan--security-agent/STEP-BY-STEP-MIGRATION-PLAN.md
git add docs-int-plan--security-agent/IMPLEMENTATION-PRIORITIES.md
git add docs-int-plan--security-agent/DELIVERABLES-AND-SUCCESS-CRITERIA.md
git add docs-int-plan--security-agent/PR-CREATION-GUIDE.md

# 3. Create commit
git commit -m "docs: add security agent integration planning documentation

Add comprehensive planning documentation for integrating the security
agent into the modular framework with standardized JSON communication.

Documentation includes:
- Complete integration plan
- JSON communication structure and schemas
- System architecture and design patterns
- Step-by-step migration plan (6 phases)
- Implementation priorities and timeline (3 weeks)
- Deliverables and success criteria
- PR creation guide

This planning documentation prepares for:
- Extracting 7 modular security skills
- Creating 4 security workflows
- Implementing standardized JSON agent outputs
- Enabling inter-agent communication
- Maintaining backward compatibility"

# 4. Push to remote
git push -u origin claude/integrate-security-agent-011CUhexCxHke2zNNGED3ogb

# 5. Create PR (use web interface with provided title and description)
```

---

## Success!

If you've followed this guide, you should now have:
- ✅ Clean commit with all documentation
- ✅ Changes pushed to feature branch
- ✅ Pull request created with comprehensive description
- ✅ Reviewers assigned
- ✅ Labels added

**Next**: Wait for reviews and respond to feedback!

---

**Questions?** Ask in #security-agent-integration or email the team.

**Good luck!** 🚀
