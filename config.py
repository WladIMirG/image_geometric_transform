import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--angulo', type=float,   default=0, help='Ânguo de rotação medido em graus no  sentido anti-horario')
parser.add_argument('-e', '--escala', type=float,   default=0, help='Factor de escala')
parser.add_argument('-d', '--altura', type=float,   default=0, help='Largura altura')
parser.add_argument('-m', '--interp', type=float,   default=0, help='Interpolação')
parser.add_argument('-i',  '--img_i', type = str,   default=0, help='Path to video file (if not using camera)')
parser.add_argument('-o',  '--img_o', type = str,   default=0, help='Path to video file (if not using camera)')

args = vars(parser.parse_args())
