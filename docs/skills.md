# 🛠️ Skills Reference

## Built-in Skills

These are always available. The agent selects them automatically based on the task.

| Skill | Description |
|---|---|
| `table_info` | Get metadata: shape, columns, dtypes, missing values, sample rows |
| `filter_rows` | Filter rows using a pandas query expression |
| `select_columns` | Select a subset of columns |
| `aggregate` | Group by and aggregate (sum, mean, count, max, min…) |
| `sort_table` | Sort rows by one or more columns |
| `merge_tables` | Join two tables (inner / left / right / outer) |
| `pivot_table` | Create a pivot table |
| `add_column` | Add a computed column via pandas eval expression |
| `describe_stats` | Descriptive statistics (mean, std, quartiles…) |
| `find_values` | Find rows matching a value or regex pattern |
| `drop_duplicates` | Remove duplicate rows |
| `rename_columns` | Rename columns |
| `sample_rows` | Get a random sample of N rows |
| `value_counts` | Count unique values in a column |
| `correlation_matrix` | Pearson correlation matrix for numeric columns |
| `head_rows` | Get the first N rows |

## Code Tool

Enable **Code Tool** in the toolbar to add a 17th skill: `execute_python`.

The agent can write arbitrary pandas code executed in an AST-checked sandbox:

- **Allowed libraries:** `pandas` (`pd`), `numpy` (`np`), `math`, `re`, `json`, `collections`, `itertools`, `datetime`, `statistics`, `functools`
- **Blocked:** `os`, `sys`, `subprocess`, `socket`, and any network or filesystem module
- **Table access:** each uploaded table is pre-loaded by ID (e.g. `r_abc123`) and by sanitised name (e.g. `sales_2023`)
- **Output:** assign a DataFrame to `result` to produce a new table; use `print()` for intermediate output

## Custom Skills

Add your own skills from the **Skills** sidebar panel.

### Prompt mode

Write a system prompt template. Placeholders:

| Placeholder | Replaced with |
|---|---|
| `{table_name}` | Name of the selected table |
| `{user_request}` | The invocation instruction from the agent |

A 30-row preview of the table is automatically appended as context.

### Code mode

Write Python code that runs in the same sandbox as Code Tool. Access tables via the `tables` dict:

```python
df = tables[tid]['df']   # tid is the table ID string
result = df.groupby('region')['profit'].sum().reset_index()
```

### Skill Learning

After completing non-trivial tasks (≥ 3 tool calls), TabClaw automatically reviews the interaction and may create a new custom skill. Learned skills appear with a 🧠 badge in the chat and are immediately available for future tasks. You can view, edit, or delete them from the Skills panel.
