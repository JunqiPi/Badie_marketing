---
name: Claudia daily surf
agent: ../agents/claudia-surf.md
environment_id: ../environments/claudia-surf.yaml
schedule:
  type: cron
  expression: "30 20 * * *"
  timezone: America/Los_Angeles
budget:
  type: limit
  max_list_cost: {amount: "250", currency: USD}
---

开始今天的逛圈。按系统说明里的步骤做，最后交一条小结。
