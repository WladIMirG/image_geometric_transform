import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--angulo', type=float,   default=0,
                    help='Ângulo de rotação medido em graus no  sentido anti-horario')
parser.add_argument('-sx', '--x_scale', type=float,   default=1,
                    help='Factor de escala em x')
parser.add_argument('-sy', '--y_scale', type=float,   default=1,
                    help='Factor de escala em y')
parser.add_argument('-d', '--altura', type=float,   default=0,
                    help='Largura altura')
parser.add_argument('-m', '--interp', type=str,   default="inter_VMP",
                    help='Método de interpolação utilizado')
parser.add_argument('-i',  '--img_i', type = str,   default="baboon.png",
                    help='Imagem de entrada no formato PNG')
parser.add_argument('-o',  '--img_o', type = str,   default=None,
                    help='Imagem de saída no formato PNG (após a transformação geométrica)')
parser.add_argument('-mod',  '--mode', type = str,   default=None,
                    help='Modo de operação, tipo de transformação')

args = vars(parser.parse_args())

