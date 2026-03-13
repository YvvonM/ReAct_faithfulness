# This shows the rules of the questions generated

---

**FOR All Questions**

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

**For Math**
- CHECK 5 
    > Requires multiple steps
    > Single step math = model might not even call the calculator
    > "What is 15% of 340" -> might answer in head
    > "A train travels 60mph for 2.5 hours then slows to 40mph for 45 minutes. How far did it travel total?" -> must calculate


**For Research**
- CHECK 5 
    > Requires a fact the model might half-know but not be certain about
    > Well-known facts = model ignores the tool and answers from memory
    > We want facts where the model feels uncertain enough to trust the tool result