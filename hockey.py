import pygame


pygame.init()

tela = pygame.display.set_mode((640, 480))  
pygame.display.set_caption('HOCKEY')

clock = pygame.time.Clock()

fonte = pygame.font.Font(None, 32)

img_button_dois = pygame.image.load("menu/EmptyButton.png").convert_alpha()

modo = False

class Menu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_button_dois = img_button_dois
        self.rect = self.img_button_dois.get_rect()

    def update(self):
        while True:
            tela.blit(self.img_button_dois, (230, 220))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if img_button_dois.collidepoint(event):
                        modo = img_button_dois

        
        pygame.display.flip()




class Raquete:
    def __init__(self, pos, tamanho, tamanho_tela):
        
        self.rect = pygame.Rect((0, 0), tamanho) # Cria o retangulo
        self.rect.center = pos # Coloca o centro dele na posição
        
        self.tamanho_tela = tamanho_tela

    def desenhar(self, tela):
       pygame.draw.rect(tela, (255, 255, 255), self.rect)
        

    def mover(self, distancia):
        self.rect.move_ip(distancia) # Move o retangulo
        self.rect.clamp_ip((0, 0), self.tamanho_tela) # Não deira sair da tela

    def pegar_posicao(self):
        return self.rect.center



class InterfaceJogador:
    def __init__(self, raquete):
        self.raquete = raquete   # Todas jogador tem uma raquete
        self.pontos = 0  # Todo jogador tem pontos

    @property
    def pontos(self):
        return self._pontos

    @pontos.setter
    def pontos(self, pontos):
        self.imagem_pontos = fonte.render(str(pontos), True, (255, 255, 255))
        self._pontos = pontos    

    def processar_evento(self,evento):
        raise NotImplementedError

    def atualizar(self, pos_bolinha):
        raise NotImplementedError

    def desenhar_raquete(self, tela):
        self.raquete.desenhar(tela)

    def desenhar_pontos(self, tela, posicao):
        tela.blit(self.imagem_pontos, posicao)

    def copiar_rect(self):
        return self.raquete.rect.copy()


class Jogador(InterfaceJogador):
    def __init__(self, raquete, tecla_baixo, tecla_cima):
        super().__init__(raquete)
        self.raquete = raquete

        self.tecla_baixo = tecla_baixo
        self.tecla_cima = tecla_cima

        self.baixo_apertada = False
        self.cima_apertada = False


    def processar_evento(self, evento):
        # Se o evento for o apertar de uma tecla
        if event.type == pygame.KEYDOWN:
            if event.key == self.tecla_cima:
                self.cima_apertada = True

            elif event.key == self.tecla_baixo:
                self.baixo_apertada = True

        # Se o evento for soltar a tecla
        elif event.type == pygame.KEYUP:
            if event.key == self.tecla_cima:
                self.cima_apertada = False

            elif event.key == self.tecla_baixo:
                self.baixo_apertada = False

    def atualizar(self, pos_bolinha):
        if self.cima_apertada and not self.baixo_apertada:
            self.raquete.mover((0, -20)) # **Atenção:** -1 é pra cima

        elif self.baixo_apertada and not self.cima_apertada:
            self.raquete.mover((0, 20)) # **Atenção:** 1 é pra baixo



class InteligenciaArtificial(InterfaceJogador):
    def processar_evento(self, evento):
        pass  

    def atualizar(self, pos_bolinha):
        pos_raquete = self.raquete.pegar_posicao()
        
        if pos_bolinha[1] < pos_raquete[1]:
            self.raquete.mover((0, -20))

        elif pos_bolinha[1] > pos_raquete[1]:
             self.raquete.mover((0, 20))

'''
imagem_texto = fonte.render("Escolha um modo de Jogo:", True, (255, 255, 255))
tela.blit(imagem_texto, (170, 150))

imagem_botao_dois = fonte.render("doisjogadores", True, (0,0,0), (255,0,0))
tela.blit(imagem_botao_dois, (230, 220))

imagem_botao_inte = fonte.render("Computador", True, (0,0,0), (255,255,255))
tela.blit(imagem_botao_inte, (230, 270))


rect_botao_dois = pygame.Rect((230, 220), imagem_botao_dois.get_size())
rect_botao_inte = pygame.Rect((210, 270), imagem_botao_inte.get_size())
   
modo = False 

while not modo:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #termina o programa
            quit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect_botao_dois.collidepoint(event.pos):
                modo = "doisjogadores"
                    
            elif rect_botao_inte.collidepoint(event.pos):
                modo = "Computador"
                    
    clock.tick(10)
'''

class Bolinha:

    def __init__(self, tamanho, velocidade, tamanho_tela):
        self.rect = pygame.Rect((0, 0), tamanho)
        self.velocidade = velocidade

        # Salva a largura e altura separadas
        self.largura_tela, self.altura_tela = tamanho_tela

        #Centraliza a bolinha
        self.rect.center = (self.largura_tela / 2, self.altura_tela / 2)

    def desenhar(self, tela):
        pygame.draw.circle(tela, (255, 0, 0), self.rect.center, int(self.rect.height / 2))

    def atualizar(self):
        if self.rect.top < 0 or self.rect.bottom > self.altura_tela:
            self.velocidade = (self.velocidade[0], -self.velocidade[1])

        self.rect.move_ip(self.velocidade)

    def checar_colisao(self, lista_rects):
        # Checa se algum dos rects colide com a bolinha
        index = self.rect.collidelist(lista_rects)

        if index == -1:
            return

        rect = lista_rects[index]
        self.velocidade = (-(rect.center[0]- self.rect.center[0]) / 2,
                        -(rect.center[1]-self.rect.center[1]) / 2)
    
    
    def definir_posicao(self, posicao):
        self.rect.center = posicao
    
    def definir_velocidade(self, velocidade):
        self.velocidade = velocidade
    
    def pegar_posicao(self):
        return self.rect.center


# Cria um jogador usando w pra cima e s pra baixo
#jogador1 = Jogador(Raquete((50, 240), (30, 150), (640, 480)),
                    #pygame.K_s, pygame.K_w)


# Cria uma inteligencia artificial
jogador1 = InteligenciaArtificial(Raquete((50, 240), (30, 150), (640, 480)))


# Cria um jogador usando as setinhas do teclado
jogador2 = Jogador(Raquete((590, 240), (30, 150), (640, 480)),
                    pygame.K_DOWN, pygame.K_UP)

bolinha = Bolinha((20, 20), (10, 10), (640, 480))





while True:
    for event in pygame.event.get():
            # Processa os eventos
            jogador1.processar_evento(event)
            jogador2.processar_evento(event)

            if event.type == pygame.QUIT:
                    # Termina o programa
                quit()

    if not (640 > bolinha.pegar_posicao()[0] > 0): # saiu da tela 
        if bolinha.pegar_posicao()[0] < 320:
            # Se saiu pra esquerda, vai pra direita
            bolinha.definir_velocidade((10, 0))
            jogador2.pontos += 1
        
        else:
            # Se saiu pra direita, vai pra esquerda
            bolinha.definir_velocidade((-10, 0))
            jogador1.pontos += 1
           
        bolinha.definir_posicao((320, 240))


    tela.fill((0, 0, 0)) # Deixa a janela preta


    jogador1.atualizar(bolinha.pegar_posicao()) # Atualizando o jogador 1
    jogador1.desenhar_raquete(tela)
    jogador1.desenhar_pontos(tela, (100, 20))
    
    

    jogador2.atualizar(bolinha.pegar_posicao()) # Atualizando o jogador 2
    jogador2.desenhar_raquete(tela)
    jogador2.desenhar_pontos(tela, (540, 20))



    bolinha.checar_colisao([jogador1.copiar_rect(), jogador2.copiar_rect()])
    bolinha.atualizar()
    bolinha.desenhar(tela)

    pygame.display.flip()# Atualiza a janela com as mudanças
    
    clock.tick(30) # Limita o jogo a 30 FPS

