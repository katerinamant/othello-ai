import PySimpleGUI as sg
from board import Board
from player import Player


class WindowClosedError(Exception):
    """
    The user unexpectedly closed the window
    """

class GUI:
    def __init__(self) -> None:
        sg.theme("DarkBlue2")
        self._board_window = None
        self._used_cells = set()

    def welcome_window(self) -> tuple[str, str]:
        """
        Displays a welcome window and requests necessary input

        """
        # Title
        layout = [[sg.Text("Welcome to Othello AI!")]]

        # Choose difficulty
        layout.append([sg.Text("Choose difficulty:")])
        difficulties = ["Novice", "Medium", "Expert"]
        difficulty_row = []
        for difficulty in difficulties:
            difficulty_row.append(sg.Button(difficulty))
        layout.append(difficulty_row)
        diff_input = None

        # Choose color
        layout.append([sg.Text("Choose color! Remember, black goes first...")])
        colors = ["Black", "White"]
        color_row = []
        for color in colors:
            color_row.append(sg.Button(color))
        layout.append(color_row)
        color_input = None

        layout.append([sg.Button("Start", disabled=(diff_input == None) or (color_input == None))])

        # Create window
        window = sg.Window(title="Othello AI", layout=layout)

        # Event loop
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                window.close()
                raise WindowClosedError

            if event == "Start":
                window.close()
                break

            if event in difficulties:
                diff_input = event
                for diff in difficulties:
                    window[diff].update(disabled=diff != event)
                    window["Start"].update(disabled=(diff_input == None) or (color_input == None))

            if event in colors:
                color_input = event
                for color in colors:
                    window[color].update(disabled=color != event)
                    window["Start"].update(disabled=(diff_input == None) or (color_input == None))

        return (diff_input, color_input)

    def create_board_window(self, board: Board, ai_player: Player):
        """
        Creates the window with the game board
        """
        layout = []

        if ai_player.piece_val == Board.B:
            row = [sg.Text(f"Black is calculating a move...", key="title")]
        else:
            row = [sg.Text(f"Time for black to make a move!", key="title")]
        # Add continue button
        row.append(sg.Text('', size=(8, 1)))
        row.append(sg.Button("Continue",disabled=ai_player.piece_val != Board.B))
        layout.append(row)

        # Create board layout
        game_board = board.game_board
        for row in range(board.dimension):
            new_row = []
            for column in range(board.dimension):
                key = (row, column)
                piece = " "
                if game_board[row][column] == Board.B:
                    piece = "X"
                    self._used_cells.add(key)
                elif game_board[row][column] == Board.W:
                    piece = "O"
                    self._used_cells.add(key)
                new_row.append(sg.Button(button_text=piece, size=(3, 2), key=key))
            layout.append(new_row)

        # Add score messages
        layout.append([sg.Text(f"Black (X): {board.black_pieces}", key="black_pieces")])
        layout.append([sg.Text(f"White (O): {board.white_pieces}", key="white_pieces")])

        self._board_window = sg.Window(title="Othello AI", layout=layout, finalize=True)

    def user_move(self, board: Board, user_player: Player):
        """
        Updates the board when the user chooses
        a cell to place a piece
        """
        if user_player.piece_val == Board.B:
            player_name = "black"
            ai_name = "White"
        else:
            player_name = "white"
            ai_name = "Black"
        self._board_window["title"].update(f"Time for {player_name} to make a move!")

        self._board_window["Continue"].update(disabled=True)

        self._board_window.refresh()

        # Event loop
        while True:
            event, values = self._board_window.read()

            if event == sg.WIN_CLOSED:
                self._board_window.close()
                raise WindowClosedError

            if event not in self._used_cells:
                pieces_to_flip = board.is_valid_move(event[0], event[1], user_player.piece_val)
                if pieces_to_flip:
                    board.make_move(event[0], event[1], user_player.piece_val, pieces_to_flip)

                    # Update board layout
                    game_board = board.game_board
                    for row in range(board.dimension):
                        for column in range(board.dimension):
                            key = (row, column)
                            piece = " "
                            if game_board[row][column] == Board.B:
                                piece = "X"
                                self._used_cells.add(key)
                            elif game_board[row][column] == Board.W:
                                piece = "O"
                                self._used_cells.add(key)
                            self._board_window[key].update(piece)

                    # Update score messages
                    self._board_window["black_pieces"].update(f"Black (X): {board.black_pieces}")
                    self._board_window["white_pieces"].update(f"White (O): {board.white_pieces}")

                    # Update title
                    self._board_window["title"].update(f"{ai_name} is calculating a move...")

                self._board_window.refresh()
                break

    def ai_move(self, board: Board, ai_player: Player, x: int, y: int):
        """
        Updates the board when the ai
        makes a move
        """
        if ai_player.piece_val == Board.B:
            player_name = "black"
        else:
            player_name = "white"
        self._board_window["title"].update(f"{player_name[0].upper() + player_name[1:]} placed a piece on {x + 1} x {y + 1}")

        self._board_window["Continue"].update(disabled=False)

        # Update board layout
        game_board = board.game_board
        for row in range(board.dimension):
            for column in range(board.dimension):
                key = (row, column)
                piece = " "
                if game_board[row][column] == Board.B:
                    piece = "X"
                    self._used_cells.add(key)
                elif game_board[row][column] == Board.W:
                    piece = "O"
                    self._used_cells.add(key)
                self._board_window[key].update(piece)

        # Update score messages
        self._board_window["black_pieces"].update(f"Black (X): {board.black_pieces}")
        self._board_window["white_pieces"].update(f"White (O): {board.white_pieces}")

        self._board_window.refresh()

        # Event loop
        while True:
            event, values = self._board_window.read()

            if event == sg.WIN_CLOSED:
                self._board_window.close()
                raise WindowClosedError

            if event == "Continue":
                break
