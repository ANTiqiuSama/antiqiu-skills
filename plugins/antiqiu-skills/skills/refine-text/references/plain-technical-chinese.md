# Plain Chinese Technical Writing

Use this reference for existing Chinese technical material: README files, runbooks, API documentation, engineering proposals, operator messages, error messages, and manuals.

## Boundary

This is a practical Chinese controlled-writing mode. It borrows the general idea of reducing ambiguity from controlled languages, but it is not a translation, implementation, or certification of ASD-STE100 Simplified Technical English.

The source facts and the user's terminology remain authoritative. Improve expression without inventing actors, guarantees, measurements, prerequisites, or failure modes. Preserve code, commands, paths, API fields, log fragments, quoted text, product names, and other literal tokens exactly unless the user asks to change them.

Do not impose fixed character, clause, paragraph, or list quotas. Split or combine text only when doing so improves comprehension, execution, or verification.

## Rewrite method

1. Identify the reader's task or question and the information that must survive unchanged.
2. Separate explanations from procedures. Explanations build understanding; procedures cause an observable action or state change.
3. Choose one preferred name for each concept. Use official product and API names. Define an abbreviation at first use when the audience may not know it.
4. Put conditions before the action they govern. Keep scope, exceptions, uncertainty, and ownership attached to the relevant statement.
5. Prefer a concrete verb over an empty frame when meaning stays the same. For example, prefer “检查日志” to “对日志进行检查.”
6. Name the actor when ownership would otherwise be ambiguous. Do not invent one when the source does not establish it; leave the ambiguity visible if it affects correctness.

## Explanations

- Give each paragraph one main topic. Lead with the decision, definition, conclusion, or relationship that makes the details useful.
- Use a list only for genuinely parallel items. Keep causal or chronological reasoning in prose when a list would hide the relationship.
- Replace unsupported claims such as “充分保障”“显著提升” or “完全解决” with the evidence actually present in the source.
- Remove throat-clearing and editorial narration such as “需要说明的是” when the sentence can state the fact directly.
- Avoid rotating synonyms for the same technical concept. Variety is less important than stable reference.
- Use pronouns only when their referent is unmistakable. Repeat the exact noun when ambiguity would cost the reader time.

## Procedures

- Use numbered steps only when order matters. Use bullets for unordered options, inputs, or checks.
- Start a step with the condition or the action. Make the object and expected observable result clear when the source provides them.
- Put one main action in a step when actions have different failure, retry, rollback, ownership, or verification behavior. Keep tightly coupled actions together when splitting them would add ceremony without helping execution.
- Put commands, paths, configuration keys, and exact error text in code formatting or code blocks. Explain them outside the literal text.
- Keep warnings proportional to evidence. When all parts are known, state the trigger, consequence, and safe response; do not manufacture a warning template for a hypothetical risk.

## Incremental document updates

Before appending new material, reread the affected older sections. Update stale terms, states, numbers, conclusions, and cross-references in place. Remove contradictions and duplicate explanations so the document reads as one current whole, not as a chronological patch log. Respect an explicit request to change only one location.

## Finish

Stop when a reader can identify the relevant fact or action without guessing, terminology is consistent, procedures remain executable, and no source meaning or uncertainty was lost. Do not keep polishing to satisfy a score or a fixed stylistic quota.
