# AdaptiShoot: AI-Powered Dynamic Difficulty Shooter

## Overview

AdaptiShoot is a 2D target shooting game implemented in Python using the Pygame library. What sets it apart is its real-time dynamic difficulty adjustment system powered by a heuristic-based AI. The game continuously monitors the player's performance and adapts the challenge by modifying various game parameters on the fly. This aims to provide a personalized and engaging gaming experience, ensuring the difficulty is always appropriately matched to the player's skill level.

## Key Features

* **Dynamic Difficulty Adjustment:** The game's AI intelligently adjusts difficulty in real-time based on player performance metrics.
* **Heuristic AI:** Difficulty adjustments are driven by a set of rules (heuristics) that analyze player hit rate, reaction time, and consecutive successes/failures.
* **Adaptive Game Parameters:** The AI controls target speed, target spawn rate, and target movement patterns to alter the difficulty.
* **Multiple Difficulty Presets:** Players can choose from Easy, Medium, or Hard starting difficulty levels.
* **Enhanced Target Movement:** Targets exhibit varied movement patterns, with complexity increasing at higher difficulty levels.
* **Game Over Condition:** The game ends when the player runs out of lives after being hit by targets.
* **Score Tracking:** The player's score is displayed during gameplay.
* **High Score:** The game tracks and displays the highest achieved score, saved between sessions.
* **Retry Option:** After a game over, players can easily retry the game.
* **Lives System:** Players start with a set number of lives, lost upon collision with targets.
* **Clear Visuals:** Simple yet effective visuals using Pygame shapes (or optional spaceship images).

## How to Play

1.  **Install Pygame:** If you don't have Pygame installed, open your terminal or command prompt and run:
    ```bash
    pip install pygame
    ```
2.  **Download the Game Files:** Save the Python script (e.g., `adaptishoot.py`) and any image files (if you've added spaceships) to the same directory.
3.  **Run the Game:** Open your terminal or command prompt, navigate to the directory where you saved the files, and run:
    ```bash
    python adaptishoot.py
    ```
4.  **Difficulty Selection:** Upon starting, you'll be prompted to choose a starting difficulty level (1 for Easy, 2 for Medium, 3 for Hard).
5.  **Gameplay:**
    * Control the player (blue shape/spaceship) using the left and right arrow keys.
    * Aim and shoot at the red targets by clicking the left mouse button.
    * The goal is to shoot down as many targets as possible and survive as long as you can.
    * Avoid letting targets collide with your player, as this will cost you a life.
6.  **Game Over:** The game ends when you run out of lives. Your final score and the high score will be displayed. Press 'R' to retry or 'Q' to quit.

## AI Difficulty Adjustment Details

The AI dynamically adjusts the game's difficulty based on the following heuristics:

* **Hit Rate:** A high hit rate leads to increased difficulty (faster targets, higher spawn rate, more complex movement). A low hit rate results in decreased difficulty.
* **Reaction Time:** Fast average reaction times after a target appears increase the difficulty. Slower reaction times decrease it.
* **Consecutive Hits/Misses (Shots Fired):** Streaks of successful shots increase difficulty, while streaks of misses decrease it.
* **Missed Targets (Passed Screen):** Letting targets pass the screen without being hit also contributes to a decrease in difficulty.

The difficulty adjustments are applied smoothly to avoid abrupt and jarring changes in gameplay.

## Potential Future Enhancements

* More sophisticated AI algorithms for difficulty adjustment (e.g., using player modeling).
* Different enemy types with unique behaviors.
* Power-ups and special abilities for the player.
* Improved visual and sound effects.
* More nuanced difficulty parameters.
* Saving player profiles and progress.

## Author

[Divakshu/divakshu04]