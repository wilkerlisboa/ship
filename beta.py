import pygame
import sys
import random
import os

def obter_caminho_recurso(relativo):
    if getattr(sys, 'frozen', False):  # Se estiver empacotado
        return os.path.join(sys._MEIPASS, relativo)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relativo)

# Caminho relativo para o arquivo de música
caminho_musica = obter_caminho_recurso(os.path.join("musica", "musica.mp3"))

# Inicializa o Pygame
pygame.init()

# Inicializa o módulo de fonte
pygame.font.init()

# Inicializa o módulo de mixer para música
pygame.mixer.init()

# Carrega a música de colisão
musica_colisao = pygame.mixer.Sound(caminho_musica)
# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Configurações da tela
largura_tela = 700
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("SPACE WAR")

# Fontes
fonte_titulo = pygame.font.Font(None, 48)
fonte_info = pygame.font.Font(None, 40)
fonte_opcoes = pygame.font.Font(None, 28)
font_criador = pygame.font.Font(None, 20)

# Defina o caminho para o ícone personalizado
icone = pygame.image.load("C:/Users/Lisboa/Documents/hello/linguagem/nave/imagem/nave.png")
pygame.display.set_icon(icone)

# Carregar imagens
nave_imagem = pygame.image.load("C:/Users/Lisboa/Documents/hello/linguagem/nave/imagem/nave.png")  # Substitua "nave.png" pelo nome da sua imagem
inimigo_imagem = pygame.image.load("C:/Users/Lisboa/Documents/hello/linguagem/nave/imagem/inimigo.png")  # Substitua "inimigo.png" pelo nome da sua imagem

# Redimensionar imagens (opcional)
nave_imagem = pygame.transform.scale(nave_imagem, (50, 50))
inimigo_imagem = pygame.transform.scale(inimigo_imagem, (50, 50))

# Variáveis do jogo
pontuacao = 0
recorde = 0
nivel = 1

# Nave do jogador
nave_rect = nave_imagem.get_rect(center=(largura_tela // 2, altura_tela - 30))

# Projéteis
projeteis = []

# Inimigos
inimigos = []

# Relógio para controle de frames
relogio = pygame.time.Clock()

def novo_inimigo():
    inimigo = pygame.Rect(random.randint(0, largura_tela - inimigo_imagem.get_width()), 
                          0, inimigo_imagem.get_width(), inimigo_imagem.get_height())
    inimigos.append(inimigo)
 
# Variáveis do jogo para modo cooperativo
nave2_rect = nave_imagem.get_rect(center=(largura_tela // 2, altura_tela - 30))
projeteis2 = []

# Nave do segundo jogador
def mover_nave2_teclado():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and nave2_rect.left > 0:
        nave2_rect.x -= 5
    if keys[pygame.K_d] and nave2_rect.right < largura_tela:
        nave2_rect.x += 5

def desenhar_jogadores():
    tela.blit(nave_imagem, nave_rect)
    tela.blit(nave_imagem, nave2_rect)

def desenhar_projeteis():
    for proj in projeteis:
        pygame.draw.rect(tela, BRANCO, proj)  # Desenha projéteis do jogador 1 como retângulos brancos
    for proj in projeteis2:
        pygame.draw.rect(tela, (255, 0, 0), proj)  # Desenha projéteis do jogador 2 como retângulos vermelhos

# Variáveis do jogo para modo cooperativo
nave2_rect = nave_imagem.get_rect(center=(largura_tela // 2, altura_tela - 30))
projeteis2 = []

# Nave do segundo jogador
def mover_nave2_teclado():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and nave2_rect.left > 0:
        nave2_rect.x -= 5
    if keys[pygame.K_d] and nave2_rect.right < largura_tela:
        nave2_rect.x += 5

def desenhar_jogadores():
    tela.blit(nave_imagem, nave_rect)
    tela.blit(nave_imagem, nave2_rect)

def desenhar_projeteis():
    for proj in projeteis:
        pygame.draw.rect(tela, BRANCO, proj)  # Desenha projéteis do jogador 1 como retângulos brancos
    for proj in projeteis2:
        pygame.draw.rect(tela, (255, 0, 0), proj)  # Desenha projéteis do jogador 2 como retângulos vermelhos

def jogo_cooperativo():
    global pontuacao, recorde, nivel, nave_rect, nave2_rect, projeteis, projeteis2

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                projeteis.append(pygame.Rect(nave_rect.centerx - 2, nave_rect.top - 10, 4, 10))
                projeteis2.append(pygame.Rect(nave2_rect.centerx - 2, nave2_rect.top - 10, 4, 10))
        

        # Atualização da posição da nave do jogador 1 com a posição do mouse
        nave_rect.midbottom = pygame.mouse.get_pos()
        # Atualização da posição da nave do jogador 2 com as teclas A e D
        mover_nave2_teclado()

        # Mover nave do jogador 1 pelo teclado
        mover_nave_teclado()

        # Atualização da posição dos projéteis do jogador 1
        for proj in projeteis:
            proj.y -= 5
            if proj.y < 0:
                projeteis.remove(proj)

        # Atualização da posição dos projéteis do jogador 2
        for proj in projeteis2:
            proj.y -= 5
            if proj.y < 0:
                projeteis2.remove(proj)
                


        # Atualização da posição dos inimigos
        for inimigo in inimigos:
            if inimigo.colliderect(nave_rect) or inimigo.colliderect(nave2_rect):
                game_over()

        for inimigo in inimigos:
            inimigo.y += 3
            if inimigo.y > altura_tela:
                inimigos.remove(inimigo)
                pontuacao += 1
                pygame.mixer.Sound.play(musica_colisao)


        # Adiciona novos inimigos
        if random.randint(1, 100) < 3 * nivel:
            novo_inimigo()

        # Colisões entre projéteis do jogador 1 e inimigos
        for proj in projeteis:
            for inimigo in inimigos:
                if proj.colliderect(inimigo):
                    projeteis.remove(proj)
                    inimigos.remove(inimigo)
                    pontuacao += 10
                    pygame.mixer.Sound.play(musica_colisao)
                    


        # Colisões entre projéteis do jogador 2 e inimigos
        for proj in projeteis2:
            for inimigo in inimigos:
                if proj.colliderect(inimigo):
                    projeteis2.remove(proj)
                    inimigos.remove(inimigo)
                    pontuacao += 10
                    


        # Aumenta o nível gradualmente a cada 100 pontos
        if pontuacao >= nivel * 100:
            nivel += 1

        # Atualização da tela
        tela.fill(PRETO)
        desenhar_jogadores()
        desenhar_projeteis()
        for inimigo in inimigos:
            tela.blit(inimigo_imagem, inimigo)

        desenhar_texto_multilinha(f'Pontuação: {pontuacao}\nRecorde: {recorde}\nNível: {nivel}', fonte_info, BRANCO, 10, 10)

        pygame.display.flip()
        relogio.tick(60)
# Adicione a função para mover a nave pelo teclado
def mover_nave_teclado():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and nave_rect.left > 0:
        nave_rect.x -= 5
    if keys[pygame.K_RIGHT] and nave_rect.right < largura_tela:
        nave_rect.x += 5

def desenhar_texto_multilinha(texto, fonte, cor, x, y):
    linhas = texto.split('\n')
    altura_linha = fonte.get_linesize()
    for i, linha in enumerate(linhas):
        superficie_texto = fonte.render(linha, True, cor)
        tela.blit(superficie_texto, (x, y + i * altura_linha))

def jogo():
    global pontuacao, recorde, nivel, nave_rect


    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                projeteis.append(pygame.Rect(nave_rect.centerx - 2, nave_rect.top - 10, 4, 10))

         # Atualização da posição da nave com a posição do mouse
        nave_rect.midbottom = pygame.mouse.get_pos()

        # Mover nave pelo teclado
        mover_nave_teclado()

        # Atualização da posição dos projéteis
        for proj in projeteis:
            proj.y -= 5
            if proj.y < 0:
                projeteis.remove(proj)

        # Atualização da posição dos inimigos
        for inimigo in inimigos:
            inimigo.y += 3
            if inimigo.colliderect(nave_rect):
                game_over()
            if inimigo.y > altura_tela:
                inimigos.remove(inimigo)
                pontuacao += 1

        # Adiciona novos inimigos
        if random.randint(1, 100) < 3 * nivel:
            novo_inimigo()

        # Colisões entre projéteis e inimigos
        for proj in projeteis:
            for inimigo in inimigos:
                if proj.colliderect(inimigo):
                    projeteis.remove(proj)
                    inimigos.remove(inimigo)
                    pontuacao += 10
                    pygame.mixer.Sound.play(musica_colisao)

        # Aumenta o nível gradualmente a cada 100 pontos
        if pontuacao >= nivel * 100:
            nivel += 1

        # Atualização da tela
        tela.fill(PRETO)
        tela.blit(nave_imagem, nave_rect)
        for proj in projeteis:
            pygame.draw.rect(tela, BRANCO, proj)  # Desenha projéteis como retângulos brancos
        for inimigo in inimigos:
            tela.blit(inimigo_imagem, inimigo)

        desenhar_texto_multilinha(f'Pontuação: {pontuacao}\nRecorde: {recorde}\nNível: {nivel}', fonte_info, BRANCO, 10, 10)

        pygame.display.flip()

        relogio.tick(60)

def game_over():
    global pontuacao, recorde, nivel

    if pontuacao > recorde:
        recorde = pontuacao

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if largura_tela // 4 < mouse_x < largura_tela * 3 // 4 and altura_tela - 150 < mouse_y < altura_tela:
                    resetar_jogo()
                    main()  # Chama a função main diretamente

        tela.fill(PRETO)
        desenhar_texto_multilinha("Game Over", fonte_titulo, BRANCO, largura_tela // 4, altura_tela // 4)
        desenhar_texto_multilinha(f'Pontuação: {pontuacao}\nRecorde: {recorde}\nNível: {nivel}', fonte_info, BRANCO, largura_tela // 4, altura_tela // 2)
        desenhar_texto_multilinha("1 - VOLTA AO INÍCIO", fonte_opcoes, BRANCO, largura_tela // 4, altura_tela - 150)

        pygame.display.flip()
        relogio.tick(60)


def esperar_clique():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                return

def resetar_jogo():
    global pontuacao, nivel, projeteis, inimigos

    pontuacao = 0
    nivel = 1
    projeteis = []
    inimigos = []

# Modifique a função main para incluir a escolha do modo de jogo
def main():
    global nivel

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(PRETO)
        desenhar_texto_multilinha("SPACE WAR ", fonte_titulo, BRANCO, largura_tela // 5, altura_tela // 5)
        desenhar_texto_multilinha("1. Iniciar Novo Jogo (Modo Singleplayer)", fonte_opcoes, BRANCO, largura_tela // 4, altura_tela // 2)
        desenhar_texto_multilinha("2. Modo Cooperativo", fonte_opcoes, BRANCO, largura_tela // 4, altura_tela * 2.5 // 4)
        desenhar_texto_multilinha("Programador: WILKER LISBOA", font_criador, BRANCO,  largura_tela // 20, altura_tela - 20)


        pygame.display.flip()

        # Detecção de clique do mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Botão esquerdo do mouse
            if largura_tela // 4 < mouse_x < largura_tela * 3 // 4:
                if altura_tela // 2 < mouse_y < altura_tela * 2.5 // 4:
                    resetar_jogo()
                    jogo()
                elif altura_tela * 2.5 // 4 < mouse_y < altura_tela * 3 // 4:
                    resetar_jogo()
                    jogo_cooperativo()


        # Espera pelo clique
        esperar_clique()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro: {e}")
        pygame.time.delay(5000)  # Aguarda 5 segundos antes de sair
        pygame.quit()
        sys.exit()