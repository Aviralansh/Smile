#################################### TXN TEST #####################################


import subprocess

def send_smile_tokens(receiver_wallet_address, amount=10):
    # Your official SMILE Token Mint Address
    token_mint_address = "BQen5jjxswUZtPSmp5sv3PXdyRcwoo73ttKZefAyCVco"
    
    # The exact CLI command as a list of string arguments
    command = [
        "spl-token", 
        "transfer", 
        token_mint_address, 
        str(amount), 
        receiver_wallet_address,
        "--fund-recipient",          # Pays the tiny devnet SOL fee to create their token pocket
        "--allow-unfunded-recipient" # Allows sending to a brand new wallet that has 0 SOL
    ]
    
    print(f"Attempting to send {amount} SMILE to {receiver_wallet_address}...")
    
    try:
        # Executes the terminal command natively within Python
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        print("\n✅ Success! Transaction Details:")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n❌ Transaction Failed. Error Output:")
        print(e.stderr)
        return False

# --- QUICK TEST BLOCK ---
if __name__ == "__main__":
    
    test_receiver = "HGKsV2LX9GhJNbP5s1Uwu8WomE5E4Z8kXKy91nGy8EZV" #"PASTE_TEST_WALLET_ADDRESS_HERE" 
    
    if test_receiver != "PASTE_TEST_WALLET_ADDRESS_HERE": 
        send_smile_tokens(test_receiver, amount=10)
    else:
        print("Waiting for a test wallet address to be added!")