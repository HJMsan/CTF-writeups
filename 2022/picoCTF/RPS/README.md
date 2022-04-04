# RPS (Binary Exploit)
## overview 
Below is output of the binary:  
```
Welcome challenger to the game of Rock, Paper, Scissors
For anyone that beats me 5 times in a row, I will offer up a flag I found
```
From the above, We need JUST 5 wins in a row. So we might have been able to brute-force to win this game. But there is a obvious vulnerability.

## analyze
In `play` function, our input is stored in `player_turn`  
`r = tgetinput(player_turn, 100);`  
Then, the computer's hand is defined randomly.  
`int computer_turn = rand() % 3;`  
After that, our input and a element of `loses` are compared by `strstr` function. `loses` is defined what is a lose hand at the time.  
`char* loses[3] = {"paper", "scissors", "rock"};`
```
if (strstr(player_turn, loses[computer_turn])) {
    puts("You win! Play again?");
    return true;
} else {
    puts("Seems like you didn't win this time. Play again?");
    return false;
}
```
`strstr` function returns true if arg0 contains same string as arg1. If we input `"paperscissorsrock"`, we can always win the game regardless of computer's hand. So input `"paperscissorsrock"` 5 times then we can get the flag `picoCTF{50M3_3X7R3M3_1UCK_D80B11AA}`.