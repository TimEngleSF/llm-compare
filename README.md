# LLM Comparison

# Install

Install packages located in requirements.txt

`pip install -r requirements.txt`

# Usage

Run by `python main.py`

# Commands

`exit`

`temp=` sets temp. Use range 0 - 2. Scales according to each models range.

`merge` or `m` followed by a list of words seperated by spaces.

`split` or `s` split a word

## Examples

### Example 1

**INPUT**
`merge water fire`
or
`m water fire`

**OUTPUT**

```
--------------------------------------------------
MODEL          TIME        OUTPUT
--------------------------------------------------
GPT-4 Turbo    0.9224  {'result': ['steam', 'boiling water']}
gpt-4o         0.8000  {'result': ['steam', 'extinguishing']}
Claude 3       1.5220  {'result': ['steam', 'extinguish']}
Llama3 70b     1.3013  {'result': ['steam', 'extinguished']}
```

### Example 2

**INPUT**
`split wood` or `s wood`

**OUTPUT**

```
--------------------------------------------------
MODEL          TIME        OUTPUT
--------------------------------------------------
GPT-4 Turbo    0.8767  {'result': ['tree', 'carving']}
gpt-4o         0.7637  {'result': ['tree', 'plank']}
Claude 3       3.9357  {'result': ['cellulose', 'lignin']}
Llama3 70b     1.4088  {'result': ['plank', 'splinter']}
```
