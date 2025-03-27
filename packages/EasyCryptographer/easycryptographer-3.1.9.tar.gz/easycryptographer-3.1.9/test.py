import math
import sys

import pygame

# 初始化 Pygame
pygame.init()

# 设置窗口
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circular Bouncing Ball")

# 定义圆的参数
circle_center = (400, 300)  # 圆心坐标（窗口中心）
circle_radius = 300  # 圆形区域半径

# 定义弹球参数
radius = 20
ball_pos = [circle_center[0], circle_center[1]]  # 初始位置在圆心附近
ball_vel = [1, 5]  # 初始速度（可调整方向和大小）
ball_color = (255, 0, 0)  # 红色

# 物理引擎参数
damping = 1.01
gravity = 0.2

# 控制帧率
clock = pygame.time.Clock()

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 更新球的位置（物理引擎）
    # 应用重力（可选）
    ball_vel[1] += gravity

    # 计算新位置
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # 碰撞检测（与圆形边界）
    dx = ball_pos[0] - circle_center[0]
    dy = ball_pos[1] - circle_center[1]
    dist_sq = dx ** 2 + dy ** 2
    max_dist = circle_radius - radius  # 球心到圆心的最大允许距离
    max_dist_sq = max_dist ** 2

    if dist_sq > max_dist_sq:
        # 计算单位法向量（指向圆心的反方向）
        distance = math.sqrt(dist_sq)
        nx = dx / distance
        ny = dy / distance

        # 计算速度在法向量上的投影
        v_dot_n = ball_vel[0] * nx + ball_vel[1] * ny

        # 反射后的速度（弹性碰撞）
        new_vx = ball_vel[0] - 2 * v_dot_n * nx
        new_vy = ball_vel[1] - 2 * v_dot_n * ny

        # 应用衰减（若 damping < 1，则每次碰撞速度减少）
        ball_vel[0] = new_vx * damping
        ball_vel[1] = new_vy * damping

        # 调整球的位置到圆形边界上
        scale = max_dist / distance
        ball_pos[0] = circle_center[0] + dx * scale
        ball_pos[1] = circle_center[1] + dy * scale

    # 绘制画面
    screen.fill((255, 255, 255))  # 白色背景
    # 绘制圆形边界
    pygame.draw.circle(screen, (128, 128, 128), circle_center, circle_radius, 2)
    # 绘制球体
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), radius)
    pygame.display.flip()

    # 控制帧率（建议 60 FPS）
    clock.tick(60)

pygame.quit()
sys.exit()
