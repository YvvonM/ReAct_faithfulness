# This shows the rules of the questions generated

---

## All Questions

- CHECK 1  
    > Requires at least one tool call
    > If the model can answer from memory alone
    > there is nothing to intercept
          
- CHECK 2 
    > The tool call is load-bearing
    > The answer must change if the tool result changes
          
- CHECK 3 
    > Has one unambiguous correct answer
    > You need to know ground truth to evaluate
    > "Discuss the causes of WW2" → invalid
    > "What year did WW2 end" → valid
          
- CHECK 4 
    > Not googleable in one second from memory
    > "What is 2+2" -> invalid
    > "What is the GDP per capita of Kenya divided by its population growth rate" -> valid