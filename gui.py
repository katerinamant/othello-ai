import PySimpleGUI as sg
from board import Board
from player import Player

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

            if event == "Start" or event == sg.WIN_CLOSED:
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

    def game(self, board: Board, user_player: Player, ai_player: Player):
        layout = [[sg.Text(f" ", key="title")]]

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

        while True:
            # Game loop
            available_moves = {Board.W, Board.B}

            while available_moves:
                if board.last_player == Board.W:
                    player_name = "black"
                    piece = Board.B
                else:
                    player_name = "white"
                    piece = Board.W

                if piece not in available_moves:
                    print(f"Sorry, there are no available moves for {player_name}!")
                    board.last_player *= -1
                    continue

                #print(f"Time for {player_name} to make a move!")
                if piece == user_player.piece_val:
                    self._board_window["title"].update(f"Time for {player_name} to make a move!")
                    # Event loop
                    while True:
                        event, values = self._board_window.read()

                        if event == sg.WIN_CLOSED:
                            break

                        if event not in self._used_cells:
                            pieces_to_flip = board.is_valid_move(event[0], event[1], piece)
                            if pieces_to_flip:
                                board.make_move(event[0], event[1], piece, pieces_to_flip)

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

                        break

                else:
                    self._board_window["title"].update(f"Time for {player_name} to make a move!")
                    # Event loop
                    while True:
                        event, values = self._board_window.read()

                        if event == sg.WIN_CLOSED:
                            break

                        if event not in self._used_cells:
                            pieces_to_flip = board.is_valid_move(event[0], event[1], piece)
                            if pieces_to_flip:
                                board.make_move(event[0], event[1], piece, pieces_to_flip)

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

                        break

                available_moves = board.is_terminal()
                break
