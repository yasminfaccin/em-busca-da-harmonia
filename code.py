import pygame
import random
import math

# Inicializa o Pygame
pygame.init()

# Configuração da tela
LARGURA_TELA = 650
ALTURA_TELA = 800

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Busca pela Harmonia")

# Carregar a imagem de fundo
imagem_menu = pygame.image.load("menu.png")  # Nome da imagem do menu
imagem_menu = pygame.transform.scale(imagem_menu, (LARGURA_TELA, ALTURA_TELA))

# Carregar a imagem da tela "Sobre"
imagem_sobre = pygame.image.load("sobre.png")  # Nome da imagem da tela "Sobre"
imagem_sobre = pygame.transform.scale(imagem_sobre, (LARGURA_TELA, ALTURA_TELA))

# Carregar a imagem da tela "Créditos"
imagem_creditos = pygame.image.load("creditos.png")  # Nome da imagem da tela "Créditos"
imagem_creditos = pygame.transform.scale(imagem_creditos, (LARGURA_TELA, ALTURA_TELA))

selecao_modo_imagem = pygame.image.load("SelecaoModo.png") # Imagem da parte de escolehr o modo de jogo
selecao_modo_imagem = pygame.transform.scale(selecao_modo_imagem, (LARGURA_TELA, ALTURA_TELA))

playlist_image = pygame.image.load("playlist.png") # Nome da imagem para o usuario escolher a musica (ALTERAR)
playlist_image = pygame.transform.scale(playlist_image, (LARGURA_TELA, ALTURA_TELA))

jogo_imagem = pygame.image.load("jogo.png") # Nome da imagem do fundo do jogo
jogo_imagem = pygame.transform.scale(jogo_imagem, (LARGURA_TELA, ALTURA_TELA))

# Definir fonte para o texto
font = pygame.font.Font("freesansbold.ttf", 30)


# Definir o texto e suas posições
menu_items = [
    {"text": "Jogar", "position": (326, 357)},
    {"text": "Sobre", "position": (329, 439)},
    {"text": "Créditos", "position": (329, 523)},
    {"text": "Sair", "position": (329, 605)}
]

opcao_tipo_jogo = 0 # Valor da opcao selecionada pelo jogador
opcao_jogo = ["Quero escolher", "Responder"] # Texto da opcao de jogo 

# Índice do item selecionado no menu
item_selecionado = 0

# Imagens correspondentes às perguntas
imagens_perguntas = [
    pygame.image.load("imagem1.png"),  # Pergunta 1
    pygame.image.load("imagem2.png"),  # Pergunta 2
    pygame.image.load("imagem3.png")   # Pergunta 3
]

# Quantidade de perguntas no questionario 
perguntas = 3
musica_selecionada = 0

# Algumas cores definidas para facilitar 
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
ROXO = (56, 27, 176)

# Definir o FPS (frames por segundo)
FPS = 60
clock = pygame.time.Clock()

# Setlist (aqui pode se adicionar mais musicas, ou alterar alguma caracteristica delas)
musicas = {
    0: {'nome': 'musica0.mp3', 'velocidade': 6, 'frequencia': 8, 'tempo': 151.0},  
    1: {'nome': 'musica1.mp3', 'velocidade': 8, 'frequencia': 10, 'tempo': 152.0},
    2: {'nome': 'musica2.mp3', 'velocidade': 12, 'frequencia': 15, 'tempo': 145.0}, 
    3: {'menu': 'musica1.mp3', 'velocidade': 1, 'frequencia': 10, 'tempo': 30.0}
}

# Carrega a música selecionada
pygame.mixer.music.load(musicas[musica_selecionada]['nome'])

# Classe para as notas
class Nota:
    def __init__(self, x, y, tecla, cor=AZUL, velocidade=5):
        self.x = x
        self.y = y
        self.tecla = tecla
        self.cor = cor
        self.velocidade = velocidade
        self.raio = 30
        self.pontos_brilhos = []
        self.pontos_brilhos_ativos = False

    def mover(self):
        self.y += self.velocidade

    def desenhar(self):
        pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)

    def gerar_brilhos(self):
        if not self.pontos_brilhos_ativos:
            self.pontos_brilhos_ativos = True
            for _ in range(30):
                velocidade_x = random.uniform(-5, 5)
                velocidade_y = random.uniform(-5, 5)
                brilho = {
                    'x': self.x,
                    'y': self.y,
                    'vel_x': velocidade_x,
                    'vel_y': velocidade_y,
                    'cor': VERMELHO,
                    'tamanho': random.randint(3, 7),
                    'vida': 120
                }
                self.pontos_brilhos.append(brilho)

    def atualizar_brilhos(self):
        for brilho in self.pontos_brilhos[:]:
            brilho['x'] += brilho['vel_x']
            brilho['y'] += brilho['vel_y']
            brilho['vida'] -= 1
            if brilho['vida'] <= 0:
                self.pontos_brilhos.remove(brilho)

    def desenhar_brilhos(self):
        for brilho in self.pontos_brilhos:
            pygame.draw.circle(tela, brilho['cor'], (int(brilho['x']), int(brilho['y'])), brilho['tamanho'])

    def gerar_erro(self):
        self.erro_x = {
            'x': self.x - 15,
            'y': self.y + 40,
            'vida': 30
        }

    def desenhar_erro(self):
        if hasattr(self, 'erro_x') and self.erro_x:
            fonte = pygame.font.SysFont(None, 50)
            texto = fonte.render("X", True, VERMELHO)
            tela.blit(texto, (self.erro_x['x'], self.erro_x['y']))

            self.erro_x['vida'] -= 1
            if self.erro_x['vida'] <= 0:
                del self.erro_x

# Função para mostrar mensagens na tela
def mostrar_mensagem(texto, cor, posicao, tamanho=40):
    fonte = pygame.font.SysFont(None, tamanho)
    texto_renderizado = fonte.render(texto, True, cor)
    tela.blit(texto_renderizado, posicao)

# Função para desenhar os botões na parte inferior (como círculos)
def desenhar_botoes():
    botao_radius = 40
    posicoes = [100, 250, 400, 550]  # Posições horizontais para os botões
    teclas = ['a', 's', 'd', 'f']
    
    for i, tecla in enumerate(teclas):
        pygame.draw.circle(tela, BRANCO, (posicoes[i], ALTURA_TELA - 100), botao_radius)
        mostrar_mensagem(tecla.upper(), PRETO, (posicoes[i] - 10, ALTURA_TELA - 130), 40)

# Função para verificar se a bolinha está dentro do botão (círculo)
def dentro_do_botao(nota, pos_botao_x):
    botao_radius = 40
    distancia = math.sqrt((nota.x - pos_botao_x) ** 2 + (nota.y - ( 100)) ** 2)
    return distancia <= (nota.raio + botao_radius - 5)

# Função principal do jogo
def jogo():
    notas = []
    teclas_correspondentes = {'a': 100, 's': 250, 'd': 400, 'f': 550}
    jogo_rodando = True
    score = 0
    acertos = 0
    erros = 0
    tempo_total = musicas[musica_selecionada]['tempo']  # Duração total da música em segundos
    tempo_passado = 0  # Tempo passado em segundos

    # Carregar e tocar a música selecionada
    pygame.mixer.music.load(musicas[musica_selecionada]['nome'])
    pygame.mixer.music.play()

    # Linha de ação
    linha_acao_y = ALTURA_TELA - 100

    while jogo_rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f):
                    tecla = pygame.key.name(evento.key)

                    # Verificar se a tecla pressionada corresponde a uma nota
                    for nota in notas[:]:
                        if nota.cor == AZUL and nota.tecla == tecla:
                            score += 1
                            acertos += 1
                            nota.gerar_brilhos()
                            notas.remove(nota)
                            break

        if len(notas) == 0 and random.randint(1, musicas[musica_selecionada]['frequencia']) == 1:
            tecla_aleatoria = random.choice(['a', 's', 'd', 'f'])
            nota = Nota(teclas_correspondentes[tecla_aleatoria], 0, tecla_aleatoria, cor=AZUL, velocidade=musicas[musica_selecionada]['velocidade'])
            notas.append(nota)
        
        

        # Atualizar a tela
        tela.fill(PRETO)
        # Desenhar a imagem de fundo
        tela.blit(jogo_imagem, (0, 0))  # Desenha a imagem de fundo na posição (0, 0)

        # Desenhar os botões
        desenhar_botoes()

        # Mover e desenhar as notas
        for nota in notas[:]:
            nota.mover()
            nota.desenhar()
            nota.atualizar_brilhos()
            nota.desenhar_brilhos()

            if nota.y > linha_acao_y + 30:
                nota.gerar_erro()
                notas.remove(nota)
                erros += 1
            nota.desenhar_erro()

        # Mostrar o score
        mostrar_mensagem(f"Score: {score}", BRANCO, (10, 10), 30)
        mostrar_mensagem(f"Acertos: {acertos}", VERDE, (10, 50), 30)
        mostrar_mensagem(f"Erros: {erros}", VERMELHO, (10, 90), 30)

        if erros == 5:
            mostrar_mensagem("Você Perdeu!", VERMELHO, (LARGURA_TELA // 2 - 100, ALTURA_TELA // 2), 50)
            pygame.mixer.music.stop()
            pygame.display.flip()
            pygame.time.delay(2000)  # Espera 2 segundos para mostrar a mensagem
            jogo_rodando = False  # Fechar o jogo quando o tempo acabar
        
        tempo_passado += 1 / FPS
        if tempo_passado >= tempo_total:
            # Condição de vitória: se o tempo total da música foi alcançado
            mostrar_mensagem("Você Venceu!", VERDE, (LARGURA_TELA // 2 - 100, ALTURA_TELA // 2), 50)
            pygame.mixer.music.stop()
            pygame.display.flip()
            pygame.time.delay(2000)  # Espera 2 segundos para mostrar a mensagem
            jogo_rodando = False  # Fechar o jogo quando o tempo acabar

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(FPS)

    menu()  # Volta para o menu após o jogo

# Função do menu de seleção de música
def menu():
    global musica_selecionada
    menu_rodando = True

    while menu_rodando:
        tela.fill(PRETO)

        mostrar_mensagem("Selecione uma música", BRANCO, (200, 100), 40)

        # Desenhando os botões de seleção de música
        botao_radius = 40
        posicoes = [100, 250, 400]
        nomes = ['Musica 0', 'Musica 1', 'Musica 2']

        for i, nome in enumerate(nomes):
            pygame.draw.circle(tela, BRANCO, (posicoes[i], ALTURA_TELA - 100), botao_radius)
            mostrar_mensagem(nome, PRETO, (posicoes[i] - 30, ALTURA_TELA - 130), 30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                menu_rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Se o botão esquerdo do mouse for clicado
                    if 60 < evento.pos[0] < 140:
                        musica_selecionada = 0
                        jogo()  # Iniciar o jogo com a música selecionada
                    elif 220 < evento.pos[0] < 300:
                        musica_selecionada = 1
                        jogo()  # Iniciar o jogo com a música selecionada
                    elif 370 < evento.pos[0] < 450:
                        musica_selecionada = 2
                        jogo()  # Iniciar o jogo com a música selecionada

        pygame.display.flip()
        clock.tick(FPS)

    # Iniciar o menu
    menu()
# Função para desenhar o menu
def desenha_o_menu():
    tela.blit(imagem_menu, (0, 0))  # Desenha o fundo

    for index, item in enumerate(menu_items):
        text = font.render(item["text"], True, PRETO) 
        text_rect = text.get_rect(center=item["position"])
        
        # Destaque a opção selecionada
        if index == opcao_tipo_jogo:
            text = font.render(item["text"], True, ROXO) 

        tela.blit(text, text_rect)  # Desenha o texto na tela

    pygame.display.update()  # Atualiza a tela
    
# Função para desenhar a tela do jogo
def desenha_tela_jogo():
    tela.blit(selecao_modo_imagem, (0, 0))  # Desenha a imagem do jogo

    # Fonte e tamanho
    modo_jogo_fonte = pygame.font.Font("freesansbold.ttf", 20)  
    
    # Desenha as opções
    for index, option in enumerate(opcao_jogo):
        text = modo_jogo_fonte.render(option, True, PRETO)  # Cor do texto (preto)
        if index == opcao_tipo_jogo:
            text = modo_jogo_fonte.render(option, True, ROXO) 
        text_rect = text.get_rect(center=(LARGURA_TELA // (3 if index == 0 else 1.5), ALTURA_TELA // 2))  # Centraliza a opção
        tela.blit(text, text_rect)  # Desenha a opção na tela

    pygame.display.update()  # Atualiza a tela


def desenha_selecao_de_musica():
    tela.blit(playlist_image, (0, 0))  # Desenha a imagem de fundo da parte da playlist

    # Definie o texto, cordenada..
    textos_playlist = [
        {"text": "Waiting Around ( LoFi , Calm )", "position": (383, 220)},  
        {"text": "When I Was Human ( LoFi , Chill )", "position": (393, 330)},  
        {"text": "Yet Again ( LoFi , Peaceful )", "position": (375, 450)},
        {"text": "", "position" : ((LARGURA_TELA // 2), 500 )}  
    ]
    
    # Fonte e tamanho
    font_playlist = pygame.font.Font("freesansbold.ttf", 15)  
    
    # Desenha os textos personalizados com a nova fonte
    for index, item in enumerate(textos_playlist):
        # Se a música estiver selecionada, mude a cor para vermelha
        if index == musica_selecionada:
            text = font_playlist.render(item["text"], True, ROXO)  
        else:
            text = font_playlist.render(item["text"], True, PRETO)  

        text_rect = text.get_rect(center=item["position"])  # Posiciona o texto
        tela.blit(text, text_rect)  # Desenha o texto na tela
          
    pygame.display.update()  # Atualiza a tela

    
# Função principal do menu
def menu():
    global opcao_tipo_jogo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Sair do loop do menu

            # Navegação com as setas do teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcao_tipo_jogo = (opcao_tipo_jogo - 1) % len(menu_items)  # Vai para cima
                elif event.key == pygame.K_DOWN:
                    opcao_tipo_jogo = (opcao_tipo_jogo + 1) % len(menu_items)  # Vai para baixo
                elif event.key == pygame.K_RETURN:  # Enter 
                    if menu_items[opcao_tipo_jogo]["text"] == "Jogar":
                        tela_modo_jogo()
                    elif menu_items[opcao_tipo_jogo]["text"] == "Sobre":
                        mostra_tela_sobre()
                    elif menu_items[opcao_tipo_jogo]["text"] == "Créditos":
                        mostra_tela_creditos()
                    elif menu_items[opcao_tipo_jogo]["text"] == "Sair":
                        running = False  # Sair do loop do menu

        desenha_o_menu()  # Atualiza o menu

    pygame.quit()  # Encerra o Pygame

# Função para mostrar a tela "Sobre"
def mostra_tela_sobre():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Sair do loop da tela "Sobre"

            # Verifica se a tecla 'Esc' foi pressionada
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Sai do loop da tela "Sobre"

        # Desenha a imagem da tela "Sobre"
        tela.blit(imagem_sobre, (0, 0))
        pygame.display.update()  # Atualiza a tela

    # Retorna ao menu principal após sair da tela "Sobre"
    desenha_o_menu()  # Redesenha o menu

# Função para mostrar a tela "Créditos"
def mostra_tela_creditos():
    running = True
    while running :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Sair do loop da tela "Créditos"

            # Verifica se a tecla 'Esc' foi pressionada
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Sai do loop da tela "Créditos"

        # Desenha a imagem da tela "Créditos"
        tela.blit(imagem_creditos, (0, 0))
        pygame.display.update()  # Atualiza a tela

    # Retorna ao menu principal após sair da tela "Créditos"
    desenha_o_menu()  # Redesenha o menu
    
 
# Função para a tela do jogo
def tela_modo_jogo():
    global opcao_tipo_jogo
    selecao_modo = True
    while selecao_modo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selecao_modo = False  # Sair do loop da tela do jogo

            # Navegação com as setas do teclado 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    opcao_tipo_jogo = (opcao_tipo_jogo - 1) % len(opcao_jogo)  # Vai para a esquerda
                elif event.key == pygame.K_RIGHT:
                    opcao_tipo_jogo = (opcao_tipo_jogo + 1) % len(opcao_jogo)  # Vai para a direita
                elif event.key == pygame.K_RETURN:  # Enter
                    if opcao_tipo_jogo == 1:  # Se a opção 1 for selecionada
                        questionario()  # Inicia o questionário
                        print("selecionado opcao 2")
                    else:  # Se a opção 2 for selecionada
                        print("selecionado opção 1")
                        selecao_de_musica()

        desenha_tela_jogo()  # Atualiza a tela do jogo
        
# Função para a seleção de música
def selecao_de_musica():
    global musica_selecionada 
    musica_selecionada = 0  # Inicializa a variável musica_selecionada
    selecao_ativa = True
    
    while selecao_ativa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selecao_ativa = False  # Sair do loop de selecao de musica
                
            # Navegação com as setas do teclado 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: 
                    musica_selecionada = (musica_selecionada - 1) % 3  # Limitar a seleção de música a 3 opções
                elif event.key == pygame.K_DOWN:
                    musica_selecionada = (musica_selecionada + 1) % 3  # Limitar a seleção de música a 3 opções
                elif event.key == pygame.K_RETURN:  # Enter
                    if musica_selecionada == 3:
                        tela_modo_jogo()  # Se for "voltar", retorna ao modo de jogo
                    else:
                        jogo()  # Inicia o jogo com a música selecionada
                        print("Musica selecionada:", musica_selecionada)

        desenha_selecao_de_musica()  # Atualiza a tela da playlist
        
# Função do questionário
def questionario():
    pergunta_atual = 0
    respostas = []  # Lista para armazenar as respostas do usuário
    perguntas_ativas = True
    resposta_selecionada = 0  # Índice da resposta selecionada (0 para "sim", 1 para "não")

    while perguntas_ativas:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                perguntas_ativas = False  # Sair do loop do questionário

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter
                    # Armazenar a resposta do usuário
                    if resposta_selecionada == 0:  # Se o usuário escolheu "sim"
                        respostas.append(1)  # Armazena 1 para "sim"
                    elif resposta_selecionada == 1:  # Se o usuário escolheu "não"
                        respostas.append(2)  # Armazena 2 para "não"

                    # Limpa a tela e exibe a imagem da pergunta atual
                    tela.fill(BRANCO) 
                    tela.blit(imagens_perguntas[pergunta_atual], (0, 0))  # Exibe a imagem correspondente
                    pygame.display.flip()  # Atualiza a tela

                    # Aguarda um tempo antes de avançar
                    pygame.time.delay(2000)  # Espera 2 segundos
                    pergunta_atual += 1  # Avança para a próxima pergunta

                    if pergunta_atual >= perguntas:
                        print("Fim do questionário!")
                        print("Respostas:", respostas)  # Mostra as respostas do usuário
                        perguntas_ativas = False  # Termina o questionário

                elif event.key == pygame.K_LEFT:  # Seleciona a opção "sim"
                    resposta_selecionada = 0
                elif event.key == pygame.K_RIGHT:  # Seleciona a opção "não"
                    resposta_selecionada = 1

        # Renderiza a imagem correspondente à pergunta atual
        tela.fill(BRANCO)  # Limpa a tela com a cor branca

        if pergunta_atual < perguntas :
            # Exibe a imagem da pergunta atual
            tela.blit(imagens_perguntas[pergunta_atual], (0, 0))  # Exibe a imagem correspondente

            # Exibe as opções de resposta
            resposta1_texto = "sim"
            resposta2_texto = "nao"
            font = pygame.font.Font(None, 36)
            texto1 = font.render(resposta1_texto, True, PRETO)
            texto2 = font.render(resposta2_texto, True, PRETO)

            # Define as coordenadas para as opções
            coord_resposta1 = (185, 380)  # Coordenadas da opção "sim"
            coord_resposta2 = (420, 380)  # Coordenadas da opção "não"

            # Desenha as opções na tela
            if resposta_selecionada == 0:
                texto1 = font.render(resposta1_texto, True, ROXO)  # Cor do texto (roxo) para a opção selecionada
            if resposta_selecionada == 1:
                texto2 = font.render(resposta2_texto, True, ROXO)  # Cor do texto (roxo) para a opção selecionada

            tela.blit(texto1, coord_resposta1)  # Exibe a primeira opção
            tela.blit(texto2, coord_resposta2)   # Exibe a segunda opção

        pygame.display.flip()  # Atualiza a tela

    # Lógica de seleção de música com base nas respostas
    sim_count = respostas.count(1)
    nao_count = respostas.count(2)

    # Seleciona a música com base nas respostas
    if sim_count == 3:
        musica_selecionada = 0  # Todas as respostas sao sim
    elif nao_count == 3:
        musica_selecionada = 1  # Todas as respostas sao nao
    elif respostas[0] == 1 :
        musica_selecionada = 2  
    elif respostas[1] == 1 :
        musica_selecionada = 0

    print("Música selecionada:", musica_selecionada)  # Mostra a música selecionada
    jogo()  # Inicia o jogo com a música selecionada
    

menu()  # Redesenha o menu
