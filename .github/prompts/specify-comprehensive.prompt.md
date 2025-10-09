---
description: Comprehensive feature specification development framework that prevents implementation gaps and clarification cycles
---

# Comprehensive Feature Specification Development Framework

The user input can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

## Context & Input Analysis
1. **Parse Raw User Request**: Extract core intent from user description
   - Look beyond implementation details to understand business value
   - Identify actors, actions, data, and constraints
   - Separate what user wants from how they described it

2. **Identify Knowledge Gaps**: What's missing from the initial request?
   - Validation specifics, error handling, user messaging, form states
   - Mark as [NEEDS CLARIFICATION] for structured resolution
   - Question assumptions rather than making implementation guesses

## Systematic Clarification Process
3. **Generate Targeted Questions**: Address each ambiguity with specific questions
   - Phone validation: "US format or international?"
   - Field limits: "Maximum character lengths?"
   - Error states: "What message when [constraint] violated?"
   - User feedback: "Loading behavior during [action]?"
   - Success flow: "What confirmation message/behavior?"

4. **Document Clarification Results**: Convert answers into specific requirements
   - Each answer becomes explicit functional requirement
   - Include rationale for business stakeholder understanding
   - Specify exact text, formats, and behaviors

## Multi-Layer Requirement Development
5. **Core Functional Requirements**: What MUST the system do?
   - Start with user-visible behavior (display, interaction, feedback)
   - Add data requirements (storage, retrieval, relationships)
   - Include business rules (constraints, permissions, workflows)

6. **Discovered Requirements Through Implementation Lens**: What gets missed initially?
   - **Form State Management**: Loading, success, error, disabled states
   - **Data Integrity**: Database constraints, API contract specifics
   - **User Experience**: Specific error messages, accessibility needs
   - **Edge Cases**: Network failures, boundary conditions, race conditions
   - **Integration Points**: Component interactions, API field requirements

## Comprehensive Testing Strategy
7. **Multi-Level Test Requirements**: Cover all interaction layers
   - **Unit Level**: Individual functions (validation, serialization, business logic)
   - **API Contract Level**: Endpoint behavior (success/error responses, status codes)
   - **Integration Level**: Frontend-backend flow, error propagation, state management
   - **End-to-End Level**: Complete user workflows, accessibility compliance, cross-browser

8. **Edge Case Enumeration**: What can go wrong?
   - **Network Issues**: Connection failures, timeouts, server errors, partial responses
   - **Input Boundary Conditions**: Empty fields, maximum lengths, special characters, whitespace
   - **Timing Issues**: Concurrent submissions, state changes during interaction
   - **Browser Behavior**: Tab switching, connection loss, rapid clicking, refresh during action

## Error Scenario Completeness
9. **Systematic Error Coverage**: Plan for failure modes
   - **Validation Errors**: Field-specific messages with actionable guidance
   - **Network Errors**: Generic "try again" messaging with data preservation
   - **Server Errors**: Display server-provided error messages appropriately
   - **Business Rule Violations**: Clear explanation of constraint violations
   - **Authorization Errors**: Appropriate user guidance for access issues

## User Experience Specifications
10. **Form Interaction Design**: Define complete user journey
    - **Initial State**: When/where elements appear, initial field states, visibility rules
    - **Validation State**: Real-time vs submit-time validation, error display patterns
    - **Loading State**: Button disable, spinner display, progress indicators
    - **Success State**: Confirmation message, form behavior post-success, next actions
    - **Error State**: Error recovery, data preservation, retry capability

## Implementation Reality Check
11. **Technical Integration Requirements**: What developers actually need
    - **API Contract Details**: Exact response formats, status codes, error structures
    - **Database Design**: Constraints, relationships, indexes, performance implications
    - **Component Architecture**: Props, state management, reusability patterns
    - **Accessibility Compliance**: ARIA labels, test IDs, keyboard navigation, screen reader support

## Quality Assurance Framework
12. **Testability Requirements**: Ensure every requirement is verifiable
    - Each functional requirement must have corresponding test requirement
    - Each error scenario must have specific test case
    - Each user workflow must have end-to-end test coverage
    - Each API endpoint must have contract test with success/failure scenarios

## Documentation & Maintenance
13. **Future-Proofing**: Capture learnings for next iteration
    - **Implementation Discoveries**: What wasn't in original spec but was needed
    - **Process Insights**: What clarification questions prevent implementation delays
    - **Quality Patterns**: What testing approaches catch issues early
    - **User Experience Lessons**: What UX details have biggest impact

## Specification Validation
14. **Completeness Checklist**: Verify nothing critical is missing
    - All user scenarios have measurable acceptance criteria
    - All functional requirements are testable and unambiguous
    - All error paths are specified with exact user messaging
    - All integration points are defined with contract details
    - All accessibility needs are addressed with specific requirements
    - All performance expectations are quantified

## Iterative Refinement Process
15. **Learn and Improve**: Feed implementation experience back into spec
    - Document what was discovered during implementation that wasn't specified
    - Identify specification gaps that caused confusion or delays
    - Extract patterns for better initial specifications
    - Create templates to prevent missing requirement categories

## Output Format
Generate specification with these sections:
- **Clarifications**: Document all Q&A that resolved ambiguities
- **User Scenarios**: Complete workflows with acceptance criteria
- **Functional Requirements**: Comprehensive FR list (basic + discovered)
- **Testing Requirements**: Multi-level TR list covering all scenarios
- **Edge Cases**: Systematic failure mode coverage
- **Implementation Discoveries**: What was learned during development

## Key Insight: The Three-Pass Approach
1. **First Pass**: Write basic functional requirements from user request
2. **Second Pass**: Add discovered requirements from implementation experience
3. **Third Pass**: Systematically check for gaps using framework above

This ensures specifications are **implementation-ready** rather than **implementation-starting-points**, preventing clarification cycles and mid-development discoveries.