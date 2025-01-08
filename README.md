## Question 3
For this question, please attach the script and the screen log as separate files.

## Scenario
A customer, who operates a centralized crypto exchange (e.g., Binance) requiring the ability to send multiple transactions in a short period, reports the following issue while testing the Scroll Sepolia testnet ..... (see details from the initial email)

## Task
Write a script based on the customer’s pseudo code to reproduce the above issue. Include logging to verify whether the nonce remains unchanged after sending a transaction.
Are you able to reproduce the issue, or does the system works as expected? Note: you do NOT need to fix the issue if it is reproducible.
Attach both the script and the screen log when replying to this email.

---

## My observations based on the log file generated from a script representing the customer's pseudo code: `customer_script.py` > `customer_script.log`

    ### Iterations 1 to 4
    The nonce increments as expected with each transaction, starting from 40 and going up to 43.

    ### Iteration 5
    The log indicates that the transaction with nonce 43 was already known. The script retries with an incremented nonce, which works and results in a transaction hash.

    ### Iteration 6
    The nonce increments as expected from 43 to 44.

    ### Iteration 7
    Similar to iteration 5, the transaction with nonce 44 was already known. The script retries with an incremented nonce, and the transaction is successful.

    ### Iteration 8
    The nonce jumps from 44 to 46, skipping 45. This suggests that nonce 45 may have been used, or the node didn't return an updated nonce in time.

    ### Iterations 9 to 10
    The nonce continues to increment as expected from 46 to 47. However, the nonce jumps back to 46 in iteration 10.

---

## Conclusion

There are instances where the nonce remains unchanged or skips an expected increment. Specifically, the issue is evident when the transaction with a given nonce is already known (iterations 5 and 7) and in the jump from nonce 44 to 46 (iteration 8).

While the error handling retries address some immediate issues, such as repeated nonce conflicts, they don't fully resolve broader issues like nonce skipping, delayed updates, concurrency handling, and network latency. These underlying problems highlight the need for a more robust nonce management strategy, such as local nonce tracking, to ensure consistency and reliability in transaction handling.

---

## Solution: `fix_script.py` > `fix_script.log`

The previous script relies solely on the node's pending nonce, which can cause inconsistencies, leading to repeated or skipped nonces.

Instead of relying solely on the node's pending nonce, we'll maintain and update our own nonce tracker to ensure consistency and avoid conflicts.

- Maintain our own nonce tracker, starting with the latest nonce retrieved from the node.
- After each successful transaction, we increment the nonce locally.
- This approach ensures that our nonce management is consistent and avoids conflicts with the node's pending nonce.

    ## Changes made in `fix_script.py` 

    Line 53 
    nonce = get_latest_nonce(web3, source_address) before the loop

    Line 57
    nonce += 1  # Increment nonce after each successful transaction