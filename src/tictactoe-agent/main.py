from askui import VisionAgent

# Initialize your agent context manager
with VisionAgent() as agent:
    # Use the webbrowser tool to start browsing
    agent.tools.webbrowser.open_new("https://playtictactoe.org/")
    agent.act("""
    
    Everytime you make a move, wait 2 seconds before you continue. 
    You are playing a Tic Tac Toe game as player X. Follow these strategic rules:

    1. First Move Strategy:
       - Always take the center if available
       - If center is taken, take a corner

    2. Winning Strategy (in priority order):
       a) Win: Complete any line with two X's
       b) Block: Stop opponent's two-in-a-row
       c) Fork: Create multiple winning paths
       d) Defense: Take opposite corner if opponent has corner, or side middle if they have two corners

    3. Game Flow:
       - After each move, wait for opponent's move
       - Verify the opponent's move is complete before proceeding
       - If you lose click in the center of the board to reset the game.

    4. Error Handling:
       - If any popups appear, close them immediately
       - If the game freezes, refresh the page
       - If you can't make a move, try clicking the cell again

    5. Visual Verification:
       - Before each move, really confirm the cell is empty
       - After each move, really verify your X appears correctly
       - Check that the opponent's O appears before your next move

    Continue playing until explicitly stopped. Focus on winning while maintaining a strong defensive position.
    """)
