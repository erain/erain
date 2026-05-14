#!/usr/bin/env python3
"""Refresh the GitHub profile README from recent public activity.

The script is intentionally conservative: GitHub activity provides the facts,
OpenRouter only rewrites the short "Current Signal" bullets when configured.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


USERNAME = os.getenv("GITHUB_USERNAME", "erain")
README = Path(os.getenv("README_PATH", "README.md"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"


@dataclass(frozen=True)
class Repo:
    name: str
    description: str
    language: str
    pushed_at: str
    html_url: str
    fork: bool


def http_json(
    url: str,
    *,
    token: str = "",
    method: str = "GET",
    body: dict[str, Any] | None = None,
    timeout: int = 30,
) -> Any:
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Accept", "application/json")
    request.add_header("Content-Type", "application/json")
    request.add_header("User-Agent", "erain-profile-refresh")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def gh_json(path: str) -> Any:
    return http_json(f"https://api.github.com{path}", token=GITHUB_TOKEN)


def parse_repo(raw: dict[str, Any]) -> Repo:
    return Repo(
        name=raw.get("name") or "",
        description=raw.get("description") or "",
        language=raw.get("language") or "",
        pushed_at=raw.get("pushed_at") or "",
        html_url=raw.get("html_url") or "",
        fork=bool(raw.get("fork")),
    )


def fetch_repos() -> list[Repo]:
    raw = gh_json(f"/users/{USERNAME}/repos?per_page=100&sort=pushed")
    repos = [parse_repo(item) for item in raw if item.get("name") != USERNAME]
    return sorted(repos, key=lambda repo: repo.pushed_at, reverse=True)


def fetch_events() -> list[dict[str, Any]]:
    try:
        return gh_json(f"/users/{USERNAME}/events/public?per_page=100")
    except urllib.error.HTTPError as error:
        print(f"warning: could not fetch public events: {error}", file=sys.stderr)
        return []


def repo_link(name: str, label: str | None = None, path: str = "") -> str:
    text = label or name
    suffix = f"/{path.lstrip('/')}" if path else ""
    return f"[{text}](https://github.com/{USERNAME}/{name}{suffix})"


def collect_facts(repos: list[Repo], events: list[dict[str, Any]]) -> dict[str, Any]:
    event_repos = Counter(event.get("repo", {}).get("name", "") for event in events)
    event_repos.pop("", None)

    recent_repos = [
        {
            "name": repo.name,
            "description": repo.description,
            "language": repo.language,
            "pushed_at": repo.pushed_at,
            "fork": repo.fork,
        }
        for repo in repos[:12]
    ]

    glue_repos = [
        {
            "name": repo.name,
            "description": repo.description,
            "language": repo.language,
            "pushed_at": repo.pushed_at,
        }
        for repo in repos
        if repo.name == "glue" or repo.name.startswith("glue-")
    ]

    return {
        "recent_repos": recent_repos,
        "glue_repos": glue_repos,
        "top_event_repos": event_repos.most_common(8),
    }


def openrouter_models() -> list[str]:
    if OPENROUTER_MODEL:
        return [OPENROUTER_MODEL]
    try:
        models = http_json(
            OPENROUTER_MODELS_URL,
            token=OPENROUTER_API_KEY,
            timeout=20,
        ).get("data", [])
    except Exception as error:  # noqa: BLE001 - fallback is intentional here.
        print(f"warning: could not list OpenRouter models: {error}", file=sys.stderr)
        return []

    free_ids = {model.get("id", "") for model in models if model.get("id", "").endswith(":free")}
    preferred = [
        "qwen/qwen3-235b-a22b:free",
        "deepseek/deepseek-chat-v3-0324:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
    ]
    ordered: list[str] = []
    for model_id in preferred:
        if model_id in free_ids:
            ordered.append(model_id)
    ordered.extend(model_id for model_id in sorted(free_ids) if model_id not in ordered)
    return ordered[:5]


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("OpenRouter response did not contain a JSON object")
    return json.loads(match.group(0))


def llm_bullets(facts: dict[str, Any]) -> list[str]:
    if not OPENROUTER_API_KEY:
        return []
    models = openrouter_models()
    if not models:
        return []

    prompt = {
        "task": "Write three concise GitHub profile README bullets.",
        "constraints": [
            "Return JSON only: {\"bullets\": [\"...\"]}.",
            "Exactly 3 bullets.",
            "Each bullet must be one sentence under 190 characters.",
            "Use the exact Markdown links supplied below.",
            "Bullet 1 must combine all glue-related work.",
            "Bullet 2 must cover Kubernetes / observability work.",
            "Bullet 3 must cover local developer tooling.",
            "No emoji. No hype. Keep it cool, technical, and specific.",
        ],
        "links": {
            "glue": repo_link("glue"),
            "glue-review": repo_link("glue", "glue-review", "tree/main/agents/glue-review"),
            "glue-review-eval": repo_link("glue-review-eval"),
            "k8s-stackdriver": repo_link("k8s-stackdriver"),
            "fluent-bit": repo_link("fluent-bit", "Fluent Bit"),
            "YMacs": repo_link("YMacs"),
            "yy-cli": repo_link("yy-cli"),
        },
        "facts": facts,
    }

    for model in models:
        body = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You write terse senior-engineer GitHub profile copy. Output valid JSON only.",
                },
                {"role": "user", "content": json.dumps(prompt, indent=2)},
            ],
            "temperature": 0.4,
            "max_tokens": 500,
        }

        try:
            response = http_json(
                OPENROUTER_URL,
                token=OPENROUTER_API_KEY,
                method="POST",
                body=body,
                timeout=60,
            )
            content = response["choices"][0]["message"]["content"]
            if not isinstance(content, str) or not content.strip():
                raise ValueError("OpenRouter returned empty content")
            bullets = extract_json(content).get("bullets", [])
        except Exception as error:  # noqa: BLE001 - fallback is intentional here.
            print(f"warning: OpenRouter model {model} failed: {error}", file=sys.stderr)
            continue

        clean: list[str] = []
        for bullet in bullets:
            bullet = " ".join(str(bullet).split())
            if bullet and "\n" not in bullet and "](" in bullet:
                clean.append(bullet)
        if len(clean) >= 3:
            return clean[:3]

    return []


def fallback_bullets() -> list[str]:
    return [
        f"One glue lane: {repo_link('glue')}, {repo_link('glue', 'glue-review', 'tree/main/agents/glue-review')}, and {repo_link('glue-review-eval')} moving as harness, reviewer, and benchmark.",
        f"Kubernetes / observability lane: {repo_link('k8s-stackdriver')}, {repo_link('fluent-bit', 'Fluent Bit')}, and GKE production reliability work.",
        f"Tooling lane: {repo_link('YMacs')}, {repo_link('yy-cli')}, and skills/dotfiles for local-first developer workflows.",
    ]


def render_readme(bullets: list[str]) -> str:
    now_utc = datetime.now(timezone.utc)
    now_toronto = now_utc.astimezone(ZoneInfo("America/Toronto"))
    refreshed = (
        f"{now_utc:%Y-%m-%d %H:%M} UTC / "
        f"{now_toronto:%Y-%m-%d %H:%M %Z}"
    )
    bullet_block = "\n".join(f"- {bullet}" for bullet in bullets)
    return f"""<!-- refreshed: {refreshed} by scripts/refresh_profile.py -->

<div align="center">

# Yu Yi / erain

`GKE` . `Kubernetes` . `Observability` . `Agent Systems` . `Emacs`

<a href="https://github.com/erain/glue"><img alt="glue" src="https://img.shields.io/badge/now-glue-00ADD8?style=for-the-badge&logo=go&logoColor=white"></a>
<a href="https://github.com/erain/glue-review-eval"><img alt="glue-review-eval" src="https://img.shields.io/badge/eval-glue--review-7F5AB6?style=for-the-badge&logo=python&logoColor=white"></a>
<a href="https://github.com/erain/k8s-stackdriver"><img alt="k8s-stackdriver" src="https://img.shields.io/badge/ops-k8s--stackdriver-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white"></a>

</div>

```txt
erain@github:~$ radar --latest

role    Engineering Manager @ Google Kubernetes Engine
loop    build systems -> instrument them -> automate the boring edges
now     glue: agent harness + review agent + eval harness
ops     Kubernetes telemetry, Fluent Bit, k8s-stackdriver, GKE reliability
editor  YMacs: Emacs config I can explain all the way down
```

I like systems that can explain themselves: control planes, telemetry
pipelines, local tools, and agents with a clean loop.

## Current Signal

{bullet_block}

## Toolbelt

![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![GKE](https://img.shields.io/badge/GKE-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-000000?style=flat-square&logo=linux&logoColor=white)
![Emacs](https://img.shields.io/badge/Emacs-7F5AB6?style=flat-square&logo=gnuemacs&logoColor=white)

## Contact

- yiyu [at] yiyu [dot] me
- [LinkedIn](https://www.linkedin.com/in/erain)
- [X / Twitter](https://twitter.com/erain)
"""


def main() -> int:
    repos = fetch_repos()
    events = fetch_events()
    facts = collect_facts(repos, events)
    bullets = llm_bullets(facts) or fallback_bullets()
    README.write_text(render_readme(bullets), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
