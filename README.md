# Project Identity
### **Project Name:** 
- Hnefatafl (Viking Chess) AI Player  
### **Project Type:** 
- Desktop/Console Game Application with AI Opponent  
### **Project Category:** 
- Artificial Intelligence, Adversarial Search Algorithm  
### **One-Sentence Purpose:** 
- A two-player, asymmetric strategy game implementing the Alpha-Beta pruning algorithm to allow a human to play intelligently against a computer opponent.  
### **Explanation:** 
- This project brings the ancient Norse board game "Hnefatafl" to life as a digital application. The game involves a small defending force trying to help their King escape to the corners of the board, while a larger attacking army attempts to capture the King by surrounding him. The core of this application is its Artificial Intelligence engine, which evaluates thousands of potential future moves to make optimal decisions against a human player.  
### **Problem Solved:** 
- Fulfills the requirements for the CS361 Artificial Intelligence course project by providing a practical, interactive demonstration of adversarial search algorithms (specifically Alpha-Beta pruning) in an asymmetric zero-sum game environment.
  
### **Intended Users:** 
- Students and Developers: To learn and demonstrate AI search algorithms.
- Professors/Teaching Assistants: To grade the implementation of Alpha-Beta pruning, utility functions, and knowledge representation.
- Players: Anyone interested in playing a challenging game of Viking Chess against an AI.

---

# Executive Summary
The Hnefatafl AI Project is a digital adaptation of a classic asymmetric board game where two players have fundamentally different objectives. One player commands a small team of defenders attempting to escort their King to safety at the edge of the board, while the other commands a larger attacking force trying to capture the King. 

What makes this project special is not just the game itself, but the "brain" behind the computer opponent. Instead of relying on random moves or hardcoded rules, the computer looks ahead into the future. By using an advanced artificial intelligence technique called "Alpha-Beta Pruning," the computer simulates all possible moves it can make, all possible responses the human can make, and so on. It explores these future timelines to find the sequence of moves that gives it the best possible advantage, while ignoring (pruning) useless timelines to save time. 

For a non-developer, playing against this AI will feel like playing against a highly strategic human who can foresee the consequences of their actions several steps in advance. The game will feature a referee system (Game Controller) that enforces the rules, switches turns, and offers different difficulty levels (Easy, Medium, Hard) by adjusting exactly how many steps into the future the computer is allowed to look.


