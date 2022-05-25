from audioop import mul
from msilib.schema import RemoveIniFile
from unittest import result
from importlib_metadata import distribution
from psutil import CONN_CLOSE_WAIT
from depends import *
from gameVar import *
from Ball import Ball
from Wall import Wall
from gameFunc import *
import time
from numpy import dot, random
from numpy.linalg import norm
from copy import deepcopy


class ChaosModel:
    def __init__(self, population_size, life_span, epochs):
        self.population_size = max(6, population_size)
        self.life_span = life_span
        self.epochs = epochs

        self.goal_walls, self.walls, self.spawnArea = setupStage()

    def fitness(self):
        center_n = pygame.Vector2( sum(x.body.position.x for x in self.balls)/self.population_size, sum(x.body.position.y for x in self.balls)/self.population_size )
        for ball in self.balls:
            score = 0
            score += (1e3 - ball.best) / 1e3
            # score += norm(ball.body.position-center_n)/1e3
            ball.prev_score = ball.new_score
            ball.new_score = score
        self.balls.sort(key=lambda x: -x.new_score)
        return self.balls

    def train(self):
        self.balls = generate_balls(self.population_size, self.spawnArea, self.goal_walls)

        for i in range(self.epochs):
            runMotion(
                self.goal_walls, self.walls, self.balls, self.spawnArea, self.life_span
            )
            scores = self.fitness()
            best_path = deepcopy(scores[0].paths)

            # for ball in self.balls:
            #     ball.remove()
            # self.balls = generate_balls(self.population_size, self.spawnArea, self.goal_walls)

            
            for ball in self.balls:
                self.mutate(ball)
                ball.body.position = self.spawnArea.center
                ball.best = 100000
                ball.pause = False
                ball.counter = 0
                ball.color = RED

            parents = self.random_selection([[ball.new_score,ball.paths]for ball in self.balls], 4)

            self.balls[-1].paths = best_path
            self.balls[-1].color = CYAN

            # remove_indices = []
            # for i in range(len(self.balls)):
            #     if self.balls[i].new_score<=self.balls[i].prev_score*1.2 and self.population_size-len(remove_indices)>4:
            #         self.balls[i].remove()
            #         remove_indices.append(i)
            #     self.balls[i].color = YELLOW
            # removed_n = 3*len(remove_indices)//4
            # for i in sorted(self.raXndom_selection(remove_indices, removed_n))[::-1]:
            # for i in remove_indices[::-1]:
            #     self.balls.pop(i)

            # gap = self.population_size-len(self.balls)

            # best_n = min(4, len(self.balls))
            # child_cnt = gap//2
            # parents = scores[:best_n]

            # for b in parents:b.color = GREEN
            # offsprings = self.crossOver(parents, child_cnt)
            # random_gen = generate_balls(
            #     gap - child_cnt , self.spawnArea, self.goal_walls
            # )

            # for ball in self.balls:
            #     ball.body.position = self.spawnArea.center
            #     ball.counter = 0
            #     ball.should_pause = False
            #     ball.best = 10000
            #     self.mutate(ball)
            #     ball.body.position = self.spawnArea.center

            # self.balls[-1].remove()
            # self.balls.pop(-1)
            # best = Ball(screen,space,self.spawnArea.x,self.spawnArea.y,self.goal_walls,paths=best_path,color=CYAN)
            # self.balls.append(best)



            # new_gen = self.balls

            # new_gen = self.balls + offsprings + random_gen
            # print(len(new_gen), gap-child_cnt)

            # self.balls = new_gen

    def random_selection(self, scores, cnt):

        total = sum([x[0] for x in scores])  # Total sum of scores
        temp_scores = [[x[0] / total, x[1]] for x in scores]  # Normailizing scores data
        cdf = []
        cur_total = 0
        for x in temp_scores:
            cur_total += x[0]
            cdf += [cur_total]

        # Random selection directed by cdf
        selected = []
        for _ in range(cnt):
            p = random.random()
            for i in range(len(cdf)):
                if p <= cdf[i]:
                    selected += [scores[i][1]]
                    break

        return selected

    def mutate(self, ball):
        
        data_size = len(ball.paths)
        mutated_strip_length = max(1, data_size // 20)
        for _ in range(2):
            path_strip = random_path(n_steps=mutated_strip_length)
            i = random.randint(0, data_size)
            ball.paths[i : i + mutated_strip_length] = path_strip
        return

    def crossOver(self, parents, child_cnt):
        if len(parents)==0 or child_cnt==0:
            return []
        
        children = generate_balls(child_cnt, self.spawnArea, self.goal_walls)

        def cross(parent1, parent2):
            size = len(parent1)
            strip_size = int(random.normal(size / 20, size / 20))
            strip_size = max(0, strip_size)
            strip_size = min(size, strip_size)
            while random.random() < 0.7:
                i = random.randint(0, size - strip_size)
                j = random.randint(0, size - strip_size)

                parent1[i : i + strip_size], parent2[j : j + strip_size] = (
                    parent2[j : j + strip_size],
                    parent1[i : i + strip_size],
                )

            return [parent1, parent2]

        paths = []
        for parent1 in parents:
            for parent2 in parents:
                paths += cross(deepcopy(parent1.paths), deepcopy(parent2.paths))

        random.shuffle(paths)
        for child, path in zip(children, paths):
            child.paths = path
            child.color = WHITE
            self.mutate(child)

        return children



class LinearModel:
    def __init__(self, population_size, life_span, epochs):
        self.population_size = max(10, population_size)
        self.life_span = life_span
        self.epochs = epochs

        self.goal_walls, self.walls, self.spawnArea = setupStage()

    def fitness(self):
        center_n = pygame.Vector2( sum(x.body.position.x for x in self.balls)/self.population_size, sum(x.body.position.y for x in self.balls)/self.population_size )

        for ball in self.balls:
            score = 0
            # score += (1e3 - ball.best) / 1e3
            score += norm(ball.body.position-center_n)/1e3
            ball.prev_score = ball.new_score
            ball.new_score = score
        self.balls.sort(key=lambda x: -x.new_score)
        return self.balls

    def farthest_from_center(self):
        center_n = pygame.Vector2( sum(x.body.position.x for x in self.balls)/self.population_size, sum(x.body.position.y for x in self.balls)/self.population_size )

        distances = []
        for ball in self.balls:
            distances.append((norm(center_n-ball.body.position),ball.body.velocity))

        return sorted(distances)[::-1]

    def closest_to_goal(self):
        distances = []
        for ball in self.balls:
            distances.append((ball.best, ball.body.velocity))

        m = max([x[0]for x in distances])
        distances = [(x[0]/m, x[1]) for x in distances]
        
        return sorted(distances)

    def train(self):
        self.balls = generate_balls(self.population_size, self.spawnArea, self.goal_walls,chaos = False)

        for i in range(self.epochs):
            runMotion(
                self.goal_walls, self.walls, self.balls, self.spawnArea, self.life_span
            )

            farthest = self.farthest_from_center()
            closest = self.closest_to_goal()

            for ball in self.balls:
                ball.remove()
            self.balls.clear()
            new_gen = []

            c = deepcopy(farthest)
            children2 = self.crossOver([x[1] for x in farthest[:4]],4)
            children1 = self.crossOver([x[1] for x in closest[:4]],4)


            # for val in farthest[:4]:
            #     ball = Ball(screen, space, self.spawnArea.x, self.spawnArea.y, self.goal_walls, color = YELLOW)
            #     ball.body.velocity = val[1]
            #     new_gen.append(ball)
            # for child in children1:
            #     ball = Ball(screen, space, self.spawnArea.x, self.spawnArea.y, self.goal_walls, color = DARK_YELLOW)
            #     ball.body.velocity = child[0], child[1]
            #     new_gen.append(ball)
            for val in closest[:4]:
                ball = Ball(screen, space, self.spawnArea.x, self.spawnArea.y, self.goal_walls, color = PURPLE)
                ball.body.velocity = val[1]
                new_gen.append(ball)
            # for child in children2:
            #     ball = Ball(screen, space, self.spawnArea.x, self.spawnArea.y, self.goal_walls, color = VIOLET)
            #     ball.body.velocity = child[0], child[1]
            #     new_gen.append(ball)

            gap = self.population_size-len(new_gen)
            new_gen += generate_balls(gap, self.spawnArea, self.goal_walls, chaos=False)

            self.balls = new_gen

    def mutate(self, subject):
        x, y = sorted(map(abs, subject))
        factor = 50*x/y

        multiplier = self.random_selection([[x,x] for x in range(-100,100,20)], 1)[0]
        x += multiplier*factor
        y -= multiplier*factor

        velocity = pygame.Vector2(x,y).normalize()*300
        
        return velocity

    def crossOver(self, parents, child_cnt):
        if len(parents)==0 or child_cnt==0:
            return []
        
        def cross(parent1, parent2):
            child1 = (parent1+parent2)/2
            child1 = self.mutate(child1)

            child2 = pygame.Vector2(parent1[0], parent2[1])
            child2 = self.mutate(child2)

            child3 = pygame.Vector2(parent1[1], parent2[0])
            child3 = self.mutate(child3)

            return [child1, child2, child3]

        children = []
        for parent1 in parents:
            for parent2 in parents:
                children += cross(parent1, parent2)

        random.shuffle(children)
        return children[:child_cnt]

    def random_selection(self, scores, cnt):

        total = sum([x[0] for x in scores])  # Total sum of scores
        temp_scores = [[x[0] / total, x[1]] for x in scores]  # Normailizing scores data
        cdf = []
        cur_total = 0
        for x in temp_scores:
            cur_total += x[0]
            cdf += [cur_total]

        # Random selection directed by cdf
        selected = []
        for _ in range(cnt):
            p = random.random()
            for i in range(len(cdf)):
                if p <= cdf[i]:
                    selected += [scores[i][1]]
                    break

        return selected
