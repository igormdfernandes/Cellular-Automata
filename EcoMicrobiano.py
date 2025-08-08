import pygame
import numpy as np
from enum import Enum
import random

LARGURA, ALTURA = 800, 600
TAMANHO_CELULA = 10
COR_FUNDO = (10, 10, 10)
COR_GRADE = (40, 40, 40)

class TipoAgente(Enum):
    VAZIO = 0
    PRODUTOR = 1
    CONSUMIDOR = 2
    DECOMPOSITOR = 3

class AgenteMicrobiano:
    def __init__(self, tipo=TipoAgente.VAZIO, energia=100):
        self.tipo = tipo
        self.energia = energia
        self.metabolismo = np.random.uniform(0.8, 1.2)
        self.resistencia = np.random.uniform(0.5, 1.5)
        self.idade = 0
        
    def get_cor(self):
        if self.tipo == TipoAgente.PRODUTOR:
            return (0, 200, 0)
        elif self.tipo == TipoAgente.CONSUMIDOR:
            return (200, 0, 0)
        elif self.tipo == TipoAgente.DECOMPOSITOR:
            return (150, 150, 0)
        return (0, 0, 0)
        
    def atualizar(self, vizinhos):
        self.idade += 1
        self.energia -= 2 * self.metabolismo
        
        if self.tipo == TipoAgente.PRODUTOR:
            self.energia += 5 * self.resistencia
        elif self.tipo == TipoAgente.CONSUMIDOR:
            self.alimentar(vizinhos)
        elif self.tipo == TipoAgente.DECOMPOSITOR:
            self.reciclar(vizinhos)
            
        if self.energia <= 0 or self.idade > 100:
            return TipoAgente.VAZIO
        return self.tipo
    
    def alimentar(self, vizinhos):
        for vizinho in vizinhos:
            if vizinho and vizinho.tipo == TipoAgente.PRODUTOR and random.random() < 0.3:
                self.energia += vizinho.energia * 0.5
                vizinho.energia *= 0.5
                break
                
    def reciclar(self, vizinhos):
        for vizinho in vizinhos:
            if vizinho and vizinho.tipo == TipoAgente.VAZIO and random.random() < 0.1:
                vizinho.tipo = TipoAgente.PRODUTOR
                vizinho.energia = 50
                self.energia += 10
                break
                
    def reproduzir(self):
        if self.energia > 150:
            self.energia /= 2
            novo_agente = AgenteMicrobiano(self.tipo)
            novo_agente.metabolismo = max(0.5, self.metabolismo + random.uniform(-0.1, 0.1))
            novo_agente.resistencia = max(0.3, self.resistencia + random.uniform(-0.1, 0.1))
            return novo_agente
        return None

def inicializar_grid(linhas, colunas):
    grid = [[AgenteMicrobiano(TipoAgente.VAZIO) for _ in range(colunas)] for _ in range(linhas)]
    
    for _ in range(100):
        x, y = random.randint(0, linhas-1), random.randint(0, colunas-1)
        tipo = random.choice([TipoAgente.PRODUTOR, TipoAgente.CONSUMIDOR, TipoAgente.DECOMPOSITOR])
        grid[x][y] = AgenteMicrobiano(tipo)
        
    return grid

def atualizar_grid(grid):
    linhas, colunas = len(grid), len(grid[0])
    novas_celulas = [[None for _ in range(colunas)] for _ in range(linhas)]
    
    for i in range(linhas):
        for j in range(colunas):
            if grid[i][j]:
                novas_celulas[i][j] = AgenteMicrobiano(grid[i][j].tipo)
                novas_celulas[i][j].energia = grid[i][j].energia
                novas_celulas[i][j].metabolismo = grid[i][j].metabolismo
                novas_celulas[i][j].resistencia = grid[i][j].resistencia
                novas_celulas[i][j].idade = grid[i][j].idade
            else:
                novas_celulas[i][j] = AgenteMicrobiano(TipoAgente.VAZIO)
    
    for i in range(linhas):
        for j in range(colunas):
            if novas_celulas[i][j].tipo != TipoAgente.VAZIO:
                vizinhos = []
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < linhas and 0 <= nj < colunas and grid[ni][nj]:
                            vizinhos.append(grid[ni][nj])
                
                resultado = novas_celulas[i][j].atualizar(vizinhos)
                if resultado == TipoAgente.VAZIO:
                    novas_celulas[i][j] = AgenteMicrobiano(TipoAgente.VAZIO)
    
    for i in range(linhas):
        for j in range(colunas):
            if novas_celulas[i][j].tipo != TipoAgente.VAZIO and random.random() < 0.01:
                filho = novas_celulas[i][j].reproduzir()
                if filho:
                    ni, nj = i + random.randint(-1, 1), j + random.randint(-1, 1)
                    if 0 <= ni < linhas and 0 <= nj < colunas:
                        if novas_celulas[ni][nj].tipo == TipoAgente.VAZIO:
                            novas_celulas[ni][nj] = filho
                            
    return novas_celulas

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Ecossistema Microbiano")
    
    linhas, colunas = ALTURA // TAMANHO_CELULA, LARGURA // TAMANHO_CELULA
    grid = inicializar_grid(linhas, colunas)
    
    executando = False
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    executando = not executando
                elif event.key == pygame.K_r:
                    grid = inicializar_grid(linhas, colunas)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = pos[1] // TAMANHO_CELULA, pos[0] // TAMANHO_CELULA
                if 0 <= x < linhas and 0 <= y < colunas:
                    grid[x][y] = AgenteMicrobiano(random.choice([TipoAgente.PRODUTOR, TipoAgente.CONSUMIDOR, TipoAgente.DECOMPOSITOR]))
        
        screen.fill(COR_FUNDO)
        
        for x in range(0, LARGURA, TAMANHO_CELULA):
            pygame.draw.line(screen, COR_GRADE, (x, 0), (x, ALTURA))
        for y in range(0, ALTURA, TAMANHO_CELULA):
            pygame.draw.line(screen, COR_GRADE, (0, y), (LARGURA, y))
        
        for i in range(linhas):
            for j in range(colunas):
                cor = grid[i][j].get_cor()
                pygame.draw.rect(screen, cor, (j*TAMANHO_CELULA, i*TAMANHO_CELULA, TAMANHO_CELULA-1, TAMANHO_CELULA-1))
        
        pygame.display.flip()
        
        if executando:
            grid = atualizar_grid(grid)
        
        clock.tick(10)

if __name__ == "__main__":
    main()