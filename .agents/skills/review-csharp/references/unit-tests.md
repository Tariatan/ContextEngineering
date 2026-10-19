# C# unit test review

Read from the Instructions section of `SKILL.md` when the change adds or edits tests.

Verify:

- Arrange / Act / Assert structure (comments marking each section are a cheap, high-value readability aid)
- meaningful assertions (not just "doesn't throw")
- proper mocking — mock only what you don't own or what's genuinely expensive/nondeterministic
- naming convention: `MethodUnderTest_Scenario_ExpectedOutcome`
- if the codebase already names mock fields `[nameOfMockedThing]Mock`, follow that convention for new tests rather than introducing a different one
