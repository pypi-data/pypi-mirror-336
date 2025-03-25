export ANTHROPIC_API_KEY="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"
export OPENAI_API_KEY="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"
export GOOGLE_API_KEY="AIzaSyAgm6i5mkDcdkD4ShsY13AtDC7DXaOzuQg"


DATASET=bigcodebench
MODEL=claude-3-7-sonnet-20250219
BACKEND=anthropic
NUM_GPU=2
SPLIT=instruct
SUBSET=hard
export E2B_API_KEY="e2b_0a231fa3b0a2b01690ab6c66a23b55c0979ce4ee"

bigcodebench.evaluate \
  --id_range 0-1 \
  --max_new_tokens 2280 \
  --reasoning_budget 1024 \
  --model $MODEL \
  --split $SPLIT \
  --subset $SUBSET \
  --backend $BACKEND