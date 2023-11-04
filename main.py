import pygame
import os
import random


ECRA_LARGURA = 500
ECRA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))
IMAGEM_CHAO =pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))
IMAGEM_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png'))) ]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial",50)



class Passaro:
    IMGS = IMAGEM_PASSARO
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO= 20
    TEMPO_ANIMACAO = 5

    def __init__(self,x,y):
        self.x = x
        self.y =x
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular a deslocação
        self.tempo += 1
        deslocacao = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        # restringir a deslocação
        if deslocacao > 16:
            deslocacao = 16
        elif deslocacao <0:
            deslocacao -=2

        self.y += deslocacao
        # angulo do passaro

        if deslocacao < 0 or self.y < (self.altura + 50): # angulo do passaro na imagem na curva descendente
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO


    def desenhar(self,ecra):
        # definir imagem do passaro
        self.contagem_imagem += 1
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0
        # se o passaro estiver a cair, deixa de bater asas
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2



        # desenhar a imagem

        imagem_com_rotacao = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem= self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_com_rotacao.get_rect(center=pos_centro_imagem) # buscar o retangulo da imagem
        ecra.blit(imagem_com_rotacao, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_top = 0
        self.pos_base = 0
        self.cano_topo = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.cano_base = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50,450)
        self.pos_top = self.altura - self.cano_topo.get_height()
        self.pos_base = self.altura + self. DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, ecra):
        ecra.blit(self.cano_topo, (self.x, self.pos_top))
        ecra.blit(self.cano_base, (self.x, self.pos_base))

    def colisao(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_top-round(passaro.y))
        distancia_base =  (self.x - passaro.x, self.pos_base-round(passaro.y))
        topo_ponto = passaro_mask.overlap(topo_mask,distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, ecra):
        ecra.blit(self.IMAGEM, (self.x1,self.y))
        ecra.blit(self.IMAGEM, (self.x2,self.y))


def desenhar_ecra(ecra, passaros, canos, chao, pontos):
    ecra.blit(IMAGEM_BACKGROUND, (0,0))
    for passaro in passaros:
        passaro.desenhar(ecra)
    for cano in canos:
        cano.desenhar(ecra)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255,255,255))
    ecra.blit(texto, (ECRA_LARGURA-10-texto.get_width(),10))
    chao.desenhar(ecra)
    pygame.display.update()




def main():
    passaros = [Passaro(230,350)]
    chao = Chao(730)
    canos = [Cano(700)]
    ecra = pygame.display.set_mode((ECRA_LARGURA, ECRA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    correr_jogo = True
    while correr_jogo:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr_jogo = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                for passaro in passaros:
                    passaro.pular()
        # mover as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adionar_canos= False
        remover_canos =[]
        for cano in canos:
            for i ,passaro in enumerate(passaros):
                if cano.colisao(passaro):
                    passaros.pop(i)
                    correr_jogo = False
                    pygame.quit()
                    quit()
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adionar_canos = True
            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)

        if adionar_canos:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
        desenhar_ecra(ecra,passaros,canos,chao,pontos)


if __name__== '__main__':
    main()

