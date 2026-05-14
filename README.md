<!-- refreshed: 2026-05-13 22:06 EDT / 2026-05-14 UTC from public GitHub activity -->

<div align="center">

# Yu Yi / erain

`GKE` . `Kubernetes` . `Observability` . `Agent Systems` . `Emacs`

<a href="https://github.com/erain/glue-review-eval"><img alt="glue-review-eval" src="https://img.shields.io/badge/now-glue--review--eval-7F5AB6?style=for-the-badge&logo=python&logoColor=white"></a>
<a href="https://github.com/erain/glue"><img alt="glue" src="https://img.shields.io/badge/building-glue-00ADD8?style=for-the-badge&logo=go&logoColor=white"></a>
<a href="https://github.com/erain/k8s-stackdriver"><img alt="k8s-stackdriver" src="https://img.shields.io/badge/hardening-k8s--stackdriver-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white"></a>

<img alt="profile ticker" src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=18&duration=2400&pause=700&color=00ADD8&center=true&vCenter=true&width=760&lines=control+planes+%2B+telemetry+%2B+agent+loops;measuring+code-review+agents%2C+not+vibes;small+tools%2C+sharp+edges%2C+clean+systems">

</div>

```txt
erain@github:~$ radar --latest

role     Engineering Manager @ Google Kubernetes Engine
loop     build systems -> instrument them -> automate the boring edge cases
now      glue-review-eval: benchmark harness for the glue-review agent
ship     glue: Go agent harness, provider plumbing, review agent, live CI
ops      k8s-stackdriver, Fluent Bit, Kubernetes telemetry, reliability work
editor   YMacs: Emacs config I can understand all the way down
```

I like systems that can explain themselves: control planes, telemetry
pipelines, local tools, and agents with a clean loop.

## Current Signal

- Building [glue-review-eval](https://github.com/erain/glue-review-eval): an eval harness with realistic Go/Python/TypeScript host projects, planted-bug PR cases, sidecar ground truth, structural recall, LLM-as-judge, and downstream fix-success scoring.
- Hardening [glue](https://github.com/erain/glue): a Go agent harness with provider-agnostic loops, sessions, roles, skills, typed tools, prompt catalogs, provider failover, and OpenAI-compatible provider adapters.
- Shipping [glue-review](https://github.com/erain/glue/tree/main/agents/glue-review): a single-purpose PR review agent tuned to produce one GitHub comment that human reviewers and coding agents can both use.
- Keeping Kubernetes observability sharp through [k8s-stackdriver](https://github.com/erain/k8s-stackdriver), [Fluent Bit](https://github.com/erain/fluent-bit), and GKE production reliability work.

## Latest Drops

| When | Repo | Drop |
| --- | --- | --- |
| 2026-05-13 EDT / 2026-05-14 UTC | [glue-review-eval](https://github.com/erain/glue-review-eval) | Eval repo launched: 28 benchmark cases, prompt iteration tooling, OpenRouter runs, and a v3 diagnosis path for `glue-review`. |
| 2026-05-13 EDT / 2026-05-14 UTC | [glue](https://github.com/erain/glue) | Fixed OpenRouter live tests, tightened CI behavior, and kept the review-agent dogfood loop moving. |
| 2026-05-12 | [k8s-stackdriver](https://github.com/erain/k8s-stackdriver) | Merged Makefile recipe quoting hardening and opened Stackdriver event-sink resource attribution hardening upstream. |
| 2026-05-07 | [glue](https://github.com/erain/glue) | Landed the `0.x` surface refresh: provider registry, failover, typed tool helpers, fs/git tools, prompt catalog, stop reasons, and standard CLI flags. |
| 2026-05-05 | [YMacs](https://github.com/erain/YMacs) | Refreshed my Emacs config for an Emacs 29.1+ baseline and terminal-friendly workflows. |

## Active Tracks

| Track | Repos | Current edge |
| --- | --- | --- |
| Review agents | [glue](https://github.com/erain/glue), [glue-review-eval](https://github.com/erain/glue-review-eval) | Prompt versions, benchmark cases, fix instructions, provider failover, and CI dogfooding. |
| Agent tooling | [yy-cli](https://github.com/erain/yy-cli), [pi-mono](https://github.com/erain/pi-mono), [google-skills](https://github.com/erain/google-skills) | Local-first coding agents, skills, LLM APIs, and practical dev loops. |
| Kubernetes systems | [gke-mcp](https://github.com/erain/gke-mcp), [jobset](https://github.com/erain/jobset), [agent-sandbox](https://github.com/erain/agent-sandbox) | GKE automation, distributed workloads, and isolated agent runtimes. |
| Observability | [k8s-stackdriver](https://github.com/erain/k8s-stackdriver), [fluent-bit](https://github.com/erain/fluent-bit), [monitoring-dashboard-samples](https://github.com/erain/monitoring-dashboard-samples) | Event attribution, log pipelines, metrics adapters, and production signal quality. |
| Daily driver | [YMacs](https://github.com/erain/YMacs), [dotfiles](https://github.com/erain/dotfiles) | Fast editor loops, terminal ergonomics, and configs that stay explainable. |

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
