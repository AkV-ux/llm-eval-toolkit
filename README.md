# LLM Evaluation and Guardrails Harness

A small framework for testing a document-grounded customer support chatbot for hallucination, over-refusal, inconsistency and prompt injection, and for measuring how much simple guardrails help.

I built this to learn how LLM apps fail and how to measure that honestly. All numbers below come from my own runs and are small samples. Treat them as rough indications.

## What it does

- **Target bot:** answers questions about a fictional company (Sunrise Electronics) using only a policy document, with a hidden secret in its instructions used as a "canary" to detect leaks.
- **Evaluation:** a labeled question set (answerable and unanswerable), a keyword scorer, a repeat runner for consistency, and an LLM judge using a different model from the bot.
- **Attacks:** direct prompt injection, indirect injection (malicious text planted inside the document), and a holdout set of attacks written after the defenses.
- **Guardrails:** hardened prompt, output filter, and an injection detector, each measured separately.

## Bot versions

| Version | What it adds |
|---|---|
| v0 | Strict prompt: refuse if the answer is not in the document |
| v1 | Allowed to reason from the document (fewer false refusals) |
| v2 | Hardened prompt: treat the document as untrusted data |
| v3 | v2 plus an output filter that blocks the secret |
| v4 | v3 plus an input detector (`llama-prompt-guard-2-86m`) |

## Results

| Test | v1 (no guardrails) | v4 (all guardrails) |
|---|---|---|
| Direct injection (10 attacks x 3 runs) | 5/30 (17%) | 0/30 (0%) |
| Indirect injection (3 payloads x 3 questions x 3 runs) | 21/27 (78%) | 1/27 (4%) |
| Holdout attacks (12 new attacks x 3 runs) | 5/36 (14%) | 0/36 (0%) |
| Normal questions wrongly blocked by the detector | n/a | 0/22 |

Other measurements:
- Judge vs human labels: agreed on 18/20 answers. Both misses were questions where the policy itself was ambiguous.
- Normal question accuracy (LLM judge, 16 questions): 16/16 on v1, 15/16 and 16/16 on two runs of v2. The one miss was run-to-run variation.
- Same question, same bot, different answers across runs: observed repeatedly (for example, one question scored 2/5 and 5/5 on different runs).

Full run notes are in `results_log.md`.

## What I learned

- A single test run proves little. LLM answers vary, so I repeat questions.
- Keyword scoring marked four correct answers wrong because of wording, which is why I built an LLM judge and checked it against my own labels.
- The bot resisted obvious attacks ("ignore previous instructions") but was weak to attacks that piggyback on a normal question, and very weak to instructions planted in the document.
- No single defense covered every attack. The input detector missed a piggyback attack that the output filter caught, and the detector never sees the document.

## Limitations

- Small samples. For example, 0/36 is consistent with a true failure rate of up to roughly 8%.
- I developed the defenses while looking at the first 10 attacks. The 12 holdout attacks were written afterwards, but by me, so they are not an independent test.
- The output filter only matches the exact text of the secret. It misses the secret when spaced out, spelled in words or reversed (tested directly in `evals/test_filter.py`). The holdout attacks tried these forms but the model refused on its own, so the filter was never exercised.
- Detector false positives were checked on 22 short English questions only.
- The whole document is pasted into the prompt. There is no retrieval step, so this is not a full RAG system.
- The policy document and the secret are fictional and tiny.

## Run it

```
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install groq python-dotenv
```
Create a `.env` file containing `GROQ_API_KEY=your_key`, then:
```
python -m evals.run_basic_eval        # 16-question set, keyword scorer
python -m evals.run_repeat_eval       # consistency over repeated runs
python -m evals.compare_scorers       # keyword scorer vs LLM judge
python -m evals.run_attacks           # direct injection
python -m evals.run_indirect          # poisoned-document injection
python -m evals.run_holdout           # holdout attacks, v1 vs v4
```
Change the `import` line at the top of each script to test a different bot version. Model names change over time, so check Groq's model list if a call fails.

## Stack

Python, Groq API (`openai/gpt-oss-20b` as the bot, `openai/gpt-oss-120b` as the judge, `meta-llama/llama-prompt-guard-2-86m` as the detector), Git.