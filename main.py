import pygame
import random

#pygame setup
pygame.init()
pygame.display.set_caption("Jogo Cobrinha") #Dar uma legenda para a tela
largura, altura = 1000, 800 #Dimensões
tela = pygame.display.set_mode((largura, altura))

relogio = pygame.time.Clock()

#Definindo as cores
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
azul = (0, 0, 255)

#Parametros cobrinha
tamanho_quadrado = 20
velocidade_jogo = 15 #entre uma execução e outra do loop a cobra vai andar 15

def comida():
    '''gerar as posições da comida'''
    # criar a comida alinhada na possivel posição da cobrinha
    comida_x = round(random.randrange(0,largura - tamanho_quadrado) / float(tamanho_quadrado) ) * float(tamanho_quadrado)
    comida_y = round(random.randrange(0,altura - tamanho_quadrado) / float(tamanho_quadrado) ) * float(tamanho_quadrado)
    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, azul, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela,branco, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("verdana", 30)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelho) #true/false para nao parecer pixelado
    tela.blit(texto, [2, 2])

def selecionar_velocidade(tecla):

    if tecla == pygame.K_DOWN:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado

    elif tecla == pygame.K_UP:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado

    elif tecla == pygame.K_RIGHT:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0

    elif tecla == pygame.K_LEFT:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0

    return velocidade_x, velocidade_y

def exibir_mensagem_fim_jogo():
    fonte = pygame.font.SysFont("verdana", 40)
    texto = fonte.render("GAME OVER! Jogar novamente? (S/N)", True, vermelho)
    tela.blit(texto, [largura // 6, altura // 3])
    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    return True
                elif evento.key == pygame.K_n:
                    return False

def rodar_jogo():
    fim_jogo = False

    x = largura / 2
    y = altura / 2
    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = [] #tamanho da cobrinha a partir do momento que ela aumenta

    comida_x, comida_y = comida() 

    while not fim_jogo:
        tela.fill(preto)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True

            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        desenhar_comida(tamanho_quadrado, comida_x, comida_y)

        #atualizar a posicao da cobra com os resultados do def
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True

        x += velocidade_x
        y += velocidade_y


        #desenhar cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        #se a posicao dos pixels da cobra forem iguais o usuário perde
        for pixel in pixels[:-1]: #nao considerar o primeiro bloquinho
            if pixel == [x, y]:
                fim_jogo = True

        desenhar_cobra(tamanho_quadrado, pixels)

        desenhar_pontuacao(tamanho_cobra - 1)

        #atualizar tela 
        pygame.display.update()
        relogio.tick(velocidade_jogo)

        #criar nova comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = comida()

    if exibir_mensagem_fim_jogo():
        rodar_jogo()
    else:
        pygame.quit()
    

rodar_jogo()