# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: erivero- <erivero-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/23 23:09:08 by migarci2          #+#    #+#              #
#    Updated: 2025/04/14 10:44:38 by erivero-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

COMPOSE_FILE := docker-compose.yaml

all: up

up:
	docker compose -f $(COMPOSE_FILE) up -d --build

down:
	docker compose -f $(COMPOSE_FILE) down

clean:
	docker compose -f $(COMPOSE_FILE) down --volumes --rmi all

fclean: clean
	docker system prune --all --force --volumes

re: down up

.PHONY: all up down re clean fclean