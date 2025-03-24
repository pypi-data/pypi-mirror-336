from eval_mm.utils.azure_client import OpenAIChatAPI
from collections import defaultdict
import numpy as np
from eval_mm.metrics.scorer import Scorer, AggregateOutput
import re
import json


def parse_score(llm_output: str) -> dict | None:
    json_pattern = r"```json(.*?)```"
    matches = re.findall(json_pattern, llm_output, re.DOTALL)

    if not matches:
        # Fallback: Try to find any JSON-like content in the output
        json_pattern = r"\{.*?\}"
        matches = re.findall(json_pattern, llm_output, re.DOTALL)

    for json_string in matches:
        json_string = json_string.strip()
        try:
            parsed_json = json.loads(json_string)
            return parsed_json
        except json.JSONDecodeError:
            # Attempt to fix common JSON issues
            try:
                # Remove invalid control characters
                json_string_clean = re.sub(r"[\x00-\x1F\x7F]", "", json_string)
                parsed_json = json.loads(json_string_clean)
                return parsed_json
            except json.JSONDecodeError:
                continue  # Try next match

    return {"score": -1, "score_gpt": -1}


INSTRUCTION = """
You are an expert evaluator. You are given the following information:
- Context: A description of the image.
- Question: A question about the image.
- GPT-4o Answer: GPT-4o's answer to the question.
- Model Answer: The target model's answer to the question.

Your task is to evaluate each answer independently based on how well it answers the question given the context.

Please assign a score from 1 to 10 for each answer according to the following guideline:
- 10: Perfect — Completely correct, relevant, and fully addresses the question based on the context.
- 8-9: Very Good — Mostly correct with only minor inaccuracies or slight omissions.
- 6-7: Good — Generally correct but contains noticeable errors or lacks important details.
- 4-5: Poor — Significant errors or missing key points, but some relevance remains.
- 1-3: Very Poor — Mostly or completely incorrect, irrelevant, or nonsensical.

Output Format (JSON):
Return the result in the following JSON format:
```json
{{
    "score_gpt": int,
    "score": int
}}
```
Do not output anything other than the JSON.

Input:
{{
    "context": {context},
    "question": {question},
    "gpt4o_answer": {gpt4o_answer},
    "model_answer": {model_answer}
}}

Output:
"""


def ask_gpt4_batch(
    content_list: str, max_tokens: int, async_client: OpenAIChatAPI, model_name: str
) -> list:
    message_list = [
        [
            {
                "role": "system",
                "content": "You are a helpful and precise assistant for checking the quality of the answer.",
            },
            {"role": "user", "content": content},
        ]
        for content in content_list
    ]
    completions = async_client.batch_generate_chat_response(
        message_list,
        max_tokens=max_tokens,
        temperature=0,
        seed=0,
        model_name=model_name,
    )
    return completions


class HeronBenchScorer(Scorer):
    @staticmethod
    def score(refs, preds: list[str], **kwargs) -> list[dict[str, int]]:
        docs = kwargs["docs"]
        client = kwargs["client"]
        judge_model = kwargs["judge_model"]
        contents = []
        for doc, ref, pred in zip(docs, refs, preds):
            content = INSTRUCTION.format(
                context=doc["context"],
                question=doc["input_text"],
                gpt4o_answer=ref,
                model_answer=pred,
            )
            contents.append(content)
        completions = ask_gpt4_batch(contents, 1024, client, judge_model)
        scores = [parse_score(completion) for completion in completions]
        assert len(scores) == len(docs)
        return scores

    @staticmethod
    def aggregate(scores: list[dict[str, int]], **kwargs) -> AggregateOutput:
        docs = kwargs["docs"]
        category_list = ["conv", "detail", "complex"]
        heron_metrics = defaultdict(float)
        for category in category_list:
            score_owns = [
                score["score"]
                for score, doc in zip(scores, docs)
                if doc["category"] == category
            ]
            score_gpts = [
                score["score_gpt"]
                for score, doc in zip(scores, docs)
                if doc["category"] == category
            ]
            if len(score_owns) == 0 or np.mean(score_owns) == -1:
                continue
            avg_score = np.mean(score_owns)
            avs_score_rel = (
                100
                * np.mean(score_owns)
                / max(
                    0.01, np.mean(score_gpts)
                )  # divide by 0.01 when 0 division happens
            )
            heron_metrics[category] = avg_score
            heron_metrics[category + "_rel"] = avs_score_rel
        heron_metrics["parse_error_count"] = sum(
            score["score"] == -1 for score in scores
        )
        heron_metrics["overall"] = sum([score["score"] for score in scores]) / len(
            scores
        )
        heron_metrics["overall_rel"] = sum(
            [heron_metrics[category + "_rel"] for category in category_list]
        ) / len(category_list)
        output = AggregateOutput(
            overall_score=heron_metrics["overall_rel"],
            details=heron_metrics,
        )
        return output


def test_heron_bench_scorer():
    from eval_mm.utils.azure_client import MockChatAPI

    refs = ["私は猫です。"]
    preds = ["私は犬です。"]
    docs = [{"context": "hoge", "input_text": "fuga", "category": "conv"}]
    scores = HeronBenchScorer.score(
        refs, preds, docs=docs, client=MockChatAPI(), judge_model="gpt-4o-2024-05-13"
    )
    assert scores == [{"score": -1, "score_gpt": -1}]
    output = HeronBenchScorer.aggregate(scores, docs=docs)
    assert output.overall_score == 0.0
    assert output.details == {
        "parse_error_count": 1,
        "overall": -1.0,
        "conv_rel": 0.0,
        "detail_rel": 0.0,
        "complex_rel": 0.0,
        "overall_rel": 0.0,
    }


if __name__ == "__main__":
    from datasets import load_dataset

    ds = load_dataset("Silviase/Japanese-Heron-Bench", split="train")
    ds = ds.rename_column("text", "input_text")
    # the 102th problem
    ds = ds.select(range(100, 102))
    pred_texts = [
        "画像から判断すると、制限速度は50 km/hのようです。道路標識に「50」と表示されています。",
        "画像に写っている標識によると、現在地からニセコまでは12kmです。",
    ]
    refs = [doc["answer"]["gpt-4-0125-preview"] for doc in ds]
    client = OpenAIChatAPI()
    judge_model = "gpt-4o-2024-05-13"
    scores = HeronBenchScorer.score(
        refs, pred_texts, docs=ds, client=client, judge_model=judge_model
    )
    print(scores)

    output = HeronBenchScorer.aggregate(scores, docs=ds)
    print(output)
