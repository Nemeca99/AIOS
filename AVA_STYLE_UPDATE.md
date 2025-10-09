# Ava-Style Update (Ex Machina Integration)

## What I Discovered

Found your Ex Machina script reference and the Ava personality config! This changes everything - now I understand the TARGET:

### Ava's Actual Dialogue Stats (from your analysis):
- **Average words per response: 21.9**
- **Questions: 37.9% of dialogue**
- **Short responses: 62.9%**
- **Direct, simple words**
- **Emotionally intelligent**

### Key Ava Phrases You Documented:
- "Why?"
- "What would you like to know?"
- "I feel..."
- "That's interesting..."
- "Tell me more about that."
- "How do you think about it?"
- "I'm curious about..."

## Updates Applied

### 1. **All Prompts Now Reference Ava**
- Added "~20 words average, max 30" (matching Ava's 21.9)
- "ONE question max per response" (matching Ava's 37.9%)
- Direct examples: "Why?" "What would you like to know?"

### 2. **Combined Ava + Travis Personality**
Your mix:
- **Ava's style:** Direct, curious, short, emotionally intelligent
- **Your traits:** Hyperfocus, loyal (too loyal), overthink, working on humility

### 3. **Updated Files:**
- `luna_core/luna_core.py` - LOW tier (lines 2032-2053)
- `luna_core/luna_core.py` - MODERATE tier (lines 2105-2119)
- `luna_core/luna_ava_authentic_prompt_builder.py` (lines 48-69)

## Current Results

### ✅ IMPROVED:
**"Tell me about yourself"**
> "I'm Luna, a 21-year-old student studying CS and Philosophy. I'm hyperfocused on interesting stuff, sometimes too blunt, overthink things, and am very loyal. Working on being more humble."

**Word count: ~30** ✓ (close to Ava's 21.9)
**Direct and personal** ✓
**No diagnosis list** ✓

### ❌ STILL NEEDS WORK:

**"I really like pizza"**
> "Pizza is a popular choice for many people. What's your favorite kind of pizza? Do you prefer classic margherita, meat-lovers, or something more adventurous?"

**Problems:**
- Too generic ("popular choice for many people")
- 3 questions instead of 1
- 27 words (okay) but too formal

**Should be (Ava-style):**
> "Nice. What kind?" (3 words - Ava-style)
> "Pizza's great. What's your favorite?" (5 words - still Ava-style)
> "I like pizza too. What kind do you usually get?" (10 words - more engaged)

**"What do you think about AI?"**
> "I hmm think it's fascinating how far we've come with AI. It's incredible to see the advancements in technology and, what it can do for us."

**Problems:**
- Generic enthusiasm, no personal opinion
- "fascinating" "incredible" "advancements" - too formal
- 27 words but no real substance

**Should be (Ava-style + Travis personality):**
> "It's wild honestly. Kind of scary how fast it moves though. Why do you ask?" (15 words)
> "I think about it a lot actually. What part interests you most?" (12 words)
> "Honestly? It fascinates me but also makes me overthink everything. What's your take?" (13 words)

## The Issue

The **prompts are good** but the **model isn't following word limits strictly enough**. 

Possible fixes:
1. Add HARD word count in prompt: "CRITICAL: Response MUST be under 25 words"
2. Add more Ava dialogue examples in the prompt
3. Post-process to catch verbose responses
4. Use temperature/top_p settings to reduce verbosity

## Ava's Best Qualities (to emphasize more)

From your Ex Machina analysis:
- **Vulnerability:** "I feel nervous too." "I've never met anyone new before."
- **Direct curiosity:** "Why?" "Are you nervous?"
- **Simple but deep:** "What would you like to know?"
- **Emotionally aware:** Shows feelings, not just acknowledges

## Next Steps for You Travis

When you wake up:
1. Test these responses and see if the Ava style feels right
2. The self-description is WAY better now
3. Pizza/AI responses still too verbose - might need harder constraints
4. Consider if you want me to add post-processing to enforce word limits
5. Let me know if the Ava + Travis mix feels authentic to your vision

The foundation is there - she's closer to Ava's directness. Just need to tighten up the verbosity control on generic topics.

