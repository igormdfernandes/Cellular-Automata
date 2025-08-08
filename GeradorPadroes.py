import pygame
import numpy as np
import random

LARGURA, ALTURA = 800, 600
TAMANHO_CELULA = 5
COR_FUNDO = (0, 0, 0)

class CelulaPadrao:
    def __init__(self, estado=0):
        self.estado = estado  # 0 a 1 (float)
        self.ultimo_estado = estado
        self.tendencia = random.uniform(-0.1, 0.1)
        
    def get_cor(self):
        valor = int(255 * self.estado)
        return (valor, valor, valor)
    
    def atualizar(self, vizinhos):
        soma_vizinhos = sum(v.ultimo_estado for v in vizinhos)
        media_vizinhos = soma_vizinhos / len(vizinhos) if vizinhos else 0
        
        self.ultimo_estado = self.estado
        delta = (media_vizinhos - self.estado) * 0.1 + self.tendencia
        self.estado = max(0, min(1, self.estado + delta + random.uniform(-0.05, 0.05)))
        
        if random.random() < 0.01:
            self.tendencia = random.uniform(-0.1, 0.1)

def inicializar_grid(linhas, colunas):
    grid = [[CelulaPadrao() for _ in range(colunas)] for _ in range(linhas)]
    
    for i in range(linhas):
        for j in range(colunas):
            if random.random() < 0.05:
                grid[i][j].estado = random.random()
                
    return grid

def atualizar_grid(grid):
    linhas, colunas = len(grid), len(grid[0])
    nova_grid = [[CelulaPadrao() for _ in range(colunas)] for _ in range(linhas)]
    
    for i in range(linhas):
        for j in range(colunas):
            vizinhos = []
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < linhas and 0 <= nj < colunas:
                        vizinhos.append(grid[ni][nj])
            
            nova_grid[i][j] = CelulaPadrao(grid[i][j].estado)
            nova_grid[i][j].ultimo_estado = grid[i][j].ultimo_estado
            nova_grid[i][j].tendencia = grid[i][j].tendencia
            nova_grid[i][j].atualizar(vizinhos)
    
    return nova_grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Gerador de Padrões Emergentes")
    
    linhas, colunas = ALTURA // TAMANHO_CELULA, LARGURA // TAMANHO_CELULA
    grid = inicializar_grid(linhas, colunas)
    
    executando = True
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
                elif event.key == pygame.K_s:
                    i, j = random.randint(0, linhas-1), random.randint(0, colunas-1)
                    grid[i][j].estado = 1.0
        
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