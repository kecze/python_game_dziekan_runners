import pygame
import os


width, height = 1273,845
d_w, d_h = 40,50 #deans width, height
s_w, s_h = 100, 90 #students width and height
b_w, b_h = 100, 100 #bullet width and height
b_fix_w = 30 #bullet width spawn fixing due to wrong size
b_fix_h = 50 #bullet height spawn fixing due to wrong size

#SETTINGS
s_vel = 8 # students velocity
bullet_vel = 8
FPS = 120
max_stud_bullets = 6


#EVENTS
student_hit_dean1 = pygame.USEREVENT + 1
student_hit_dean2 = pygame.USEREVENT + 2

WIN = pygame.display.set_mode((width,height))
pygame.display.set_caption("Dziekan Runners")

bg_img = pygame.image.load("mapa.png")
bg_img = pygame.transform.scale(bg_img,(width,height))

red = (255, 0, 0)

act_dir = 'left'  # start dir

Dziekan1_image = pygame.image.load(os.path.join('characters','dean1.png'))
Dziekan1 = pygame.transform.scale(Dziekan1_image, (d_w, d_h))
Dziekan2_image = pygame.image.load(os.path.join('characters','dean2.png'))
Dziekan2 = pygame.transform.flip(pygame.transform.scale(Dziekan2_image, (d_w, d_h)), True, False)
Student1_image = pygame.image.load(os.path.join('characters','stud1_stop.png'))
Student1 = pygame.transform.scale(Student1_image, (s_w, s_h))
Student_bullet_image = pygame.image.load(os.path.join('items','student_bullet.png'))
Student_bullet = pygame.transform.scale(Student_bullet_image, (b_w, b_h))

border =pygame.Rect(10, 10, width, height)

def draw_window(dziekan1, dziekan2, student1, bullets_right, bullets_left):
    WIN.blit(bg_img, (0, 0))
    WIN.blit(Dziekan1, (dziekan1.x, dziekan1.y))
    WIN.blit(Dziekan2, (dziekan2.x, dziekan2.y))
    WIN.blit(Student1, (student1.x, student1.y))
    for bullet in bullets_right:
        WIN.blit(Student_bullet, (bullet.x, bullet.y))
    for bullet in bullets_left:
        WIN.blit(Student_bullet, (bullet.x, bullet.y))
    pygame.display.update()

def student_movement(keys_pressed, student):
    global act_dir
    if keys_pressed[pygame.K_a] and student.x - s_vel > 0:  # left student
        student.x -= s_vel
        #print('left')
        act_dir = 'left'
    if keys_pressed[pygame.K_d] and student.x + s_vel + student.width < width:  # reight student
        student.x += s_vel
        #print("right")
        act_dir = 'right'
    if keys_pressed[pygame.K_w] and student.y - s_vel > 0:  # up student
        student.y -= s_vel
    if keys_pressed[pygame.K_s] and student.y + s_vel + student.height < height:  # down student
        student.y += s_vel
    return act_dir

def handle_bullets(student_bullets_right, student_bullets_left, student, dziekan1, dziekan2):
    for bullets in student_bullets_right:
        bullets.x += bullet_vel
        if dziekan1.colliderect(bullets):
            pygame.event.post(pygame.event.Event(student_hit_dean1))
            student_bullets_right.remove(bullets)
        elif bullets.x > width or bullets.x < 0:
            student_bullets_right.remove(bullets)

    for bullets in student_bullets_left:
        bullets.x -= bullet_vel
        if dziekan1.colliderect(bullets):
            pygame.event.post(pygame.event.Event(student_hit_dean1))
            student_bullet_right.remove(bullets)
        elif bullets.x > width or bullets.x < 0:
            student_bullets_left.remove(bullets)


def main():
    dziekan1 = pygame.Rect(941, 622, d_w, d_h)
    dziekan2 = pygame.Rect(215, 430, d_w, d_h)
    student1 = pygame.Rect(512, 518, s_w, s_h)

    student_bullet_left = []
    student_bullet_right = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        print(act_dir)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys_pressed = pygame.key.get_pressed()
            student_movement(keys_pressed, student1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event)
                if pygame.mouse.get_pressed(num_buttons=3):
                    if act_dir == 'left' and len(student_bullet_left) < max_stud_bullets:
                        bullet = pygame.Rect(student1.x, student1.y , b_w, b_h)
                        student_bullet_left.append(bullet)
                    if act_dir == 'right' and len(student_bullet_right) < max_stud_bullets:
                        bullet = pygame.Rect(student1.x + student1.width, student1.y , b_w, b_h)
                        student_bullet_right.append(bullet)
        handle_bullets(student_bullet_right, student_bullet_left, student1, dziekan1, dziekan2)
        draw_window(dziekan1, dziekan2, student1, student_bullet_right, student_bullet_left)
    pygame.quit()

if __name__ == "__main__":
    main()