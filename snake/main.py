"""The main module for executing the game.

Takes care of starting the application and reading/writing highscores.
The following command line arguments are required:

- `--username`: Name of the player (for tracking high scores)
- `--scorefile`: Path to the high score file

One can optionally provide the following command line arguments too:

- `-w` or `--width`: Width of the game screen (default: `480`)
- `-h` or `--height`: Height of the game screen (default: `360`)
- `--fps`: The framerate of the game, i.e. how often to update
"""

import argparse

import ezpygame

import menu


def parse_args():
    """Parse the provided command line arguments."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--username', required=True)
    parser.add_argument('--scorefile', required=True)
    parser.add_argument('-w', '--width', type=int, default=480)
    parser.add_argument('-h', '--height', type=int, default=360)
    parser.add_argument('--fps', type=int, default=30)
    return parser.parse_args()


def read_high_scores(file_path):
    """Read the previous high scores from a file.
    
    Prints out an issue if there are invalid lines or if the file
    is missing altogether, but does not prevent the game from starting.

    Be aware that the file will be overwritten with new high scores
    as the game progresses.
    """
    high_scores = []
    try:
        with open(file_path) as file:
            for line in file:
                line = line.strip()
                try:
                    name, score = line.split(':')
                except ValueError:
                    print(f'Invalid high score line: {line}')
                    continue
                try:
                    score = int(score)
                except ValueError:
                    print(f'Invalid high score value: {line}')
                    continue
                high_scores.append((name, score))
    except FileNotFoundError:
        print(f'High score file not found: {file_path}')
    return high_scores


def write_high_scores(file_path, high_scores):
    """Write new high scores to a file."""
    with open(file_path, 'w') as file:
        for name, score in high_scores:
            file.write(f'{name}:{score}\n')


if __name__ == '__main__':
    args = parse_args()
    app = ezpygame.Application(
        title='Snake',
        resolution=(args.width, args.height),
        update_rate=args.fps,
    )
    high_scores = read_high_scores(args.scorefile)
    menu_scene = menu.Menu(high_scores, username=args.username)
    app.run(menu_scene)
    write_high_scores(args.scorefile, high_scores)
