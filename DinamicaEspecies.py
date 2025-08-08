import pygame
import numpy as np
import random
from enum import Enum
from dataclasses import dataclass

LARGURA, ALTURA = 800, 600
TAMANHO_CELULA = 10
COR_FUNDO = (10, 10, 10)

class TipoOrganismo(Enum):
    VAZIO = 0
    PRESA = 1
    PREDADOR = 2

@dataclass
class Gene:
    velocidade: float
    agressividade: float
    taxa_reproducao: float

class Organismo:
    def __init__(self, tipo, genes=None):
        self.tipo = tipo
        self.genes = genes or self.gerar_genes()
        self.energia = 100
        self.memoria = []
        self.idade = 0
        
    def gerar_genes(self):
        if self.tipo == TipoOrganismo.PRESA:
            return Gene(
                velocidade=random.uniform(1.0, 1.5),
                agressividade=random.uniform(0, 0.3),
                taxa_reproducao=random.uniform(0.2, 0.4)
            )
        else:
            return Gene(
                velocidade=random.uniform(0.8, 1.2),
                agressividade=random.uniform(0.5, 1.0),
                taxa_reproducao=random.uniform(0.1, 0.3)
            )
    
    def get_cor(self):
        if self.tipo == TipoOrganismo.PRESA:
            return (0, 255, 0)
        elif self.tipo == TipoOrganismo.PREDADOR:
            return (255, 0, 0)
        return (0, 0, 0)
    
    def tomar_decisao(self, vizinhos):
        self.idade += 1
        self.energia -= 1
        
        if self.tipo == TipoOrganismo.PRESA:
            predadores_vizinhos = sum(1 for v in vizinhos if v.tipo == TipoOrganismo.PREDADOR)
            if predadores_vizinhos > 0:
                return "fugir"
            return "pastar"
        else:
            presas_vizinhos = sum(1 for v in vizinhos if v.tipo == TipoOrganismo.PRESA)
            if presas_vizinhos > 0:
                return "caçar"
            return "explorar"
    
    def executar_acao(self, acao, grid, i, j):
        if acao == "fugir":
            return self.mover_aleatorio(grid, i, j)
        elif acao == "pastar":
            self.energia += 2
        elif acao == "caçar":
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                        if grid[ni][nj].tipo == TipoOrganismo.PRESA:
                            self.energia += grid[ni][nj].energia * 0.7
                            grid[ni][nj] = Organismo(TipoOrganismo.VAZIO)
                            return
        elif acao == "explorar":
            return self.mover_aleatorio(grid, i, j)
    
    def mover_aleatorio(self, grid, i, j):
        direcoes = [(0,1), (1,0), (0,-1), (-1,0)]
        random.shuffle(direcoes)
        for di, dj in direcoes:
            ni, nj = i + di, j + dj
            if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                if grid[ni][nj].tipo == TipoOrganismo.VAZIO:
                    grid[ni][nj] = self
                    grid[i][j] = Organismo(TipoOrganismo.VAZIO)
                    return
    
    def reproduzir(self):
        if self.energia > 120 and self.idade > 10:
            self.energia /= 2
            novos_genes = Gene(
                max(0.5, self.genes.velocidade + random.uniform(-0.1, 0.1)),
                max(0, min(1, self.genes.agressividade + random.uniform(-0.05, 0.05))),
                max(0.05, self.genes.taxa_reproducao + random.uniform(-0.02, 0.02))
            )
            return Organismo(self.tipo, novos_genes)
        return None

def inicializar_grid(linhas, colunas):
    grid = [[Organismo(TipoOrganismo.VAZIO) for _ in range(colunas)] for _ in range(linhas)]
    for _ in range(100):
        x, y = random.randint(0, linhas-1), random.randint(0, colunas-1)
        grid[x][y] = Organismo(TipoOrganismo.PRESA)
    
    for _ in range(20):
        x, y = random.randint(0, linhas-1), random.randint(0, colunas-1)
        grid[x][y] = Organismo(TipoOrganismo.PREDADOR)
        
    return grid

def atualizar_grid(grid):
    linhas, colunas = len(grid), len(grid[0])
    nova_grid = [[Organismo(TipoOrganismo.VAZIO) for _ in range(colunas)] for _ in range(linhas)]
    
    for i in range(linhas):
        for j in range(colunas):
            if grid[i][j].tipo != TipoOrganismo.VAZIO:
                vizinhos = []
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < linhas and 0 <= nj < colunas:
                            vizinhos.append(grid[ni][nj])
                
                acao = grid[i][j].tomar_decisao(vizinhos)
                grid[i][j].executar_acao(acao, grid, i, j)
                if grid[i][j].energia <= 0 or grid[i][j].idade > 50:
                    grid[i][j] = Organismo(TipoOrganismo.VAZIO)
                if random.random() < grid[i][j].genes.taxa_reproducao:
                    filho = grid[i][j].reproduzir()
                    if filho:
                        ni, nj = i + random.randint(-1, 1), j + random.randint(-1, 1)
                        if 0 <= ni < linhas and 0 <= nj < colunas and grid[ni][nj].tipo == TipoOrganismo.VAZIO:
                            grid[ni][nj] = filho
    
    return grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Dinâmica de Espécies")
    
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
        
        screen.fill(COR_FUNDO)
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