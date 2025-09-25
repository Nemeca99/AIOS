import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# Load the model and tokenizer
model_name = "EleutherAI/gpt-neo-2.7B"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPTNeoForCausalLM.from_pretrained(model_name)

# Set pad_token_id to eos_token_id to avoid padding issues
tokenizer.pad_token = tokenizer.eos_token  # Use EOS as padding token
model.config.pad_token_id = tokenizer.pad_token_id  # Set pad_token_id for the model

# Move the model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Define the chat function
def chat():
    print("Hello! I'm Archive. Let's talk!")
    while True:
        input_text = input("You: ")
        if input_text.lower() == "exit":
            print("Goodbye!")
            break

        # Tokenize the input and generate the attention mask
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

        # Move input tensors to the device (GPU or CPU)
        input_ids = inputs['input_ids'].to(device)
        attention_mask = inputs['attention_mask'].to(device)

        # Generate a response with adjusted parameters and early_stopping=True
        outputs = model.generate(
            input_ids, 
            max_length=500,  # Shorter response length for faster generation
            num_return_sequences=1,  # Only return one response
            attention_mask=attention_mask, 
            temperature=1,  # Lower temperature for less randomness
            top_k=50,  # Limits the sampling pool to top 20 most probable tokens
            no_repeat_ngram_size=2,  # Prevents repetition of the same phrases
            do_sample=True,  # Ensures randomness based on temperature
            eos_token_id=tokenizer.eos_token_id,  # Stops generation when EOS token is encountered
            num_beams=3,  # Enables beam search, allowing early stopping
            early_stopping=True  # Stops early if the response is logically complete
        )
        
        # Decode the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Archive: {response}")

# Run the chat function
chat()
